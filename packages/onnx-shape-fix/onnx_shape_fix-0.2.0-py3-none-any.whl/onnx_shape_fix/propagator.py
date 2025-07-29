import onnx
from typing import Dict, List, Optional, Any
import numpy as np
import traceback
from onnx import numpy_helper
from onnx import TensorProto, helper

from onnx_shape_fix.utils.logger import Logger
from onnx_shape_fix.handlers import get_handler_for_op
from onnx_shape_fix.batch.tracker import BatchDimensionTracker
from onnx_shape_fix.batch.remover import BatchDimensionRemover
from onnx_shape_fix.utils.onnx_shape_infer import get_inferred_shapes


class ShapePropagator:

    def __init__(self, 
                 model, 
                 input_shapes: Dict[str, List[int]], 
                 verbose: bool = False,
                 remove_batch: bool = False,
                 input_batch_dim: int = 0,
                 continue_on_error: bool = False):

        if isinstance(model, str) or hasattr(model, '__fspath__'):
            # Load from file path
            self.model = onnx.load(model)
        else:
            # Assume it's a ModelProto
            self.model = model

        self.shape_dict = {}  # Stores tensor shapes
        self.handlers = {}
        self.input_shapes = input_shapes
        self.input_batch_dim = input_batch_dim
        self.verbose = verbose
        self.continue_on_error = continue_on_error
        self.logger = Logger(verbose=verbose)
        self.errors = []
        self.remove_batch = remove_batch  # Store this for later use

        self._validate_input_shapes()        
        self.inferred_shapes = get_inferred_shapes(self.model, verbose=self.verbose)

        # Initialize batch tracker if remove_batch is True
        self.batch_tracker = BatchDimensionTracker(verbose=self.verbose) if remove_batch else None
        if self.batch_tracker:
            self.batch_tracker.initialize(self.model, self.input_batch_dim)
            self.logger.info(f"🎛️ Batch dimension tracking enabled with batch at dim {self.input_batch_dim}")
        
    def _validate_input_shapes(self) -> None:
        """Validate input shapes against model expectations."""
        model_inputs = {inp.name: inp for inp in self.model.graph.input}
        
        for name, shape in self.input_shapes.items():
            if name not in model_inputs:
                raise ValueError(f"Input '{name}' not found in model inputs")
            
            # Retrieve the expected type for the input
            expected_type = model_inputs[name].type.tensor_type
            if not expected_type.HasField("shape"):
                self.logger.warning("Input '%s' has no shape info", name)
                continue

            # Extract expected dimensions from the model
            expected_dims = []
            for dim in expected_type.shape.dim:
                if dim.HasField("dim_value"):
                    expected_dims.append(dim.dim_value)
                elif dim.HasField("dim_param"):
                    expected_dims.append(dim.dim_param) # Symbolic dimension
                else:
                    expected_dims.append(None) # Unknown dimension

            # Validate rank (number of dimensions)
            if len(shape) != len(expected_dims):
                self.logger.warning(
                    "Input '%s' rank mismatch: Expected %d, got %d",
                    name, len(expected_dims), len(shape)
                )

            for i, (exp_dim, act_dim) in enumerate(zip(expected_dims, shape)):
                if isinstance(exp_dim, str):
                    self.logger.info("Symbolic dim '%s' at %s[%d]", exp_dim, name, i)
                elif exp_dim is not None and exp_dim != act_dim:
                    self.logger.warning(
                        "Dim %d mismatch for %s: Expected %s, got %d",
                        i, name, exp_dim, act_dim
                    )          

    def propagate_shapes(self) -> None:
        """Propagate shapes through the ONNX model graph."""
        try:
            # Initialize shape dictionary with input shapes
            self.logger.info("=" * 80)
            self.logger.info("📥 MODEL INPUTS")
            self.logger.info("-" * 80)
            for name, shape in self.input_shapes.items():
                self.shape_dict[name] = shape
                # Show batch dimension if available
                if self.batch_tracker:
                    batch_dim = self.batch_tracker.get_batch_dim(name)
                    if batch_dim is not None:
                        batch_remover = BatchDimensionRemover(verbose=False)
                        shape_without_batch = batch_remover.remove_batch_dimensions(shape, batch_dim)
                        self.logger.info(f"  • {name:<20} {str(shape):<20} (batch@{batch_dim} → {shape_without_batch})")
                    else:
                        self.logger.info(f"  • {name:<20} {str(shape):<20} (no batch)")
                else:
                    self.logger.info(f"  • {name:<20} {str(shape)}")
            
            # Process initializers (only in debug mode)
            for initializer in self.model.graph.initializer:
                shape = list(initializer.dims)
                self.shape_dict[initializer.name] = shape
            
            # Set up node counting for progress tracking
            self.total_nodes = len(self.model.graph.node)
            self.current_node_idx = 0
            
            self.logger.info("=" * 80)
            self.logger.info(f"⏳ PROCESSING {self.total_nodes} NODES")
            self.logger.info("=" * 80)
            
            # Process nodes in topological order
            for node in self.model.graph.node:
                self.current_node_idx += 1
                
                # Skip nodes with no outputs
                if not node.output:
                    continue
                    
                # Process node
                handler = self._get_handler_for_node(node)
                if handler:
                    input_shapes = self._get_input_shapes(node)
                    self._process_node_with_handler(node, input_shapes, handler)
            
            # Summarize results
            self.logger.info("=" * 80)
            self.logger.info(f"✅ SHAPE PROPAGATION COMPLETED")
            self.logger.info("-" * 80)
            self.logger.info(f"  • Processed {self.current_node_idx}/{self.total_nodes} nodes")
            
            if self.errors:
                self.logger.warning(f"  • ⚠️ {len(self.errors)} errors encountered")
            
            # Check output shapes
            missing_outputs = []
            for output in self.model.graph.output:
                if output.name not in self.shape_dict:
                    missing_outputs.append(output.name)
            
            if missing_outputs:
                self.logger.error(f"  • ❌ Missing shapes for {len(missing_outputs)} outputs")
            else:
                self.logger.info(f"  • ✅ All model outputs have shapes")
            
            self.logger.info("=" * 80)
            
        except Exception as e:
            self.logger.error(f"❌ Error during shape propagation: {str(e)}")
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    def propagate(self) -> 'ShapePropagator':
        """Method chaining interface for propagation."""
        self.propagate_shapes()
        return self

    def _initialize_shape_dict(self) -> None:
        """
        Initialize the shape dictionary with input shapes.
        """
        for name, shape in self.input_shapes.items():
            self.shape_dict[name] = shape
            self.logger.info("Input '%s' shape: %s", name, shape)

    def _process_initializers(self) -> None:
        """
        Process initializers (constants) and add their shapes to the shape dictionary.
        """
        for initializer in self.model.graph.initializer:
            shape = list(initializer.dims)
            self.shape_dict[initializer.name] = shape
            # self.logger.debug("Initializer '%s' shape: %s", initializer.name, shape) #slow
        self.logger.debug("processed initializers Done")

    def _process_nodes(self) -> None:
        """Process all nodes in topological order."""
        for idx, node in enumerate(self.model.graph.node):
            try:
                self.logger.info(f"⭐ ======== Processing node {idx+1}/{len(self.model.graph.node)}: '{node.name}' ('{node.op_type}') ======== ⭐")
                self._process_node(node)
            except Exception as e:
                self.logger.error(f"Failed to process node '{node.name}' ('{node.op_type}'): {str(e)}")
                self.logger.debug(f"Stack trace:\n{traceback.format_exc()}")
                if not self.continue_on_error:
                    raise

    def _process_node(self, node) -> None:
        """Process individual node with error handling."""

        # Step 1: Skip nodes with no outputs
        if not node.output:
            self.logger.debug("Skipping node '%s' (%s) with no outputs", node.name, node.op_type)
            return  
        
        try:    
            # Step 2: Retrieve input shapes for this node
            input_shapes = self._get_input_shapes_for_node(node)
            
            # Step 3: Get the appropriate handler for this operation type
            handler = get_handler_for_op(node.op_type, self.verbose)
            
            if handler:
                self.logger.info("Processing node '%s' (%s) with handler: %s",
                                node.name, node.op_type, handler.__class__.__name__)
                # Step 4: Process single-output and multi-output nodes
                self._process_node_with_handler(node, input_shapes, handler)
            else:
                self.logger.error("No handler for op_type: %s", node.op_type)

            # Step 5: Compare shapes with inferred shapes
            self._compare_with_inferred_shapes(node)
        
        except Exception as e:
            self.logger.error("Error processing node '%s' (%s): %s", 
                            node.name, node.op_type, str(e))
            self.logger.debug('Stack trace:\n%s', traceback.format_exc())
            if not self.continue_on_error:
                raise    
    
    def _get_input_shapes_for_node(self, node) -> List[Optional[List[int]]]:
        """
        Retrieve input shapes for a given node.
        
        Args:
            node: The ONNX node to process.
        
        Returns:
            List of input shapes for the node.
        """
        # Early exit if there are no inputs
        if not node.input:
            return []
    
        input_shapes = []
        missing_shapes = []  # To aggregate missing shapes for logging
    
        for i, input_name in enumerate(node.input):
            if not input_name:  # Skip empty input names
                input_shapes.append(None)
                self.logger.warning("Node '%s' (%s) has an empty input name", node.name, node.op_type)
                continue
            
            # Look up shape in our dictionary
            shape = self.shape_dict.get(input_name)
            if shape is None:
                missing_shapes.append(input_name)
            input_shapes.append(shape)
            self.logger.debug(f"    Input {i}: {input_name}: {shape}")
    
        # Log aggregated missing shapes if any
        if missing_shapes:
            self.logger.warning(
                f"Inputs {missing_shapes} for node '{node.name}' ('{node.op_type}') have no known shapes"
            )
        
        # self.logger.debug(f"Input shapes for node '{node.name}' ('{node.op_type}'): {input_shapes}")
        return input_shapes

    def _process_node_with_handler(self, node, input_shapes, handler) -> None:
        """Process a node using its associated handler."""
        try:
            # Check if node is important (an output node or if verbose mode is on)
            is_important = any(output in self.model.graph.output for output in node.output)
            
            # Only log detailed node information if important or in verbose mode
            if is_important or self.verbose:
                # Node header with clear separation
                self.logger.info("-" * 80)
                self.logger.info(f"📊 NODE {self.current_node_idx}/{self.total_nodes}: {node.name or 'unnamed'} ({node.op_type})")
                
                # Display inputs in a clear, organized way
                if node.input:
                    self.logger.info("  📥 INPUTS:")
                    for i, (name, shape) in enumerate(zip(node.input, input_shapes)):
                        if name and shape is not None:
                            # Show batch dimension if available
                            if self.batch_tracker:
                                batch_dim = self.batch_tracker.get_batch_dim(name)
                                if batch_dim is not None:
                                    batch_remover = BatchDimensionRemover(verbose=False)
                                    shape_without_batch = batch_remover.remove_batch_dimensions(shape, batch_dim)
                                    self.logger.info(f"    • {name:<30} {str(shape):<20} (batch@{batch_dim} → {shape_without_batch})")
                                else:
                                    self.logger.info(f"    • {name:<30} {str(shape):<20} (no batch)")
                            else:
                                self.logger.info(f"    • {name:<30} {str(shape)}")
            
            # Apply the handler to compute output shapes
            output_shapes = handler.handle_node(node, input_shapes, self)
            
            if output_shapes is None or not isinstance(output_shapes, list):
                raise ValueError(f"Invalid handler output for '{node.name}' ('{node.op_type}')")
            
            # Handle batch dimension tracking if enabled
            if self.batch_tracker:
                self.batch_tracker.update_for_node(node, input_shapes, output_shapes)
            
            # Display outputs in a clear, organized way
            if is_important or self.verbose:
                self.logger.info("  📤 OUTPUTS:")
                for i, (output_name, output_shape) in enumerate(zip(node.output, output_shapes)):
                    if output_shape is not None:
                        self.shape_dict[output_name] = output_shape
                        
                        # Show batch dimension if available
                        if self.batch_tracker:
                            batch_dim = self.batch_tracker.get_batch_dim(output_name)
                            if batch_dim is not None:
                                batch_remover = BatchDimensionRemover(verbose=False)
                                shape_without_batch = batch_remover.remove_batch_dimensions(output_shape, batch_dim)
                                self.logger.info(f"    • {output_name:<30} {str(output_shape):<20} (batch@{batch_dim} → {shape_without_batch})")
                                
                                # Compare with inferred shape
                                inferred = self.inferred_shapes.get(output_name)
                                if inferred:
                                    if inferred == output_shape:
                                        self.logger.info(f"      ✓ Matches inferred shape: {inferred}")
                                    else:
                                        self.logger.warning(f"      ⚠️ Mismatch with inferred shape: {inferred}")
                            else:
                                self.logger.info(f"    • {output_name:<30} {str(output_shape):<20} (no batch)")
                                
                                # Compare with inferred shape
                                inferred = self.inferred_shapes.get(output_name)
                                if inferred:
                                    if inferred == output_shape:
                                        self.logger.info(f"      ✓ Matches inferred shape: {inferred}")
                                    else:
                                        self.logger.warning(f"      ⚠️ Mismatch with inferred shape: {inferred}")
                        else:
                            self.logger.info(f"    • {output_name:<30} {str(output_shape)}")
                            
                            # Compare with inferred shape
                            inferred = self.inferred_shapes.get(output_name)
                            if inferred:
                                if inferred == output_shape:
                                    self.logger.info(f"      ✓ Matches inferred shape: {inferred}")
                                else:
                                    self.logger.warning(f"      ⚠️ Mismatch with inferred shape: {inferred}")
        
        except Exception as e:
            self.logger.error(f"❌ Error in node '{node.name}' ({node.op_type}): {str(e)}")
            self.errors.append((node, str(e)))
            
            if not self.continue_on_error:
                raise

    def _compare_with_inferred_shapes(self, node) -> None:
        """
        Validate propagated shapes against ONNX shape inference results.
        
        Handles unknown dimensions (-1) intelligently:
        - If inferred dimension is -1, our propagated value is considered valid
        - Only flags discrepancies for specific dimension values that don't match
        """
        for out_name in node.output:
            propagated = self.shape_dict.get(out_name)
            inferred = self.inferred_shapes.get(out_name)
            
            if not propagated or not inferred:
                continue
            if len(propagated) != len(inferred):
                self.logger.warning(f" ⚠️ WRONG: Rank mismatch in {out_name}: Propagated: {propagated}, Inferred: {inferred}")
                continue
            
            # Compare dimensions one by one
            has_discrepancy = False
            discrepancy_details = []
            
            for i, (prop_dim, inf_dim) in enumerate(zip(propagated, inferred)):
                # If inferred is -1 (unknown), our propagated value is considered correct
                if inf_dim == -1:
                    continue
                # Otherwise, dimensions should match
                elif prop_dim != inf_dim:
                    has_discrepancy = True
                    discrepancy_details.append(f"dim[{i}]: {prop_dim} vs {inf_dim}")
            
            if has_discrepancy:
                self.logger.warning(f" ⚠️ WRONG: Shape discrepancy in {out_name}: Propagated: {propagated}, Inferred: {inferred}")
                raise ValueError(f"Specific discrepancies: {', '.join(discrepancy_details)}")
            else:
                # If all specific dimensions match (ignoring -1s)
                if -1 in inferred:
                    self.logger.debug(f" ☑️ VALID: Shape for {out_name}: Propagated: {propagated}, Inferred: {inferred} (with unknown dims)")
                else:
                    self.logger.debug(f" ✅ EXACT: Shape for {out_name}: Propagated: {propagated}, Inferred: {inferred}")
                
    def _check_batch_dim_consistency(self, batch_dims: Dict[str, Optional[int]]) -> Dict:
        """
        Check batch dimension consistency across tensors.
        
        This checks if the *value* of the batch dimension (e.g., 1) is consistent,
        regardless of which position it appears in (0, 1, 2, etc.).
        
        Args:
            batch_dims: Dictionary mapping tensor names to their batch dimension indices
            
        Returns:
            Dictionary with consistency information
        """
        result = {
            "consistent": True,
            "issues": [],
            "batch_values": {},
            "batch_dims": {}
        }
        
        # Group tensors by batch dimension position
        grouped_by_dim = {}
        for tensor, dim in batch_dims.items():
            if dim is not None:
                if dim not in grouped_by_dim:
                    grouped_by_dim[dim] = []
                grouped_by_dim[dim].append(tensor)
        
        # Collect batch values for each tensor
        tensor_batch_values = {}
        for tensor, dim in batch_dims.items():
            if dim is not None and tensor in self.shape_dict:
                shape = self.shape_dict[tensor]
                if shape and 0 <= dim < len(shape):
                    value = shape[dim]
                    tensor_batch_values[tensor] = value
                    
                    # Group tensors by batch value
                    if value not in result["batch_values"]:
                        result["batch_values"][value] = []
                    result["batch_values"][value].append(tensor)
        
        # Check for inconsistent batch values
        batch_values = set(result["batch_values"].keys())
        if len(batch_values) > 1:
            result["consistent"] = False
            batch_values_str = ", ".join([str(v) for v in batch_values])
            result["issues"].append(f"Inconsistent batch values found: {batch_values_str}")
        
        # Add batch dimension grouping for reference
        for dim, tensors in grouped_by_dim.items():
            result["batch_dims"][dim] = tensors
        
        # Log consistency information
        if self.verbose:
            self.logger.info("🔍 Batch Dimension Value Verification Report:")
            if result["consistent"]:
                self.logger.info("  ✅ Batch dimension values are consistent")
            else:
                self.logger.warning("  ⚠️ Batch dimension values are inconsistent")
                for issue in result["issues"]:
                    self.logger.warning(f"    • {issue}")
            
            for batch_value, tensor_names in result["batch_values"].items():
                count = len(tensor_names)
                self.logger.info(f"  📊 Batch value {batch_value}: {count} tensors")
        
        return result

    def update_model_shapes(self) -> None:
        """Update shapes in the model's ValueInfo and fix unknown dimensions"""
        from onnx import TensorProto, helper
        
        # Fix unknown dimensions in shape dictionary first
        self._fix_unknown_dimensions()
        
        # Update input shapes
        for input_info in self.model.graph.input:
            self._update_tensor_shape_info(input_info)
            
        # Update output shapes
        for output_info in self.model.graph.output:
            self._update_tensor_shape_info(output_info)
            
        # Update intermediate value shapes
        for value_info in self.model.graph.value_info:
            self._update_tensor_shape_info(value_info)

    def _fix_unknown_dimensions(self):
        """Fix unknown string dimensions in shape dictionary"""
        # First pass: collect all dimension names and their values
        dim_values = {}
        for tensor_name, shape in self.shape_dict.items():
            if not shape:
                continue
            for i, dim in enumerate(shape):
                if isinstance(dim, str) and dim.startswith("unk_"):
                    if dim not in dim_values:
                        dim_values[dim] = set()
                    # Try to find a concrete value for this dimension from other tensors
                    for other_name, other_shape in self.shape_dict.items():
                        if (other_shape and i < len(other_shape) and 
                            isinstance(other_shape[i], int) and
                            len(shape) == len(other_shape)):
                            dim_values[dim].add(other_shape[i])
        
        # Second pass: replace unknown dimensions with concrete values if possible
        for tensor_name, shape in self.shape_dict.items():
            if not shape:
                continue
            for i, dim in enumerate(shape):
                if isinstance(dim, str) and dim.startswith("unk_"):
                    if dim in dim_values and len(dim_values[dim]) == 1:
                        # If we have a unique concrete value, use it
                        shape[i] = next(iter(dim_values[dim]))
                        if self.verbose:
                            self.logger.debug(f"Fixed unknown dimension {dim} → {shape[i]} in {tensor_name}")

    def _update_tensor_shape_info(self, value_info):
        """Update a tensor's shape information in the model"""
        tensor_name = value_info.name
        if tensor_name not in self.shape_dict:
            return
        
        shape = self.shape_dict[tensor_name]
        if not shape:
            return
        
        try:
            # Keep original data type
            elem_type = value_info.type.tensor_type.elem_type
            
            # Create a new TensorTypeProto with updated shape
            new_shape = []
            for dim in shape:
                if isinstance(dim, int):
                    new_shape.append(dim)
                elif isinstance(dim, str):
                    # Handle string dimensions by adding them as parameters
                    new_shape.append(dim)
                else:
                    # Handle None or other types
                    new_shape.append("?")
            
            new_type = helper.make_tensor_type_proto(elem_type, new_shape)
            value_info.type.tensor_type.CopyFrom(new_type.tensor_type)
        except Exception as e:
            self.logger.error(f"Error updating shape for {tensor_name}: {str(e)}")
            self.logger.debug(traceback.format_exc())

    def save_model_with_shapes(self, output_path: str) -> None:
        """Save the model with corrected shapes."""
        import os
        
        self.logger.info("=" * 80)
        self.logger.info("💾 SAVING MODEL WITH SHAPES")
        self.logger.info("-" * 80)

        try:
            # First update all shapes in the model
            self.update_model_shapes()
            
            # Apply the batch dimension remover if needed
            if self.remove_batch and self.batch_tracker:
                try:
                    # Get all batch dimensions tracked
                    batch_dims = self.batch_tracker.get_all_batch_dims()
                    
                    # Debug information about batch dimensions
                    self.logger.info(f"🔄 Removing batch dimensions from {len(batch_dims)} tensors")
                    
                    dim_counts = {}
                    for tensor, dim in batch_dims.items():
                        if dim is not None:
                            dim_counts[dim] = dim_counts.get(dim, 0) + 1
                    
                    # Only log the counts, not individual tensors
                    if dim_counts:
                        self.logger.info("Batch dimension distribution:")
                        for dim, count in sorted(dim_counts.items()):
                            self.logger.info(f"  • Position {dim}: {count} tensors")
                    
                    # Check for batch dimension value consistency
                    consistency = self._check_batch_dim_consistency(batch_dims)
                    if not consistency.get("consistent", True):
                        self.logger.warning("⚠️ Inconsistent batch values detected")
                        for issue in consistency.get("issues", []):
                            self.logger.warning(f"  • {issue}")
                    
                    # Apply the batch dimension remover
                    from onnx_shape_fix.batch.remover import BatchDimensionRemover
                    remover = BatchDimensionRemover(
                        model=self.model,
                        batch_dims=batch_dims,
                        input_shapes=self.input_shapes,
                        verbose=self.verbose
                    )
                    
                    # Give remover access to shape_dict and propagator for better logging
                    remover.propagator = self
                    
                    # Apply the remover using the tracked batch dimensions
                    remover.apply_to_model()
                    self.logger.info("✅ Batch dimensions removed")
                except Exception as e:
                    import traceback
                    self.logger.error(f"❌ Batch dimension removal failed: {str(e)}")
                    self.logger.debug(traceback.format_exc())
            
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            
            # Save the model
            onnx.save(self.model, output_path)
            self.logger.info(f"✅ Model saved to {output_path}")
            self.logger.info("=" * 80)
        except Exception as e:
            import traceback
            self.logger.error(f"❌ Error saving model: {str(e)}")
            self.logger.debug(traceback.format_exc())
            raise

    def _update_tensor_shape(self, tensor, shape: List[int]) -> None:
        """Helper to update tensor shape in proto."""
        tensor.type.tensor_type.shape.ClearField("dim")
        for dim in shape:
            new_dim = tensor.type.tensor_type.shape.dim.add()
            if dim != -1:
                new_dim.dim_value = dim
            else:
                new_dim.dim_param = '?'

    def _validate_outputs(self) -> None:
        """Verify all model outputs have shapes."""
        for out in self.model.graph.output:
            if out.name not in self.shape_dict:
                self.logger.warning("Missing shape for output %s", out.name)

    def _get_handler_for_node(self, node):
        """
        Get the appropriate handler for a node based on its operation type.
        
        Args:
            node: The ONNX node to process.
            
        Returns:
            A handler instance for the operation type or None if no handler exists.
        """
        try:
            handler = get_handler_for_op(node.op_type, self.verbose)
            
            if handler is None:
                raise ValueError (f"⚠️ No handler available for op_type: '{node.op_type}'")
                
            return handler
        except Exception as e:
            self.logger.error(f"❌ Error getting handler for {node.op_type}: {str(e)}")
            return None

    def _get_input_shapes(self, node):
        """
        Get input shapes for a node from the shape dictionary.
        
        Args:
            node: The ONNX node
            
        Returns:
            List of input shapes for the node
        """
        input_shapes = []
        for input_name in node.input:
            shape = self.shape_dict.get(input_name)
            input_shapes.append(shape)
        return input_shapes





'''
Steps:
    1. Load model
    2. Validate input shapes given by user
    3. Check batch tracking is enabled if user wants to remove batch dimension
    4. Initialize shape dictionary
    5. Process initializers
    6. Process nodes
        a. Skip nodes with no outputs
        b. Retrieve input shapes for this node
        c. Get the appropriate handler for this operation type
        d. Process single-output and multi-output nodes
        e. Compare shapes with inferred shapes
    7. Validate outputs
    8. Save model with updated shapes
'''