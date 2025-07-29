#!/usr/bin/env python3
import argparse
import json
import os
import sys
from typing import Dict, List

from .propagator import ShapePropagator
from .utils.logger import Logger


def parse_input_shapes(shapes_str: str) -> Dict[str, List[int]]:
    """Parse input shapes from a string in format 'name:[dim1,dim2,...];name2:[dim1,dim2,...]'."""
    shapes = {}
    if not shapes_str:
        return shapes

    for shape_pair in shapes_str.split(';'):
        if ':' not in shape_pair:
            continue
        name, shape_str = shape_pair.split(':', 1)
        try:
            # Handle both [1,2,3] and 1,2,3 formats
            shape_str = shape_str.strip()
            if shape_str.startswith('[') and shape_str.endswith(']'):
                shape_str = shape_str[1:-1]
            shape = [int(dim.strip()) for dim in shape_str.split(',')]
            if any(dim < 0 for dim in shape):
                raise ValueError("Dimensions must be non-negative.")
            shapes[name.strip()] = shape
        except ValueError as e:
            Logger.warning(f"Could not parse shape '{shape_str}' for input '{name}': {e}. Skipping.")

    return shapes


def load_input_shapes(input_shapes_arg: str) -> Dict[str, List[int]]:
    """Load input shapes from a string or JSON file."""
    if not input_shapes_arg:
        Logger.error("No input shapes provided. Use --input-shapes to specify input shapes.")
        sys.exit(1)

    if os.path.isfile(input_shapes_arg):
        try:
            with open(input_shapes_arg, 'r') as f:
                input_shapes = json.load(f)
                # Convert keys to strings and values to lists in case JSON uses non-string keys
                return {str(k): list(v) for k, v in input_shapes.items()}
        except (json.JSONDecodeError, FileNotFoundError) as e:
            Logger.error(f"Error loading JSON shapes file: {e}")
            sys.exit(1)
    else:
        return parse_input_shapes(input_shapes_arg)


def validate_model_path(model_path: str) -> None:
    """Validate that the model file exists."""
    if not os.path.exists(model_path):
        Logger.error(f"Model file {model_path} does not exist")
        sys.exit(1)


def determine_output_path(model_path: str, output_path: str) -> str:
    """Determine the output path for the fixed model."""
    if not output_path:
        base, ext = os.path.splitext(model_path)
        return f"{base}_shape_fixed{ext}"
    return output_path


def propagate_and_save(propagator: ShapePropagator, output_path: str, remove_batch: bool) -> Dict[str, List[int]]:
    """Propagate shapes and save the fixed model."""
    try:
        shapes = propagator.propagate_shapes()
        Logger.info(f"Propagated shapes for {len(shapes)} tensors")

        propagator.save_model_with_shapes(output_path, remove_batch=remove_batch)
        Logger.success(f"Saved fixed model to {output_path}")
        return shapes
    except Exception as e:
        Logger.error(f"Error during shape propagation or saving: {str(e)}")
        if Logger.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def print_summary(input_shapes: Dict[str, List[int]], output_shapes: Dict[str, List[int]], propagated_shapes: Dict[str, List[int]]):
    """Print summaries of input, output, and propagated shapes."""
    summary_lines = []

    summary_lines.append("\nSummary of Model Input Shapes:")
    for name, shape in input_shapes.items():
        summary_lines.append(f"  {name}: {shape}")

    summary_lines.append("\nSummary of Model Output Shapes:")
    for name, shape in output_shapes.items():
        summary_lines.append(f"  {name}: {shape if shape else 'shape not propagated'}")

    summary_lines.append("\nAll Propagated Shapes:")
    for name, shape in sorted(propagated_shapes.items()):
        if name not in input_shapes and name not in output_shapes:
            summary_lines.append(f"  {name}: {shape}")

    return "\n".join(summary_lines)


def save_summary_to_file(summary: str, summary_file: str):
    """Save the summary to a file."""
    try:
        with open(summary_file, 'w') as f:
            f.write(summary)
        Logger.success(f"Summary saved to {summary_file}")
    except Exception as e:
        Logger.error(f"Failed to save summary to file: {str(e)}")
        sys.exit(1)


def setup_logger(log_file: str):
    """Set up logging to a file if log_file is provided."""
    if log_file:
        Logger.set_log_file(log_file)
        Logger.info(f"Logging to file: {log_file}")


def main():
    parser = argparse.ArgumentParser(description='ONNX Shape Fix - Fix shapes in ONNX models')
    parser.add_argument('model_path', help='Path to the ONNX model')
    parser.add_argument('--output', '-o', default=None, 
                        help='Output path for the fixed model. Defaults to model_path with _shape_fixed.onnx suffix.')
    parser.add_argument('--input-shapes', '-i', required=True, 
                        help='Input shapes as a string (e.g., "input1:[1,2,3];input2:[4,5,6]") or a JSON file path.')
    parser.add_argument('--remove-batch', '-r', action='store_true', 
                        help='Remove batch dimension from shapes.')
    parser.add_argument('--verbose', '-v', action='store_true', 
                        help='Enable verbose output.')
    parser.add_argument('--summary', '-s', default=None, 
                        help='Save summary to a file instead of printing to console.')
    parser.add_argument('--log', '-l', default=None, 
                        help='Save all logs to a file.')

    args = parser.parse_args()

    # Set up logger
    Logger.verbose = args.verbose
    setup_logger(args.log)

    # Validate inputs
    validate_model_path(args.model_path)
    output_path = determine_output_path(args.model_path, args.output)
    input_shapes = load_input_shapes(args.input_shapes)
    Logger.info(f"Using input shapes: {input_shapes}")

    # Initialize propagator
    try:
        propagator = ShapePropagator(
            args.model_path,
            input_shapes,
            verbose=args.verbose,
            track_batch=args.remove_batch
        )
    except Exception as e:
        Logger.error(f"Failed to initialize ShapePropagator: {str(e)}")
        if Logger.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

    # Propagate shapes and save the model
    shapes = propagate_and_save(propagator, output_path, args.remove_batch)
    output_shapes = {o.name: shapes.get(o.name) for o in propagator.model.graph.output}

    # Generate summary
    summary = print_summary(input_shapes, output_shapes, shapes)

    # Handle summary output
    if args.summary:
        save_summary_to_file(summary, args.summary)
    else:
        print(summary)


if __name__ == "__main__":
    main()