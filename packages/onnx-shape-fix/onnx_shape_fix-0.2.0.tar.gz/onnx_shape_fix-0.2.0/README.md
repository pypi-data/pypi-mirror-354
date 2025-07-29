# ONNX Shape Fix

A Python package for fixing shape information in ONNX models, with special support for ParticleTransformer models.

## Features

- Propagate shape information through an ONNX model graph
- Track batch dimension movement throughout the model
- Optionally remove batch dimensions from model shapes for deployment to batch-less platforms
- Special support for ParticleTransformer models
- Command-line interface for easy use
- Python API for integration with other tools

## Installation

You can install the package directly from GitHub:

```bash
pip install git+https://github.com/ha/onnx-shape-fix.git
```

Or from PyPI (once published):

```bash
pip install onnx-shape-fix
```

## Command-line Usage

```bash
# Basic usage
onnx-shape-fix model.onnx --input-shapes "input_1:[1,3,224,224];input_2:[1,10]"

# Using JSON file for input shapes
onnx-shape-fix model.onnx --input-shapes-json shapes.json

# Remove batch dimension
onnx-shape-fix model.onnx --input-shapes "input:[1,3,224,224]" --remove-batch

# Special handling for ParticleTransformer models
onnx-shape-fix model.onnx --input-shapes "points:[32,128,4];features:[32,128,8]" --particle-transformer

# Verbose output
onnx-shape-fix model.onnx --input-shapes "input:[1,3,224,224]" --verbose
```

## Example Scripts

The package includes example scripts to demonstrate its usage:

### Generic ONNX Model Example

```bash
# Run the generic example script
python examples/generic_example.py model.onnx -i "input:[1,3,224,224]" -v
```

### ParticleTransformer Model Example

```bash
# Run the ParticleTransformer example script (uses pre-defined input shapes)
python examples/particle_transformer_example.py model.onnx -r -v
```

Both example scripts demonstrate:
- Loading an ONNX model
- Propagating shapes through the model
- Optionally removing batch dimensions
- Saving the model with fixed shapes

## Python API

```python
from onnx_shape_fix import ShapePropagator

# Basic usage with method chaining
ShapePropagator(
    model_path="model.onnx",
    input_shapes={"input": [1, 3, 224, 224]},
    verbose=True
).propagate().save_model_with_shapes("model_fixed.onnx")

# More detailed usage
propagator = ShapePropagator(
    model_path="model.onnx",
    input_shapes={"input": [1, 3, 224, 224]},
    verbose=True,
    track_batch=True
)

# Propagate shapes through the model
propagator.propagate()

# Access the shape dictionary
shapes = propagator.shape_dict
print(f"Shape of output tensor: {shapes['output']}")

# Save model with fixed shapes
propagator.save_model_with_shapes("model_fixed.onnx", remove_batch=False)

# For ParticleTransformer models
from onnx_shape_fix import ParticleTransformerShapePropagator

# Method chaining for cleaner code
ParticleTransformerShapePropagator(
    model_path="particle_transformer.onnx",
    input_shapes={
        "pf_features": [1, 7, 128],
        "pf_vectors": [1, 4, 128],
        "pf_mask": [1, 1, 128]
    },
    verbose=True
).propagate().save_model_with_shapes("pt_fixed.onnx", remove_batch=True)
```

## Batch Dimension Tracking and Removal

The package automatically tracks the batch dimension throughout the model graph, allowing for:

1. Understanding where the batch dimension is located for each tensor
2. Removing batch dimensions for deployment to batch-less platforms
3. Handling operations that reorder dimensions (like Transpose or Reshape)

```python
from onnx_shape_fix import ShapePropagator

# Create propagator and run shape propagation
propagator = ShapePropagator(
    model_path="model.onnx",
    input_shapes={"input": [1, 3, 224, 224]},
    track_batch=True,
    verbose=True
).propagate()

# Get batch dimension index for a tensor
tensor_name = "some_intermediate_tensor"
batch_idx = propagator.batch_tracker.get_batch_dim(tensor_name)
print(f"Batch dimension for {tensor_name} is at index {batch_idx}")

# Save model with batch dimensions removed
propagator.save_model_with_shapes("model_batchless.onnx", remove_batch=True)
```

### How Batch Removal Works

When `remove_batch=True`, the package:
- Identifies the batch dimension for each tensor
- Removes that dimension from the tensor shape
- Updates all shape information in the ONNX model

This is particularly useful for:
- Deploying models to hardware accelerators that don't support batching
- Simplifying models for single-sample inference
- Fixing shapes in models where the batch dimension is dynamic but hardware requires fixed dimensions

## License

MIT

## Extending the Package

### Adding Custom Operation Handlers

You can extend the package to support custom ONNX operations by creating your own handlers:

```python
from onnx_shape_fix.handlers import BaseHandler, register_handler
from typing import List, Optional
from onnx import NodeProto

# Create a custom handler for your operation
class MyCustomOpHandler(BaseHandler):
    def __init__(self, verbose: bool = False):
        super().__init__(verbose)
    
    def handle_node(self, node: NodeProto, input_shapes: List[List[int]], propagator) -> Optional[List[int]]:
        # Implement your shape handling logic here
        # Return the output shape as a list of integers
        return input_shapes[0]  # Example: pass-through shape

# Register your handler
register_handler("MyCustomOp", MyCustomOpHandler)

# Now use the propagator as usual
from onnx_shape_fix import ShapePropagator

ShapePropagator(
    model_path="model_with_custom_ops.onnx",
    input_shapes={"input": [1, 3, 224, 224]},
    verbose=True
).propagate().save_model_with_shapes("fixed_model.onnx")
```

### Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Add your feature or fix
4. Add tests for your changes
5. Submit a pull request

When adding support for new operations, place them in the appropriate handler file based on operation type:
- `elementwise.py` - Element-wise operations (Add, Mul, etc.)
- `shape_ops.py` - Shape manipulation operations (Reshape, Transpose, etc.)
- `math_ops.py` - Mathematical operations (MatMul, Conv, etc.)
- `nn_ops.py` - Neural network operations (BatchNormalization, Dropout, etc.)
