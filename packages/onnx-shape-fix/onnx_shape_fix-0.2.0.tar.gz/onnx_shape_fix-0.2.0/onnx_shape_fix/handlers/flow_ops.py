from typing import List, Optional, Any, Dict
from onnx import NodeProto, GraphProto
from .base_handler import BaseHandler
from ..utils.logger import Logger
from ..utils.constant_utils import get_constant_value
from onnx.helper import ValueInfoProto

class FlowControlHandler(BaseHandler):
    """Handler for flow control operations like If and Loop"""
    
    def __init__(self, verbose: bool = False):
        super().__init__(verbose)
        self.logger = Logger(verbose=verbose)
    
    def handle_node(self, node: NodeProto, input_shapes: List[List[int]], propagator: Any) -> List[List[int]]:
        if node.op_type == "If":
            return self._handle_if(node, input_shapes, propagator)
        else:
            self.logger.error(f"Unhandled flow control op: {node.op_type}")
            return [None] * len(node.output)

    def _evaluate_condition(self, cond_shape: List[int], cond_input: str, propagator: Any) -> bool:
        """Evaluate the condition of an If node by checking constant inputs"""
        if not cond_shape:
            self.logger.warning(f"Empty condition shape")
            return None
            
        if cond_shape != [1]:
            self.logger.warning(f"If condition shape {cond_shape} is not scalar")
            return None

        # Use get_constant_value from constant_utils
        constant_value = get_constant_value(cond_input, propagator)
        if constant_value is not None:
            # Ensure boolean result
            return bool(constant_value.item() if hasattr(constant_value, 'item') else constant_value)

        self.logger.warning("Could not determine If condition value statically")
        return None

    def _create_subgraph_propagator(self, graph: GraphProto, input_shapes: Dict[str, List[int]], 
                                  propagator: Any) -> Any:
        """Create a propagator for a subgraph with inherited context"""
        # Create new propagator with dummy model but proper input shapes
        from onnx import ModelProto
        from onnx_shape_fix.propagator import ShapePropagator
        
        # Create a new model with the subgraph
        model = ModelProto()
        model.graph.CopyFrom(graph)
        
        # Create a new propagator for the subgraph with the same batch tracking settings
        subprop = ShapePropagator(
            model=model,
            input_shapes=input_shapes,
            verbose=propagator.verbose,
            continue_on_error=True,
            remove_batch=propagator.remove_batch if hasattr(propagator, 'remove_batch') else False,
            input_batch_dim=propagator.input_batch_dim if hasattr(propagator, 'input_batch_dim') else 0
        )
        
        # Copy shape_dict from parent propagator to maintain context
        for name, shape in propagator.shape_dict.items():
            subprop.shape_dict[name] = shape
        
        # Copy constants if available
        if hasattr(propagator, 'constants') and hasattr(subprop, 'constants'):
            for name, value in propagator.constants.items():
                subprop.constants[name] = value
        
        # Copy batch dimensions if tracking is enabled
        if hasattr(propagator, 'batch_tracker') and hasattr(subprop, 'batch_tracker'):
            subprop.batch_tracker.batch_dims = propagator.batch_tracker.batch_dims.copy()
        
        return subprop

    def _prepare_subgraph_propagator(self, target_graph: GraphProto, input_shapes: Dict[str, List[int]], 
                                   node_inputs: List[str], propagator: Any) -> Any:
        """Create and prepare a propagator for a subgraph"""
        # Create a mapping of original inputs to their shapes
        subgraph_inputs = {}
        
        # Map each graph input to its corresponding shape from node inputs
        for i, graph_input in enumerate(target_graph.input):
            if i < len(node_inputs):
                input_name = node_inputs[i]
                if input_name in propagator.shape_dict:
                    subgraph_inputs[graph_input.name] = propagator.shape_dict[input_name]
        
        # Include all other available shapes
        subgraph_inputs.update(propagator.shape_dict)
        
        # Add original input shapes
        if hasattr(propagator, 'input_shapes'):
            subgraph_inputs.update(propagator.input_shapes)
        
        return subgraph_inputs

    def _handle_if(self, node: NodeProto, input_shapes: List[List[int]], propagator: Any) -> List[List[int]]:
        """Handle If operation with better error handling."""
        if not node.input:
            return [None] * len(node.output)
        
        # Get condition value if possible
        cond_input_name = node.input[0]
        cond_shape = input_shapes[0] if input_shapes else None
        cond_value = None
        
        try:
            cond_value = self._evaluate_condition(cond_shape, cond_input_name, propagator)
        except Exception as e:
            self.logger.warning(f"Could not evaluate If condition: {str(e)}")
        
        if cond_value is None:
            # If condition can't be determined statically, use the 'then' branch by default
            self.logger.warning("If condition could not be determined statically, using 'then' branch by default")
            cond_value = True
            
        # Find the appropriate branch to process based on condition
        then_branch = None
        else_branch = None
        for attr in node.attribute:
            if attr.name == "then_branch":
                then_branch = attr.g
            elif attr.name == "else_branch":
                else_branch = attr.g
                
        if then_branch is None or else_branch is None:
            self.logger.error("Missing required branch attribute in If node")
            return [None] * len(node.output)
            
        target_graph = then_branch if cond_value else else_branch
        branch_name = "then" if cond_value else "else"

        try:
            # Map inputs from parent graph to subgraph inputs
            subgraph_inputs = {}
            
            # Process inputs that are explicitly mapped to the subgraph
            for i, graph_input in enumerate(target_graph.input):
                if i < len(node.input) - 1:  # Skip condition input
                    node_input_idx = i + 1  # Adjust index to skip condition
                    if node_input_idx < len(node.input):
                        input_name = node.input[node_input_idx]
                        if input_name in propagator.shape_dict:
                            subgraph_inputs[graph_input.name] = propagator.shape_dict[input_name]
            
            # Create a model for the subgraph to enable proper propagation
            from onnx import ModelProto, helper
            model = ModelProto()
            model.graph.CopyFrom(target_graph)
            
            # Inherit opset from parent
            if hasattr(propagator.model, 'opset_import') and propagator.model.opset_import:
                model.opset_import.extend(propagator.model.opset_import)
            else:
                opset = model.opset_import.add()
                opset.version = 13
                opset.domain = ""

            # Create a subpropagator with proper error handling
            try:
                from copy import deepcopy
                
                # Use the same type of propagator for consistency
                subprop = type(propagator)(
                    model,
                    input_shapes=subgraph_inputs,
                    verbose=propagator.verbose,
                    continue_on_error=True  # Force continue on error for subgraphs
                )

                # Copy relevant state from parent propagator
                # Include shapes for any tensors that might be used from the parent graph
                for tensor_name, shape in propagator.shape_dict.items():
                    if tensor_name not in subprop.shape_dict:
                        subprop.shape_dict[tensor_name] = shape
                
                # Copy constants if available
                if hasattr(propagator, 'constants') and hasattr(subprop, 'constants'):
                    for name, value in propagator.constants.items():
                        subprop.constants[name] = value
                
                # Propagate shapes through subgraph
                result = subprop.propagate_shapes()
                
                # Debug what's in the result
                if self.verbose:
                    self.logger.debug(f"Subgraph result type: {type(result)}")
                    if result:
                        self.logger.debug(f"Subgraph result keys: {list(result.keys())}")
                
                # Get output shapes in correct order
                output_shapes = []
                for output in target_graph.output:
                    output_name = output.name
                    shape = None
                    
                    # First try to get it from the result
                    if result and output_name in result:
                        shape = result[output_name]
                    # Then try the subprop shape_dict
                    elif output_name in subprop.shape_dict:
                        shape = subprop.shape_dict[output_name]
                    
                    output_shapes.append(shape)
                    if self.verbose:
                        self.logger.debug(f"Subgraph output {output_name}: shape = {shape}")

                return output_shapes
                
            except Exception as e:
                self.logger.error(f"Error in subgraph propagator for {branch_name} branch: {str(e)}")
                import traceback
                self.logger.debug(f"Traceback: {traceback.format_exc()}")
                return [None] * len(node.output)

        except Exception as e:
            self.logger.error(f"Error processing {branch_name} branch: {str(e)}")
            import traceback
            self.logger.debug(f"Traceback: {traceback.format_exc()}")
            return [None] * len(node.output)
