from typing import List, Optional, Any
import numpy as np
from onnx import NodeProto, numpy_helper

from .base_handler import BaseHandler
from ..utils.logger import Logger
from ..utils.constant_utils import get_constant_value

class MathOpsHandler(BaseHandler):
    """
    Handler for mathematical operations.
    
    This handler implements shape inference for math operations like
    MatMul, Gemm, Conv, ReduceMean, etc.
    """
    
    def __init__(self, verbose: bool = False):
        super().__init__(verbose)
        self.logger = Logger(verbose=verbose)
    
    def handle_node(self, node: NodeProto, input_shapes: List[List[int]], propagator: Any) -> List[List[int]]:
        """
        Handle math operations by dispatching to specific method based on op_type.
        
        Args:
            node: The ONNX node
            input_shapes: Shapes of the input tensors
            propagator: The shape propagator instance
            
        Returns:
            A list of output shapes, one for each output of the node
        """
        try:
            # Dispatch to specific handler method based on op_type
            if node.op_type == "MatMul":
                shape = self._handle_matmul(node, input_shapes)
                return [shape] if shape else [None] * len(node.output)
            elif node.op_type == "Gemm":
                shape = self._handle_gemm(node, input_shapes)
                return [shape] if shape else [None] * len(node.output)
            elif node.op_type == "Conv":
                shape = self._handle_conv(node, input_shapes)
                return [shape] if shape else [None] * len(node.output)
            elif node.op_type in ["ReduceMean", "ReduceSum", "ReduceMax", "ReduceMin", 
                                  "ReduceL1", "ReduceL2", "ReduceLogSum", "ReduceLogSumExp",
                                  "ReduceProd", "ReduceSumSquare"]:
                shape = self._handle_reduce(node, input_shapes, propagator)
                return [shape] if shape else [None] * len(node.output)
            elif node.op_type == "Softmax":
                shape = self._handle_softmax(node, input_shapes)
                return [shape] if shape else [None] * len(node.output)
            elif node.op_type == "Mod":
                shape = self._handle_elementwise(node, input_shapes)
                return [shape] if shape else [None] * len(node.output)
            elif node.op_type == "Constant":
                shape = self._handle_constant(node, propagator)
                return [shape] if shape else [None] * len(node.output)
            elif node.op_type == "Einsum":
                shape = self._handle_einsum(node, input_shapes)
                return [shape] if shape else [None] * len(node.output)
            elif node.op_type == "Where":
                shape = self._handle_where(node, input_shapes)
                return [shape] if shape else [None] * len(node.output)
            else:
                self.logger.error("Unhandled math op: %s", node.op_type)
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
    
    def _handle_matmul(self, node: NodeProto, input_shapes: List[List[int]], propagator: Any = None) -> Optional[List[int]]:
        """
        Handle MatMul operation.
        
        MatMul performs matrix multiplication with broadcasting of batch dimensions.
        Includes special handling for attention mechanisms.
        """
        try:
            if not input_shapes or len(input_shapes) < 2:
                self.logger.error("Insufficient input shapes for MatMul %s", node.name)
                return None
            
            a_shape = input_shapes[0]
            b_shape = input_shapes[1]
            
            if not a_shape or not b_shape:
                self.logger.error("Missing input shapes for MatMul %s", node.name)
                return None
            
            # Handle special case for 1D inputs
            if len(a_shape) == 1 and len(b_shape) == 1:
                # Vector-vector multiplication -> scalar
                if a_shape[0] != b_shape[0] and a_shape[0] != -1 and b_shape[0] != -1:
                    self.logger.error("Incompatible dimensions for 1D MatMul %s: %d != %d", 
                                   node.name, a_shape[0], b_shape[0])
                    return None
                return []  # Scalar output
            
            if len(a_shape) == 1:
                # Vector-matrix -> vector
                if a_shape[0] != b_shape[-2] and a_shape[0] != -1 and b_shape[-2] != -1:
                    self.logger.error("Incompatible dimensions for MatMul %s: %d != %d", 
                                   node.name, a_shape[0], b_shape[-2])
                    return None
                return b_shape[:-2] + [b_shape[-1]]
            
            if len(b_shape) == 1:
                # Matrix-vector -> vector
                if a_shape[-1] != b_shape[0] and a_shape[-1] != -1 and b_shape[0] != -1:
                    self.logger.error("Incompatible dimensions for MatMul %s: %d != %d", 
                                   node.name, a_shape[-1], b_shape[0])
                    return None
                return a_shape[:-1]
            
            # Check inner dimensions for compatibility
            if a_shape[-1] != b_shape[-2] and a_shape[-1] != -1 and b_shape[-2] != -1:
                self.logger.error("Incompatible inner dimensions for MatMul %s: %d != %d", 
                               node.name, a_shape[-1], b_shape[-2])
                return None
            
            # Special case for attention mechanisms
            is_attention_block = node.name and ("attn" in node.name.lower() or "attention" in node.name.lower())
            
            # Batch dimensions (all except last 2)
            a_batch = a_shape[:-2]
            b_batch = b_shape[:-2]
            
            # If one has no batch dimensions, broadcast it
            if not a_batch:
                return b_batch + [a_shape[-2], b_shape[-1]]
            if not b_batch:
                return a_batch + [a_shape[-2], b_shape[-1]]
            
            # If batch dimensions don't match but we're in an attention block, use special handling
            if a_batch != b_batch and is_attention_block and len(a_batch) == len(b_batch):
                self.logger.warning("Special attention batch broadcasting in MatMul %s: %s and %s", 
                                 node.name, a_batch, b_batch)
                
                # Take max of each batch dimension
                output_batch = []
                for a_dim, b_dim in zip(a_batch, b_batch):
                    if a_dim == 1:
                        output_batch.append(b_dim)
                    elif b_dim == 1:
                        output_batch.append(a_dim)
                    elif a_dim == -1 or b_dim == -1:
                        output_batch.append(-1)  # Unknown
                    else:
                        # For attention mechanisms, take the max dimension
                        output_batch.append(max(a_dim, b_dim))
                
                return output_batch + [a_shape[-2], b_shape[-1]]
            
            # Try to broadcast batch dimensions (standard behavior)
            try:
                output_batch = []
                
                # Pad with 1s if batch ranks don't match
                if len(a_batch) > len(b_batch):
                    b_batch_padded = [1] * (len(a_batch) - len(b_batch)) + b_batch
                    a_batch_padded = a_batch
                elif len(b_batch) > len(a_batch):
                    a_batch_padded = [1] * (len(b_batch) - len(a_batch)) + a_batch
                    b_batch_padded = b_batch
                else:
                    a_batch_padded = a_batch
                    b_batch_padded = b_batch
                
                # Apply broadcasting rules to batch dimensions
                for a_dim, b_dim in zip(a_batch_padded, b_batch_padded):
                    if a_dim == 1:
                        output_batch.append(b_dim)
                    elif b_dim == 1:
                        output_batch.append(a_dim)
                    elif a_dim == b_dim:
                        output_batch.append(a_dim)
                    elif a_dim == -1 or b_dim == -1:
                        output_batch.append(-1)  # Unknown
                    else:
                        # If dimensions don't match and we're in an attention block, allow it
                        if is_attention_block:
                            self.logger.warning("Using max batch dim for attention MatMul %s: %d vs %d", 
                                             node.name, a_dim, b_dim)
                            output_batch.append(max(a_dim, b_dim))
                        else:
                            self.logger.error("Cannot broadcast batch dimensions %d and %d in MatMul %s", 
                                          a_dim, b_dim, node.name)
                            return None
                
                # Combine batch with output matrix dimensions
                output_shape = output_batch + [a_shape[-2], b_shape[-1]]
                self.logger.debug("MatMul %s: %s × %s -> %s", node.name, a_shape, b_shape, output_shape)
                return output_shape
                
            except Exception as e:
                self.logger.error("Batch broadcasting error in MatMul %s: %s", node.name, str(e))
                return None
            
        except Exception as e:
            self.logger.error("MatMul error in %s: %s", node.name, str(e))
            return None
    
    def _handle_gemm(self, node, inputs: List[List[int]]) -> Optional[List[int]]:
        """Handle Gemm operation - general matrix multiplication"""
        try:
            if not inputs or len(inputs) < 2:
                print(f"🧮 {node.name}: Gemm requires at least 2 inputs (A, B)")
                return None
                
            a_shape = inputs[0]  # Input tensor A
            b_shape = inputs[1]  # Input tensor B
            
            # Get attributes with defaults
            alpha = 1.0
            beta = 1.0
            transA = 0
            transB = 0
            
            for attr in node.attribute:
                if attr.name == "alpha":
                    alpha = attr.f
                elif attr.name == "beta":
                    beta = attr.f
                elif attr.name == "transA":
                    transA = attr.i
                elif attr.name == "transB":
                    transB = attr.i
            
            # Handle special case for 1D input
            if len(a_shape) == 1:
                print(f"   🗒️ Note: Gemm with 1D input A shape {a_shape}, treating as [1, {a_shape[0]}]")
                a_shape = [1, a_shape[0]]
                
            # Handle special case for 1D weight matrix
            if len(b_shape) == 1:
                print(f"   🗒️ Note: Gemm with 1D input B shape {b_shape}, treating as [{b_shape[0]}, 1]")
                b_shape = [b_shape[0], 1]
            
            # Apply transpositions if specified
            if transA:
                a_shape = list(reversed(a_shape))
            if transB:
                b_shape = list(reversed(b_shape))
            
            # Validate matrix dimensions for multiplication
            if len(a_shape) < 2 or len(b_shape) < 2:
                print(
                    f"🧮 {node.name}: Invalid shapes for Gemm: A={a_shape}, B={b_shape}"
                )
                # Try to infer a reasonable output shape as fallback
                if len(a_shape) >= 1 and len(b_shape) >= 1:
                    return [a_shape[0], b_shape[-1]]
                return None
                
            if a_shape[-1] != b_shape[0]:
                print(
                    f"🧮 {node.name}: Incompatible dimensions for matrix multiplication: "
                    f"A={a_shape}, B={b_shape}"
                )
                # Try to infer a reasonable output shape as fallback
                return [a_shape[0], b_shape[-1]]
            
            # Output shape is [a_rows, b_cols]
            output_shape = [a_shape[0], b_shape[-1]]
            
            # If C is provided (bias), validate its shape
            if len(inputs) > 2 and inputs[2]:
                c_shape = inputs[2]
                
                # C should be a vector with length matching b_cols, or a matrix matching the output shape
                if len(c_shape) == 1:
                    if c_shape[0] != output_shape[-1]:
                        print(f"   ☢️ Warning: Bias shape {c_shape} doesn't match output columns {output_shape[-1]}")
                elif len(c_shape) == 2:
                    if c_shape != output_shape:
                        print(f"   ☢️ Warning: Bias shape {c_shape} doesn't match output shape {output_shape}")
            
            return output_shape
            
        except Exception as e:
            print(f"❌ Gemm error in {node.name}: {str(e)}")
            return None

    def _handle_conv(self, node: NodeProto, input_shapes: List[List[int]]) -> Optional[List[int]]:
        """
        Handle Conv operation.
        
        Conv performs convolution on input tensor with specified kernel.
        """
        try:
            if not input_shapes or len(input_shapes) < 2:
                self.logger.error("Insufficient input shapes for Conv %s", node.name)
                return None
            
            x_shape = input_shapes[0]  # Input
            w_shape = input_shapes[1]  # Weight
            
            if not x_shape or not w_shape:
                self.logger.error("Missing input shapes for Conv %s", node.name)
                return None
            
            # Get attributes with defaults
            auto_pad = self._get_attribute(node, "auto_pad", "NOTSET")
            dilations = self._get_attribute(node, "dilations", [1] * (len(x_shape) - 2))
            group = self._get_attribute(node, "group", 1)
            kernel_shape = self._get_attribute(node, "kernel_shape", w_shape[2:])
            pads = self._get_attribute(node, "pads", [0] * (2 * (len(x_shape) - 2)))
            strides = self._get_attribute(node, "strides", [1] * (len(x_shape) - 2))
            
            # Validate input/kernel dimensions
            if len(x_shape) < 3:
                self.logger.error("Input rank too small for Conv %s", node.name)
                return None
            
            if len(w_shape) != len(x_shape):
                self.logger.error("Weight and input rank mismatch for Conv %s", node.name)
                return None
            
            # Calculate spatial dimensions
            spatial_dims = len(x_shape) - 2
            
            # Validate dilations and strides length
            if len(dilations) != spatial_dims:
                self.logger.error("Dilations length does not match spatial dimensions for Conv %s", node.name)
                return None
            
            if len(strides) != spatial_dims:
                self.logger.error("Strides length does not match spatial dimensions for Conv %s", node.name)
                return None
            
            # Output shape starts with batch size and output channels
            output_shape = [x_shape[0], w_shape[0]]
            
            # Calculate spatial output dimensions based on pad type
            if auto_pad == "NOTSET":
                # Explicit padding
                if len(pads) != 2 * spatial_dims:
                    self.logger.error("Pads length does not match 2*spatial_dims for Conv %s", node.name)
                    return None
                
                for i in range(spatial_dims):
                    pad_begin = pads[i]
                    pad_end = pads[i + spatial_dims]
                    input_size = x_shape[i + 2]
                    kernel_size = kernel_shape[i]
                    dilation = dilations[i]
                    stride = strides[i]
                    
                    # Calculate effective kernel size with dilation
                    effective_kernel_size = (kernel_size - 1) * dilation + 1
                    
                    # Calculate output size
                    output_size = (input_size + pad_begin + pad_end - effective_kernel_size) // stride + 1
                    output_shape.append(max(0, output_size))
                    
            elif auto_pad == "SAME_UPPER" or auto_pad == "SAME_LOWER":
                # For SAME padding, output size = ceil(input_size / stride)
                for i in range(spatial_dims):
                    input_size = x_shape[i + 2]
                    stride = strides[i]
                    output_size = (input_size + stride - 1) // stride
                    output_shape.append(output_size)
                    
            elif auto_pad == "VALID":
                # For VALID padding (no padding)
                for i in range(spatial_dims):
                    input_size = x_shape[i + 2]
                    kernel_size = kernel_shape[i]
                    dilation = dilations[i]
                    stride = strides[i]
                    
                    # Calculate effective kernel size with dilation
                    effective_kernel_size = (kernel_size - 1) * dilation + 1
                    
                    # Calculate output size
                    output_size = (input_size - effective_kernel_size) // stride + 1
                    output_shape.append(max(0, output_size))
            
            self.logger.debug("Conv %s: input %s, weight %s -> %s", 
                          node.name, x_shape, w_shape, output_shape)
            return output_shape
            
        except Exception as e:
            self.logger.error("Conv error in %s: %s", node.name, str(e))
            return None
    
    def _handle_reduce(self, node: NodeProto, input_shapes: List[List[int]], propagator: Any) -> List[int]:
        """
        Handle Reduce operations (ReduceMean, ReduceSum, etc.).
        
        Reduce operations reduce a tensor along specified axes.
        """
        try:
            if not input_shapes or len(input_shapes) < 1 or not input_shapes[0]:
                self.logger.error("Missing input shape for Reduce %s", node.name)
                return None
            
            input_shape = input_shapes[0]
            
            # Get attributes
            axes = None
            keepdims = self._get_attribute(node, "keepdims", 1)
            
            # Try to get axes from attribute (opset < 13)
            axes_attr = self._get_attribute(node, "axes", None)
            if axes_attr is not None:
                axes = axes_attr
            
            # Try to get axes from second input (opset >= 13)
            if axes is None and len(node.input) > 1:
                axes_value = get_constant_value(node.input[1], propagator)
                if axes_value is not None:
                    axes = axes_value.flatten().tolist()
            
            # If axes not specified, reduce along all dimensions
            if axes is None:
                axes = list(range(len(input_shape)))
            
            # Handle negative axes
            axes = [axis if axis >= 0 else len(input_shape) + axis for axis in axes]
            
            # Validate axes
            if any(axis < 0 or axis >= len(input_shape) for axis in axes):
                self.logger.error("Invalid axes for Reduce %s", node.name)
                return None
            
            # Calculate output shape
            output_shape = []
            for i, dim in enumerate(input_shape):
                if i in axes:
                    if keepdims:
                        output_shape.append(1)
                else:
                    output_shape.append(dim)
            
            self.logger.debug("Reduce%s %s: %s along axes %s with keepdims=%d -> %s", 
                           node.op_type[6:], node.name, input_shape, axes, keepdims, output_shape)
            return output_shape
            
        except Exception as e:
            self.logger.error("Reduce error in %s: %s", node.name, str(e))
            return None
    
    def _handle_softmax(self, node: NodeProto, input_shapes: List[List[int]]) -> Optional[List[int]]:
        """
        Handle Softmax operation.
        
        Softmax applies softmax function along a specified axis.
        The shape is preserved.
        """
        try:
            if not input_shapes or len(input_shapes) < 1 or not input_shapes[0]:
                self.logger.error("Missing input shape for Softmax %s", node.name)
                return None
            
            input_shape = input_shapes[0]
            
            # Softmax preserves shape
            output_shape = list(input_shape)
            
            self.logger.debug("Softmax %s: %s -> %s", node.name, input_shape, output_shape)
            return output_shape
            
        except Exception as e:
            self.logger.error("Softmax error in %s: %s", node.name, str(e))
            return None
    
    def _handle_elementwise(self, node: NodeProto, input_shapes: List[List[int]]) -> Optional[List[int]]:
        """
        Handle elementwise operations like Mod.
        
        Elementwise operations apply broadcasting rules.
        """
        try:
            # Filter out None inputs
            valid_shapes = [shape for shape in input_shapes if shape is not None]
            
            if not valid_shapes:
                self.logger.error("No valid input shapes for %s %s", node.op_type, node.name)
                return None
            
            if len(valid_shapes) == 1:
                # Single input operations
                # self.logger.debug("Single input elementwise op %s: input shape %s", 
                #                node.op_type, valid_shapes[0])
                return valid_shapes[0]
            
            # Start with the first input shape
            result_shape = list(valid_shapes[0])
            
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
                        else:
                            # Dimensions don't match and neither is 1
                            self.logger.error("Cannot broadcast dimensions %d and %d in %s %s", 
                                           dim1, dim2, node.op_type, node.name)
                            return None
                    
                    result_shape = broadcast_shape
                    
                except Exception as e:
                    self.logger.error("Broadcasting error in %s %s: %s", node.op_type, node.name, str(e))
                    return None
            
            self.logger.debug("Elementwise op %s: input shapes %s -> output shape %s", 
                           node.op_type, valid_shapes, result_shape)
            return result_shape
            
        except Exception as e:
            self.logger.error("%s error in %s: %s", node.op_type, node.name, str(e))
            return None
    
    def _handle_constant(self, node: NodeProto, propagator: Any) -> Optional[List[int]]:
        """
        Handle Constant operation.
        
        Constant produces a constant tensor.
        """
        try:
            # Get value attribute
            for attr in node.attribute:
                if attr.name == "value":
                    # Get tensor shape
                    shape = list(attr.t.dims)
                    
                    # Store the actual value for potential use later
                    try:
                        value = numpy_helper.to_array(attr.t)
                        # Store in propagator for later use
                        propagator.shape_dict[node.output[0] + "_value"] = value
                    except Exception as e:
                        self.logger.warning("Could not convert Constant to array: %s", str(e))
                    
                    self.logger.debug("Constant %s: shape %s", node.name, shape)
                    return shape
            
            self.logger.error("Constant %s missing value attribute", node.name)
            return None
            
        except Exception as e:
            self.logger.error("Constant error in %s: %s", node.name, str(e))
            return None
    
    def _handle_einsum(self, node: NodeProto, input_shapes: List[List[int]], propagator: Any = None) -> Optional[List[int]]:
        """
        Handle Einsum operation.
        
        Einsum performs operations according to an Einstein summation equation.
        """
        try:
            if not input_shapes:
                self.logger.error("No input shapes for Einsum %s", node.name)
                return None
            
            # Get equation attribute
            equation = self._get_attribute(node, "equation", None)
            if equation is None:
                self.logger.error("Einsum %s missing equation attribute", node.name)
                return None
            
            # Parse the equation
            try:
                left_right = equation.split('->')
                if len(left_right) != 2:
                    self.logger.error("Invalid Einsum equation format: %s", equation)
                    return None
                
                input_part = left_right[0]
                output_part = left_right[1]
                
                input_subscripts = input_part.split(',')
                
                # Verify number of input subscripts matches number of inputs
                if len(input_subscripts) != len(input_shapes):
                    self.logger.warning("Mismatch between input subscripts (%d) and input shapes (%d)",
                                     len(input_subscripts), len(input_shapes))
                
                # Handle specific equation patterns
                
                # Special case for "tbhd,h->tbdh" (attention pattern)
                if equation == "tbhd,h->tbdh" and len(input_shapes) >= 2:
                    t, b, h, d = input_shapes[0] if len(input_shapes[0]) == 4 else (0, 0, 0, 0)
                    # Correctly reorder dimensions for the output
                    output_shape = [t, b, d, h]
                    self.logger.debug("Special case for equation 'tbhd,h->tbdh': %s -> %s", 
                                   input_shapes, output_shape)
                    return output_shape
                
                # Matrix multiplication "ij,jk->ik"
                elif equation == "ij,jk->ik" and len(input_shapes) == 2:
                    a_shape = input_shapes[0]
                    b_shape = input_shapes[1]
                    
                    if len(a_shape) != 2 or len(b_shape) != 2:
                        self.logger.error("Invalid shapes for 'ij,jk->ik' pattern: %s, %s", a_shape, b_shape)
                        return None
                    
                    if a_shape[1] != b_shape[0] and a_shape[1] != -1 and b_shape[0] != -1:
                        self.logger.error("Inner dimensions don't match for 'ij,jk->ik': %d != %d", 
                                       a_shape[1], b_shape[0])
                        return None
                    
                    return [a_shape[0], b_shape[1]]
                
                # Batch matrix multiplication "bij,bjk->bik"
                elif equation == "bij,bjk->bik" and len(input_shapes) == 2:
                    a_shape = input_shapes[0]
                    b_shape = input_shapes[1]
                    
                    if len(a_shape) != 3 or len(b_shape) != 3:
                        self.logger.error("Invalid shapes for 'bij,bjk->bik' pattern: %s, %s", a_shape, b_shape)
                        return None
                    
                    if (a_shape[0] != b_shape[0] and a_shape[0] != 1 and b_shape[0] != 1 and 
                        a_shape[0] != -1 and b_shape[0] != -1):
                        self.logger.error("Batch dimensions don't match for 'bij,bjk->bik'")
                        return None
                    
                    batch_dim = max(a_shape[0], b_shape[0])
                    if batch_dim == -1:
                        batch_dim = a_shape[0] if a_shape[0] != -1 else b_shape[0]
                    
                    return [batch_dim, a_shape[1], b_shape[2]]
                
                # For more general cases, map dimensions based on the equation
                else:
                    self.logger.warning("Using generic inference for Einsum equation: %s", equation)
                    
                    # Map indices to their dimensions
                    dim_sizes = {}
                    
                    # Process each input tensor's subscripts
                    for idx, (subscript, shape) in enumerate(zip(input_subscripts, input_shapes)):
                        if len(subscript) != len(shape):
                            self.logger.warning("Mismatch between subscript '%s' length (%d) and shape %s length (%d)",
                                           subscript, len(subscript), shape, len(shape))
                            continue
                        
                        # Map each dimension label to its size
                        for label, size in zip(subscript, shape):
                            if label in dim_sizes and dim_sizes[label] != size and dim_sizes[label] != -1 and size != -1:
                                self.logger.warning("Inconsistent size for dim '%s': %d vs %d",
                                               label, dim_sizes[label], size)
                            # Prefer non-negative values
                            if label not in dim_sizes or (size > 0 and dim_sizes[label] == -1):
                                dim_sizes[label] = size
                    
                    # Construct output shape using the output subscript
                    output_shape = []
                    for label in output_part:
                        if label in dim_sizes:
                            output_shape.append(dim_sizes[label])
                        else:
                            self.logger.error("Unknown dimension label '%s' in output", label)
                            output_shape.append(-1)  # Unknown size
                    
                    return output_shape
                    
            except Exception as e:
                self.logger.error("Error parsing Einsum equation: %s", str(e))
                self.logger.debug("Stack trace: %s", traceback.format_exc())
                return input_shapes[0]  # Fallback to first input shape
                
        except Exception as e:
            self.logger.error("Einsum error in %s: %s", node.name, str(e))
            return None
    
    def _handle_where(self, node: NodeProto, input_shapes: List[List[int]]) -> Optional[List[int]]:
        """
        Handle Where operation.
        
        Where selects elements from X or Y based on condition.
        Output shape follows ONNX multidirectional broadcasting rules.
        """
        try:
            # Get input shapes, handling None or empty shapes
            condition_shape = input_shapes[0] if len(input_shapes) > 0 and input_shapes[0] else []
            x_shape = input_shapes[1] if len(input_shapes) > 1 and input_shapes[1] else []
            y_shape = input_shapes[2] if len(input_shapes) > 2 and input_shapes[2] else []
            
            # Debug the exact shapes we're working with
            self.logger.debug("Where raw inputs: condition=%s, x=%s, y=%s", 
                          condition_shape, x_shape, y_shape)
            
            # For empty shapes, treat them as scalar [1]
            # This is crucial for ONNX broadcasting with empty tensors
            if not condition_shape:
                condition_shape = [1]
            if not x_shape:
                x_shape = [1]
            if not y_shape:
                y_shape = [1]
            
            # Find max rank among all shapes
            max_rank = max(len(condition_shape), len(x_shape), len(y_shape))
            
            # Pad all shapes to the max rank by prepending 1s
            padded_cond = [1] * (max_rank - len(condition_shape)) + list(condition_shape)
            padded_x = [1] * (max_rank - len(x_shape)) + list(x_shape)
            padded_y = [1] * (max_rank - len(y_shape)) + list(y_shape)
            
            # Apply multidirectional broadcasting rules dimension by dimension
            output_shape = []
            for i in range(max_rank):
                # Get dimensions at this position from all inputs
                dims = [padded_cond[i], padded_x[i], padded_y[i]]
                
                # Check if dimensions are compatible for broadcasting
                max_dim = max(dims)
                if any(d != 1 and d != max_dim and d != -1 for d in dims):
                    self.logger.error("Cannot broadcast dimensions %s in Where %s", dims, node.name)
                    return None
                
                # If any dimension is unknown (-1), result is unknown
                if -1 in dims:
                    output_shape.append(-1)
                else:
                    output_shape.append(max_dim)
            
            self.logger.debug("Where %s: condition %s, x %s, y %s -> %s", 
                           node.name, condition_shape, x_shape, y_shape, output_shape)
            return output_shape
            
        except Exception as e:
            self.logger.error("Where error in %s: %s", node.name, str(e))
            return None
