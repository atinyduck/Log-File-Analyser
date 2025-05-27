# utils/colours.py
"""
Utility module for ANSI color codes to format terminal output.
This module provides a class `Colours` that contains ANSI escape codes for text formatting,
including foreground and background colors, as well as styles like bold and underline.
"""

class Colours:
    # ANSI escape codes for terminal text formatting
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"

    # Foreground Colours
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Background Colours (less commonly used for logs)
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

    # Helper function to apply color and reset
    @staticmethod
    def apply(text, color_code):
        return f"{color_code}{text}{Colours.RESET}"

    @staticmethod
    def error(text):
        return f"{Colours.BOLD}{Colours.RED}{text}{Colours.RESET}"

    @staticmethod
    def warning(text):
        return f"{Colours.BOLD}{Colours.YELLOW}{text}{Colours.RESET}"

    @staticmethod
    def success(text):
        return f"{Colours.BOLD}{Colours.GREEN}{text}{Colours.RESET}"