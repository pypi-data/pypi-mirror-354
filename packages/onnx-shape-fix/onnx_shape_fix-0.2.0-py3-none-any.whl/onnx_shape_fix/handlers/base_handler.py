from abc import ABC, abstractmethod
from onnx import NodeProto
from typing import List, Optional, Dict, Any

class BaseHandler(ABC):
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
    
    @abstractmethod
    def handle_node(self, node: NodeProto, input_shapes: List[List[int]], propagator: Any = None) -> List[List[int]]:
        """
        Process an ONNX node and compute its output shapes.
        
        Args:
            node: The ONNX node to process
            input_shapes: List of input tensor shapes for this node
            propagator: The shape propagator instance (provides context and helper methods)
            
        Returns:
            A list of output shapes, one for each output of the node.
            Each shape is represented as a list of integers.
        """
        pass