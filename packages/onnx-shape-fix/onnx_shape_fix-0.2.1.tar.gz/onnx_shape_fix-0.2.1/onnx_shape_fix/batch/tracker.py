from typing import Dict, List, Optional, Set, Any, Callable
import onnx
from onnx import NodeProto
from ..utils.logger import Logger
from .bn_tracker import tracker_registry

class BatchDimensionTracker:
    """
    Enhanced batch dimension tracker with improved op support and safety checks
    
    Features:
    - Full opset 15 support
    - Dynamic tracker dispatch
    - Shape inference integration
    - Better error handling
    - Constant/initializer tracking
    """
    
    def __init__(self, propagator=None, verbose=False):
        """Initialize batch dimension tracker.
        
        Args:
            propagator: Reference to the ShapePropagator instance
            verbose: Whether to enable verbose logging
        """
        self.batch_dims: Dict[str, Optional[int]] = {}
        self.constants: Set[str] = set()
        self.logger = Logger(verbose=verbose)
        self.verbose = verbose  # Store the verbose parameter
        self.propagator = propagator  # Store reference to propagator
        self._op_trackers = self._create_tracker_map()
        

    def _create_tracker_map(self) -> Dict[str, callable]:
        """Create tracker map with both specific and category-based trackers"""
        # Start with registered trackers from the trackers module
        trackers = {op_type: tracker for op_type, tracker in tracker_registry.items()}
        
        # Add category-based trackers
        trackers.update({
            'shape_preserving': self._track_shape_preserving,
            'default': self._track_default
        })
        
        self.logger.debug("Tracker map: %s", trackers)
        return trackers

    def initialize(self, model, initial_batch_dim: int) -> None:
        """
        Register model inputs and constants/initializers with their batch dimensions.
        - Assigns `initial_batch_dim` to all model inputs.
        - Identifies constants/initializers and sets their batch dimensions to `None`.
        """
        try:
            # Register batch dimensions for model inputs
            for input_tensor in model.graph.input:
                self.batch_dims[input_tensor.name] = initial_batch_dim
                self.logger.debug(f"Tracking dimension {initial_batch_dim} as batch dimension for input '{input_tensor.name}'")
            
            # Identify and register constants/initializers
            self.constants.update(init.name for init in model.graph.initializer)
            for node in model.graph.node:
                if node.op_type == 'Constant':
                    self.constants.update(node.output)
            
            # Set batch dimensions for constants to None
            for const_name in self.constants:
                self.batch_dims[const_name] = None
            
            self.logger.info(f"Initialized batch dimensions for model inputs = {initial_batch_dim} and constants/initializers = None")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize batch dimensions: {e}")

    def get_batch_dim(self, tensor_name: str) -> Optional[int]:
        """Get the batch dimension for a tensor, returns None if not tracked or not applicable."""
        # self.logger.debug("Getting batch dimension for tensor: %s", tensor_name)
        return self.batch_dims.get(tensor_name)

    def get_all_batch_dims(self) -> Dict[str, Optional[int]]:
        """Get all tracked batch dimensions"""
        self.logger.debug("Getting all tracked batch dimensions")
        return self.batch_dims
    
    def update_for_node(self, node: NodeProto, 
                       input_shapes: Optional[List[List[int]]] = None,
                       output_shapes: Optional[List[List[int]]] = None) -> None:
        """Update batch dimensions for a node."""
        if not node.output:
            return

        try:
            # Apply the appropriate tracker
            tracker = self._get_tracker(node.op_type)
            
            # Apply specific tracker from registry
            if node.op_type in tracker_registry:
                tracker_registry[node.op_type](self, node, input_shapes, output_shape=output_shapes[0] if output_shapes else None)
            # Apply general shape-preserving tracker
            elif tracker == self._track_shape_preserving:
                tracker(node, input_shapes, output_shapes)
            # Apply general value-preserving tracker  
            elif tracker == self._track_value_preserving:
                tracker(node)
            # Apply default tracker
            else:
                tracker(node, input_shapes, output_shapes)
            
            # Check for batch dimension consistency in this node's outputs
            self._check_batch_dim_consistency(node, output_shapes)
            
            # Log batch dimension updates for debugging
            if self.verbose and node.output:
                # Check what batch dimensions were set
                for output_name in node.output:
                    if output_name:
                        batch_dim = self.get_batch_dim(output_name)
                        if batch_dim is not None:
                            self.logger.debug(f"  ✓ Set batch dimension for {output_name} to {batch_dim}")
                        else:
                            self.logger.debug(f"  ⚠️ No batch dimension set for {output_name}")
            
        except Exception as e:
            # Set batch dimensions to None on error and log the exception
            self._set_outputs(node, None)
            self.logger.error(f"Error tracking batch dimension for {node.op_type}: {str(e)}")

    def _get_tracker(self, op_type: str) -> callable:
        """Get appropriate tracker for operation type"""
        if op_type in self._op_trackers:
            # self.logger.debug("Using specific tracker for op_type: %s", op_type)
            return self._op_trackers[op_type]
        if op_type in self._shape_preserving_ops():
            # self.logger.debug("Using shape preserving tracker for op_type: %s", op_type)
            return self._op_trackers['shape_preserving']
        
        self.logger.debug("No batch dimension tracker found for op_type: %s using default tracker", op_type)
        return self._op_trackers['default']

    def _track_error(self, node: NodeProto, error: Exception) -> None:
        """track errors during processing with warnings"""
        self.logger.error("Error processing node '%s' (%s): %s", node.name, node.op_type, str(error))
        self._set_outputs(node, None)

    def _set_outputs(self, node: NodeProto, value: Optional[int]) -> None:
        """Safely set output dimensions"""
        for out in node.output:
            self.batch_dims[out] = value

    @staticmethod
    def _get_attribute(node: NodeProto, name: str, default=None) -> Any:
        """Safe attribute extraction helper"""
        return next((attr for attr in node.attribute if attr.name == name), default)

    def _shape_preserving_ops(self) -> List[str]:
        """
        Return a list of operations that preserve tensor shape.
        These operations maintain batch dimension location.
        """
        return [
            'Cast', 'Relu', 'LeakyRelu', 'Sigmoid', 'Tanh', 'Softplus',
            'Neg', 'Abs', 'Exp', 'Log', 'Sin', 'Cos', 'Tan',
            'Asin', 'Acos', 'Atan', 'Sinh', 'Cosh', 'Asinh', 'Acosh',
            'Atanh', 'Erf', 'Not', 'Identity', 'Dropout', 'Reciprocal',
            'Floor', 'Ceil', 'Clip', 'Round', 'Hardmax', 'HardSigmoid',
            'Selu', 'Shrink', 'ThresholdedRelu', 'Softsign',
            'InstanceNormalization', 'LayerNormalization', 'GroupNormalization',
            'BatchNormalization',  # These normalization ops keep dimensions
        ]

    def _track_default(self, node: NodeProto, input_shapes: List[List[int]], output_shape: List[int]) -> None:
        """Default tracker for operations without specific logic."""
        if not node.input or not node.output:
            return

        # Assume first input's batch dimension propagates
        input_bdim = None
        for input_name in node.input:
            input_bdim = self.get_batch_dim(input_name)
            if input_bdim is not None:
                break

        for output_name in node.output:
            self.batch_dims[output_name] = input_bdim

    def _track_shape_preserving(self, node: NodeProto, 
                              input_shapes: Optional[List[List[int]]] = None, 
                              output_shapes: Optional[List[List[int]]] = None) -> None:
        """
        Track operations that preserve tensor shape, like elementwise ops.
        For these operations, the batch dimension location stays the same.
        """
        if not node.input:
            self._set_outputs(node, None)
            return
        
        # Get batch dimension from first input
        first_input = node.input[0]
        if not first_input:
            self._set_outputs(node, None)
            return
        
        input_bdim = self.get_batch_dim(first_input)
        
        # Shape-preserving operations maintain the batch dimension
        self._set_outputs(node, input_bdim)
        
        if self.verbose:
            self.logger.debug(f"  🔄 {node.op_type}: batch dim preserved at {input_bdim}")

    def _track_value_preserving(self, node: NodeProto) -> None:
        """Placeholder for value-preserving operations"""
        # Implement value-preserving operations tracking logic here
        pass

    def _check_batch_dim_consistency(self, node: NodeProto, output_shapes: Optional[List[List[int]]] = None) -> None:
        """Check for batch dimension consistency in the node's outputs."""
        # Only proceed if we have a valid propagator with input shapes
        if not hasattr(self, 'propagator') or self.propagator is None or not hasattr(self.propagator, 'input_shapes'):
            return
        
        # Get batch dimensions from model inputs (these are our reference batch dimensions)
        model_input_batch_dims = set()
        for name in self.propagator.input_shapes.keys():
            batch_dim = self.get_batch_dim(name)
            if batch_dim is not None:
                model_input_batch_dims.add(batch_dim)
        
        # If we have no reference batch dimensions, we can't check consistency
        if not model_input_batch_dims:
            return
        
        # Check batch dimensions in this node's outputs
        for output_name in node.output:
            if not output_name:
                continue
            
            output_batch_dim = self.get_batch_dim(output_name)
            if output_batch_dim is not None and output_batch_dim not in model_input_batch_dims:
                # This output has a batch dimension that doesn't match any input
                # Generate a warning but don't change it - it might be intentional
                if self.verbose:
                    self.logger.warning(f"  ⚠️ Output {output_name} has batch dimension {output_batch_dim} "
                                      f"which differs from model input batch dimensions {model_input_batch_dims}")


