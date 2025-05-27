import argparse
import sys
import os
import re
import datetime
from utils.colours import Colours  # type: ignore

class LogEntry:
    """
    Represents a single log entry.
    Currently stores the raw line and the line number.
    """
    
    def __init__(self, raw_line, line_number):
        self.raw_line = raw_line.strip()
        self.line_number = line_number
        
    def __str__(self):
        return f" {self.line_number} :: {self.raw_line}"
    
    def __repr__(self):
        return f"LogEntry(line_number={self.line_number}, raw_line={self.raw_line[:50]}...)"
    
class LogReader:
    """
    Responsible only for reading the contents of the log file.
    """
    def __init__(self, file_path):
        self.file_path = file_path
    
    def __repr__(self):
        return f"ReadLog(file_path={self.file_path})"
    
    def read_lines(self):
        """
        Generates LogEntry objects from the file line by line.
        Handles FileNotFoundErrors and General I/O errors.
        """
        
        if not os.path.exists(self.file_path): # Handles file not existing.
            raise FileNotFoundError(f"The file {self.file_path} does not exist.")
        
        if not os.path.isfile(self.file_path): # Handles path not being a file.
            raise IOError(f"The file {self.file_path} is not a file.")
        
        if not os.access(self.file_path, os.R_OK): # Handles permission not being granted.
            raise PermissionError(f"Permission not granted to read {self.file_path}.")
        
        try: # Handles reading all lines.
            with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as file:
                for line_num, line in enumerate(file, 1):
                    yield LogEntry(raw_line=line, line_number=line_num)
            # returns a list of LogEntry objects.
        except Exception as e: # Catches all exceptions during runtime.
            raise IOError(f"An error occured when reading file: {self.file_path}:\n{e}")
        
class LogFilter:
    """
    Applies filters to LogEntry objects.
    """
    def __init__(self, keywords: list[str] = None):
        # Ensure all keywords are lowercase to ensure they are read
        self.keywords = [k.lower() for k in keywords] if keywords else []
        
    def __repr__(self):
        return f"LogFilter(keywords={self.keywords})"
        
    def matches(self, log_entry: LogEntry) -> bool:
        """
        Checks if a log entry matches specified keywords.
        Returns true is keywords are empty (no filtering) or if any keywords match else returns false.
        """
        if not self.keywords:
            return True
            
        for keyword in self.keywords:
            if keyword in log_entry.raw_line.lower():
                return True
        return False
    
    
    
class LogAnalyser:
    """
    Main class that orchestrates reading and filtering log entries.
    """
    def __init__(self, file_path: str, keywords: list[str] = None):
        self.log_reader = LogReader(file_path)
        self.log_filter = LogFilter(keywords)
        self.total_lines = 0
        self.filtered_lines = 0
        
    def __repr__(self):
        return f"LogAnalyser(file_path={self.log_reader.file_path}, keywords={self.log_filter.keywords})"
        
    def analyse(self):
        """
        Reads the log file and applies filters.
        Yields a list of filtered LogEntry objects.
        """
        try:
            for entry in self.log_reader.read_lines():
                self.total_lines += 1
                if self.log_filter.matches(entry):
                    self.filtered_lines += 1
                    yield entry
        except Exception as e:
            print(f"Error during log analysis: {e}", file=sys.stderr)
            sys.exit(1)
            
    def get_summary(self):
        """
        Returns a summary of the log analysis.
        """
        return {
            "file_path": self.log_reader.file_path,
            "keywords": self.log_filter.keywords,
            "total_lines": self.total_lines,
            "filtered_lines": self.filtered_lines,
            "has_filters": bool(self.log_filter.keywords)  
        }

def clear_terminal():
    """Clears the terminal screen based on the operating system."""
    if sys.platform.startswith('win'): # Windows
        os.system('cls')
    else: # Linux, macOS, and other POSIX systems
        os.system('clear')

def main():
    arg_parser = argparse.ArgumentParser(
        description="A Python-based command-line utility for parsing, filtering, and analyzing log files."
    )
    arg_parser.add_argument(
        "--file", "-f", type=str, required=True,
        help="Path to the log file to be analyzed."
    )
    arg_parser.add_argument(
        "--keywords", "-k", type=str, nargs='*', default=[],
        help="List of keywords to filter log entries. If not provided, all entries are returned."
    )
    arg_parser.add_argument(
        "--count_only", "-c", action='store_true',
        help="If set, only displays the count of logs and filtered logs, without showing the entries."
    )
    
    args = arg_parser.parse_args()
    
    # Create an instance of log analyser with provided arguments
    log_analyser = LogAnalyser(file_path=args.file, keywords=args.keywords)
    line_break = Colours.apply(f"\n{"-" * 50}\n\n", Colours.DIM)
    
    clear_terminal()  # Clear the terminal for a fresh start

    print(line_break + Colours.apply("= = = Log File Analyser = = =", Colours.BOLD + Colours.GREEN))
    print(Colours.apply("By Jake Morgan, v 1.0", Colours.DIM + Colours.GREEN))
    
    # Print the provided arguments 
    print(line_break + f"Log file path: {log_analyser.log_reader.file_path}")
    if args.keywords:
        print(f"Keywords provided: {', '.join(args.keywords)}")
    else:
        print("No keywords provided, all log entries will be shown.")
    print(f"Count only mode: {'Enabled' if args.count_only else 'Disabled'}")

    print(line_break + Colours.apply("Starting log analysis...", Colours.YELLOW))
    
    for entry in log_analyser.analyse():
        if not args.count_only:
            print(Colours.apply(entry, Colours.DIM))
            
    summary = log_analyser.get_summary() # Get the summary of the analysis
    
    # Print the summary of the log analysis
    print(f"\nTotal log entries: {summary['total_lines']}")
    if summary['has_filters']:
        print(f"Total filtered log entries: {summary['filtered_lines']}")
    
    print(line_break + Colours.apply("Log analysis completed.", Colours.GREEN))
    
    # Thank you message
    print(Colours.apply("Thank you for using the log file analyser.", Colours.DIM + Colours.GREEN))
    print(line_break)
    
if __name__ == "__main__":
    main()