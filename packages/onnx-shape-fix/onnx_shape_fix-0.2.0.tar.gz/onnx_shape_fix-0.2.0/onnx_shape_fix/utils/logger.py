import sys
import threading
from typing import Any, Optional, IO

class Logger:
    def __init__(self, verbose: bool = True, output_stream: Optional[IO] = None):
        """
        Initialize the logger.
        :param verbose: Show all logs when True (default), only errors and info when False
        :param output_stream: Output stream for logs (default: sys.stdout).
        """
        self.verbose = verbose
        self.output_stream = output_stream or sys.stdout
        self.lock = threading.Lock()

    def _log(self, level: str, msg: str, *args: Any) -> None:
        """
        Centralized logging method with thread safety and error handling.
        :param level: Log level label (DEBUG, INFO, etc.)
        :param msg: Log message format string
        :param args: Arguments to format the message string
        """
        try:
            formatted_msg = msg % args if args else msg
            with self.lock:
                print(f"[{level}]: {formatted_msg}", file=self.output_stream, flush=True)
        except Exception as e:
            self._critical(f"Failed to log message: {str(e)}")

    def _colored_log(self, level: str, color_code: str, msg: str, *args: Any) -> None:
        """
        Centralized colored logging method.
        :param level: Log level label (DEBUG, INFO, etc.)
        :param color_code: ANSI escape sequence for color
        :param msg: Log message format string
        :param args: Arguments to format the message string
        """
        try:
            formatted_msg = msg % args if args else msg
            with self.lock:
                # Use ANSI escape codes for coloring
                print(f"{color_code}[{level}]\033[0m: {formatted_msg}", 
                      file=self.output_stream, flush=True)
        except Exception as e:
            self._critical(f"Failed to log message: {str(e)}")

    def _critical(self, msg: str) -> None:
        """Log critical messages directly to stderr"""
        print(f"\033[91m[CRITICAL]\033[0m: {msg}", file=sys.stderr, flush=True)

    def debug(self, msg: str, *args: Any) -> None:
        """Log debug messages with blue DEBUG indicator (verbose mode only)"""
        if self.verbose:
            self._colored_log("DEBUG", "\033[94m", msg, *args)

    def info(self, msg: str, *args: Any) -> None:
        """Log info messages with green INFO indicator (always shown)"""
        self._colored_log("INFO", "\033[92m", msg, *args)

    def warning(self, msg: str, *args: Any) -> None:
        """Log warnings with yellow WARNING indicator (verbose mode only)"""
        if self.verbose:
            self._colored_log("WARNING", "\033[93m", msg, *args)

    def error(self, msg: str, *args: Any) -> None:
        """Log errors with red ERROR indicator (always shown)"""
        self._colored_log("ERROR", "\033[91m", msg, *args)

    def success(self, msg: str, *args: Any) -> None:
        """Log success messages with bright green SUCCESS indicator (verbose mode only)"""
        if self.verbose:
            self._colored_log("SUCCESS", "\033[92m", msg, *args)