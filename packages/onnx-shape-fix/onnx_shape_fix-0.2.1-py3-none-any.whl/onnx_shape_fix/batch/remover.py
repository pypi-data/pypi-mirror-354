from typing import Dict, List, Optional, Any, Union
import onnx
from onnx import NodeProto, ModelProto, TensorProto, ValueInfoProto
import numpy as np
from ..utils.logger import Logger
from onnx import numpy_helper

'''
    When removing batch dimensions, we need to make sure that the model is still valid.
    it should update axes and other attributes that might be affected by removal of batch dim
    and make sure that the model still functions as intended (bascially as one batch dim model).

    tracker.py: where the batch dim is tracked for each nodes output tensors
    propagator.py: if the batch remove is true, it will remove the batch dim from the model when saving the new model
'''
class BatchDimensionRemover:
    """
    Removes batch dimensions from an ONNX model while adjusting attributes and shapes.
    
    This class handles:
    - Removing batch dimensions from tensor shapes
    - Adjusting node attributes that reference dimensions (e.g., axis parameters)
    - Ensuring the model remains valid after dimension removal
    """
    
    def __init__(self, model=None, batch_dims=None, input_shapes=None, verbose=False):
        """
        Initialize the batch dimension remover.
        
        Args:
            model: ONNX model to remove batch dimensions from
            batch_dims: Dictionary mapping tensor names to their batch dimensions
            input_shapes: Dictionary mapping input names to their shapes
            verbose: Whether to enable verbose logging
        """
        self.model = model
        self.batch_dims = batch_dims or {}
        self.input_shapes = input_shapes or {}
        self.verbose = verbose
        self.logger = Logger(verbose)
        self.initializers = {}
        
        # Store initializers for easy access
        if model and hasattr(model, 'graph'):
            self.graph = model.graph
            for initializer in model.graph.initializer:
                self.initializers[initializer.name] = initializer
        
        # Map of ops that need special attribute handling
        self._attr_handlers = self._initialize_attribute_handlers()
        
        # Add aliases for method names to avoid missing method errors
        self._remove_conv = self._update_conv_attrs
        self._update_conv = self._update_conv_attrs
        self._remove_batchnorm = self._update_batchnorm_attrs
        
        # Add aliases for all handlers to avoid missing method errors
        for op_type, handler in self._attr_handlers.items():
            alias_name = f"_remove_{op_type.lower()}"
            setattr(self, alias_name, handler)
    
    def _initialize_attribute_handlers(self) -> Dict[str, callable]:
        """Initialize handlers for updating attributes of specific op types."""
        return {
            'Concat': self._update_axis_attr,
            'Split': self._update_axis_attr,
            'Squeeze': self._update_axes_attr,
            'Unsqueeze': self._update_axes_attr,
            'ReduceMean': self._update_axes_attr,
            'ReduceSum': self._update_axes_attr,
            'ReduceMax': self._update_axes_attr,
            'ReduceMin': self._update_axes_attr,
            'Flatten': self._update_axis_attr,
            'Reshape': self._update_reshape_attrs,
            'BatchNormalization': self._update_axis_attr,
            'Softmax': self._update_axis_attr,
            'Conv': self._update_conv_attrs,
            'Gemm': self._remove_gemm,
            'Einsum': self._remove_einsum,
            'MatMul': self._remove_matmul,
            'Expand': self._remove_expand,
            'Where': self._remove_where,
            'Transpose': self._update_transpose_attrs,
            'Gather': self._update_gather_attrs,
            'Slice': self._update_slice_attrs,
            'Reshape': self._update_reshape_attrs,
            'Unsqueeze': self._adjust_squeeze_unsqueeze_axes,
            'Squeeze': self._adjust_squeeze_unsqueeze_axes,
            'Split': self._update_axis_attr,
            'BatchNormalization': self._update_batchnorm_attrs,
            'Conv': self._update_conv_attrs,
        }
    
    def remove_batch_dimensions(self, shape: List[int], batch_dim: Optional[int]) -> List[int]:
        """Remove a batch dimension from a shape."""
        if batch_dim is None or not shape:
            return shape
        
        if batch_dim < 0 or batch_dim >= len(shape):
            return shape
        
        # Create a new shape without the batch dimension
        new_shape = shape[:batch_dim] + shape[batch_dim+1:]
        return new_shape
    
    def _update_tensor_shape(self, 
                            tensor: ValueInfoProto, 
                            shape: List[int], 
                            batch_dim: Optional[int]) -> None:
        """
        Update tensor shape info by removing batch dimension.
        
        Args:
            tensor: ONNX tensor to update
            shape: Current shape
            batch_dim: Batch dimension to remove
        """
        try:
            if batch_dim is None:
                return
                
            if not hasattr(tensor, 'type') or not hasattr(tensor.type, 'tensor_type'):
                self.logger.warning(f"Tensor {tensor.name} has no tensor type")
                return
                
            tensor_shape = tensor.type.tensor_type.shape
            
            # Clear existing dimensions
            tensor_shape.ClearField('dim')
            
            # Add new dimensions, skipping batch dimension
            new_shape = self.remove_batch_dimensions(shape, batch_dim)
            for dim_size in new_shape:
                dim = tensor_shape.dim.add()
                dim.dim_value = dim_size
                
            self.logger.debug(f"Updated tensor {tensor.name} shape: {shape} -> {new_shape}")
        except Exception as e:
            self.logger.error(f"Error updating tensor shape for {tensor.name}: {str(e)}")
    
    def _update_initializer_shape(self, 
                                 initializer: TensorProto, 
                                 batch_dim: Optional[int]) -> None:
        """
        Update initializer shape by removing batch dimension.
        
        Args:
            initializer: ONNX initializer to update
            batch_dim: Batch dimension to remove
        """
        if batch_dim is None:
            return
            
        try:
            # Get current shape (dims)
            shape = list(initializer.dims)
            
            if batch_dim >= len(shape):
                self.logger.warning(
                    f"Batch dimension {batch_dim} is out of range for initializer {initializer.name} with shape {shape}"
                )
                return
                
            # Calculate new shape
            new_shape = self.remove_batch_dimensions(shape, batch_dim)
            
            # Get the data and reshape
            if initializer.data_type == TensorProto.FLOAT:
                raw_data = np.frombuffer(initializer.raw_data, dtype=np.float32).reshape(shape)
                # Remove batch dimension
                new_data = np.squeeze(raw_data, axis=batch_dim)
                
                # Update initializer
                initializer.ClearField('raw_data')
                initializer.raw_data = new_data.astype(np.float32).tobytes()
                initializer.ClearField('dims')
                initializer.dims.extend(new_shape)
                
                self.logger.debug(
                    f"Updated initializer {initializer.name} shape: {shape} -> {new_shape}"
                )
            else:
                self.logger.warning(
                    f"Skipping reshape of initializer {initializer.name} with data type {initializer.data_type}"
                )
        except Exception as e:
            self.logger.error(f"Error updating initializer {initializer.name}: {str(e)}")
    
    def _update_node_attributes(self, node: NodeProto, batch_dim: int) -> None:
        """
        Update node attributes that reference dimensions.
        
        Args:
            node: The node to update
            batch_dim: Batch dimension to remove
        """
        # Find the appropriate attribute handler for this op type
        if node.op_type in self._attr_handlers:
            self._attr_handlers[node.op_type](node, batch_dim)

    
    def _update_axis_attr(self, node: NodeProto, batch_dim: int) -> None:
        """
        Update 'axis' attribute in node to account for removed batch dimension.
        
        Args:
            node: ONNX node to update
            batch_dim: Batch dimension that was removed
        """
        for attr in node.attribute:
            if attr.name == 'axis':
                if attr.i == batch_dim:
                    self.logger.warning(
                        f"Node {node.name} ({node.op_type}) has axis attribute equal to batch dimension. "
                        f"This could lead to unexpected results."
                    )
    
    def _update_axes_attr(self, node: NodeProto, batch_dim: int) -> None:
        """
        Update 'axes' attribute in node to account for removed batch dimension.
        
        Args:
            node: ONNX node to update
            batch_dim: Batch dimension that was removed
        """
        for attr in node.attribute:
            if attr.name == 'axes':
                new_axes = []
                for axis in attr.ints:
                    if axis == batch_dim:
                        self.logger.warning(
                            f"Node {node.name} ({node.op_type}) has an axis equal to batch dimension. "
                            f"Removing this axis."
                        )
                    elif axis > batch_dim:
                        new_axes.append(axis - 1)
                    else:
                        new_axes.append(axis)
                
                # Update attribute
                attr.ClearField('ints')
                attr.ints.extend(new_axes)

    
    def _update_transpose_attrs(self, node: NodeProto, batch_dim: int) -> None:
        """
        Update 'perm' attribute in Transpose node.
        
        Args:
            node: Transpose node to update
            batch_dim: Batch dimension that was removed
        """
        for attr in node.attribute:
            if attr.name == 'perm':
                old_perm = list(attr.ints)
                new_perm = []
                                
                # Adjust each value in the permutation
                for axis in old_perm:
                    if axis == batch_dim:
                        # Skip batch dimension
                        continue
                    elif axis > batch_dim:
                        # Decrease by one for axes after batch dimension
                        new_perm.append(axis - 1)
                    else:
                        # Keep as is for axes before batch dimension
                        new_perm.append(axis)
                
                # Update the attribute
                attr.ints[:] = new_perm
                # self.logger.debug(f"Updated transpose permutation: {old_perm} → {new_perm}")
    
    def _update_slice_attrs(self, node: NodeProto, batch_dim: int) -> None:
        """
        Update attributes for Slice node.
        
        Args:
            node: Slice node to update
            batch_dim: Batch dimension that was removed
        """
        # For older ONNX versions where starts/ends/axes are attributes
        axes = None
        for attr in node.attribute:
            if attr.name == 'axes':
                axes = list(attr.ints)
                break
                
        if axes is not None:
            # Check if batch dimension is in axes
            if batch_dim in axes:
                self.logger.warning(
                    f"Slice node {node.name} has batch dimension in axes attribute. "
                    "This could lead to unexpected results."
                )
            
            # Adjust axes values
            new_axes = []
            for axis in axes:
                if axis == batch_dim:
                    # Skip batch dimension
                    continue
                elif axis > batch_dim:
                    new_axes.append(axis - 1)
                else:
                    new_axes.append(axis)
            
            # Update attribute
            for attr in node.attribute:
                if attr.name == 'axes':
                    attr.ClearField('ints')
                    attr.ints.extend(new_axes)
                    self.logger.debug(
                        f"Updated Slice axes for {node.name}: {axes} -> {new_axes}"
                    )
    
    def _update_reshape_attrs(self, node: NodeProto, batch_dim: int, input_shape: Optional[List[int]] = None) -> None:
        """
        Update the shape tensor for Reshape nodes when removing batch dimension.
        
        Args:
            node: Reshape node to update
            batch_dim: Batch dimension that was removed
            input_shape: Optional shape of input tensor after batch removal
        """
        if len(node.input) < 2:
            return  # Reshape needs a shape input
        
        # Get the shape input
        shape_input = node.input[1]
        
        # Find initializer or constant node that provides the shape
        shape_value = None
        if hasattr(self, 'initializers') and shape_input in self.initializers:
            shape_value = numpy_helper.to_array(self.initializers[shape_input])
        else:
            if hasattr(self, 'graph'):
                for input_node in self.graph.node:
                    if input_node.op_type == 'Constant' and input_node.output[0] == shape_input:
                        for attr in input_node.attribute:
                            if attr.name == 'value':
                                shape_value = numpy_helper.to_array(attr.t)
                                break
    
        if shape_value is None:
            self.logger.warning(f"Could not find shape value for Reshape {node.name}, cannot adapt shape")
            return
        
        # Log original shape
        old_shape = shape_value.tolist() if hasattr(shape_value, 'tolist') else list(shape_value)
        self.logger.debug(f"Original reshape target shape: {old_shape}")
        
        # Get batch dimension information from tracker if available
        batch_tracker = getattr(self, 'batch_tracker', None)
        input_name = node.input[0] if node.input else None
        output_name = node.output[0] if node.output else None
        
        # Get information needed for adjusting shapes properly
        input_batch_dim = None
        output_batch_dim = None
        input_batch_size = None
        
        if batch_tracker and input_name:
            input_batch_dim = batch_tracker.get_batch_dim(input_name)
        
        if batch_tracker and output_name:
            output_batch_dim = batch_tracker.get_batch_dim(output_name)
        
        # Get the input shape information if available
        if hasattr(self, 'shape_info') and input_name and input_name in self.shape_info:
            input_tensor_shape = self.shape_info[input_name].shape
            if input_tensor_shape and input_batch_dim is not None and input_batch_dim < len(input_tensor_shape.dim):
                input_batch_size = input_tensor_shape.dim[input_batch_dim].dim_value
        
        # Create new shape based on batch dimension analysis
        new_shape = []
        
        # Case 1: Reshape target has a -1 dimension (dynamic)
        if -1 in old_shape:
            dynamic_idx = old_shape.index(-1)
            
            # Adjust dimensions around the dynamic one
            for i, dim in enumerate(old_shape):
                if i == dynamic_idx:
                    # Keep the dynamic dimension
                    new_shape.append(-1)
                elif output_batch_dim is not None and i == output_batch_dim:
                    # Skip the batch dimension, as it will be removed
                    continue
                else:
                    # Keep other dimensions unchanged
                    new_shape.append(dim)
                
            self.logger.debug(f"Adjusted reshape target with dynamic dim: {old_shape} -> {new_shape}")
        
        # Case 2: Output batch dim is known - remove that dimension
        elif output_batch_dim is not None and output_batch_dim < len(old_shape):
            for i, dim in enumerate(old_shape):
                if i != output_batch_dim:
                    new_shape.append(dim)
        
            self.logger.debug(f"Removed batch dimension {output_batch_dim} from reshape target: {old_shape} -> {new_shape}")
        
        # Case 3: First dimension matches input batch size - remove it
        elif input_batch_size is not None and len(old_shape) > 0 and old_shape[0] == input_batch_size:
            new_shape = old_shape[1:]
            self.logger.debug(f"Removed batch size {input_batch_size} from reshape target: {old_shape} -> {new_shape}")
        
        # Case 4: Conservative approach - just remove the dimension 1 if present at index 0
        elif len(old_shape) > 0 and old_shape[0] == 1:
            new_shape = old_shape[1:]
            self.logger.debug(f"Removed dimension 1 from reshape target: {old_shape} -> {new_shape}")
        
        # Case 5: Fallback - keep shape unchanged
        else:
            self.logger.warning(f"Could not determine how to adjust reshape target shape: {old_shape}")
            new_shape = old_shape
        
        # Update the shape tensor
        if new_shape != old_shape:
            # Create new tensor
            new_tensor = numpy_helper.from_array(np.array(new_shape, dtype=np.int64))
            
            # Update initializer or constant node
            if hasattr(self, 'initializers') and shape_input in self.initializers:
                self.initializers[shape_input] = new_tensor
                self.logger.debug(f"Updated initializer {shape_input} with new shape {new_shape}")
            else:
                if hasattr(self, 'graph'):
                    for input_node in self.graph.node:
                        if input_node.op_type == 'Constant' and input_node.output[0] == shape_input:
                            for attr in input_node.attribute:
                                if attr.name == 'value':
                                    attr.t.CopyFrom(new_tensor)
                                    self.logger.debug(f"Updated constant {input_node.name} with new shape {new_shape}")
                                    break
    
    def _remove_einsum(self, node: NodeProto, batch_dim: int) -> None:
        """
        Special handling for Einsum nodes - update equation to account for removed batch dim.
        
        Args:
            node: Einsum node to update
            batch_dim: Batch dimension that was removed
        """
        for attr in node.attribute:
            if attr.name == 'equation':
                equation = attr.s.decode('utf-8') if isinstance(attr.s, bytes) else attr.s
                self.logger.warning(
                    f"Einsum node {node.name} with equation '{equation}' found. "
                    "Batch dimension removal may affect the semantics. Manual verification recommended."
                )
                # Einsum equations are complex to automatically update - best to warn
    
    def _update_conv_attrs(self, node: NodeProto, batch_dim: int) -> None:
        """
        Update attributes in Conv node when removing batch dimension.
        
        Args:
            node: Conv node to update
            batch_dim: Batch dimension that was removed
        """
        # For most common Conv operations, no attribute updates are needed as 
        # batch dimension is typically the first dimension (N in NCHW format)
        # and Conv ops typically work on the channel dimensions
        
        # Check if batch dimension is 0 (standard case)
        if batch_dim == 0:
            # Standard case - no attribute changes needed
            # self.logger.debug(f"Conv {node.name}: Standard batch dimension removal, no attribute changes needed")
            return
        
        # For non-standard batch dimension locations, we need to issue a warning
        # as removing them might fundamentally change the operation
        self.logger.warning(
            f"Conv {node.name} has non-standard batch dimension {batch_dim}. "
            f"Removing it may change model behavior."
        )
    
    def _remove_gemm(self, node: NodeProto, batch_dim: int) -> None:
        """
        Special handling for Gemm nodes.
        
        Args:
            node: Gemm node to update
            batch_dim: Batch dimension that was removed
        """
        # Gemm operation might need special handling if batch_dim is not 0
        if batch_dim != 0:
            self.logger.warning(
                f"Gemm node {node.name} with non-standard batch dimension {batch_dim}. "
                "This could lead to unexpected results."
            )
    
    def _remove_matmul(self, node: NodeProto, batch_dim: int):
        """
        Handle MatMul operations with batch dimension.
        For MatMul operations, batch dimensions can be in different positions.
        """
        # No specific attribute changes needed for MatMul
        # As long as batch dimensions are tracked correctly in the inputs and outputs
        if self.verbose:
            self.logger.debug(f"MatMul {node.name}: Removing batch dimension at position {batch_dim}")
    
    def _remove_expand(self, node: NodeProto, batch_dim: int) -> None:
        """
        Special handling for Expand nodes.
        
        Args:
            node: Expand node to update
            batch_dim: Batch dimension that was removed
        """
        # Expand needs careful handling - shapes used for expansion may need adjustment
        self.logger.warning(
            f"Expand node {node.name} found. Batch dimension removal may affect "
            "the semantics of this operation. Manual verification recommended."
        )
    
    def _remove_where(self, node: NodeProto, batch_dim: int) -> None:
        """
        Special handling for Where nodes which do element-wise selection.
        
        Args:
            node: Where node to update
            batch_dim: Batch dimension that was removed
        """
        # Where follows broadcasting rules, so it should adapt automatically
        # But warn in case there's something unusual
        self.logger.debug(f"Where node {node.name} found. Broadcasting should handle batch dim removal.")
    
    def _adjust_squeeze_unsqueeze_axes(self, node: NodeProto, batch_dim: int) -> None:
        """
        Adjust axes for Squeeze/Unsqueeze operations when removing batch dimension.
        
        Args:
            node: The node to adjust
            batch_dim: The batch dimension being removed
        """
        op_type = node.op_type
        if op_type not in ('Squeeze', 'Unsqueeze'):
            return
        
        # self.logger.debug(f"🔍 Checking axis adjustment for {op_type} node: {node.name}")
        
        # Handle axes in attributes (ONNX <13)
        axes_attr = None
        for attr in node.attribute:
            if attr.name == 'axes':
                axes_attr = attr
                break
        
        if axes_attr:
            # Get current axes
            current_axes = list(axes_attr.ints)
            
            # Adjust axes that are greater than batch_dim (decrement by 1)
            new_axes = []
            for axis in current_axes:
                if axis > batch_dim:
                    new_axes.append(axis - 1)
                elif axis < batch_dim:
                    new_axes.append(axis)
                # Skip axes equal to batch_dim as they will be irrelevant after batch removal
            
            # Update attribute with new axes
            axes_attr.ints[:] = new_axes
            
            self.logger.debug(f"📐 {op_type} {node.name}: Adjusted axes attribute from {current_axes} to {new_axes} (batch_dim={batch_dim})")
        
        # Handle axes as input (ONNX >=13)
        elif len(node.input) > 1:
            # Find the initializer for the axes input
            axes_input_name = node.input[1]
            
            # Look for the initializer in the graph
            found_initializer = False
            for initializer in self.model.graph.initializer:
                if initializer.name == axes_input_name:
                    found_initializer = True
                    # Convert to NumPy array
                    import numpy as np
                    
                    axes_tensor = numpy_helper.to_array(initializer)
                    current_axes = axes_tensor.flatten().tolist()
                    
                    # Adjust axes
                    new_axes = []
                    for axis in current_axes:
                        if axis > batch_dim:
                            new_axes.append(axis - 1)
                        elif axis < batch_dim:
                            new_axes.append(axis)
                        # Skip axes equal to batch_dim
                    
                    # Create new initializer tensor
                    new_tensor = numpy_helper.from_array(
                        np.array(new_axes, dtype=axes_tensor.dtype),
                        name=initializer.name
                    )
                    
                    # Replace the initializer
                    initializer.CopyFrom(new_tensor)
                    
                    break
            
            if not found_initializer:
                self.logger.debug(f"⚠️ Could not find initializer for axes input: {axes_input_name}")
    
    def _adjust_reduce_op_axes(self, node: NodeProto, batch_dim: int) -> None:
        """
        Adjust axes for reduce operations when removing batch dimension.
        
        Args:
            node: The node to adjust
            batch_dim: The batch dimension being removed
        """
        # List of ONNX reduce operations
        reduce_ops = [
            'ReduceMax', 'ReduceMean', 'ReduceMin', 'ReduceProd', 
            'ReduceSum', 'ReduceSumSquare', 'ReduceL1', 'ReduceL2',
            'ReduceLogSum', 'ReduceLogSumExp'
        ]
        
        if node.op_type not in reduce_ops:
            return
        
        # self.logger.debug(f"🔍 Checking axis adjustment for {node.op_type} node: {node.name}")
        
        # Find axes attribute
        axes_attr = None
        for attr in node.attribute:
            if attr.name == 'axes':
                axes_attr = attr
                break
        
        if axes_attr:
            # Get current axes
            current_axes = list(axes_attr.ints)
            
            # Adjust axes that are greater than batch_dim (decrement by 1)
            new_axes = []
            for axis in current_axes:
                if axis > batch_dim:
                    new_axes.append(axis - 1)
                elif axis < batch_dim:
                    new_axes.append(axis)
                # Skip axes equal to batch_dim
            
            # Update attribute with new axes
            axes_attr.ints[:] = new_axes
            
            self.logger.debug(f"📐 {node.op_type} {node.name}: Adjusted axes attribute from {current_axes} to {new_axes} (batch_dim={batch_dim})")
        
        # Handle axes as input (newer opsets)
        elif len(node.input) > 1:
            # Find the initializer for the axes input
            axes_input_name = node.input[1]
            
            # Look for the initializer in the graph
            found_initializer = False
            for initializer in self.model.graph.initializer:
                if initializer.name == axes_input_name:
                    found_initializer = True
                    # Convert to NumPy array
                    import numpy as np
                    
                    axes_tensor = numpy_helper.to_array(initializer)
                    current_axes = axes_tensor.flatten().tolist()
                    
                    # Adjust axes
                    new_axes = []
                    for axis in current_axes:
                        if axis > batch_dim:
                            new_axes.append(axis - 1)
                        elif axis < batch_dim:
                            new_axes.append(axis)
                        # Skip axes equal to batch_dim
                    
                    # Create new initializer tensor
                    new_tensor = numpy_helper.from_array(
                        np.array(new_axes, dtype=axes_tensor.dtype),
                        name=initializer.name
                    )
                    
                    # Replace the initializer
                    initializer.CopyFrom(new_tensor)
                    
                    break
            
            if not found_initializer:
                self.logger.debug(f"⚠️ Could not find initializer for axes input: {axes_input_name}")
    
    def _remove_batch_dimension(self, node: NodeProto, batch_dim: int) -> None:
        """
        Remove batch dimension from node inputs and outputs.
        
        Args:
            node: ONNX node to process
            batch_dim: Batch dimension to remove
        """
        # Special handlers for specific node types
        special_handlers = {
            'Conv': self._remove_conv,
            'BatchNormalization': self._remove_batchnorm,
            'MatMul': self._remove_matmul,
            'Gemm': self._remove_gemm,
            'Expand': self._remove_expand,
            'Softmax': self._remove_softmax,
            'Where': self._remove_where,
            # Add other special handlers as needed
        }
        
        # First adjust axes for operations that use them
        self._adjust_squeeze_unsqueeze_axes(node, batch_dim)
        self._adjust_reduce_op_axes(node, batch_dim)
        
        # Process with special handler if available, otherwise use default
        if node.op_type in special_handlers:
            special_handlers[node.op_type](node, batch_dim)

    
    def process_model(self, 
                     model: ModelProto, 
                     batch_dims: Dict[str, Optional[int]]) -> ModelProto:
        """Remove batch dimensions from model tensors."""
        try:
            model_copy = onnx.ModelProto()
            model_copy.CopyFrom(model)
            
            # Track shapes for all tensors
            shape_map = {}
            
            # Process inputs with simplified logging
            self.logger.info("🔄 Removing batch dimensions from model")
            
            # Process inputs
            input_count = len(model_copy.graph.input)
            self.logger.info(f"  • Processing {input_count} inputs")
            
            for input_info in model_copy.graph.input:
                shape = self._get_shape_from_value_info(input_info)
                if not shape:
                    continue
                
                shape_map[input_info.name] = shape
                
                # Update shape if batch dimension exists
                batch_dim = batch_dims.get(input_info.name)
                if batch_dim is not None:
                    new_shape = self.remove_batch_dimensions(shape, batch_dim)
                    self._update_tensor_shape(input_info, new_shape)
                    shape_map[input_info.name] = new_shape
                    self.logger.info(f"    ✓ {input_info.name}: {shape} → {new_shape}")
            
            # Similarly process other tensors with minimal logging
            # [rest of the method with simplified logging]
            
            self.logger.info("✅ Batch dimension removal complete")
            return model_copy
            
        except Exception as e:
            self.logger.error(f"❌ Error removing batch dimensions: {str(e)}")
            raise

    def remove_batch_dimension(self) -> None:
        """Remove batch dimension from all tensors in the model."""
        
        # Verify that all required inputs have batch dimensions tracked
        missing_batch_inputs = []
        for input_name in self.input_shapes:
            if input_name not in self.batch_dims:
                missing_batch_inputs.append(input_name)
        
        if missing_batch_inputs:
            self.logger.warning(f"⚠️ The following inputs don't have batch dimensions tracked: {missing_batch_inputs}")
            self.logger.warning("⚠️ Model might not be correctly processed!")
        
        # Process model nodes
        for node in self.model.graph.node:
            if self.verbose:
                self.logger.debug(f"Processing node: {node.name} ({node.op_type})")
            
            # Check if any input has a batch dimension to remove
            batch_dims_to_remove = {}
            for idx, input_name in enumerate(node.input):
                if input_name in self.batch_dims:
                    batch_dims_to_remove[idx] = self.batch_dims[input_name]
            
            # Process each batch dimension to remove
            for idx, batch_dim in batch_dims_to_remove.items():
                if batch_dim is not None:
                    self.logger.debug(f"🔄 Removing batch dimension {batch_dim} from input {idx}: {node.input[idx]}")
                    
                    # First adjust axes for operations that use them - this is key for correct operation
                    self._adjust_squeeze_unsqueeze_axes(node, batch_dim)
                    self._adjust_reduce_op_axes(node, batch_dim)
                    
                    # Then remove the batch dimension
                    self._remove_batch_dimension(node, batch_dim)

    def verify_batch_dimensions(self) -> dict:
        """
        Verify that batch dimensions are consistent throughout the model.
        
        Returns:
            dict: Report of batch dimension consistency
        """
        result = {
            "consistent": True,
            "issues": [],
            "batch_dims": {}
        }
        
        # Group tensors by their batch dimensions
        for tensor_name, batch_dim in self.batch_dims.items():
            if batch_dim is not None:
                if batch_dim not in result["batch_dims"]:
                    result["batch_dims"][batch_dim] = []
                result["batch_dims"][batch_dim].append(tensor_name)
        
        # Check for multiple batch dimensions
        if len(result["batch_dims"]) > 1:
            result["consistent"] = False
            dims = ", ".join(str(d) for d in result["batch_dims"].keys())
            result["issues"].append(f"Multiple batch dimensions found: {dims}")
        
        # Check for missing batch dimensions in input shapes
        for tensor_name in self.input_shapes:
            if tensor_name not in self.batch_dims:
                result["consistent"] = False
                result["issues"].append(f"Missing batch dimension for input: {tensor_name}")
        
        # Log detailed report in verbose mode
        if self.verbose:
            self.logger.info("🔍 Batch Dimension Verification Report:")
            if result["consistent"]:
                self.logger.info("  ✅ Batch dimensions are consistent")
            else:
                self.logger.warning("  ⚠️ Batch dimensions are not consistent")
                for issue in result["issues"]:
                    self.logger.warning(f"    • {issue}")
            
            for batch_dim, tensor_names in result["batch_dims"].items():
                count = len(tensor_names)
                self.logger.info(f"  📊 Batch dimension {batch_dim}: {count} tensors")
        
        return result

    def _update_gather_attrs(self, node: NodeProto, batch_dim: int) -> None:
        """
        Update 'axis' attribute in Gather node.
        
        Args:
            node: Gather node to update
            batch_dim: Batch dimension that was removed
        """
        for attr in node.attribute:
            if attr.name == 'axis':
                old_axis = attr.i
                
                # If the axis is greater than the batch dimension, it needs to be adjusted
                if old_axis > batch_dim:
                    new_axis = old_axis - 1
                    attr.i = new_axis
                    self.logger.debug(
                        f"Updated Gather axis: {old_axis} → {new_axis} (batch_dim={batch_dim})"
                    )
                # If axis equals batch_dim, gather behavior changes fundamentally
                elif old_axis == batch_dim:
                    self.logger.warning(
                        f"Gather {node.name} was gathering along batch dimension (axis={old_axis}). "
                        f"This may change model behavior."
                    )

    def _update_batchnorm_attrs(self, node: NodeProto, batch_dim: int) -> None:
        """
        Update attributes in BatchNormalization node when removing batch dimensions.
        
        Args:
            node: BatchNormalization node to update
            batch_dim: Batch dimension that was removed
        """
        # BatchNormalization generally operates on the second dimension (channel dimension)
        # No attribute updates are needed if batch is in standard position (dimension 0)
        if batch_dim == 0:
            # self.logger.debug(f"BatchNormalization {node.name}: Standard batch dimension removal, no attribute changes needed")
            return
        
        # If batch dimension is not 0, it's in a non-standard position
        # This might fundamentally change the operation's behavior
        self.logger.warning(
            f"BatchNormalization {node.name} has non-standard batch dimension {batch_dim}. "
            f"Removing it may change model behavior."
        )

    def apply_to_model(self):
        """
        Apply batch dimension removal to the model.
        
        This method:
        1. Updates tensor shapes in the model
        2. Updates node attributes that reference dimensions
        3. Returns the updated model
        """
        try:
            self.logger.info("Applying batch dimension removal to model")
            
            # First, collect all expected shapes after batch removal
            self.expected_shapes = {}
            if hasattr(self, 'propagator') and hasattr(self.propagator, 'shape_dict'):
                for tensor_name, full_shape in self.propagator.shape_dict.items():
                    if tensor_name in self.batch_dims and self.batch_dims[tensor_name] is not None:
                        batch_dim = self.batch_dims[tensor_name]
                        if full_shape and 0 <= batch_dim < len(full_shape):
                            expected_shape = full_shape.copy()
                            del expected_shape[batch_dim]
                            self.expected_shapes[tensor_name] = expected_shape
            
            # Process inputs
            for input_value in self.model.graph.input:
                self._remove_batch_from_value_info(input_value)
                
            # Process outputs
            for output_value in self.model.graph.output:
                self._remove_batch_from_value_info(output_value)
                
            # Process value_info
            for value_info in self.model.graph.value_info:
                self._remove_batch_from_value_info(value_info)
                
            # Process nodes
            for node in self.model.graph.node:
                self._process_node(node)
                
            # Process initializers if needed (usually not affected by batch dimensions)
            for initializer in self.model.graph.initializer:
                self._process_initializer(initializer)
                
            self.logger.info("✅ Batch dimension removal completed")
            return self.model
        except Exception as e:
            self.logger.error(f"❌ Error applying batch dimension removal: {str(e)}")
            import traceback
            self.logger.debug(f"Traceback: {traceback.format_exc()}")
            # Return the model unchanged if an error occurs
            return self.model
        
    def _process_node(self, node: NodeProto):
        """Process a node's attributes to adjust for batch dimension removal."""
        # Get batch dimension from the node's first input, if it exists
        batch_dim = None
        for input_name in node.input:
            if input_name and input_name in self.batch_dims:
                batch_dim = self.batch_dims.get(input_name)
                if batch_dim is not None:
                    break
        
        # If no batch dimension found, skip processing
        if batch_dim is None:
            return
        
        # Check if we have a specialized handler
        handler = None
        if node.op_type in self._attr_handlers:
            # Use registered handler
            handler = self._attr_handlers[node.op_type]
        else:
            # Try specific remover
            handler_name = f"_remove_{node.op_type.lower()}"
            handler = getattr(self, handler_name, None)
        
        # Apply handler or default
        if handler is not None:
            handler(node, batch_dim)
    def _remove_batch_from_value_info(self, value_info: ValueInfoProto):
        """Remove batch dimension from a ValueInfoProto."""
        tensor_name = value_info.name
        if tensor_name not in self.batch_dims:
            return
        
        batch_dim = self.batch_dims[tensor_name]
        if batch_dim is None:
            return
        
        try:
            # Check if tensor has shape
            if not value_info.type.tensor_type.HasField("shape"):
                return
            
            # Get current shape
            old_shape = []
            for dim in value_info.type.tensor_type.shape.dim:
                if dim.HasField("dim_value"):
                    old_shape.append(int(dim.dim_value))
                elif dim.HasField("dim_param"):
                    old_shape.append(dim.dim_param)
                else:
                    old_shape.append(None)
            
            # Use expected shape from propagation if available
            if hasattr(self, 'expected_shapes') and tensor_name in self.expected_shapes:
                expected_shape = self.expected_shapes[tensor_name]
                # Skip shape processing and directly use expected shape
                new_shape = expected_shape
            else:
                # Remove batch dimension
                new_shape = self.remove_batch_dimensions(old_shape, batch_dim)
            
            # Update shape in value_info
            value_info.type.tensor_type.shape.ClearField("dim")
            for dim_value in new_shape:
                new_dim = value_info.type.tensor_type.shape.dim.add()
                if isinstance(dim_value, int):
                    new_dim.dim_value = dim_value
                elif isinstance(dim_value, str):
                    new_dim.dim_param = dim_value
                elif dim_value is None:
                    # For None/unknown dimensions, use a parameter
                    new_dim.dim_param = "?"
            
            # Check if we got an unexpected shape
            if hasattr(self, 'expected_shapes') and tensor_name in self.expected_shapes:
                expected_shape = self.expected_shapes[tensor_name]
                if new_shape != expected_shape:
                    # Try to fix any mismatches by using expected values for non-None dimensions
                    for i, (actual, expected) in enumerate(zip(new_shape, expected_shape)):
                        if expected is not None and isinstance(expected, int) and (actual is None or actual == '?' or isinstance(actual, str)):
                            # Replace unknown with known expected value
                            value_info.type.tensor_type.shape.dim[i].ClearField("dim_param")
                            value_info.type.tensor_type.shape.dim[i].dim_value = expected
                            new_shape[i] = expected
                            
                    # Log if still different
                    if new_shape != expected_shape:
                        self.logger.warning(f"Unexpected shape after batch removal for {tensor_name}: {new_shape} (expected {expected_shape})")
            
            elif self.verbose:
                self.logger.debug(f"Updated shape for {tensor_name}: {old_shape} → {new_shape}")
        except Exception as e:
            self.logger.error(f"Error updating shape for {tensor_name}: {str(e)}")

    def _process_initializer(self, initializer: TensorProto):
        """Process an initializer tensor (typically doesn't need batch dimension changes)."""
        tensor_name = initializer.name
        if tensor_name not in self.batch_dims:
            return
        
        batch_dim = self.batch_dims[tensor_name]
        if batch_dim is None:
            return
        
        # Most initializers should not have batch dimensions
        # This is just a safeguard in case some do
        self.logger.warning(f"Initializer {tensor_name} has batch dimension {batch_dim}. " 
                            f"This is unusual and may indicate an issue.")
