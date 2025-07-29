from typing import List, Optional, Any
import numpy as np
from onnx import NodeProto, numpy_helper

from .base_handler import BaseHandler
from ..utils.logger import Logger
from ..utils.constant_utils import get_constant_value
from onnx import GraphProto


class NNOpsHandler(BaseHandler):
    """
    Handler for neural network operations.
    
    This handler implements shape inference for neural network operations like
    BatchNormalization, Dropout, activation functions, etc.
    """
    
    def __init__(self, verbose: bool = False):
        super().__init__(verbose)
        self.logger = Logger(verbose=verbose)
    
    def handle_node(self, node: NodeProto, input_shapes: List[List[int]], propagator: Any) -> List[List[int]]:
        """
        Handle neural network operations by dispatching to specific method based on op_type.
        
        Args:
            node: The ONNX node
            input_shapes: Shapes of the input tensors
            propagator: The shape propagator instance
            
        Returns:
            A list of output shapes, one for each output of the node
        """
        try:
            # Group shape-preserving ops
            shape_preserving_ops = [
                "Relu", "LeakyRelu", "Sigmoid", "Tanh", "Softplus", 
                "Selu", "Elu", "Dropout", "Clip", "InstanceNormalization"
            ]
            
            if node.op_type in shape_preserving_ops:
                shape = self._handle_shape_preserving(node, input_shapes)
                return [shape] if shape else [None] * len(node.output)
            elif node.op_type == "BatchNormalization":
                return self._handle_batch_normalization(node, input_shapes)
            elif node.op_type == "If":
                shape = self._handle_if(node, input_shapes, propagator)
                return [shape] if shape else [None] * len(node.output)
            elif node.op_type == "Where":
                shape = self._handle_where(node, input_shapes)
                return [shape] if shape else [None] * len(node.output)
            else:
                self.logger.error("Unhandled neural network op: %s", node.op_type)
                return [None] * len(node.output)
                
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
    
    def _handle_shape_preserving(self, node: NodeProto, input_shapes: List[List[int]]) -> List[int]:
        """
        Handle operations that preserve the input shape.
        
        This includes most activation functions and other element-wise operations.
        """
        try:
            if not input_shapes or len(input_shapes) < 1 or not input_shapes[0]:
                self.logger.error("Missing input shape for %s %s", node.op_type, node.name)
                return None
            
            input_shape = input_shapes[0]
            output_shape = list(input_shape)
            
            self.logger.debug("%s %s: %s -> %s", node.op_type, node.name, input_shape, output_shape)
            return output_shape
            
        except Exception as e:
            self.logger.error("%s error in %s: %s", node.op_type, node.name, str(e))
            return None
    
    def _handle_batch_normalization(self, node: NodeProto, input_shapes: List[List[int]]) -> List[List[int]]:
        """
        Handle BatchNormalization operation.
        
        BatchNormalization normalizes input across batch dimension and preserves shape.
        The operation can have multiple outputs:
        - Y: The main output with same shape as input
        - mean: Runtime mean with shape [C]
        - var: Runtime variance with shape [C]
        - saved_mean: Optional saved mean with shape [C]
        - saved_var: Optional saved variance with shape [C]
        """
        try:
            if not input_shapes or len(input_shapes) < 1 or not input_shapes[0]:
                self.logger.error("Missing input shape for BatchNormalization %s", node.name)
                return [None] * len(node.output)
            
            data_shape = input_shapes[0]
            
            # Validate parameter shapes
            if len(input_shapes) >= 5:
                # Expected shapes:
                # input[1] (scale): [C]
                # input[2] (B): [C]
                # input[3] (mean): [C]
                # input[4] (var): [C]
                
                # Get channel dimension (default is 1 for NCHW format)
                axis = self._get_attribute(node, "axis", 1)
                
                if len(data_shape) <= axis:
                    self.logger.warning("Input rank too small for BatchNormalization %s", node.name)
                    return [data_shape] + [[1]] * (len(node.output) - 1)
                
                channel_size = data_shape[axis]
                
                for i, param_name in enumerate(['scale', 'bias', 'mean', 'var']):
                    if i + 1 < len(input_shapes) and input_shapes[i + 1]:
                        param_shape = input_shapes[i + 1]
                        
                        if len(param_shape) != 1:
                            self.logger.warning("%s has %d dimensions, expected 1 in %s", 
                                            param_name, len(param_shape), node.name)
                            
                        elif param_shape[0] != channel_size:
                            self.logger.warning("%s has size %d, expected %d in %s",
                                            param_name, param_shape[0], channel_size, node.name)
            
            # BatchNormalization preserves input shape for first output
            # Additional outputs are channel statistics with shape [C]
            output_shapes = [list(data_shape)]
            
            # For the additional outputs (mean, var, saved_mean, saved_var)
            # Get the channel dimension shape
            channel_dim = self._get_attribute(node, "axis", 1)
            channel_shape = [data_shape[channel_dim]] if channel_dim < len(data_shape) else [1]
            
            # Add channel shape for each additional output
            for _ in range(1, len(node.output)):
                output_shapes.append(channel_shape)
            
            self.logger.debug("BatchNormalization %s: %s -> %s", 
                         node.name, data_shape, output_shapes)
            return output_shapes
            
        except Exception as e:
            self.logger.error("BatchNormalization error in %s: %s", node.name, str(e))
            return [None] * len(node.output)

    def _handle_where(self, node: NodeProto, input_shapes: List[List[int]]) -> List[int]:
        """
        Handle Where operation.
        
        Where selects elements from X or Y based on a condition.
        """
        try:
            if not input_shapes or len(input_shapes) < 3:
                self.logger.error("Insufficient input shapes for Where %s", node.name)
                return None
            
            condition_shape = input_shapes[0]
            x_shape = input_shapes[1]
            y_shape = input_shapes[2]
            
            # Skip empty shapes
            if not condition_shape or not x_shape or not y_shape:
                # Try to infer from the non-empty shapes
                shapes = [s for s in [condition_shape, x_shape, y_shape] if s]
                if shapes:
                    # Use the shape with the highest rank
                    max_rank_shape = max(shapes, key=len)
                    self.logger.debug("Where %s: Using max rank shape %s from available shapes", 
                                   node.name, max_rank_shape)
                    return max_rank_shape
                else:
                    self.logger.error("All input shapes are empty for Where %s", node.name)
                    return None
            
            # Apply broadcasting rules
            
            # Get max rank
            max_rank = max(len(condition_shape), len(x_shape), len(y_shape))
            
            # Pad shapes to max rank
            padded_condition = [1] * (max_rank - len(condition_shape)) + list(condition_shape)
            padded_x = [1] * (max_rank - len(x_shape)) + list(x_shape)
            padded_y = [1] * (max_rank - len(y_shape)) + list(y_shape)
            
            # Apply broadcasting rules to determine output shape
            output_shape = []
            for i in range(max_rank):
                dims = [padded_condition[i], padded_x[i], padded_y[i]]
                max_dim = max(dims)
                
                for d in dims:
                    if d != 1 and d != max_dim:
                        self.logger.error("Cannot broadcast dimensions %s in Where %s", dims, node.name)
                        return None
                
                output_shape.append(max_dim)
            
            self.logger.debug("Where %s: condition %s, x %s, y %s -> %s", 
                           node.name, condition_shape, x_shape, y_shape, output_shape)
            return output_shape
            
        except Exception as e:
            self.logger.error("Where error in %s: %s", node.name, str(e))
            return None

