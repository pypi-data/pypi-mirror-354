from typing import Dict, List, Optional
import onnx
from onnx.shape_inference import infer_shapes
from .logger import Logger

def get_inferred_shapes(model, verbose: bool = False) -> Dict[str, List[int]]:
    """
    Run shape inference on an ONNX model and return inferred shapes.
    
    Args:
        model: Loaded ONNX model.
    
    Returns:
        Dictionary mapping tensor names to their inferred shapes.
    """
    logger = Logger(verbose=verbose)
    inferred_shapes = {}
    
    try:
        # Perform ONNX shape inference
        inferred_model = infer_shapes(model)
        
        # Process each value_info in the inferred model
        for value_info in inferred_model.graph.value_info:
            name = value_info.name
            
            # Infer shape for the current tensor
            shape = _infer_tensor_shape(value_info, logger)
            
            # Validate and store the inferred shape
            if shape is not None:
                inferred_shapes[name] = shape
                # logger.debug(f"Inferred shape for '{name}': {shape}")   #slow TODO: make it print the number of elemenst with known shapes and other with dynamic shapes at the end
            else:
                logger.error(f"Failed to infer shape for '{name}'")
        
    except Exception as e:
        logger.error(f"Error during ONNX shape inference: {str(e)}")
        import traceback
        logger.debug(traceback.format_exc())
    
    return inferred_shapes

def _infer_tensor_shape(value_info, logger) -> Optional[List[int]]:
    """
    Infer the shape of a single tensor from its value_info.
    
    Args:
        value_info: ONNX ValueInfoProto containing tensor metadata.
    
    Returns:
        List of dimensions or None if inference fails.
    """
    try:
        shape = []
        for dim in value_info.type.tensor_type.shape.dim:
            if dim.HasField("dim_value"):
                shape.append(dim.dim_value)
            elif dim.HasField("dim_param"):
                # Log symbolic dimensions (e.g., batch size)
                # logger.warning(f"Symbolic dimension '{dim.dim_param}' found for tensor '{value_info.name}'") #slow and prinitng a lot
                shape.append(-1)  # Treat symbolic dimensions as unknown (-1)
            else:
                # Handle completely unknown dimensions
                logger.warning(f"Unknown dimension found for tensor '{value_info.name}'")
                shape.append(-1)
        return shape
    except Exception as e:
        logger.error(f"Error inferring shape for tensor '{value_info.name}': {str(e)}")
        return None