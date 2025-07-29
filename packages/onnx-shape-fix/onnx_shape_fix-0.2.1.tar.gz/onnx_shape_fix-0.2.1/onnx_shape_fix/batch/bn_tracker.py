from typing import Dict, Callable, List, Optional, Any
from onnx import NodeProto

# Registry to store all trackers
tracker_registry: Dict[str, Callable] = {}

def bn_tracker(op_type: str):
    """
    Decorator to register batch dimension trackers.
    
    Args:
        op_type: The ONNX operation type this tracker processes
    """
    def decorator(func):
        tracker_registry[op_type] = func
        return func
    return decorator

@bn_tracker('Transpose')
def track_transpose(tracker, node: NodeProto, 
                    input_shapes: Optional[List[List[int]]] = None,
                    output_shape: Optional[List[int]] = None) -> None:
    """Track Transpose operation batch dimensions."""
    if not node.input:
        tracker._set_outputs(node, None)
        return
        
    input_name = node.input[0]
    input_bdim = tracker.get_batch_dim(input_name)
    
    if input_bdim is None:
        tracker._set_outputs(node, None)
        return

    # Find permutation attribute
    perm = []
    for attr in node.attribute:
        if attr.name == 'perm':
            perm = list(attr.ints)
            break
            
    # Log the transpose operation
    if tracker.verbose:
        input_shape = input_shapes[0] if input_shapes and input_shapes[0] else "unknown"
        output_shape = output_shape if output_shape else "unknown"
        tracker.logger.debug(f"Transpose {node.name}: {input_shape} with perm {perm} -> {output_shape}")

    # If no permutation is specified, it's a default reverse
    if not perm and input_shapes and input_shapes[0]:
        perm = list(range(len(input_shapes[0])))
        perm.reverse()

    # Calculate what the permutation would be after batch dimension removal
    if perm and input_bdim is not None and tracker.verbose:
        adjusted_perm = []
        for axis in perm:
            if axis == input_bdim:
                # Skip batch dimension
                continue
            elif axis > input_bdim:
                # Adjust axis value
                adjusted_perm.append(axis - 1)
            else:
                adjusted_perm.append(axis)
        
        tracker.logger.debug(f"  🔍 After batch removal, perm would become: {adjusted_perm} (batch_dim={input_bdim})")

    # Determine the output batch dimension
    output_bdim = None
    if perm:
        # Find where the batch dimension goes
        if input_bdim < len(perm):
            output_bdim = perm.index(input_bdim)
            
            # Log the batch dimension transformation
            if tracker.verbose:
                tracker.logger.debug(f"  📐 Transpose: batch dim {input_bdim} → {output_bdim}")
        else:
            if tracker.verbose:
                tracker.logger.debug(f"  ⚠ Transpose: batch dim {input_bdim} is out of bounds for permutation")

    tracker._set_outputs(node, output_bdim)

@bn_tracker('Reshape')
def track_reshape(tracker, node: NodeProto,
                  input_shapes: Optional[List[List[int]]] = None,
                  output_shape: Optional[List[int]] = None) -> None:
    """Track Reshape operation batch dimensions with improved shape analysis."""
    if not node.input or len(node.input) < 2:
        tracker._set_outputs(node, None)
        return
        
    # Get input batch dimension
    input_name = node.input[0]
    input_bdim = tracker.get_batch_dim(input_name)
    
    if input_bdim is None:
        tracker._set_outputs(node, None)
        return

    # Get shape input (the target shape for reshape)
    shape_input = node.input[1]
    target_shape = None
    
    # Try to extract the target shape from initializers or constants
    if hasattr(tracker, 'propagator') and tracker.propagator:
        propagator = tracker.propagator
        
        # Check in initializers
        if shape_input in propagator.initializers:
            target_shape = propagator.get_initializer_array(shape_input).tolist()
        # Check in constant nodes
        else:
            target_shape = propagator.get_constant_value(shape_input)
            if target_shape is not None:
                target_shape = target_shape.tolist() if hasattr(target_shape, 'tolist') else list(target_shape)

    # Log the reshape operation
    tracker.logger.debug(f"Handling Reshape {node.name}")
    
    # Log the target shape if we found it
    if target_shape:
        tracker.logger.debug(f"Reshape target shape from input: {target_shape}")
    
    if input_shapes and input_shapes[0] and output_shape:
        tracker.logger.debug(f"Reshape {node.name}: {input_shapes[0]} -> {output_shape}")

    # Determine if the batch dimension is preserved by comparing shapes
    output_bdim = None
    
    # Case 1: First dimension is preserved (common case)
    if (input_bdim == 0 and 
        input_shapes and input_shapes[0] and output_shape and 
        len(output_shape) > 0 and len(input_shapes[0]) > 0 and
        input_shapes[0][0] == output_shape[0]):
        output_bdim = 0
        if tracker.verbose:
            tracker.logger.debug(f"  ✓ First dimension preserved: batch dim {input_bdim} retained")
    
    # Case 2: Look for batch size in output (check if dimension with batch size exists in output)
    elif input_shapes and input_shapes[0] and output_shape and input_bdim < len(input_shapes[0]):
        batch_size = input_shapes[0][input_bdim]
        # Look for the batch size in the output dimensions
        for i, dim in enumerate(output_shape):
            if dim == batch_size:
                output_bdim = i
                if tracker.verbose:
                    tracker.logger.debug(f"  ✓ Batch size {batch_size} found at new position {output_bdim}")
                break
    
    # Log what the input shape would look like after batch removal
    if input_shapes and input_shapes[0] and input_bdim is not None and input_bdim < len(input_shapes[0]) and tracker.verbose:
        input_without_batch = input_shapes[0][:input_bdim] + input_shapes[0][input_bdim+1:]
        tracker.logger.debug(f"  🔍 After batch removal (size {input_shapes[0][input_bdim]}), input would be: {input_without_batch}")
        
    # Log what the target shape would need to be adjusted to
    if target_shape and "-1" in str(target_shape) and tracker.verbose:
        tracker.logger.debug(f"  🔍 Reshape target has dynamic dimension: {target_shape}")
        
        # Calculate how dynamic dimension would be affected
        if any(dim == -1 for dim in target_shape):
            dynamic_idx = target_shape.index(-1)
            tracker.logger.debug(f"  🔍 Adjusted dynamic dimension at index {dynamic_idx} would be: {max(0, dynamic_idx-1 if dynamic_idx > input_bdim else dynamic_idx)}")
    
    tracker._set_outputs(node, output_bdim)

@bn_tracker('Concat')
def track_concat(tracker, node: NodeProto, 
                 input_shapes: Optional[List[List[int]]] = None,
                 output_shape: Optional[List[int]] = None) -> None:
    """
    track Concat operation which combines tensors along an axis.
    
    Args:
        tracker: The BatchDimensionTracker instance
        node: ONNX node to process
        input_shapes: Optional shapes of input tensors
        output_shape: Optional shape of output tensor
    """
    if not node.input:
        tracker._set_outputs(node, None)
        return
    
    # Collect batch dimensions from all inputs
    input_bdims = []
    for i, input_name in enumerate(node.input):
        bdim = tracker.get_batch_dim(input_name)
        if bdim is not None:
            input_bdims.append((i, bdim))
    
    # Get the axis attribute
    axis = 0  # Default to axis 0
    for attr in node.attribute:
        if attr.name == 'axis':
            axis = attr.i
            break
    
    # Log the concat operation details
    if tracker.verbose:
        in_shapes_str = str([s for s in input_shapes]) if input_shapes else "unknown"
        axis_str = str(axis)
        out_shape_str = str(output_shape) if output_shape else "unknown"
        tracker.logger.debug(f"Concat {node.name}: {in_shapes_str} along axis {axis_str} -> {out_shape_str}")
    
    # If there are no batch dimensions, set output to None
    if not input_bdims:
        tracker._set_outputs(node, None)
        return
    
    # Check if all batch dimensions are consistent
    unique_bdims = set(bd for _, bd in input_bdims)
    
    # If there's only one unique batch dimension, use that
    if len(unique_bdims) == 1:
        input_bdim = next(iter(unique_bdims))
        
        # Check if we're concatenating along the batch dimension
        if axis == input_bdim:
            # Concatenating along batch dimension - the result is still a batch dimension
            # but batch size changes, so we don't need special handling
            tracker._set_outputs(node, input_bdim)
        else:
            # Calculate the adjusted axis if batch dimension is removed
            adjusted_axis = axis
            if axis > input_bdim:
                adjusted_axis = axis - 1
                
            if tracker.verbose and adjusted_axis != axis:
                tracker.logger.debug(f"  🔍 After batch removal, concatenation axis would become: {adjusted_axis} (batch_dim={input_bdim})")
            
            # Not concatenating along batch dimension - just pass batch dim through
            tracker._set_outputs(node, input_bdim)
    else:
        # Inconsistent batch dimensions, we can't determine output batch dimension
        tracker._set_outputs(node, None)

@bn_tracker('Squeeze')
def track_squeeze(tracker, node: NodeProto, 
                 input_shapes: Optional[List[List[int]]] = None,
                 output_shape: Optional[List[int]] = None) -> None:
    """
    Track Squeeze operation batch dimensions.
    
    Squeeze removes specified dimensions from the tensor.
    If batch dimension is not affected, it should be preserved,
    but its index may change if dimensions before it are removed.
    """
    if not node.input:
        tracker._set_outputs(node, None)
        return
    
    # Get batch dimension of input
    input_name = node.input[0]
    input_bdim = tracker.get_batch_dim(input_name)
    input_rank = len(input_shapes[0]) if input_shapes and input_shapes[0] else None
    
    if input_bdim is None:
        tracker._set_outputs(node, None)
        return
    
    # Get the axes attribute (which dimensions to squeeze)
    axes = []
    
    # Check if axes are provided as attribute (ONNX <13)
    for attr in node.attribute:
        if attr.name == 'axes':
            axes = list(attr.ints)
            
            # Normalize negative axes if we have shape information
            if input_rank:
                original_axes = axes.copy()
                axes = [a if a >= 0 else a + input_rank for a in axes]
                if tracker.verbose:
                    if original_axes != axes:
                        tracker.logger.debug(f"  📊 Got axes from attribute: {original_axes} (normalized to {axes})")
                    else:
                        tracker.logger.debug(f"  📊 Got axes from attribute: {axes}")
            else:
                tracker.logger.debug(f"  📊 Got axes from attribute: {axes} (cannot normalize negative indices without input shape)")
            
            # Always show what would happen after batch dimension removal
            if input_bdim is not None and input_rank:
                adjusted_axes = []
                for axis in axes:
                    if axis > input_bdim:
                        adjusted_axes.append(axis - 1)
                    elif axis < input_bdim:
                        adjusted_axes.append(axis)
                    # Skip axes equal to batch_dim
                
                if adjusted_axes != axes:
                    tracker.logger.debug(f"  🔍 After batch removal, axes would become: {adjusted_axes} (batch_dim={input_bdim})")
            break
    
    # Check if axes are provided as input (ONNX >=13)
    if len(node.input) > 1 and not axes:
        # Import here to avoid circular imports
        from ..utils.constant_utils import get_constant_value
        
        # Try to get axes from second input using constant_utils
        try:
            axes_tensor = get_constant_value(node.input[1], tracker.propagator)
            if axes_tensor is not None:
                axes = axes_tensor.flatten().tolist()
                
                # Normalize negative axes if we have shape information
                if input_rank:
                    original_axes = axes.copy()
                    axes = [a if a >= 0 else a + input_rank for a in axes]
                    if tracker.verbose:
                        if original_axes != axes:
                            tracker.logger.debug(f"  📊 Got axes from input: {original_axes} (normalized to {axes})")
                        else:
                            tracker.logger.debug(f"  📊 Got axes from input: {axes}")
                else:
                    tracker.logger.debug(f"  📊 Got axes from input: {axes} (cannot normalize negative indices without input shape)")
                
                # Always show what would happen after batch dimension removal
                if input_bdim is not None and input_rank:
                    adjusted_axes = []
                    for axis in axes:
                        if axis > input_bdim:
                            adjusted_axes.append(axis - 1)
                        elif axis < input_bdim:
                            adjusted_axes.append(axis)
                        # Skip axes equal to batch_dim
                    
                    if adjusted_axes != axes:
                        tracker.logger.debug(f"  🔍 After batch removal, axes would become: {adjusted_axes} (batch_dim={input_bdim})")
        except Exception as e:
            if tracker.verbose:
                tracker.logger.warning(f"  ⚠️ Couldn't get axes from input: {e}")
    
    # If no axes specified, Squeeze removes all dimensions of size 1
    if not axes and input_shapes and input_shapes[0]:
        input_shape = input_shapes[0]
        axes = [i for i, dim in enumerate(input_shape) if dim == 1]
        if tracker.verbose:
            tracker.logger.debug(f"  📏 Inferred axes from shape: {axes}")
    
    # Calculate new batch dimension after squeeze
    new_bdim = input_bdim
    
    # Adjust batch dimension if dimensions before it are removed
    if axes:
        # Count how many dimensions before batch_dim are squeezed
        dims_removed_before_batch = sum(1 for axis in axes if axis < input_bdim)
        
        # Check if batch dimension itself is being squeezed
        if input_bdim in axes:
            # If batch dimension is being squeezed, then we no longer have a batch dimension
            new_bdim = None
            
            if tracker.verbose:
                tracker.logger.debug(f"  ⚠️ Squeeze: batch dimension {input_bdim} is being removed")
        else:
            # Otherwise, adjust batch dimension by number of dimensions removed before it
            new_bdim = input_bdim - dims_removed_before_batch
            
            if tracker.verbose:
                tracker.logger.debug(f"  📏 Squeeze: batch dim adjusted from {input_bdim} → {new_bdim}")
                if dims_removed_before_batch > 0:
                    tracker.logger.debug(f"      (Removed {dims_removed_before_batch} dimensions before batch dim)")
    
    # Set output batch dimension
    tracker._set_outputs(node, new_bdim)

@bn_tracker('Unsqueeze')
def track_unsqueeze(tracker, node: NodeProto,
                   input_shapes: Optional[List[List[int]]] = None,
                   output_shape: Optional[List[int]] = None) -> None:
    """
    Track Unsqueeze operation batch dimensions.
    
    Unsqueeze adds new dimensions to the tensor.
    If batch dimension is in the input, we need to adjust its index
    if dimensions are added before it.
    """
    if not node.input:
        tracker._set_outputs(node, None)
        return
    
    # Get batch dimension and shape of input
    input_name = node.input[0]
    input_bdim = tracker.get_batch_dim(input_name)
    input_rank = len(input_shapes[0]) if input_shapes and input_shapes[0] else None
    
    if input_bdim is None:
        tracker._set_outputs(node, None)
        return
    
    # Get the axes attribute (which dimensions to unsqueeze)
    axes = []
    
    # Check if axes are provided as attribute (ONNX <13)
    for attr in node.attribute:
        if attr.name == 'axes':
            axes = list(attr.ints)
            
            # Normalize negative axes if we have shape information
            if input_rank is not None:
                original_axes = axes.copy()
                normalized_axes = [a if a >= 0 else a + input_rank + 1 for a in axes]
                if tracker.verbose:
                    if original_axes != normalized_axes:
                        tracker.logger.debug(f"  📊 Got axes from attribute: {original_axes} (normalized to {normalized_axes})")
                    else:
                        tracker.logger.debug(f"  📊 Got axes from attribute: {axes}")
                axes = normalized_axes
            else:
                if tracker.verbose:
                    tracker.logger.debug(f"  📊 Got axes from attribute: {axes} (cannot normalize negative indices without input shape)")
            
            # Show what would happen after batch removal
            if input_bdim is not None and input_rank:
                adjusted_axes = []
                for axis in axes:
                    if axis > input_bdim:
                        adjusted_axes.append(axis - 1)
                    elif axis < input_bdim:
                        adjusted_axes.append(axis)
                    # Skip axes equal to batch_dim
                
                if adjusted_axes != axes and tracker.verbose:
                    tracker.logger.debug(f"  🔍 After batch removal, axes would become: {adjusted_axes} (batch_dim={input_bdim})")
            break
    
    # Check if axes are provided as input (ONNX >=13)
    if len(node.input) > 1 and not axes:
        from ..utils.constant_utils import get_constant_value
        
        try:
            axes_tensor = get_constant_value(node.input[1], tracker.propagator)
            if axes_tensor is not None:
                axes = axes_tensor.flatten().tolist()
                
                # Normalize negative axes
                if input_rank is not None:
                    original_axes = axes.copy()
                    normalized_axes = [a if a >= 0 else a + input_rank + 1 for a in axes]
                    if tracker.verbose:
                        if original_axes != normalized_axes:
                            tracker.logger.debug(f"  📊 Got axes from input: {original_axes} (normalized to {normalized_axes})")
                        else:
                            tracker.logger.debug(f"  📊 Got axes from input: {axes}")
                    axes = normalized_axes
                else:
                    if tracker.verbose:
                        tracker.logger.debug(f"  📊 Got axes from input: {axes} (cannot normalize negative indices without input shape)")
                
                # Show what would happen after batch removal
                if input_bdim is not None and input_rank:
                    adjusted_axes = []
                    for axis in axes:
                        if axis > input_bdim:
                            adjusted_axes.append(axis - 1)
                        elif axis < input_bdim:
                            adjusted_axes.append(axis)
                    
                    if adjusted_axes != axes and tracker.verbose:
                        tracker.logger.debug(f"  🔍 After batch removal, axes would become: {adjusted_axes} (batch_dim={input_bdim})")
        except Exception as e:
            if tracker.verbose:
                tracker.logger.warning(f"  ⚠️ Couldn't get axes from input: {e}")
    
    # Determine new batch dimension position
    output_bdim = input_bdim
    
    # Count how many new dimensions are added before the batch dimension
    dims_added_before_batch = 0
    for axis in axes:
        if axis <= input_bdim:
            dims_added_before_batch += 1
    
    # Adjust batch dimension
    if dims_added_before_batch > 0:
        output_bdim = input_bdim + dims_added_before_batch
        if tracker.verbose:
            tracker.logger.debug(f"  📏 Unsqueeze: batch dim adjusted from {input_bdim} → {output_bdim}")
    
    # Set output batch dimension
    tracker._set_outputs(node, output_bdim)

@bn_tracker('Gather')
def track_gather(tracker, node: NodeProto,
                input_shapes: Optional[List[List[int]]] = None,
                output_shape: Optional[List[int]] = None) -> None:
    """Track Gather operation batch dimensions."""
    if not node.input or len(node.input) < 2:
        tracker._set_outputs(node, None)
        return
        
    data_name = node.input[0]
    data_bdim = tracker.get_batch_dim(data_name)
    
    if data_bdim is None:
        tracker._set_outputs(node, None)
        return
        
    # Get axis attribute (default is 0)
    axis = 0
    for attr in node.attribute:
        if attr.name == 'axis':
            axis = attr.i
            break
            
    # Get indices shape if available
    indices_shape = None
    if input_shapes and len(input_shapes) > 1:
        indices_shape = input_shapes[1]
        
    # Log the gather operation
    if tracker.verbose:
        if indices_shape is not None:
            tracker.logger.debug(f"Retrieved indices shape {indices_shape} for Gather {node.name}")
        data_shape = input_shapes[0] if input_shapes and input_shapes[0] else "unknown"
        output_shape = output_shape if output_shape else "unknown"
        indices_desc = indices_shape if indices_shape else "unknown"
        tracker.logger.debug(f"Gather {node.name}: data {data_shape}, indices {indices_desc}, axis {axis} -> {output_shape}")
        
        # Show how axis would change after batch dimension removal
        if data_bdim is not None:
            if axis == data_bdim:
                tracker.logger.debug(f"  🔍 After batch removal, gather operates on batch dimension (axis={axis})")
            elif axis > data_bdim:
                adjusted_axis = axis - 1
                tracker.logger.debug(f"  🔍 After batch removal, axis would become: {adjusted_axis} (batch_dim={data_bdim})")
        
    # Determine output batch dimension based on gather behavior
    output_bdim = None
    
    # Case 1: If we're gathering along batch dimension, no batch in output
    if axis == data_bdim:
        output_bdim = None
    # Case 2: If batch dimension is before the gather axis, it stays at same position  
    elif data_bdim < axis:
        output_bdim = data_bdim
    # Case 3: If batch dimension is after gather axis, depends on indices
    else:  # data_bdim > axis
        # For scalar indices, dimension count reduces by 1
        if not indices_shape or len(indices_shape) == 0:
            # Batch dim shifts left by 1
            output_bdim = data_bdim - 1
        else:
            # For non-scalar indices, batch dimension position depends on indices shape
            # This is a complex case that would need more detailed handling
            # For now, set conservatively to None
            output_bdim = None
            
    tracker._set_outputs(node, output_bdim)

@bn_tracker('Slice')
def track_slice(tracker, node: NodeProto,
               input_shapes: Optional[List[List[int]]] = None,
               output_shape: Optional[List[int]] = None) -> None:
    """
    Track batch dimension for Slice operations.
    
    Slice extracts parts of a tensor based on starts, ends, axes, and steps.
    The batch dimension is preserved if it's not affected by the slicing.
    """
    if not node.input:
        tracker._set_outputs(node, None)
        return
    
    # Get batch dimension of input
    input_name = node.input[0]
    input_bdim = tracker.get_batch_dim(input_name)
    input_shape = input_shapes[0] if input_shapes and len(input_shapes) > 0 else None
    input_rank = len(input_shape) if input_shape else None
    
    if input_bdim is None:
        tracker._set_outputs(node, None)
        return
    
    # By default, Slice doesn't affect batch dimension
    output_bdim = input_bdim
    
    # Check if we have specific slice parameters
    starts, ends, axes, steps = [], [], [], []
    
    # Try to extract from attributes (ONNX opset < 10)
    for attr in node.attribute:
        if attr.name == 'starts':
            starts = list(attr.ints)
        elif attr.name == 'ends':
            ends = list(attr.ints)
        elif attr.name == 'axes':
            axes = list(attr.ints)
    
    # Try to extract from inputs (ONNX opset >= 10)
    from ..utils.constant_utils import get_constant_value
    
    if len(node.input) > 1:
        try:
            starts_tensor = get_constant_value(node.input[1], tracker.propagator)
            if starts_tensor is not None:
                starts = starts_tensor.tolist() if hasattr(starts_tensor, 'tolist') else [starts_tensor]
        except Exception:
            pass
    
    if len(node.input) > 2:
        try:
            ends_tensor = get_constant_value(node.input[2], tracker.propagator)
            if ends_tensor is not None:
                ends = ends_tensor.tolist() if hasattr(ends_tensor, 'tolist') else [ends_tensor]
        except Exception:
            pass
    
    if len(node.input) > 3:
        try:
            axes_tensor = get_constant_value(node.input[3], tracker.propagator)
            if axes_tensor is not None:
                axes = axes_tensor.tolist() if hasattr(axes_tensor, 'tolist') else [axes_tensor]
        except Exception:
            pass
    
    if len(node.input) > 4:
        try:
            steps_tensor = get_constant_value(node.input[4], tracker.propagator)
            if steps_tensor is not None:
                steps = steps_tensor.tolist() if hasattr(steps_tensor, 'tolist') else [steps_tensor]
        except Exception:
            pass
    
    # If no axes provided, default is to slice on all axes
    if not axes and input_rank:
        axes = list(range(input_rank))
        if tracker.verbose:
            tracker.logger.debug(f"  📊 Slice: using axes {axes}")
    
    # Default steps to 1 if not provided
    if not steps and axes:
        steps = [1] * len(axes)
    
    # Check if batch dimension is affected by slicing
    if input_bdim is not None and input_rank and axes:
        # Check if batch dimension is being sliced
        if input_bdim in axes:
            idx = axes.index(input_bdim)
            start = starts[idx] if idx < len(starts) else 0
            end = ends[idx] if idx < len(ends) else input_shape[input_bdim] if input_shape else 0
            step = steps[idx] if idx < len(steps) else 1
            
            # If the slice takes exactly one item from the batch dimension
            slice_size = (end - start)
            if slice_size == 1 and step == 1:
                if tracker.verbose:
                    tracker.logger.debug(f"  ⚠️ Slice: batch dimension {input_bdim} is being sliced to a single element")
                    tracker.logger.debug(f"  ⚠️ Consider preserving batch dimension even with size 1")
            elif slice_size > 1 or (slice_size == 1 and step != 1):
                # We're taking multiple items or stepping through batch dimension
                if tracker.verbose:
                    tracker.logger.debug(f"  ✓ Slice: batch dimension {input_bdim} is preserved (size {slice_size}, step {step})")
        else:
            if tracker.verbose:
                tracker.logger.debug(f"  ✓ Slice: batch dimension {input_bdim} is not affected by slicing")
        
        # Show how indices would be adjusted after batch dimension removal
        if tracker.verbose:
            adjusted_starts = []
            adjusted_ends = []
            adjusted_axes = []
            adjusted_steps = []
            
            # Create mapping from original axis to adjusted axis
            axis_mapping = {}
            for i, axis in enumerate(range(input_rank)):
                if axis == input_bdim:
                    # Skip the batch dimension
                    continue
                elif axis > input_bdim:
                    # Shift down by 1 after batch dim
                    axis_mapping[axis] = axis - 1
                else:
                    # Keep the same before batch dim
                    axis_mapping[axis] = axis
            
            # Apply the mapping to the slice parameters
            for i, axis in enumerate(axes):
                # Get the corresponding start, end, step if available
                curr_start = starts[i] if i < len(starts) else 0
                curr_end = ends[i] if i < len(ends) else input_shape[axis] if input_shape and axis < len(input_shape) else 0
                curr_step = steps[i] if i < len(steps) else 1
                
                if axis == input_bdim:
                    # This axis would be removed in the final model
                    # But we still track it for debugging purposes
                    adjusted_axes.append("batch_dim")
                    adjusted_starts.append(curr_start)
                    adjusted_ends.append(curr_end)
                    adjusted_steps.append(curr_step)
                elif axis in axis_mapping:
                    # Apply the axis mapping
                    adjusted_axes.append(axis_mapping[axis])
                    adjusted_starts.append(curr_start)
                    adjusted_ends.append(curr_end)
                    adjusted_steps.append(curr_step)
            
            has_changes = (adjusted_axes != axes or 
                          adjusted_starts != starts or 
                          adjusted_ends != ends or 
                          adjusted_steps != steps)
            
            if has_changes:
                tracker.logger.debug(f"  🔍 After batch removal:")
                tracker.logger.debug(f"     - axes: {adjusted_axes} (batch_dim={input_bdim})")
                # Only show other parameters if they've been defined
                if starts != adjusted_starts:
                    tracker.logger.debug(f"     - starts: {adjusted_starts}")
                if ends != adjusted_ends:
                    tracker.logger.debug(f"     - ends: {adjusted_ends}") 
                if steps != adjusted_steps:
                    tracker.logger.debug(f"     - steps: {adjusted_steps}")
    
    # Set output batch dimension
    tracker._set_outputs(node, output_bdim)

@bn_tracker('ReduceSum')
@bn_tracker('ReduceMean')
@bn_tracker('ReduceMax')
@bn_tracker('ReduceMin')
@bn_tracker('ReduceProd')
@bn_tracker('ReduceL1')
@bn_tracker('ReduceL2')
@bn_tracker('ReduceLogSum')
@bn_tracker('ReduceLogSumExp')
@bn_tracker('ReduceSumSquare')
def track_reduce_op(tracker, node: NodeProto,
                    input_shapes: Optional[List[List[int]]] = None,
                    output_shape: Optional[List[int]] = None) -> None:
    """
    Track reduction operations (ReduceSum, ReduceMean, etc.).
    
    Args:
        tracker: The BatchDimensionTracker instance
        node: ONNX node to process
        input_shapes: Optional shapes of input tensors
        output_shape: Optional shape of output tensor
    """
    if not node.input:
        tracker._set_outputs(node, None)
        return
        
    input_name = node.input[0]
    input_bdim = tracker.get_batch_dim(input_name)
    
    if input_bdim is None:
        tracker._set_outputs(node, None)
        return
    
    # Get reduction axes and keepdims
    axes = None
    keepdims = 1  # Default is true
    input_rank = len(input_shapes[0]) if input_shapes and input_shapes[0] else None
    
    # Track opset differences for axes
    if len(node.input) > 1:
        # In newer opsets, axes can be an input tensor
        from ..utils.constant_utils import get_constant_value
        
        try:
            axes_tensor = get_constant_value(node.input[1], tracker.propagator)
            if axes_tensor is not None:
                axes = axes_tensor.flatten().tolist()
                
                # Normalize negative axes if we have shape information
                if input_rank:
                    original_axes = axes.copy()
                    axes = [a if a >= 0 else a + input_rank for a in axes]
                    if tracker.verbose:
                        if original_axes != axes:
                            tracker.logger.debug(f"  📊 Got axes from input: {original_axes} (normalized to {axes})")
                        else:
                            tracker.logger.debug(f"  📊 Got axes from input: {axes}")
                else:
                    tracker.logger.debug(f"  📊 Got axes from input: {axes} (cannot normalize negative indices without input shape)")
                
                # Always show what would happen after batch dimension removal
                if input_bdim is not None and input_rank:
                    adjusted_axes = []
                    for axis in axes:
                        if axis > input_bdim:
                            adjusted_axes.append(axis - 1)
                        elif axis < input_bdim:
                            adjusted_axes.append(axis)
                        # Skip axes equal to batch_dim
                    
                    if adjusted_axes != axes:
                        tracker.logger.debug(f"  🔍 After batch removal, axes would become: {adjusted_axes} (batch_dim={input_bdim})")
        except Exception as e:
            if tracker.verbose:
                tracker.logger.warning(f"  ⚠️ Couldn't get axes from input tensor: {e}")
            # We couldn't determine statically
            tracker._set_outputs(node, None)
            return
    
    # Get from attributes if not from input
    if axes is None:
        for attr in node.attribute:
            if attr.name == 'axes':
                axes = list(attr.ints)
                
                # Normalize negative axes if we have shape information
                if input_rank:
                    original_axes = axes.copy()
                    axes = [a if a >= 0 else a + input_rank for a in axes]
                    if tracker.verbose:
                        if original_axes != axes:
                            tracker.logger.debug(f"  📊 Got axes from attribute: {original_axes} (normalized to {axes})")
                        else:
                            tracker.logger.debug(f"  📊 Got axes from attribute: {axes}")
                else:
                    tracker.logger.debug(f"  📊 Got axes from attribute: {axes} (cannot normalize negative indices without input shape)")
                
                # Always show what would happen after batch dimension removal
                if input_bdim is not None and input_rank:
                    adjusted_axes = []
                    for axis in axes:
                        if axis > input_bdim:
                            adjusted_axes.append(axis - 1)
                        elif axis < input_bdim:
                            adjusted_axes.append(axis)
                        # Skip axes equal to batch_dim
                    
                    if adjusted_axes != axes:
                        tracker.logger.debug(f"  🔍 After batch removal, axes would become: {adjusted_axes} (batch_dim={input_bdim})")
            elif attr.name == 'keepdims':
                keepdims = attr.i
    
    # If no specific axes provided, can't determine
    if axes is None:
        tracker._set_outputs(node, None)
        return
    
    # Normalize negative axes if we have shape information
    if input_shapes and input_shapes[0]:
        input_rank = len(input_shapes[0])
        axes = [a if a >= 0 else a + input_rank for a in axes]
    
    # Determine output batch dimension
    if input_bdim in axes:
        # If reducing along batch dimension
        output_bdim = input_bdim if keepdims else None
    else:
        # If not reducing along batch dimension
        if keepdims:
            output_bdim = input_bdim
        else:
            # Adjust batch dimension position based on removed axes
            output_bdim = input_bdim - sum(1 for a in axes if a < input_bdim)
    
    tracker._set_outputs(node, output_bdim)

@bn_tracker('MatMul')
def track_matmul(tracker, node: NodeProto,
                input_shapes: Optional[List[List[int]]] = None,
                output_shape: Optional[List[int]] = None) -> None:
    """
    Track batch dimension for MatMul operations.
    
    MatMul performs matrix multiplication with the following rules:
    - If both inputs are 2D, it's a straightforward matrix multiplication
    - If inputs have more dimensions, it follows broadcasting rules
    - Batch dimensions are preserved in the output
    
    Args:
        tracker: The BatchDimensionTracker instance
        node: ONNX node to process
        input_shapes: Optional shapes of input tensors
        output_shape: Optional shape of output tensor
    """
    if len(node.input) < 2:
        tracker._set_outputs(node, None)
        return
    
    # Get input batch dimensions and shapes
    input_A_name = node.input[0]
    input_B_name = node.input[1]
    
    batch_dim_A = tracker.get_batch_dim(input_A_name)
    batch_dim_B = tracker.get_batch_dim(input_B_name)
    
    # Extract shapes if available for better analysis
    shape_A = input_shapes[0] if input_shapes and len(input_shapes) > 0 else None
    shape_B = input_shapes[1] if input_shapes and len(input_shapes) > 1 else None
    
    if tracker.verbose:
        if shape_A and batch_dim_A is not None:
            tracker.logger.debug(f"  • Input A: {input_A_name} shape={shape_A} (batch@{batch_dim_A})")
        elif shape_A:
            tracker.logger.debug(f"  • Input A: {input_A_name} shape={shape_A} (no batch)")
        
        if shape_B and batch_dim_B is not None:
            tracker.logger.debug(f"  • Input B: {input_B_name} shape={shape_B} (batch@{batch_dim_B})")
        elif shape_B:
            tracker.logger.debug(f"  • Input B: {input_B_name} shape={shape_B} (no batch)")
    
    # Output batch dimension determination
    output_batch_dim = None
    
    # Special handling for the common case where A has 3 dimensions and B has 2 dimensions
    # This is the case in the log: A [128, 1, 7] and B [7, 128]
    if shape_A and shape_B and len(shape_A) == 3 and len(shape_B) == 2:
        # For shapes like A[N, batch, K] × B[K, M] → output[N, batch, M]
        # batch dimension at position 1 should be preserved
        if batch_dim_A is not None:
            output_batch_dim = batch_dim_A
            if tracker.verbose:
                tracker.logger.debug(f"  ✓ MatMul: broadcasting case - preserving batch dimension {batch_dim_A} from input A")
    
    # If we still don't have an output batch dimension, use the general rules
    if output_batch_dim is None and shape_A and shape_B and output_shape:
        # General rules for batch dimension preservation in MatMul
        if batch_dim_A is not None:
            # Usually batch dimensions are preserved from the first input
            output_batch_dim = batch_dim_A
            if tracker.verbose:
                tracker.logger.debug(f"  ✓ MatMul: preserving batch dimension {batch_dim_A} from input A")
        elif batch_dim_B is not None:
            # If only second input has batch, mapping is more complex
            # For this case, detailed analysis using output shape is needed
            if len(shape_B) >= 3 and len(output_shape) >= 3:
                # In this case, the batch dimension might be preserved
                output_batch_dim = batch_dim_B
                if tracker.verbose:
                    tracker.logger.debug(f"  ✓ MatMul: preserving batch dimension {batch_dim_B} from input B")
    
    # As a fallback, if neither of the above rules applied, use batch from first input if available
    if output_batch_dim is None:
        output_batch_dim = batch_dim_A
        if batch_dim_A is not None and tracker.verbose:
            tracker.logger.debug(f"  ✓ MatMul: fallback to batch dimension {batch_dim_A} from input A")
    
    # Set batch dimensions for all outputs
    tracker._set_outputs(node, output_batch_dim)
    
    # Log the final decision
    if tracker.verbose:
        if output_batch_dim is not None:
            tracker.logger.debug(f"  ✓ MatMul: set output batch dimension to {output_batch_dim}")
        else:
            tracker.logger.debug(f"  ⚠ MatMul: could not determine output batch dimension")

@bn_tracker('Conv')
def track_conv(tracker, node: NodeProto, 
               input_shapes: Optional[List[List[int]]] = None,
               output_shape: Optional[List[int]] = None) -> None:
    """
    track Conv operation which performs convolution.
    
    Args:
        tracker: The BatchDimensionTracker instance
        node: ONNX node to process
        input_shapes: Optional shapes of input tensors
        output_shape: Optional shape of output tensor
    """
    if not node.input:
        tracker._set_outputs(node, None)
        return
        
    input_bdim = tracker.get_batch_dim(node.input[0])
    
    # For convolution operations, batch dimension is typically the first dimension (N in NCHW)
    # and is preserved through the operation
    tracker._set_outputs(node, input_bdim)

@bn_tracker('Softmax')
def track_softmax(tracker, node: NodeProto, 
                  input_shapes: Optional[List[List[int]]] = None,
                  output_shape: Optional[List[int]] = None) -> None:
    """
    track Softmax operation which normalizes along an axis.
    
    Args:
        tracker: The BatchDimensionTracker instance
        node: ONNX node to process
        input_shapes: Optional shapes of input tensors
        output_shape: Optional shape of output tensor
    """
    if not node.input:
        tracker._set_outputs(node, None)
        return
        
    input_name = node.input[0]
    input_bdim = tracker.get_batch_dim(input_name)
    
    if input_bdim is None:
        tracker._set_outputs(node, None)
        return
    
    # Get softmax axis
    axis = 1  # Default for softmax in ONNX
    for attr in node.attribute:
        if attr.name == 'axis':
            axis = attr.i
            break
    
    # If softmax along batch dimension, result doesn't have a clear batch dimension
    output_bdim = None if axis == input_bdim else input_bdim
    
    tracker._set_outputs(node, output_bdim)

@bn_tracker('Split')
def track_split(tracker, node: NodeProto, 
                input_shapes: Optional[List[List[int]]] = None,
                output_shape: Optional[List[int]] = None) -> None:
    """
    track Split operation which splits a tensor along an axis.
    
    Args:
        tracker: The BatchDimensionTracker instance
        node: ONNX node to process
        input_shapes: Optional shapes of input tensors
        output_shape: Optional shape of output tensor
    """
    if not node.input:
        tracker._set_outputs(node, None)
        return
        
    input_name = node.input[0]
    input_bdim = tracker.get_batch_dim(input_name)
    input_shape = input_shapes[0] if input_shapes and len(input_shapes) > 0 else None
    
    if input_bdim is None:
        tracker._set_outputs(node, None)
        return
    
    # Get split axis
    axis = 0
    for attr in node.attribute:
        if attr.name == 'axis':
            axis = attr.i
            break
            
    # Try to extract from inputs (for newer ONNX versions)
    if len(node.input) > 1:
        from ..utils.constant_utils import get_constant_value
        try:
            axis_tensor = get_constant_value(node.input[1], tracker.propagator)
            if axis_tensor is not None:
                axis = axis_tensor.item() if hasattr(axis_tensor, 'item') else axis_tensor
        except Exception:
            pass
    
    # Get number of outputs (split sizes if specified)
    split = None
    for attr in node.attribute:
        if attr.name == 'split':
            split = list(attr.ints)
            break
            
    # Try to extract split sizes from inputs (for newer ONNX versions)
    if len(node.input) > 2:
        try:
            split_tensor = get_constant_value(node.input[2], tracker.propagator)
            if split_tensor is not None:
                split = split_tensor.tolist() if hasattr(split_tensor, 'tolist') else [split_tensor]
        except Exception:
            pass
            
    # Log the split operation details
    if tracker.verbose:
        in_shape_str = str(input_shape) if input_shape else "unknown"
        axis_str = str(axis)
        split_str = str(split) if split else "equal parts"
        output_count = len(node.output)
        tracker.logger.debug(f"Split {node.name}: {in_shape_str} along axis {axis_str} with sizes {split_str} -> {output_count} outputs")
    
    # If splitting along batch dimension, result doesn't have a clear batch dimension
    output_bdim = None if axis == input_bdim else input_bdim
    
    # Calculate how the axis would be adjusted if batch dimension is removed
    if input_bdim is not None and axis != input_bdim:
        adjusted_axis = axis
        if axis > input_bdim:
            adjusted_axis = axis - 1
            
        if tracker.verbose and adjusted_axis != axis:
            tracker.logger.debug(f"  🔍 After batch removal, split axis would become: {adjusted_axis} (batch_dim={input_bdim})")
    
    tracker._set_outputs(node, output_bdim)

@bn_tracker('Gemm')
def track_gemm(tracker, node: NodeProto, 
               input_shapes: Optional[List[List[int]]] = None,
               output_shape: Optional[List[int]] = None) -> None:
    """
    track Gemm operation (general matrix multiplication).
    
    Args:
        tracker: The BatchDimensionTracker instance
        node: ONNX node to process
        input_shapes: Optional shapes of input tensors
        output_shape: Optional shape of output tensor
    """
    if not node.input:
        tracker._set_outputs(node, None)
        return
        
    # For Gemm, typically the batch dimension is in the first input
    # But only if it's in the first position
    input_bdim = tracker.get_batch_dim(node.input[0])
    
    # Gemm in ONNX doesn't support batching in the standard way
    # Only forward batch dimension if it's at position 0
    tracker._set_outputs(node, 0 if input_bdim == 0 else None)

@bn_tracker('Expand')
def track_expand(tracker, node: NodeProto, 
                 input_shapes: Optional[List[List[int]]] = None,
                 output_shape: Optional[List[int]] = None) -> None:
    """
    track Expand operation which broadcasts a tensor.
    
    Args:
        tracker: The BatchDimensionTracker instance
        node: ONNX node to process
        input_shapes: Optional shapes of input tensors
        output_shape: Optional shape of output tensor
    """
    if not node.input:
        tracker._set_outputs(node, None)
        return
        
    input_name = node.input[0]
    input_bdim = tracker.get_batch_dim(input_name)
    
    # Expand typically preserves dimensions so batch dimension stays the same
    tracker._set_outputs(node, input_bdim)

@bn_tracker('Shape')
def track_shape(tracker, node: NodeProto, 
                input_shapes: Optional[List[List[int]]] = None,
                output_shape: Optional[List[int]] = None) -> None:
    """
    track Shape operation which returns tensor dimensions.
    
    Args:
        tracker: The BatchDimensionTracker instance
        node: ONNX node to process
        input_shapes: Optional shapes of input tensors
        output_shape: Optional shape of output tensor
    """
    # Shape output is a 1D tensor of the input dimensions
    # It doesn't have a batch dimension
    tracker._set_outputs(node, None)

@bn_tracker('Flatten')
def track_flatten(tracker, node: NodeProto, 
                  input_shapes: Optional[List[List[int]]] = None,
                  output_shape: Optional[List[int]] = None) -> None:
    """
    track Flatten operation which collapses dimensions.
    
    Args:
        tracker: The BatchDimensionTracker instance
        node: ONNX node to process
        input_shapes: Optional shapes of input tensors
        output_shape: Optional shape of output tensor
    """
    if not node.input:
        tracker._set_outputs(node, None)
        return
        
    input_name = node.input[0]
    input_bdim = tracker.get_batch_dim(input_name)
    
    if input_bdim is None:
        tracker._set_outputs(node, None)
        return
    
    # Get axis attribute
    axis = 1  # Default value for Flatten
    for attr in node.attribute:
        if attr.name == 'axis':
            axis = attr.i
            break
    
    # Determine output batch dimension
    # If input batch dim is before flattening axis, it becomes first dim (0)
    # Otherwise, it's folded into the second dimension
    output_bdim = 0 if input_bdim < axis else None
    
    tracker._set_outputs(node, output_bdim)

@bn_tracker('Identity')
def track_identity(tracker, node: NodeProto, 
                   input_shapes: Optional[List[List[int]]] = None,
                   output_shape: Optional[List[int]] = None) -> None:
    """
    track Identity operation which passes tensor through unchanged.
    
    Args:
        tracker: The BatchDimensionTracker instance
        node: ONNX node to process
        input_shapes: Optional shapes of input tensors
        output_shape: Optional shape of output tensor
    """
    if not node.input:
        tracker._set_outputs(node, None)
        return
        
    input_name = node.input[0]
    input_bdim = tracker.get_batch_dim(input_name)
    
    # Identity preserves batch dimension
    tracker._set_outputs(node, input_bdim)

@bn_tracker('Cast')
def track_cast(tracker, node: NodeProto,
              input_shapes: Optional[List[List[int]]] = None,
              output_shape: Optional[List[int]] = None) -> None:
    """
    Track Cast operation batch dimensions.
    
    Cast operations preserve the shape and batch dimension of the input.
    """
    if not node.input:
        tracker._set_outputs(node, None)
        return
    
    # Get batch dimension of input
    input_name = node.input[0]
    input_bdim = tracker.get_batch_dim(input_name)
    
    # Cast preserves batch dimension
    if tracker.verbose:
        tracker.logger.debug(f"  🔄 Cast: batch dim preserved at {input_bdim}")
    
    # Set output batch dimension
    tracker._set_outputs(node, input_bdim)

@bn_tracker('Constant')
def track_constant(tracker, node: NodeProto, 
                   input_shapes: Optional[List[List[int]]] = None,
                   output_shape: Optional[List[int]] = None) -> None:
    """
    track Constant operation which creates a constant tensor.
    
    Args:
        tracker: The BatchDimensionTracker instance
        node: ONNX node to process
        input_shapes: Optional shapes of input tensors
        output_shape: Optional shape of output tensor
    """
    # Constants don't have batch dimensions
    tracker._set_outputs(node, None)

@bn_tracker('Pad')
def track_pad(tracker, node: NodeProto, 
              input_shapes: Optional[List[List[int]]] = None,
              output_shape: Optional[List[int]] = None) -> None:
    """
    track Pad operation which adds padding.
    
    Args:
        tracker: The BatchDimensionTracker instance
        node: ONNX node to process
        input_shapes: Optional shapes of input tensors
        output_shape: Optional shape of output tensor
    """
    if not node.input:
        tracker._set_outputs(node, None)
        return
        
    input_name = node.input[0]
    input_bdim = tracker.get_batch_dim(input_name)
    
    # Pad preserves dimensions
    tracker._set_outputs(node, input_bdim)

@bn_tracker('Tile')
def track_tile(tracker, node: NodeProto, 
               input_shapes: Optional[List[List[int]]] = None,
               output_shape: Optional[List[int]] = None) -> None:
    """
    track Tile operation which repeats a tensor.
    
    Args:
        tracker: The BatchDimensionTracker instance
        node: ONNX node to process
        input_shapes: Optional shapes of input tensors
        output_shape: Optional shape of output tensor
    """
    if not node.input:
        tracker._set_outputs(node, None)
        return
        
    input_name = node.input[0]
    input_bdim = tracker.get_batch_dim(input_name)
    
    # Tile preserves dimensions
    tracker._set_outputs(node, input_bdim)

@bn_tracker('Resize')
def track_resize(tracker, node: NodeProto, 
                 input_shapes: Optional[List[List[int]]] = None,
                 output_shape: Optional[List[int]] = None) -> None:
    """
    track Resize operation which scales tensor dimensions.
    
    Args:
        tracker: The BatchDimensionTracker instance
        node: ONNX node to process
        input_shapes: Optional shapes of input tensors
        output_shape: Optional shape of output tensor
    """
    if not node.input:
        tracker._set_outputs(node, None)
        return
        
    input_name = node.input[0]
    input_bdim = tracker.get_batch_dim(input_name)
    
    # Resize preserves dimension positions (though sizes change)
    tracker._set_outputs(node, input_bdim)

@bn_tracker('If')
def track_if(tracker, node: NodeProto, 
             input_shapes: Optional[List[List[int]]] = None,
             output_shape: Optional[List[int]] = None) -> None:
    """
    track If operation which represents a conditional branch.
    
    Args:
        tracker: The BatchDimensionTracker instance
        node: ONNX node to process
        input_shapes: Optional shapes of input tensors
        output_shape: Optional shape of output tensor
    """
    # If operations are complex as they involve subgraphs
    # Without analyzing the subgraphs, we can't reliably determine batch dims
    # Safest approach is to set outputs to None
    tracker._set_outputs(node, None)

@bn_tracker('Einsum')
def track_einsum(tracker, node: NodeProto, 
                 input_shapes: Optional[List[List[int]]] = None,
                 output_shape: Optional[List[int]] = None) -> None:
    """
    track Einsum operation which performs Einstein summation.
    
    Args:
        tracker: The BatchDimensionTracker instance
        node: ONNX node to process
        input_shapes: Optional shapes of input tensors
        output_shape: Optional shape of output tensor
    """
    if not node.input:
        tracker._set_outputs(node, None)
        return
    
    # Get equation from attribute
    equation = None
    for attr in node.attribute:
        if attr.name == 'equation':
            equation = attr.s.decode('utf-8') if isinstance(attr.s, bytes) else attr.s
            break
    
    if not equation:
        tracker._set_outputs(node, None)
        return
    
    # Get batch dimensions from inputs
    batch_dims = []
    for input_name in node.input:
        if input_name not in tracker.constants:
            bdim = tracker.get_batch_dim(input_name)
            if bdim is not None:
                batch_dims.append(bdim)
    
    # Basic heuristic for common einsum patterns
    # This is simplified - full einsum analysis is complex
    
    # Common case: batch matmul like "bij,bjk->bik"
    # If equation has format with leading dim preserved, keep batch dim at 0
    if equation and '->' in equation and equation[0] == equation.split('->')[1][0]:
        tracker._set_outputs(node, 0)
        return
        
    # For complex einsum patterns, we'd need more detailed analysis
    # Default to None when uncertain
    tracker._set_outputs(node, None)

# Add specific trackers for common elementwise operations
@bn_tracker('Add')
@bn_tracker('Sub')
@bn_tracker('Mul')
@bn_tracker('Div')
@bn_tracker('Pow')
@bn_tracker('Sqrt')
@bn_tracker('Log')
@bn_tracker('Exp')
@bn_tracker('Neg')
@bn_tracker('Abs')
@bn_tracker('Reciprocal')
@bn_tracker('Floor')
@bn_tracker('Ceil')
@bn_tracker('Round')
@bn_tracker('Min')
@bn_tracker('Max')
def track_elementwise_op(tracker, node: NodeProto,
                          input_shapes: Optional[List[List[int]]] = None,
                          output_shape: Optional[List[int]] = None) -> None:
    """
    Track batch dimension for elementwise operations.
    Elementwise operations generally preserve batch dimensions.
    
    Args:
        tracker: The BatchDimensionTracker instance
        node: ONNX node to process
        input_shapes: Optional shapes of input tensors
        output_shape: Optional shape of output tensor
    """
    if not node.input:
        tracker._set_outputs(node, None)
        return
    
    # This will track batch dimensions for all input tensors
    batch_dims = []
    for input_name in node.input:
        batch_dim = tracker.get_batch_dim(input_name)
        if batch_dim is not None:
            batch_dims.append((input_name, batch_dim))
    
    if not batch_dims:
        # No batch dimensions in inputs means no batch dimensions in outputs
        tracker._set_outputs(node, None)
        return
    
    # Validate consistency of batch dimensions
    if len(batch_dims) > 1:
        # If multiple inputs have batch dimensions, they should match
        main_batch_dim = batch_dims[0][1]
        inconsistent = [f"{name} (batch@{dim})" for name, dim in batch_dims[1:] 
                        if dim != main_batch_dim]
        
        if inconsistent:
            # Warning for inconsistent batch dims
            inconsistent_str = ", ".join(inconsistent)
            first_input = f"{batch_dims[0][0]} (batch@{main_batch_dim})"
            if tracker.verbose:
                tracker.logger.warning(f"  ⚠️ Inconsistent batch dimensions in {node.op_type} operation!")
                tracker.logger.warning(f"     First input: {first_input}")
                tracker.logger.warning(f"     Other inputs: {inconsistent_str}")
            
            # Use batch dimension from the first input that has one
            output_batch_dim = main_batch_dim
        else:
            # All batch dimensions are consistent
            output_batch_dim = main_batch_dim
            if tracker.verbose:
                tracker.logger.debug(f"  ✓ All inputs have consistent batch dimension {output_batch_dim}")
    else:
        # Only one input has a batch dimension
        output_batch_dim = batch_dims[0][1]
        
    # Check if broadcasting might affect batch dimension
    if input_shapes and len(input_shapes) > 1 and all(shape for shape in input_shapes):
        # Get shapes for inputs with batch dimensions
        batch_input_shapes = []
        non_batch_input_shapes = []
        
        for i, input_name in enumerate(node.input):
            if i < len(input_shapes) and input_shapes[i]:
                if tracker.get_batch_dim(input_name) is not None:
                    batch_input_shapes.append((input_name, input_shapes[i]))
                else:
                    non_batch_input_shapes.append((input_name, input_shapes[i]))
        
        # Check for complex broadcasting scenarios
        if batch_input_shapes and non_batch_input_shapes:
            if tracker.verbose:
                for name, shape in batch_input_shapes:
                    batch_dim = tracker.get_batch_dim(name)
                    tracker.logger.debug(f"  • Input with batch: {name} shape={shape} (batch@{batch_dim})")
                for name, shape in non_batch_input_shapes:
                    tracker.logger.debug(f"  • Input without batch: {name} shape={shape}")
    
    # Set the batch dimension for all outputs
    tracker._set_outputs(node, output_batch_dim)
    
    # if tracker.verbose:
    #     tracker.logger.debug(f"  ✓ Using explicit tracker for {node.op_type} operation")

@bn_tracker('Where')
def track_where(tracker, node: NodeProto,
               input_shapes: Optional[List[List[int]]] = None,
               output_shape: Optional[List[int]] = None) -> None:
    """
    Track batch dimension for Where operation.
    
    Where operation is like: condition ? x : y
    It selects elements from x or y based on condition.
    The output should maintain batch dimensions from inputs.
    """
    if len(node.input) < 3:
        tracker._set_outputs(node, None)
        return
    
    # Get batch dimensions from all inputs
    condition_name = node.input[0]
    x_name = node.input[1]
    y_name = node.input[2]
    
    condition_batch = tracker.get_batch_dim(condition_name)
    x_batch = tracker.get_batch_dim(x_name)
    y_batch = tracker.get_batch_dim(y_name)
    
    # Log input batch dimensions if verbose
    if tracker.verbose:
        tracker.logger.debug(f"  • Condition: {condition_name} " + 
                        (f"batch@{condition_batch}" if condition_batch is not None else "no batch"))
        tracker.logger.debug(f"  • X: {x_name} " + 
                        (f"batch@{x_batch}" if x_batch is not None else "no batch"))
        tracker.logger.debug(f"  • Y: {y_name} " + 
                        (f"batch@{y_batch}" if y_batch is not None else "no batch"))
    
    # Prefer batch from first batched input (prioritize order: condition, x, y)
    output_batch = None
    if condition_batch is not None:
        output_batch = condition_batch
        if tracker.verbose:
            tracker.logger.debug(f"  ✓ Where: using batch dimension {output_batch} from condition")
    elif x_batch is not None:
        output_batch = x_batch
        if tracker.verbose:
            tracker.logger.debug(f"  ✓ Where: using batch dimension {output_batch} from x")
    elif y_batch is not None:
        output_batch = y_batch
        if tracker.verbose:
            tracker.logger.debug(f"  ✓ Where: using batch dimension {output_batch} from y")
    
    tracker._set_outputs(node, output_batch)

# Add support for comparison operations
@bn_tracker('LessOrEqual')
@bn_tracker('Greater')
@bn_tracker('Equal')
@bn_tracker('Less')
@bn_tracker('GreaterOrEqual')
@bn_tracker('Sign')
def track_comparison_op(tracker, node: NodeProto,
                       input_shapes: Optional[List[List[int]]] = None,
                       output_shape: Optional[List[int]] = None) -> None:
    """
    Track batch dimension for comparison operations.
    
    These operations behave like elementwise operations regarding batch dimensions.
    """
    if len(node.input) < 1:
        tracker._set_outputs(node, None)
        return
    
    # Get batch dimensions from inputs
    batch_dims = []
    for input_name in node.input:
        batch_dim = tracker.get_batch_dim(input_name)
        if batch_dim is not None:
            batch_dims.append((input_name, batch_dim))
    
    if not batch_dims:
        # No batch dimensions in inputs
        tracker._set_outputs(node, None)
        return
    
    # First input with a batch dimension determines output batch dimension
    output_batch_dim = batch_dims[0][1]
    
    # Check consistency of batch dimensions
    if len(batch_dims) > 1:
        inconsistent_dims = [f"{name} (batch@{dim})" for name, dim in batch_dims[1:] 
                           if dim != output_batch_dim]
        
        if inconsistent_dims and tracker.verbose:
            first_input = f"{batch_dims[0][0]} (batch@{output_batch_dim})"
            tracker.logger.warning(f"  ⚠️ Inconsistent batch dimensions in {node.op_type}!")
            tracker.logger.warning(f"     First input: {first_input}")
            tracker.logger.warning(f"     Other inputs: {', '.join(inconsistent_dims)}")
    
    # Set output batch dimension
    tracker._set_outputs(node, output_batch_dim)

@bn_tracker('BatchNormalization')
def track_batchnorm(tracker, node: NodeProto,
                   input_shapes: Optional[List[List[int]]] = None,
                   output_shape: Optional[List[int]] = None) -> None:
    """
    Track BatchNormalization operation batch dimensions.
    
    BatchNormalization preserves the shape and batch dimension of the input.
    """
    if not node.input:
        tracker._set_outputs(node, None)
        return
    
    # Get batch dimension of input
    input_name = node.input[0]
    input_bdim = tracker.get_batch_dim(input_name)
    
    # BatchNormalization preserves batch dimension
    if tracker.verbose:
        tracker.logger.debug(f"  🔄 BatchNormalization: batch dim preserved at {input_bdim}")
    
    # Set output batch dimension
    tracker._set_outputs(node, input_bdim)
