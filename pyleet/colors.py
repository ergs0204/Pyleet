"""
Color utilities for terminal output.
Provides cross-platform colored text support using ANSI escape codes.
"""

import sys
import os


class Colors:
    """ANSI color codes for terminal output."""
    # Reset
    RESET = '\033[0m'
    
    # Regular colors
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bold colors
    BOLD_RED = '\033[1;31m'
    BOLD_GREEN = '\033[1;32m'
    BOLD_YELLOW = '\033[1;33m'
    BOLD_BLUE = '\033[1;34m'


def _supports_color():
    """
    Check if the current terminal supports color output.
    
    Returns:
        bool: True if colors are supported, False otherwise.
    """
    # Check if we're in a terminal
    if not hasattr(sys.stdout, 'isatty') or not sys.stdout.isatty():
        return False
    
    # Check environment variables that indicate color support
    if os.environ.get('NO_COLOR'):
        return False
    
    if os.environ.get('FORCE_COLOR'):
        return True
    
    # Windows terminal support
    if sys.platform == 'win32':
        # Try to enable ANSI support on Windows
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            return True
        except:
            # Fall back to checking for Windows Terminal or other modern terminals
            return os.environ.get('WT_SESSION') is not None or \
                   os.environ.get('TERM_PROGRAM') is not None
    
    # Unix-like systems
    term = os.environ.get('TERM', '')
    if term in ('dumb', 'unknown'):
        return False
    
    return True


def colorize(text, color, bold=False):
    """
    Apply color to text if color output is supported.
    
    Args:
        text (str): Text to colorize.
        color (str): Color code from Colors class.
        bold (bool): Whether to make the text bold.
    
    Returns:
        str: Colored text if supported, plain text otherwise.
    """
    if not _supports_color():
        return text
    
    if bold and not color.startswith('\033[1;'):
        # Convert regular color to bold if requested
        color_map = {
            Colors.RED: Colors.BOLD_RED,
            Colors.GREEN: Colors.BOLD_GREEN,
            Colors.YELLOW: Colors.BOLD_YELLOW,
            Colors.BLUE: Colors.BOLD_BLUE,
        }
        color = color_map.get(color, color)
    
    return f"{color}{text}{Colors.RESET}"


def green(text, bold=False):
    """Apply green color to text."""
    return colorize(text, Colors.GREEN, bold)


def red(text, bold=False):
    """Apply red color to text."""
    return colorize(text, Colors.RED, bold)


def yellow(text, bold=False):
    """Apply yellow color to text."""
    return colorize(text, Colors.YELLOW, bold)


def blue(text, bold=False):
    """Apply blue color to text."""
    return colorize(text, Colors.BLUE, bold)
