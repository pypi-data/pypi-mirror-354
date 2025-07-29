from typing import Dict, Optional, Type
from .base_handler import BaseHandler
from .elementwise import ElementwiseHandler
from .shape_ops import ShapeOpsHandler
from .math_ops import MathOpsHandler
from .nn_ops import NNOpsHandler
from .flow_ops import FlowControlHandler
from onnx_shape_fix.utils.logger import Logger

# Registry of handlers for different op types
_HANDLERS: Dict[str, type] = {}

# Map of op types to handler classes
_OP_TYPE_MAP: Dict[str, Type[BaseHandler]] = {
    # Elementwise ops
    "Add": ElementwiseHandler,
    "Sub": ElementwiseHandler,
    "Mul": ElementwiseHandler,
    "Div": ElementwiseHandler,
    "Pow": ElementwiseHandler,
    "And": ElementwiseHandler,
    "Or": ElementwiseHandler,
    "Xor": ElementwiseHandler,
    "Greater": ElementwiseHandler,
    "Less": ElementwiseHandler,
    "LessOrEqual": ElementwiseHandler,
    "Equal": ElementwiseHandler,
    "Max": ElementwiseHandler,
    "Min": ElementwiseHandler,
    "Mean": ElementwiseHandler,
    "Sum": ElementwiseHandler,
    "Cast": ElementwiseHandler,
    "Not": ElementwiseHandler,
    "Sqrt": ElementwiseHandler,
    "Erf": ElementwiseHandler,
    "Log": ElementwiseHandler,
    "Sign": ElementwiseHandler,
    "Atan": ElementwiseHandler,
    "Floor": ElementwiseHandler,
    
    # Shape operations
    "Reshape": ShapeOpsHandler,
    "Flatten": ShapeOpsHandler,
    "Squeeze": ShapeOpsHandler,
    "Unsqueeze": ShapeOpsHandler,
    "Transpose": ShapeOpsHandler,
    "Slice": ShapeOpsHandler,
    "Gather": ShapeOpsHandler,
    "Concat": ShapeOpsHandler,
    "Split": ShapeOpsHandler,
    "Expand": ShapeOpsHandler,
    "Shape": ShapeOpsHandler,
    "ConstantOfShape": ShapeOpsHandler,
    
    # Math operations
    "MatMul": MathOpsHandler,
    "Gemm": MathOpsHandler,
    "Conv": MathOpsHandler,
    "Einsum": MathOpsHandler,
    "ReduceMean": MathOpsHandler,
    "ReduceSum": MathOpsHandler,
    "Softmax": MathOpsHandler,
    "Mod": MathOpsHandler,
    "Constant": MathOpsHandler,
    
    # Neural network operations
    "BatchNormalization": NNOpsHandler,
    "Dropout": NNOpsHandler,
    "Relu": NNOpsHandler,
    "LeakyRelu": NNOpsHandler,
    "Sigmoid": NNOpsHandler,
    "Tanh": NNOpsHandler,
    "Softplus": NNOpsHandler,
    "Selu": NNOpsHandler,
    "Elu": NNOpsHandler,
    "Clip": NNOpsHandler,
    "InstanceNormalization": NNOpsHandler,
    "Where": ElementwiseHandler,
    
    # Flow control operations
    "If": FlowControlHandler,
    "Loop": FlowControlHandler,
}

def register_handler(op_type: str, handler_class: type) -> None:
    """
    Register a handler for a specific op type.
    
    Args:
        op_type: The ONNX op type
        handler_class: The handler class to register
    """
    global _HANDLERS
    _HANDLERS[op_type] = handler_class


def get_handler_for_op(op_type: str, verbose: bool = False) -> Optional[BaseHandler]:
    """
    Get a handler instance for the specified op type.
    
    Args:
        op_type: The ONNX op type
        verbose: Whether to enable verbose logging
        
    Returns:
        A handler instance or None if no handler is registered
    """
    
    logger = Logger(verbose)

    # If we already have a registered handler, return an instance
    if op_type in _HANDLERS:
        # logger.debug(f"Using registered handler for op_type: '{op_type}'")
        return _HANDLERS[op_type](verbose)
    
    # Otherwise, look up the handler class in the map
    if op_type in _OP_TYPE_MAP:
        handler_class = _OP_TYPE_MAP[op_type]
        register_handler(op_type, handler_class)
        # logger.debug(f"Found handler for op_type: '{op_type}'")
        return handler_class(verbose)
    
    return None





# Export public API
__all__ = ["register_handler", "get_handler_for_op", "BaseHandler"]
