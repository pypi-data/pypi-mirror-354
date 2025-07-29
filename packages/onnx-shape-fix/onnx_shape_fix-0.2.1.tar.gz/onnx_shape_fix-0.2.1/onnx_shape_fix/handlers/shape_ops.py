from typing import List, Optional, Any
import numpy as np
from onnx import NodeProto, numpy_helper

from .base_handler import BaseHandler
from ..utils.logger import Logger
from ..utils.constant_utils import get_constant_value

class ShapeOpsHandler(BaseHandler):
    """
    Handler for shape manipulation operations.
    
    This handler implements shape inference for operations that manipulate
    tensor shapes like Reshape, Transpose, Concat, Squeeze, etc.
    """
    
    def __init__(self, verbose: bool = False):
        super().__init__(verbose)
        self.logger = Logger(verbose=verbose)
    
    def handle_node(self, node: NodeProto, input_shapes: List[List[int]], propagator: Any) -> List[List[int]]:
        """
        Handle shape operations by dispatching to specific method based on op_type.
        
        Args:
            node: The ONNX node
            input_shapes: Shapes of the input tensors
            propagator: The shape propagator instance
            
        Returns:
            A list of output shapes, one for each output of the node
        """
        try:
            # Dispatch to specific handler method based on op_type
            if node.op_type == "Reshape":
                shape = self._handle_reshape(node, input_shapes, propagator)
            elif node.op_type == "Transpose":
                shape = self._handle_transpose(node, input_shapes)
            elif node.op_type == "Concat":
                shape = self._handle_concat(node, input_shapes)
            elif node.op_type == "Slice":
                shape = self._handle_slice(node, input_shapes, propagator)
            elif node.op_type == "Squeeze":
                shape = self._handle_squeeze(node, input_shapes, propagator)
            elif node.op_type == "Unsqueeze":
                shape = self._handle_unsqueeze(node, input_shapes, propagator)
            elif node.op_type == "Flatten":
                shape = self._handle_flatten(node, input_shapes)
            elif node.op_type == "Gather":
                shape = self._handle_gather(node, input_shapes, propagator)
            elif node.op_type == "Split":
                return self._handle_split(node, input_shapes, propagator)  # Already returns list of shapes
            elif node.op_type == "Expand":
                shape = self._handle_expand(node, input_shapes, propagator)
            elif node.op_type == "Shape":
                shape = self._handle_shape(node, input_shapes)
            elif node.op_type == "ConstantOfShape":
                shape = self._handle_constant_of_shape(node, input_shapes, propagator)
            else:
                self.logger.error("Unhandled shape op: %s", node.op_type)
                return [None] * len(node.output)
            
            # Wrap the single shape in a list for a single output node
            if shape is None:
                return [None] * len(node.output)
            return [shape]  # Return a list with one shape
                
        except Exception as e:
            self.logger.error("%s error in %s: %s", node.op_type, node.name, str(e))
            return [None] * len(node.output)
    
    def _get_attribute(self, node: NodeProto, name: str, default):
        """Helper to get an attribute from a node with a default value."""
        for attr in node.attribute:
            if attr.name == name:
                if attr.type == 1:  # FLOAT
                    return attr.f
                elif attr.type == 2:  # INT
                    return attr.i
                elif attr.type == 3:  # STRING
                    return attr.s.decode('utf-8')
                elif attr.type == 4:  # TENSOR
                    return numpy_helper.to_array(attr.t)
                elif attr.type == 7:  # INTS
                    return list(attr.ints)
        return default
    
    def _handle_reshape(self, node: NodeProto, input_shapes: List[List[int]], propagator: Any) -> Optional[List[int]]:
        """
        Handle Reshape operation.
        
        Reshape changes the shape of a tensor while preserving the total number of elements.
        """
        self.logger.debug("Handling Reshape %s", node.name)

        try:
            if not input_shapes or len(input_shapes) < 2 or not input_shapes[0]:
                self.logger.error("Reshape %s requires 2 inputs (data, shape)", node.name)
                return None
            
            input_shape = input_shapes[0]
            
            # Get target shape from second input using the propagator
            target_shape = get_constant_value(node.input[1], propagator)
            if target_shape is None:
                self.logger.error("Could not determine target shape for Reshape %s", node.name)
                return None
            else:
                self.logger.debug("Reshape target shape from input: %s", target_shape)
            
            # Convert to list if numpy array
            if isinstance(target_shape, np.ndarray):
                target_shape = target_shape.flatten().tolist()
                
            # Handle empty shape (scalar output)
            if len(target_shape) == 0:
                if np.prod(input_shape) != 1:
                    self.logger.error("Cannot reshape %s to scalar in %s", input_shape, node.name)
                    return None
                self.logger.debug("Reshape %s: scalar output: []", node.name)
                return []
            
            # Get allowzero attribute (default 0)
            allowzero = self._get_attribute(node, "allowzero", 0)
            
            # Check for invalid -1 and 0 combination
            if allowzero and (-1 in target_shape and 0 in target_shape):
                self.logger.error("Invalid shape %s with both -1 and 0 when allowzero=1 in %s", 
                            target_shape, node.name)
                return None
            
            # Process 0s (if allowzero=0)
            if not allowzero:
                new_target = []
                for i, dim in enumerate(target_shape):
                    if dim == 0:
                        if i >= len(input_shape):
                            self.logger.error("Dimension %d out of range for input rank %d in %s",
                                        i, len(input_shape), node.name)
                            return None
                        new_target.append(input_shape[i])
                    else:
                        new_target.append(dim)
                target_shape = new_target
            
            # Handle -1 dimension
            if -1 in target_shape:
                input_size = np.prod(input_shape)
                fixed_dims = [d for d in target_shape if d != -1]
                
                if len(fixed_dims) != len(target_shape) - 1:
                    self.logger.error("Multiple -1 in target shape for Reshape %s", node.name)
                    return None
                    
                fixed_size = np.prod(fixed_dims)
                if fixed_size == 0:
                    self.logger.error("Zero-size dimensions with -1 in Reshape %s", node.name)
                    return None
                    
                inferred_dim = input_size // fixed_size
                if input_size % fixed_size != 0:
                    self.logger.error("Input size %d not divisible by %d in Reshape %s",
                                input_size, fixed_size, node.name)
                    return None
                    
                target_shape = [inferred_dim if d == -1 else d for d in target_shape]
            
            # Validate total size
            input_size = np.prod(input_shape)
            output_size = np.prod(target_shape)
            if input_size != output_size:
                self.logger.error("Size mismatch %d vs %d in Reshape %s", 
                            input_size, output_size, node.name)
                return None
            
            self.logger.debug("Reshape %s: %s -> %s", node.name, input_shape, target_shape)
            return target_shape
            
        except Exception as e:
            self.logger.error("Reshape error in %s: %s", node.name, str(e))
            return None
    
    def _handle_transpose(self, node: NodeProto, input_shapes: List[List[int]]) -> Optional[List[int]]:
        """
        Handle Transpose operation.
        
        Transpose permutes the dimensions of a tensor according to a permutation list.
        """
        try:
            if not input_shapes or len(input_shapes) < 1 or not input_shapes[0]:
                self.logger.error("Missing input shape for Transpose %s", node.name)
                return None
            
            input_shape = input_shapes[0]
            
            # Get permutation from attributes (default is reverse order)
            perm = self._get_attribute(node, "perm", list(range(len(input_shape))))
            if perm == []:
                perm = list(range(len(input_shape)))
                perm.reverse()
            
            # Validate permutation
            if len(perm) != len(input_shape):
                self.logger.error("Invalid permutation %s for input shape %s in Transpose %s",
                               perm, input_shape, node.name)
                return None
            
            # Apply permutation
            output_shape = [input_shape[p] for p in perm]
            
            self.logger.debug("Transpose %s: %s with perm %s -> %s", 
                           node.name, input_shape, perm, output_shape)
            return output_shape
            
        except Exception as e:
            self.logger.error("Transpose error in %s: %s", node.name, str(e))
            return None
    
    def _handle_concat(self, node: NodeProto, input_shapes: List[List[int]]) -> Optional[List[int]]:
        """
        Handle Concat operation.
        
        Concat concatenates tensors along a specified axis.
        """
        try:
            if not input_shapes:
                self.logger.error("No input shapes for Concat %s", node.name)
                return None
            
            # Filter out None shapes
            valid_shapes = [shape for shape in input_shapes if shape is not None]
            if not valid_shapes:
                self.logger.error("No valid input shapes for Concat %s", node.name)
                return None
            
            # Get axis attribute (default is 0)
            axis = self._get_attribute(node, "axis", 0)
            
            # Handle negative axis
            if axis < 0:
                axis = len(valid_shapes[0]) + axis
            
            # Validate axis
            if axis < 0 or any(axis >= len(shape) for shape in valid_shapes):
                self.logger.error("Invalid axis %d for Concat %s", axis, node.name)
                return None
            
            # Validate input shapes
            ref_shape = valid_shapes[0]
            for i, shape in enumerate(valid_shapes[1:], 1):
                if len(shape) != len(ref_shape):
                    self.logger.error("Input %d has different rank in Concat %s", i, node.name)
                    return None
                
                for j, (dim1, dim2) in enumerate(zip(ref_shape, shape)):
                    if j != axis and dim1 != dim2:
                        self.logger.error("Dimension mismatch at axis %d in Concat %s", j, node.name)
                        return None
            
            # Calculate output shape
            output_shape = list(ref_shape)
            output_shape[axis] = sum(shape[axis] for shape in valid_shapes)
            
            self.logger.debug("Concat %s: %s along axis %d -> %s", 
                           node.name, valid_shapes, axis, output_shape)
            return output_shape
            
        except Exception as e:
            self.logger.error("Concat error in %s: %s", node.name, str(e))
            return None
    
    def _handle_slice(self, node: NodeProto, input_shapes: List[List[int]], propagator: Any) -> Optional[List[int]]:
        """
        Handle Slice operation.
        
        Slice extracts a slice from a tensor based on starts, ends, axes, and steps.
        """
        try:
            if not input_shapes or len(input_shapes) < 1 or not input_shapes[0]:
                self.logger.error("Missing input shape for Slice %s", node.name)
                return None
            
            input_shape = input_shapes[0]
            
            # Get starts, ends, axes, and steps
            # For opset >= 10, these are input tensors
            # For opset < 10, these are attributes
            starts = ends = axes = steps = None
            
            # Try to get from inputs (opset >= 10)
            if len(node.input) > 1:
                starts = get_constant_value(node.input[1], propagator)
                if len(node.input) > 2:
                    ends = get_constant_value(node.input[2], propagator)
                if len(node.input) > 3:
                    axes = get_constant_value(node.input[3], propagator)
                if len(node.input) > 4:
                    steps = get_constant_value(node.input[4], propagator)
            
            # Try to get from attributes (opset < 10)
            if starts is None:
                starts = self._get_attribute(node, "starts", None)
                ends = self._get_attribute(node, "ends", None)
                axes = self._get_attribute(node, "axes", None)
            
            # If we couldn't get the necessary parameters, we can't proceed
            if starts is None or ends is None:
                self.logger.error("Could not determine starts/ends for Slice %s", node.name)
                return None
            
            # Convert to lists
            if isinstance(starts, np.ndarray):
                starts = starts.flatten().tolist()
            if isinstance(ends, np.ndarray):
                ends = ends.flatten().tolist()
            if isinstance(axes, np.ndarray):
                axes = axes.flatten().tolist()
            if isinstance(steps, np.ndarray):
                steps = steps.flatten().tolist()
            
            # Default values
            if axes is None:
                axes = list(range(len(starts)))
            if steps is None:
                steps = [1] * len(starts)
            
            # Validate lengths
            if len(starts) != len(ends) or len(starts) != len(axes) or len(starts) != len(steps):
                self.logger.error("Inconsistent parameter lengths for Slice %s", node.name)
                return None
            
            # Handle negative axes (convert to positive)
            axes = [axis if axis >= 0 else len(input_shape) + axis for axis in axes]
            
            # Calculate output shape
            output_shape = list(input_shape)
            for i, axis in enumerate(axes):
                if axis < 0 or axis >= len(input_shape):
                    self.logger.error("Invalid axis %d for Slice %s", axis, node.name)
                    return None
                
                start = starts[i]
                end = ends[i]
                step = steps[i]
                
                # Handle negative indices and clamp to input dimension
                if start < 0:
                    start = input_shape[axis] + start
                start = max(0, min(start, input_shape[axis]))
                
                if end < 0:
                    end = input_shape[axis] + end
                end = max(0, min(end, input_shape[axis]))
                
                # Calculate output dimension size
                if start < end:
                    output_dim = (end - start + step - 1) // step
                    output_shape[axis] = output_dim
                else:
                    output_shape[axis] = 0
            
            self.logger.debug("Slice %s: %s with starts %s, ends %s, axes %s, steps %s -> %s", 
                           node.name, input_shape, starts, ends, axes, steps, output_shape)
            return output_shape
            
        except Exception as e:
            self.logger.error("Slice error in %s: %s", node.name, str(e))
            return None
    
    def _handle_squeeze(self, node: NodeProto, input_shapes: List[List[int]], propagator: Any) -> List[int]:
        """
        Handle Squeeze operation.
        
        Squeeze removes dimensions of size 1 from a tensor.
        """
        try:
            if not input_shapes or len(input_shapes) < 1 or not input_shapes[0]:
                self.logger.error("Missing input shape for Squeeze %s", node.name)
                return None
            
            input_shape = input_shapes[0]
            
            # Get axes from attribute or second input
            axes = None
            
            # Try to get from second input (opset >= 13)
            if len(node.input) > 1:
                axes_tensor = get_constant_value(node.input[1], propagator)
                if axes_tensor is not None:
                    axes = axes_tensor.flatten().tolist()
            
            # Try to get from attribute (opset < 13)
            if axes is None:
                axes = self._get_attribute(node, "axes", None)
            
            # If axes is not specified, squeeze all dimensions of size 1
            if axes is None:
                output_shape = [dim for dim in input_shape if dim != 1]
                if not output_shape:  # If all dimensions are squeezed, result is a scalar
                    output_shape = [1]  # Represent as a 1D tensor with a single element
            else:
                # Handle negative axes
                axes = [axis if axis >= 0 else len(input_shape) + axis for axis in axes]
                
                # Validate all axes are valid and correspond to dimensions of size 1
                for axis in axes:
                    if axis < 0 or axis >= len(input_shape):
                        self.logger.error("Invalid axis %d for Squeeze %s", axis, node.name)
                        return None
                    if input_shape[axis] != 1:
                        self.logger.error("Cannot squeeze axis %d with dimension %d in %s",
                                       axis, input_shape[axis], node.name)
                        return None
                
                # Create output shape by removing specified dimensions
                output_shape = [
                    dim for i, dim in enumerate(input_shape) if i not in axes
                ]
                if not output_shape:  # If all dimensions are squeezed, result is a scalar
                    output_shape = [1]  # Represent as a 1D tensor with a single element
            
            self.logger.debug("Squeeze %s: %s with axes %s -> %s", 
                           node.name, input_shape, axes, output_shape)
            return output_shape
            
        except Exception as e:
            self.logger.error("Squeeze error in %s: %s", node.name, str(e))
            return None
    
    def _handle_unsqueeze(self, node: NodeProto, input_shapes: List[List[int]], propagator: Any) -> Optional[List[int]]:
        """
        Handle Unsqueeze operation.
        
        Unsqueeze inserts dimensions of size 1 into a tensor.
        """
        try:
            # Check if input_shapes has at least one element (even if it's an empty list for scalars)
            if not input_shapes or len(input_shapes) < 1:
                self.logger.error("Missing input shape for Unsqueeze %s", node.name)
                return None
            
            input_shape = input_shapes[0]  # Could be empty list (scalar)
            
            # Get axes from input (opset >= 13) or attribute (opset < 13)
            axes = None
            
            # Try to get from input (opset >= 13)
            if len(node.input) > 1:
                axes = get_constant_value(node.input[1], propagator)
            
            # Try to get from attribute (opset < 13)
            if axes is None:
                axes = self._get_attribute(node, "axes", None)
            
            # Convert to list if numpy array
            if isinstance(axes, np.ndarray):
                axes = axes.flatten().tolist()
            
            if axes is None:
                self.logger.error("Could not determine axes for Unsqueeze %s", node.name)
                return None
            
            # Calculate output rank: input_rank (0 for scalar) + len(axes)
            input_rank = len(input_shape)
            output_rank = input_rank + len(axes)
            
            # Handle negative axes (convert to positive based on output_rank)
            normalized_axes = []
            for axis in axes:
                if axis < 0:
                    axis = output_rank + axis
                normalized_axes.append(axis)
            
            # Validate axes
            if len(set(normalized_axes)) != len(normalized_axes):
                self.logger.error("Duplicate axes for Unsqueeze %s", node.name)
                return None
            
            if any(axis < 0 or axis >= output_rank for axis in normalized_axes):
                self.logger.error("Invalid axes %s for Unsqueeze %s (output_rank=%d)", 
                            normalized_axes, node.name, output_rank)
                return None
            
            # Create output shape by inserting 1s at specified axes
            output_shape = list(input_shape)  # Empty list for scalar
            # Insert axes in reverse-sorted order to avoid shifting issues
            for axis in sorted(normalized_axes, reverse=True):
                output_shape.insert(axis, 1)
            
            self.logger.debug("Unsqueeze %s: %s with axes %s -> %s", 
                        node.name, input_shape, axes, output_shape)
            return output_shape
            
        except Exception as e:
            self.logger.error("Unsqueeze error in %s: %s", node.name, str(e))
            return None
    def _handle_flatten(self, node: NodeProto, input_shapes: List[List[int]]) -> Optional[List[int]]:
        """
        Handle Flatten operation.
        
        Flatten reshapes a tensor into a 2D matrix by flattening dimensions.
        """
        try:
            if not input_shapes or len(input_shapes) < 1 or not input_shapes[0]:
                self.logger.error("Missing input shape for Flatten %s", node.name)
                return None
            
            input_shape = input_shapes[0]
            
            # Get axis attribute (default is 1)
            axis = self._get_attribute(node, "axis", 1)
            
            # Handle negative axis
            if axis < 0:
                axis = len(input_shape) + axis
            
            # Validate axis
            if axis < 0 or axis > len(input_shape):
                self.logger.error("Invalid axis %d for Flatten %s", axis, node.name)
                return None
            
            # Calculate output shape
            # First dimension is the product of all dimensions before axis
            # Second dimension is the product of all dimensions from axis onwards
            first_dim = 1
            for i in range(axis):
                first_dim *= input_shape[i]
            
            second_dim = 1
            for i in range(axis, len(input_shape)):
                second_dim *= input_shape[i]
            
            output_shape = [first_dim, second_dim]
            
            self.logger.debug("Flatten %s: %s with axis %d -> %s", 
                           node.name, input_shape, axis, output_shape)
            return output_shape
            
        except Exception as e:
            self.logger.error("Flatten error in %s: %s", node.name, str(e))
            return None
    
    def _handle_gather(self, node: NodeProto, input_shapes: List[List[int]], propagator: Any) -> Optional[List[int]]:
        """
        Handle Gather operation.
        
        Gather takes slices from the first input (data) using indices specified in the second input.
        """
        try:
            if not input_shapes or len(input_shapes) < 2:
                self.logger.error("Insufficient inputs for Gather %s", node.name)
                return None
            
            data_shape = input_shapes[0] if input_shapes[0] else None
            indices_shape = input_shapes[1] if len(input_shapes) > 1 and input_shapes[1] else []
            
            if not data_shape:
                self.logger.error("Missing data shape for Gather %s", node.name)
                return None
            
            # Get axis attribute (default is 0)
            axis = self._get_attribute(node, "axis", 0)
            
            # Handle negative axis
            if axis < 0:
                axis = len(data_shape) + axis
            
            # Validate axis
            if axis < 0 or axis >= len(data_shape):
                self.logger.error("Invalid axis %d for Gather %s", axis, node.name)
                return None
            
            # Case 1: Empty indices shape - try to get constant value
            if not indices_shape:
                # Try to get indices from initializers or constant nodes
                indices_value = None
                if len(node.input) > 1:
                    indices_value = get_constant_value(node.input[1], propagator)
                
                if indices_value is not None:
                    # We have the actual indices value
                    indices_shape = list(indices_value.shape)
                    self.logger.debug("Retrieved indices shape %s for Gather %s", indices_shape, node.name)
                else:
                    # Assume scalar index if we can't determine
                    indices_shape = []
                    self.logger.debug("Assuming scalar index for Gather %s", node.name)
            
            # Calculate output shape
            output_shape = list(data_shape[:axis])
            if indices_shape:  # Non-scalar indices
                output_shape.extend(indices_shape)
            output_shape.extend(data_shape[axis+1:])
            
            self.logger.debug("Gather %s: data %s, indices %s, axis %d -> %s", 
                          node.name, data_shape, indices_shape, axis, output_shape)
            return output_shape
            
        except Exception as e:
            self.logger.error("Gather error in %s: %s", node.name, str(e))
            return None
    
    def _handle_split(self, node: NodeProto, input_shapes: List[List[int]], propagator: Any) -> List[List[int]]:
        """
        Handle Split operation.
        
        Split divides a tensor into multiple tensors along a specified axis.
        """
        try:
            if not input_shapes or len(input_shapes) < 1 or not input_shapes[0]:
                self.logger.error("Missing input shape for Split %s", node.name)
                return [None] * len(node.output)
            
            input_shape = input_shapes[0]
            
            # Get axis attribute (default is 0)
            axis = self._get_attribute(node, "axis", 0)
            
            # Handle negative axis
            if axis < 0:
                axis = len(input_shape) + axis
            
            # Validate axis
            if axis < 0 or axis >= len(input_shape):
                self.logger.error("Invalid axis %d for Split %s", axis, node.name)
                return [None] * len(node.output)
            
            # Get split sizes
            split = None
            
            # Try to get from second input (opset >= 13)
            if len(node.input) > 1:
                split_tensor = get_constant_value(node.input[1], propagator)
                if split_tensor is not None:
                    split = split_tensor.flatten().tolist()
            
            # Try to get from attribute (opset < 13)
            if split is None:
                split = self._get_attribute(node, "split", None)
            
            # If split is not specified, split evenly
            if split is None:
                if input_shape[axis] % len(node.output) != 0:
                    self.logger.error("Cannot split dimension %d of size %d evenly into %d parts in %s",
                                   axis, input_shape[axis], len(node.output), node.name)
                    return [None] * len(node.output)
                
                split_size = input_shape[axis] // len(node.output)
                split = [split_size] * len(node.output)
            
            # Validate split sizes sum to input dimension
            if sum(split) != input_shape[axis]:
                self.logger.error("Split sizes %s do not sum to dimension size %d in %s",
                               split, input_shape[axis], node.name)
                return [None] * len(node.output)
            
            # Create output shapes
            output_shapes = []
            for size in split:
                output_shape = list(input_shape)
                output_shape[axis] = size
                output_shapes.append(output_shape)
            
            self.logger.debug("Split %s: %s along axis %d with sizes %s -> %s", 
                           node.name, input_shape, axis, split, output_shapes)
            return output_shapes
            
        except Exception as e:
            self.logger.error("Split error in %s: %s", node.name, str(e))
            return [None] * len(node.output)
    
    def _handle_expand(self, node: NodeProto, input_shapes: List[List[int]], propagator: Any) -> Optional[List[int]]:
        """
        Handle Expand operation.
        
        Expand broadcasts a tensor to a specified shape following the ONNX broadcast rules:
        - Dimensions are right aligned
        - Two corresponding dimensions are compatible when:
          - They are equal, or
          - One of them is 1
        """
        try:
            if not input_shapes or len(input_shapes) < 1 or not input_shapes[0]:
                self.logger.error("Missing input shape for Expand %s", node.name)
                return None
            
            input_shape = input_shapes[0]
            
            # Get shape from second input as a constant value
            if len(node.input) < 2:
                self.logger.error("Missing shape input for Expand %s", node.name)
                return None
            
            shape_value = get_constant_value(node.input[1], propagator)
            if shape_value is None:
                self.logger.error("Could not determine target shape for Expand %s", node.name)
                return None
            
            # Convert to list of integers
            if isinstance(shape_value, np.ndarray):
                target_shape = shape_value.flatten().tolist()
            else:
                target_shape = shape_value
            
            self.logger.debug("Expand %s: input shape %s, target shape %s", 
                           node.name, input_shape, target_shape)
            
            # ONNX Expand uses right-aligned broadcasting
            input_rank = len(input_shape)
            target_rank = len(target_shape)
            
            # Determine which shape needs padding (right alignment)
            if input_rank < target_rank:
                # Pad input on the left
                padded_input = [1] * (target_rank - input_rank) + list(input_shape)
            else:
                # No need to pad target, just use as is
                padded_input = input_shape
                padded_target = target_shape
            
            # Apply broadcasting rules according to ONNX specification
            output_shape = []
            for i, (in_dim, target_dim) in enumerate(zip(padded_input[-len(padded_target):], padded_target)):
                # Case 1: If target dimension is 1, keep input dimension
                if target_dim == 1:
                    output_shape.append(in_dim)
                # Case 2: If input dimension is 1, expand to target dimension
                elif in_dim == 1:
                    output_shape.append(target_dim)
                # Case 3: Dimensions match, use either
                elif in_dim == target_dim:
                    output_shape.append(in_dim)
                # Case 4: Dimensions are incompatible
                else:
                    self.logger.error("Cannot broadcast dimension %d from %d to %d in %s",
                                  i, in_dim, target_dim, node.name)
                    # We could provide a fallback here if needed, but better to report the error
                    return None
            
            self.logger.debug("Expand %s: %s to %s -> %s", 
                           node.name, input_shape, target_shape, output_shape)
            return output_shape
            
        except Exception as e:
            self.logger.error("Expand error in %s: %s", node.name, str(e))
            return None
    
    def _handle_shape(self, node: NodeProto, input_shapes: List[List[int]]) -> Optional[List[int]]:
        """
        Handle Shape operation.
        
        Shape returns the shape of a tensor as a 1D tensor.
        """
        try:
            if not input_shapes or len(input_shapes) < 1 or not input_shapes[0]:
                self.logger.error("Missing input shape for Shape %s", node.name)
                return None
            
            input_shape = input_shapes[0]
            
            # Get start and end attributes (defaults to full shape)
            start = self._get_attribute(node, "start", 0)
            end = self._get_attribute(node, "end", None)
            
            if end is None:
                end = len(input_shape)
            
            # Handle negative indices
            if start < 0:
                start = len(input_shape) + start
            if end < 0:
                end = len(input_shape) + end
            
            # Validate indices
            start = max(0, min(start, len(input_shape)))
            end = max(start, min(end, len(input_shape)))
            
            # Output shape is a 1D tensor with length = end - start
            output_shape = [end - start]
            
            self.logger.debug("Shape %s: %s with start %d, end %d -> %s", 
                           node.name, input_shape, start, end, output_shape)
            return output_shape
            
        except Exception as e:
            self.logger.error("Shape error in %s: %s", node.name, str(e))
            return None
    
    def _handle_constant_of_shape(self, node: NodeProto, input_shapes: List[List[int]], propagator: Any) -> Optional[List[int]]:
        """
        Handle ConstantOfShape operation.
        
        ConstantOfShape creates a tensor with a specified shape and filled with a constant value.
        """
        try:
            # Get shape from input
            if len(node.input) < 1:
                self.logger.error("Missing shape input for ConstantOfShape %s", node.name)
                return None
            
            shape_tensor = get_constant_value(node.input[0], propagator)
            if shape_tensor is None:
                self.logger.error("Could not determine shape for ConstantOfShape %s", node.name)
                return None
            
            # Convert to list if numpy array
            if isinstance(shape_tensor, np.ndarray):
                shape_tensor = shape_tensor.flatten().tolist()
            
            # Validate shape
            if any(dim < 0 for dim in shape_tensor):
                self.logger.error("Negative dimension in ConstantOfShape %s", node.name)
                return None
            
            # Output shape is simply the shape specified by the input
            output_shape = shape_tensor
            
            self.logger.debug("ConstantOfShape %s: %s", node.name, output_shape)
            return output_shape
            
        except Exception as e:
            self.logger.error("ConstantOfShape error in %s: %s", node.name, str(e))
            return None
    
