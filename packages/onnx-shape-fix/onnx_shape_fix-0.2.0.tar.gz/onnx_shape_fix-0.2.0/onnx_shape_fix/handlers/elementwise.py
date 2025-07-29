from typing import List, Any
import numpy as np
from onnx import NodeProto

from .base_handler import BaseHandler
from ..utils.logger import Logger

class ElementwiseHandler(BaseHandler):
    """
    Handler for elementwise operations with broadcasting.
    
    Handles operations like Add, Sub, Mul, Div, Pow, etc. that apply element-wise
    transformations and follow NumPy broadcasting rules.
    """
    
    def __init__(self, verbose: bool = False):
        super().__init__(verbose)
        self.logger = Logger(verbose=verbose)
    
    def handle_node(self, node: NodeProto, input_shapes: List[List[int]], propagator: Any = None) -> List[List[int]]:
        """
        Handle elementwise operations by applying broadcasting rules.
        
        Args:
            node: The ONNX node
            input_shapes: Shapes of the input tensors
            propagator: The shape propagator instance
            
        Returns:
            A list containing the output shape after broadcasting
        """
        try:
            # Filter out None inputs
            valid_shapes = [shape for shape in input_shapes if shape is not None]
            
            if not valid_shapes:
                self.logger.error(f"No valid input shapes for '{node.name}' ('{node.op_type}')")
                # Return a list with None for each output
                return [None] * len(node.output)
            
            if len(valid_shapes) == 1:
                # Single input operations like Neg, Not, etc.
                # self.logger.debug(f"Single input elementwise op '{node.op_type}': input shape {valid_shapes[0]}")
                return [valid_shapes[0]] * len(node.output)
            
            # Start with the first input shape
            result_shape = list(valid_shapes[0])
            
            # Special case for attention mechanisms: when shapes differ only in first dimension
            # but match in all other dimensions (common in transformer models)
            if (len(valid_shapes) == 2 and
                len(valid_shapes[0]) >= 2 and len(valid_shapes[1]) >= 2 and
                len(valid_shapes[0]) == len(valid_shapes[1]) and
                valid_shapes[0][1:] == valid_shapes[1][1:]):
                
                # Take the maximum of the first dimensions, or prefer non-1 value if available
                if valid_shapes[0][0] == 1:
                    first_dim = valid_shapes[1][0]
                elif valid_shapes[1][0] == 1:
                    first_dim = valid_shapes[0][0]
                else:
                    # If neither is 1, prefer largest dimension for attention mechanisms
                    # This is a special case for transformer architectures
                    first_dim = max(valid_shapes[0][0], valid_shapes[1][0])
                    self.logger.warning(f"Special attention broadcasting in '{node.name}': "
                                       f"First dimensions {valid_shapes[0][0]} and {valid_shapes[1][0]} - using {first_dim}")
                
                output_shape = [first_dim] + valid_shapes[0][1:]
                self.logger.debug(f"Special case handling for '{node.op_type}': {valid_shapes} -> {output_shape}")
                return [output_shape] * len(node.output)
            
            # Apply broadcasting rules for each additional input
            for i in range(1, len(valid_shapes)):
                try:
                    shape2 = valid_shapes[i]
                    
                    # Pad shorter shape with 1s
                    if len(result_shape) < len(shape2):
                        result_shape = [1] * (len(shape2) - len(result_shape)) + result_shape
                    elif len(shape2) < len(result_shape):
                        shape2 = [1] * (len(result_shape) - len(shape2)) + shape2
                    
                    # Apply broadcasting rules dimension by dimension
                    broadcast_shape = []
                    for dim1, dim2 in zip(result_shape, shape2):
                        if dim1 == 1 or dim2 == 1:
                            # One dimension is 1, so it can be broadcast
                            broadcast_shape.append(max(dim1, dim2))
                        elif dim1 == dim2:
                            # Dimensions match
                            broadcast_shape.append(dim1)
                        elif dim1 == -1 or dim2 == -1:
                            # One dimension is unknown
                            broadcast_shape.append(-1)
                        else:
                            # Dimensions don't match and neither is 1
                            # Special case for transformer models with attention mechanisms
                            if node.name and ("attn" in node.name.lower() or "attention" in node.name.lower()):
                                self.logger.warning(f"Allowing special attention broadcasting between {dim1} and {dim2} in '{node.name}'")
                                broadcast_shape.append(max(dim1, dim2))
                            else:
                                self.logger.error(f"Cannot broadcast dimensions {dim1} and {dim2} in '{node.name}'")
                                return [None] * len(node.output)
                    
                    result_shape = broadcast_shape
                    
                except Exception as e:
                    self.logger.error(f"Broadcasting error in '{node.name}': {str(e)}")
                    return [None] * len(node.output)
            
            self.logger.debug(f"Elementwise op '{node.op_type}': input shapes {valid_shapes} -> output shape {result_shape}")
            
            # Return a list containing the result shape for each output
            return [result_shape] * len(node.output)
            
        except Exception as e:
            self.logger.error(f"'{node.op_type}' error in '{node.name}': {str(e)}")
            return [None] * len(node.output)
