import torch
import torch.nn as nn
from graphtransformer_digress.model import GraphTransformer, PlaceHolder

def test_graph_transformer_forward():
    """
    Tests the forward pass of the GraphTransformer model with dummy data.
    """
    # Define dummy dimensions
    input_dims = {'X': 10, 'E': 8, 'y': 6}
    hidden_dims = {
        'node_dim': 32,
        'edge_dim': 16,
        'global_dim': 64,
        'num_heads': 4,
        'node_ff_dim': 128,
        'edge_ff_dim': 64,
        'global_ff_dim': 256
    }
    
    output_dims = {'X': 10, 'E': 8, 'y': 6} # Output dims can be different, but same is fine for a basic test
    num_layers = 2
    batch_size = 2
    num_nodes = 5

    # Create dummy input tensors
    X = torch.randn(batch_size, num_nodes, input_dims['X'])
    E = torch.randn(batch_size, num_nodes, num_nodes, input_dims['E'])
    y = torch.randn(batch_size, input_dims['y'])
    # Create a dummy node mask (e.g., mask out the last node in each batch)
    node_mask = torch.ones(batch_size, num_nodes, dtype=torch.bool)
    node_mask[:, -1] = False

    # Instantiate the model
    model = GraphTransformer(
        num_layers=num_layers,
        input_dims=input_dims,
        hidden_dims=hidden_dims,
        output_dims=output_dims,
        act_fn_in=nn.ReLU(),
        act_fn_out=nn.ReLU()
    )

    # Perform forward pass
    output = model(X, E, y, node_mask)

    # Assertions
    assert isinstance(output, PlaceHolder), "Output should be a PlaceHolder instance"
    assert output.X.shape == (batch_size, num_nodes, output_dims['X']), f"Expected X shape {(batch_size, num_nodes, output_dims['X'])}, got {output.X.shape}"
    assert output.E.shape == (batch_size, num_nodes, num_nodes, output_dims['E']), f"Expected E shape {(batch_size, num_nodes, num_nodes, output_dims['E'])}, got {output.E.shape}"
    assert output.y.shape == (batch_size, output_dims['y']), f"Expected y shape {(batch_size, output_dims['y'])}, got {output.y.shape}"

    # Optional: Check if masked elements are zero (due to masking in PlaceHolder)
    assert torch.all(output.X[~node_mask] == 0), "Masked node features should be zero"
    # Create expanded edge mask based on node mask
    node_mask_expanded = node_mask.unsqueeze(-1)
    edge_mask = node_mask_expanded.unsqueeze(2) * node_mask_expanded.unsqueeze(1)
    assert torch.all(output.E[~edge_mask.squeeze(-1)] == 0), "Masked edge features should be zero"


# To run this test, you would typically use a test runner like pytest.
# For example, from the project root directory, run:
# pytest tests/test_model.py
