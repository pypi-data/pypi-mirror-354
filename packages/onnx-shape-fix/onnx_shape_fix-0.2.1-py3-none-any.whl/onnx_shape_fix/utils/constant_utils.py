from typing import Optional, List, Any
import numpy as np
from onnx import NodeProto, numpy_helper
from onnx.mapping import TENSOR_TYPE_TO_NP_TYPE
from onnx_shape_fix.utils.logger import Logger

logger = Logger(verbose=True)

# A simple cache to avoid recalculating constant values.
_constant_cache = {}

def get_constant_value(input_name: str, propagator: Any, depth: int = 0) -> Optional[np.ndarray]:
    """
    Retrieve constant value from initializers or through tracing operations.
    
    Args:
        input_name: The name of the input to retrieve.
        propagator: The shape propagator instance containing model information.
        depth: Current recursion depth (incremented on each recursive call).
        
    Returns:
        The constant value as a numpy array, or None if not constant.
    """
    # Only log for significant recursion to reduce noise
    if depth > 0 and depth % 5 == 0:
        logger.debug(f"🔍 Constant trace depth {depth}: {input_name}")

    # Limit recursion depth to prevent runaway recursion
    MAX_DEPTH = 500
    if depth > MAX_DEPTH:
        raise RecursionError(f"⛔ Maximum recursion depth ({MAX_DEPTH}) reached")

    # Use caching to avoid duplicate work
    cache_key = (input_name, depth)
    if cache_key in _constant_cache:
        return _constant_cache[cache_key]

    # Check initializers first
    for init in propagator.model.graph.initializer:
        if init.name == input_name:
            value = numpy_helper.to_array(init)
            _constant_cache[cache_key] = value
            return value

    # Find the producer node for this input
    producer = None
    for node in propagator.model.graph.node:
        if input_name in node.output:
            producer = node
            break

    if producer is None:
        # Check if it's a graph input
        for graph_input in propagator.model.graph.input:
            if graph_input.name == input_name:
                raise ValueError(f'Non-constant graph input: {input_name}')
        raise ValueError(f"Producer node not found for {input_name}")

    # Handle different op_types with cleaner logging
    if producer.op_type == 'Constant':
        for attr in producer.attribute:
            if attr.name == 'value':
                value = numpy_helper.to_array(attr.t)
                _constant_cache[cache_key] = value
                return value
        raise ValueError(f"Constant node {producer.name} has no value attribute")

    elif producer.op_type == 'ConstantOfShape':
        # Get shape from input (increment depth)
        shape = get_constant_value(producer.input[0], propagator, depth + 1)
        if shape is None:
            raise ValueError(f"Shape of {producer.name} is not constant (None)")
        
        # Get value from attribute (default to 0)
        value = np.zeros(1, dtype=np.float32)
        for attr in producer.attribute:
            if attr.name == 'value':
                value = numpy_helper.to_array(attr.t)
        result = np.full(shape, value)
        _constant_cache[cache_key] = result
        return result

    elif producer.op_type == 'Add':
        a = get_constant_value(producer.input[0], propagator, depth + 1)
        b = get_constant_value(producer.input[1], propagator, depth + 1)
        if a is not None and b is not None:
            value = a + b
            _constant_cache[cache_key] = value
            return value
        raise ValueError(f"Add node {producer.name} has non-constant inputs")

    elif producer.op_type == 'Mul':
        a = get_constant_value(producer.input[0], propagator, depth + 1)
        b = get_constant_value(producer.input[1], propagator, depth + 1)
        if a is not None and b is not None:
            value = np.multiply(a, b)
            _constant_cache[cache_key] = value
            return value
        raise ValueError(f"Mul node {producer.name} has non-constant inputs")

    elif producer.op_type == 'Equal':
        a = get_constant_value(producer.input[0], propagator, depth + 1)
        b = get_constant_value(producer.input[1], propagator, depth + 1)
        if a is not None and b is not None:
            value = np.equal(a, b)
            _constant_cache[cache_key] = value
            return value
        raise ValueError(f"Equal node {producer.name} has non-constant inputs")

    elif producer.op_type == 'Shape':
        input_shape = propagator.shape_dict.get(producer.input[0])
        if input_shape is not None:
            logger.debug(f"Found shape for {producer.input[0]} in shape_dict")
            value = np.array(input_shape, dtype=np.int64)
            _constant_cache[cache_key] = value
            return value  # Fixed: return the value when found.
        raise ValueError(f"Shape of {producer.input[0]} is not known")

    elif producer.op_type == 'Reshape':
        data = get_constant_value(producer.input[0], propagator, depth + 1)
        shape = get_constant_value(producer.input[1], propagator, depth + 1)
        if data is not None and shape is not None:
            logger.debug(f"💜 Reshaping with target shape {shape}")
            value = np.reshape(data, shape)
            _constant_cache[cache_key] = value
            return value
        raise ValueError(f"Reshape node has non-constant inputs: shape {shape}")

    elif producer.op_type == 'Cast':
        data = get_constant_value(producer.input[0], propagator, depth + 1)
        if data is not None:
            # Get target data type from attribute
            dtype = None
            for attr in producer.attribute:
                if attr.name == 'to':
                    dtype = TENSOR_TYPE_TO_NP_TYPE[attr.i]
                    break
            if dtype is not None:
                value = data.astype(dtype)
                _constant_cache[cache_key] = value
                return value
        raise ValueError(f"Cast node {producer.name} has non-constant inputs or no target dtype")

    elif producer.op_type == 'Mod':
        a = get_constant_value(producer.input[0], propagator, depth + 1)
        b = get_constant_value(producer.input[1], propagator, depth + 1)
        if a is not None and b is not None:
            value = np.mod(a, b)
            _constant_cache[cache_key] = value
            return value
        raise ValueError(f"Mod node {producer.name} has non-constant inputs")

    elif producer.op_type == 'Concat':
        axis = None
        for attr in producer.attribute:
            if attr.name == 'axis':
                axis = attr.i
                break
        if axis is None:
            raise ValueError(f"Concat node {producer.name} has no axis attribute")
        
        concat_values = []
        for inp in producer.input:
            val = get_constant_value(inp, propagator, depth + 1)
            if val is None:
                raise ValueError(f"Concat node {producer.name} has non-constant inputs")
            concat_values.append(val)
        
        try:
            value = np.concatenate(concat_values, axis=axis)
            _constant_cache[cache_key] = value
            return value
        except Exception as e:
            raise ValueError(f"Concat node {producer.name} error: {e}")

    elif producer.op_type == 'Slice':
        data = get_constant_value(producer.input[0], propagator, depth + 1)
        starts = get_constant_value(producer.input[1], propagator, depth + 1)
        ends = get_constant_value(producer.input[2], propagator, depth + 1)
        axes = None
        if len(producer.input) > 3:
            axes = get_constant_value(producer.input[3], propagator, depth + 1)
        steps = None
        if len(producer.input) > 4:
            steps = get_constant_value(producer.input[4], propagator, depth + 1)
        
        if data is None or starts is None or ends is None:
            raise ValueError(f"Slice node {producer.name} has non-constant inputs")
        
        # Handle default values
        if axes is None:
            axes = list(range(len(starts)))
        if steps is None:
            steps = [1] * len(starts)
        
        # Convert to proper formats
        starts = np.atleast_1d(starts)
        ends = np.atleast_1d(ends)
        axes = np.atleast_1d(axes)
        steps = np.atleast_1d(steps)
        
        slices = [slice(None)] * data.ndim
        for ax, s, e, step in zip(axes, starts, ends, steps):
            if ax >= data.ndim:
                raise ValueError(f"Slice node {producer.name} has invalid axis {ax}")
            slices[ax] = slice(int(s), int(e), int(step))
        
        value = data[tuple(slices)]
        _constant_cache[cache_key] = value
        return value    

    elif producer.op_type == 'Where':
        condition = get_constant_value(producer.input[0], propagator, depth + 1)
        x = get_constant_value(producer.input[1], propagator, depth + 1)
        y = get_constant_value(producer.input[2], propagator, depth + 1)
        if condition is not None and x is not None and y is not None:
            value = np.where(condition, x, y)
            _constant_cache[cache_key] = value
            return value
        raise ValueError(f"Where node {producer.name} has non-constant inputs")

    elif producer.op_type == 'Gather':
        data = get_constant_value(producer.input[0], propagator, depth + 1)
        indices = get_constant_value(producer.input[1], propagator, depth + 1)
        if data is not None and indices is not None:
            axis = 0
            for attr in producer.attribute:
                if attr.name == 'axis':
                    axis = attr.i
            value = np.take(data, indices, axis=axis)
            _constant_cache[cache_key] = value
            return value
        raise ValueError(f"Gather node {producer.name} has non-constant inputs")

    elif producer.op_type == 'Unsqueeze':
        data = get_constant_value(producer.input[0], propagator, depth + 1)
        if data is None:
            raise ValueError(f"Unsqueeze node {producer.name} has non-constant inputs")
        
        axes = None
        if len(producer.input) > 1:
            axes = get_constant_value(producer.input[1], propagator, depth + 1)
        else:
            for attr in producer.attribute:
                if attr.name == 'axes':
                    axes = attr.ints
                    break
        
        if axes is None:
            raise ValueError(f"Unsqueeze node {producer.name} has no axes attribute")
        
        result = data
        for ax in sorted(axes):
            result = np.expand_dims(result, axis=ax)
        
        _constant_cache[cache_key] = result
        return result

    elif producer.op_type == 'Squeeze':
        data = get_constant_value(producer.input[0], propagator, depth + 1)
        if data is None:
            raise ValueError(f"Squeeze node {producer.name} has non-constant inputs")
        
        axes = []
        if len(producer.input) > 1:
            axes = get_constant_value(producer.input[1], propagator, depth + 1)
        
        if axes:
            value = np.squeeze(data, axis=tuple(axes))
        else:
            value = np.squeeze(data)
        _constant_cache[cache_key] = value
        return value

    # Add other operations as needed
    else:
        raise ValueError(f"❌ Unsupported constant type: {producer.op_type}")
