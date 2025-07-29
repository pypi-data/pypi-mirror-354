"""
This script defines a Graph Transformer model that simultaneously processes and updates
node, edge, and global graph features.

The model is composed of three main parts:
1.  **Input/Output MLPs:** Pre-process input features and post-process output features
    to map them to and from the model's hidden dimensions.
2.  **GraphTransformer Layers:** The core of the model. Each layer consists of:
    a. A `GraphAttentionBlock` that performs multi-head attention, allowing nodes,
       edges, and global features to influence each other.
    b. Feed-forward networks (FFNs) for nodes, edges, and global features, applied
       after the attention block.
    c. Residual connections and layer normalization (Pre-LN style).
3.  **Feature Aggregators:** Helper modules (`NodeFeatureAggregator`, `EdgeFeatureAggregator`)
    that compute summary statistics of node/edge features to update the global
    graph representation.

The `diffusion_utils` and `utils` imports are assumed to contain helper functions.
- `diffusion_utils.assert_correctly_masked`: A debugging tool to ensure masks are applied correctly.
- `utils.PlaceHolder`: A simple data container for X, E, and y features.
These have been commented out or replaced with placeholder logic for stand-alone execution.
"""

import math
import torch
import torch.nn as nn
from torch.nn import functional as F
from torch.nn.modules.normalization import LayerNorm
from torch import Tensor

# --- Helper Modules for Global Feature Aggregation ---


class NodeFeatureAggregator(nn.Module):
    """
    Aggregates node features to create a global representation.
    It computes summary statistics (mean, min, max, std) of node features
    and maps them to the global feature dimension.
    """

    def __init__(self, node_dim: int, global_dim: int):
        """
        Args:
            node_dim: The dimensionality of the node features (dx).
            global_dim: The dimensionality of the output global features (dy).
        """
        super().__init__()
        # 4 statistics are concatenated: mean, min, max, std
        self.mlp = nn.Linear(4 * node_dim, global_dim)

    def forward(self, node_features: Tensor) -> Tensor:
        """
        Args:
            node_features (Tensor): Node features of shape (batch_size, num_nodes, node_dim).

        Returns:
            Tensor: Aggregated global features of shape (batch_size, global_dim).
        """
        mean_features = node_features.mean(dim=1)
        min_features = node_features.min(dim=1)[0]
        max_features = node_features.max(dim=1)[0]
        std_features = node_features.std(dim=1)

        aggregated_features = torch.hstack(
            (mean_features, min_features, max_features, std_features)
        )
        output = self.mlp(aggregated_features)
        return output


class EdgeFeatureAggregator(nn.Module):
    """
    Aggregates edge features to create a global representation.
    It computes summary statistics (mean, min, max, std) of edge features
    and maps them to the global feature dimension.
    """

    def __init__(self, edge_dim: int, global_dim: int):
        """
        Args:
            edge_dim: The dimensionality of the edge features (de).
            global_dim: The dimensionality of the output global features (dy).
        """
        super().__init__()
        # 4 statistics are concatenated: mean, min, max, std
        self.mlp = nn.Linear(4 * edge_dim, global_dim)

    def forward(self, edge_features: Tensor) -> Tensor:
        """
        Args:
            edge_features (Tensor): Edge features of shape (batch_size, num_nodes, num_nodes, edge_dim).

        Returns:
            Tensor: Aggregated global features of shape (batch_size, global_dim).
        """
        mean_features = edge_features.mean(dim=(1, 2))
        min_features = edge_features.min(dim=2)[0].min(dim=1)[0]
        max_features = edge_features.max(dim=2)[0].max(dim=1)[0]
        std_features = torch.std(edge_features, dim=(1, 2))

        aggregated_features = torch.hstack(
            (mean_features, min_features, max_features, std_features)
        )
        output = self.mlp(aggregated_features)
        return output


# --- Utility Function ---


def masked_softmax(x: Tensor, mask: Tensor, **kwargs):
    """
    Applies softmax to a tensor, masking out specified elements.
    """
    if mask.sum() == 0:
        # Avoid issues with all-zero masks
        return torch.softmax(x, **kwargs)

    x_masked = x.clone()
    # Set masked positions to a very small number to ensure they get near-zero probability
    x_masked[mask == 0] = -float("inf")
    return torch.softmax(x_masked, **kwargs)


# --- Core Transformer Blocks ---


class GraphAttentionBlock(nn.Module):
    """
    Multi-head attention block that updates node, edge, and global representations.

    This block implements a form of attention where:
    - Node features are updated based on an aggregation of other nodes' values,
      weighted by attention scores.
    - Attention scores are influenced by both node-pair features (queries, keys) and
      the edge features connecting them.
    - All three feature types (node, edge, global) are modulated by each other using
      FiLM (Feature-wise Linear Modulation) layers.
    """

    def __init__(
        self, node_dim: int, edge_dim: int, global_dim: int, num_heads: int, **kwargs
    ):
        super().__init__()
        assert (
            node_dim % num_heads == 0
        ), f"Node dimension ({node_dim}) must be divisible by number of heads ({num_heads})."

        self.node_dim = node_dim
        self.edge_dim = edge_dim
        self.global_dim = global_dim
        self.num_heads = num_heads
        self.head_dim = node_dim // num_heads

        # Projections for Query, Key, Value
        self.q_proj = nn.Linear(node_dim, node_dim)
        self.k_proj = nn.Linear(node_dim, node_dim)
        self.v_proj = nn.Linear(node_dim, node_dim)

        # FiLM layers for conditioning
        # Edge features modulating node-pair attention
        self.edge_to_attn_add = nn.Linear(edge_dim, node_dim)
        self.edge_to_attn_mul = nn.Linear(edge_dim, node_dim)

        # Global features modulating edge features
        # Note: Projects to node_dim, not edge_dim, as it modulates the intermediate edge representation
        self.global_to_edge_add = nn.Linear(global_dim, node_dim)
        self.global_to_edge_mul = nn.Linear(global_dim, node_dim)

        # Global features modulating node features
        self.global_to_node_add = nn.Linear(global_dim, node_dim)
        self.global_to_node_mul = nn.Linear(global_dim, node_dim)

        # Layers for updating global features
        self.global_self_update = nn.Linear(global_dim, global_dim)
        self.node_aggregator = NodeFeatureAggregator(node_dim, global_dim)
        self.edge_aggregator = EdgeFeatureAggregator(edge_dim, global_dim)

        # Output projection layers
        self.node_output_mlp = nn.Linear(node_dim, node_dim)
        self.edge_output_mlp = nn.Linear(
            node_dim, edge_dim
        )  # From intermediate node_dim back to edge_dim
        self.global_output_mlp = nn.Sequential(
            nn.Linear(global_dim, global_dim),
            nn.ReLU(),
            nn.Linear(global_dim, global_dim),
        )

    def forward(self, X: Tensor, E: Tensor, y: Tensor, node_mask: Tensor):
        """
        Args:
            X (Tensor): Node features (batch_size, num_nodes, node_dim).
            E (Tensor): Edge features (batch_size, num_nodes, num_nodes, edge_dim).
            y (Tensor): Global features (batch_size, global_dim).
            node_mask (Tensor): Mask for nodes (batch_size, num_nodes).

        Returns:
            Tuple[Tensor, Tensor, Tensor]: Updated node, edge, and global features.
        """
        batch_size, num_nodes, _ = X.shape
        node_mask_expanded = node_mask.unsqueeze(-1)  # (bs, n, 1)
        edge_mask_row = node_mask_expanded.unsqueeze(2)  # (bs, n, 1, 1)
        edge_mask_col = node_mask_expanded.unsqueeze(1)  # (bs, 1, n, 1)
        full_edge_mask = edge_mask_row * edge_mask_col  # (bs, n, n, 1)

        # 1. Project nodes to Q, K, V and reshape for multi-head attention
        Q = (self.q_proj(X) * node_mask_expanded).view(
            batch_size, num_nodes, self.num_heads, self.head_dim
        )
        K = (self.k_proj(X) * node_mask_expanded).view(
            batch_size, num_nodes, self.num_heads, self.head_dim
        )
        V = (self.v_proj(X) * node_mask_expanded).view(
            batch_size, num_nodes, self.num_heads, self.head_dim
        )

        # # Transpose for batch matrix multiplication: (bs, n_head, n, d_head)
        # Q = Q.transpose(1, 2)
        # K = K.transpose(1, 2)
        # V = V.transpose(1, 2)

        # 2. Compute attention scores biased by edge features
        # Reshape for broadcasting: (bs, 1, n, n_head, d_head) and (bs, n, 1, n_head, d_head)
        # Resulting shape: (bs, n, n, n_head, d_head) after scaling
        raw_attention_scores = (Q.unsqueeze(2) * K.unsqueeze(1)) / math.sqrt(
            self.head_dim
        )

        # Incorporate edge features into attention scores using FiLM
        edge_factor_mul = self.edge_to_attn_mul(E).view(
            batch_size, num_nodes, num_nodes, self.num_heads, self.head_dim
        )
        edge_factor_add = self.edge_to_attn_add(E).view(
            batch_size, num_nodes, num_nodes, self.num_heads, self.head_dim
        )

        # The new attention "logits" are modulated by edge features
        # Shape: (bs, n, n, n_head, d_head)

        attention_logits = (
            raw_attention_scores * (edge_factor_mul + 1) + edge_factor_add
        )

        # 3. Update Edge Features
        # The attention logits themselves form the basis for the new edge representation
        intermediate_edge_repr = attention_logits.flatten(
            start_dim=3
        )  # (bs, n, n, node_dim)

        # Modulate with global features
        global_to_edge_add = (
            self.global_to_edge_add(y).unsqueeze(1).unsqueeze(1)
        )  # (bs, 1, 1, node_dim)
        global_to_edge_mul = (
            self.global_to_edge_mul(y).unsqueeze(1).unsqueeze(1)
        )  # (bs, 1, 1, node_dim)
        intermediate_edge_repr = (
            global_to_edge_add + (global_to_edge_mul + 1) * intermediate_edge_repr
        )

        # Project to final edge dimension and apply mask
        updated_E = self.edge_output_mlp(intermediate_edge_repr) * full_edge_mask

        # 4. Compute Attention Weights and Update Node Features
        # Sum over the head dimension before softmax, common in some transformer variants
        attention_logits_summed = (
            attention_logits  # .sum(dim=-1) # (bs, n, n, n_head, df)
        )

        softmax_mask = edge_mask_col.expand(
            -1, num_nodes, -1, self.num_heads
        )  # (bs, n, n, n_head)

        attention_weights = masked_softmax(
            attention_logits_summed, softmax_mask, dim=2
        )  # (bs, n, n, n_head)

        # Aggregate values based on attention weights
        # attn: (bs, n, n, n_head), V: (bs, 1, n, n_head, d_head) -> weighted_V: (bs, n, n_head, d_head)
        weighted_V = attention_weights * V.unsqueeze(1)
        weighted_V = weighted_V.sum(dim=2)

        # Send output to input dim
        weighted_V = weighted_V.flatten(start_dim=2)  # bs, n, dx

        # Modulate with global features
        global_to_node_add = self.global_to_node_add(y).unsqueeze(1)
        global_to_node_mul = self.global_to_node_mul(y).unsqueeze(1)
        updated_X_intermediate = (
            global_to_node_add + (global_to_node_mul + 1) * weighted_V
        )

        # Project to final node dimension and apply mask
        updated_X = self.node_output_mlp(updated_X_intermediate) * node_mask_expanded

        # 5. Update Global Features
        # Update based on its previous state, and aggregated features from the updated nodes and edges
        y_self_updated = self.global_self_update(y)
        aggregated_X = self.node_aggregator(X)  # Using original X as per the paper
        aggregated_E = self.edge_aggregator(E)  # Using original E

        updated_y = y_self_updated + aggregated_X + aggregated_E
        updated_y = self.global_output_mlp(updated_y)

        return updated_X, updated_E, updated_y


class GraphTransformerLayer(nn.Module):
    """
    A single layer of the Graph Transformer.
    It follows the standard Transformer layer structure (e.g., Pre-LN):
    1. Multi-Head Attention (via `GraphAttentionBlock`).
    2. Residual connection and Layer Normalization.
    3. Feed-Forward Network (FFN).
    4. Residual connection and Layer Normalization.

    This is applied independently to node, edge, and global features.
    """

    def __init__(
        self,
        node_dim: int,
        edge_dim: int,
        global_dim: int,
        num_heads: int,
        node_ff_dim: int = 2048,
        edge_ff_dim: int = 128,
        global_ff_dim: int = 2048,
        dropout: float = 0.1,
        layer_norm_eps: float = 1e-5,
        **kwargs,
    ) -> None:
        super().__init__()

        self.attention_block = GraphAttentionBlock(
            node_dim, edge_dim, global_dim, num_heads, **kwargs
        )

        # Node FFN and Norms
        self.norm_node_1 = LayerNorm(node_dim, eps=layer_norm_eps)
        self.norm_node_2 = LayerNorm(node_dim, eps=layer_norm_eps)
        self.ffn_node = nn.Sequential(
            nn.Linear(node_dim, node_ff_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(node_ff_dim, node_dim),
            nn.Dropout(dropout),
        )

        # Edge FFN and Norms
        self.norm_edge_1 = LayerNorm(edge_dim, eps=layer_norm_eps)
        self.norm_edge_2 = LayerNorm(edge_dim, eps=layer_norm_eps)
        self.ffn_edge = nn.Sequential(
            nn.Linear(edge_dim, edge_ff_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(edge_ff_dim, edge_dim),
            nn.Dropout(dropout),
        )

        # Global FFN and Norms
        self.norm_global_1 = LayerNorm(global_dim, eps=layer_norm_eps)
        self.norm_global_2 = LayerNorm(global_dim, eps=layer_norm_eps)
        self.ffn_global = nn.Sequential(
            nn.Linear(global_dim, global_ff_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(global_ff_dim, global_dim),
            nn.Dropout(dropout),
        )

        self.dropout = nn.Dropout(dropout)

    def forward(self, X: Tensor, E: Tensor, y: Tensor, node_mask: Tensor):
        """
        Passes the input through the transformer layer.
        """
        # 1. Attention block with residual connection (Pre-Norm style)
        attn_out_X, attn_out_E, attn_out_y = self.attention_block(
            X, E, y, node_mask=node_mask
        )

        X = self.norm_node_1(X + self.dropout(attn_out_X))
        E = self.norm_edge_1(E + self.dropout(attn_out_E))
        y = self.norm_global_1(y + self.dropout(attn_out_y))

        # 2. Feed-forward block with residual connection
        ffn_out_X = self.ffn_node(X)
        X = self.norm_node_2(X + ffn_out_X)

        ffn_out_E = self.ffn_edge(E)
        E = self.norm_edge_2(E + ffn_out_E)

        ffn_out_y = self.ffn_global(y)
        y = self.norm_global_2(y + ffn_out_y)

        return X, E, y


# --- The Main Model ---
# Placeholder for a data container, if you have one.
# If not, you can simply return a tuple (X, E, y).
class PlaceHolder:
    def __init__(self, X, E, y):
        self.X = X
        self.E = E
        self.y = y

    def mask(self, node_mask):
        self.X = self.X * node_mask.unsqueeze(-1)
        self.E = (
            self.E
            * node_mask.unsqueeze(1).unsqueeze(-1)
            * node_mask.unsqueeze(2).unsqueeze(-1)
        )
        return self


class GraphTransformer(nn.Module):
    """
    A complete Graph Transformer model stacking multiple GraphTransformerLayer blocks.
    It includes input and output MLPs to map features to and from the model's
    hidden dimensions.
    """

    def __init__(
        self,
        num_layers: int,
        input_dims: dict,
        hidden_dims: dict,
        output_dims: dict,
        act_fn_in: nn.Module,
        act_fn_out: nn.Module,
    ):
        super().__init__()
        self.num_layers = num_layers
        self.output_dim_X = output_dims["X"]
        self.output_dim_E = output_dims["E"]
        self.output_dim_y = output_dims["y"]

        # Input MLPs: Project features from input dimensions to hidden dimensions
        self.input_mlp_X = nn.Sequential(
            nn.Linear(input_dims["X"], hidden_dims["node_dim"]), act_fn_in
        )
        self.input_mlp_E = nn.Sequential(
            nn.Linear(input_dims["E"], hidden_dims["edge_dim"]), act_fn_in
        )
        self.input_mlp_y = nn.Sequential(
            nn.Linear(input_dims["y"], hidden_dims["global_dim"]), act_fn_in
        )

        # Stack of Transformer Layers
        self.transformer_layers = nn.ModuleList(
            [
                GraphTransformerLayer(
                    node_dim=hidden_dims["node_dim"],
                    edge_dim=hidden_dims["edge_dim"],
                    global_dim=hidden_dims["global_dim"],
                    num_heads=hidden_dims["num_heads"],
                    node_ff_dim=hidden_dims["node_ff_dim"],
                    edge_ff_dim=hidden_dims["edge_ff_dim"],
                    global_ff_dim=hidden_dims["global_ff_dim"],
                )
                for _ in range(num_layers)
            ]
        )

        # Output MLPs: Project features from hidden dimensions to output dimensions
        self.output_mlp_X = nn.Sequential(
            nn.Linear(hidden_dims["node_dim"], hidden_dims["node_dim"]),
            act_fn_out,
            nn.Linear(hidden_dims["node_dim"], output_dims["X"]),
        )
        self.output_mlp_E = nn.Sequential(
            nn.Linear(hidden_dims["edge_dim"], hidden_dims["edge_dim"]),
            act_fn_out,
            nn.Linear(hidden_dims["edge_dim"], output_dims["E"]),
        )
        self.output_mlp_y = nn.Sequential(
            nn.Linear(hidden_dims["global_dim"], hidden_dims["global_dim"]),
            act_fn_out,
            nn.Linear(hidden_dims["global_dim"], output_dims["y"]),
        )

    def forward(self, X: Tensor, E: Tensor, y: Tensor, node_mask: Tensor):
        batch_size, num_nodes = X.shape[0], X.shape[1]

        # Create a mask to zero out the diagonal of the edge features later
        diag_mask = ~torch.eye(num_nodes, device=X.device, dtype=torch.bool)
        diag_mask = diag_mask.unsqueeze(0).unsqueeze(-1).expand(batch_size, -1, -1, -1)

        # Store a portion of the input for the final residual connection
        X_residual = X[..., : self.output_dim_X]
        E_residual = E[..., : self.output_dim_E]
        y_residual = y[..., : self.output_dim_y]

        # 1. Pre-process inputs with MLPs
        X_processed = self.input_mlp_X(X)
        E_processed = self.input_mlp_E(E)
        y_processed = self.input_mlp_y(y)

        # Enforce symmetry in edge features
        E_processed = (E_processed + E_processed.transpose(1, 2)) / 2

        # Apply node mask to inputs
        X_processed = X_processed * node_mask.unsqueeze(-1)
        E_processed = (
            E_processed
            * node_mask.unsqueeze(1).unsqueeze(-1)
            * node_mask.unsqueeze(2).unsqueeze(-1)
        )

        # 2. Pass through the transformer layers
        for layer in self.transformer_layers:
            X_processed, E_processed, y_processed = layer(
                X_processed, E_processed, y_processed, node_mask
            )

        # 3. Post-process outputs with MLPs
        X_out = self.output_mlp_X(X_processed)
        E_out = self.output_mlp_E(E_processed)
        y_out = self.output_mlp_y(y_processed)

        # 4. Add final residual connection
        X_final = X_out + X_residual
        E_final = (
            E_out + E_residual
        )  # Use mask to prevent self-loops in residual
        y_final = y_out + y_residual

        # Enforce final edge symmetry
        E_final = (E_final + E_final.transpose(1, 2)) / 2

        # Return masked results, possibly in a container
        output = PlaceHolder(X=X_final, E=E_final, y=y_final)
        return output.mask(node_mask)
