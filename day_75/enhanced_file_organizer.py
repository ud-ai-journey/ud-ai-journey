
#!/usr/bin/env python3
"""
Enhanced File Organizer Tool
Polished version with improved error handling, duplicate handling,
configuration, and basic interactive mode. Includes detailed reporting.

Phase UI-1: Basic UI with threading.
"""

import os
import shutil
import json
import argparse
import hashlib
import logging
import csv
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
import sys
import traceback
import threading
import queue # Import the queue module for thread communication

# --- Try to import CustomTkinter ---
try:
    import customtkinter as ctk
    import tkinter.filedialog as filedialog # Tkinter file dialog is standard
    import tkinter as tk # Need base tkinter sometimes
    CTK_AVAILABLE = True
    # Set CustomTkinter default appearance
    ctk.set_appearance_mode("System") # Modes: "System" (default), "Dark", "Light"
    ctk.set_default_color_theme("blue") # Themes: "blue" (default), "dark-blue", "green"

except ImportError:
    CTK_AVAILABLE = False
    print("CustomTkinter not found. GUI mode disabled. Install it with: pip install customtkinter")
    # Fallback classes to allow the rest of the script to be parsed
    class ctk:
        CTk = object
        CTkLabel = object
        CTkEntry = object
        CTkButton = object
        CTkProgressBar = object
        def set_appearance_mode(mode): pass
        def set_default_color_theme(theme): pass
    class filedialog:
        def askdirectory(): return None
    class tk:
        Tk = object # Basic Tk for fallback check

# Try to import colorama for cross-platform colored output (already present)
try:
    from colorama import init, Fore, Style
    init()
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    class Fore:
        RED = GREEN = YELLOW = BLUE = CYAN = MAGENTA = WHITE = ""
    class Style:
        RESET_ALL = BRIGHT = DIM = NORMAL = ""

# --- Data Classes and Enums (Existing) ---

@dataclass
class OrganizationStats:
    """Track organization statistics"""
    files_processed: int = 0  # Files considered for processing
    files_moved: int = 0
    files_skipped: int = 0
    folders_created: int = 0
    errors: int = 0
    total_size_moved: int = 0  # in bytes
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

class DuplicateStrategy(Enum):
    SKIP = "skip"               # Skip if destination exists (identical or different)
    RENAME = "rename"           # Skip identical, rename different
    OVERWRITE = "overwrite"     # Overwrite if destination exists (identical or different)
    ASK = "ask"                 # Ask user interactively on conflict

@dataclass
class DuplicateResolutionResult:
    """Describes the outcome of processing a single file."""
    action_taken: str
    source: Path
    destination: Optional[Path]
    category: str
    size: int
    reason: str = ""
    error_info: Optional[str] = None


# --- Custom Exception (Existing) ---

class FileOrganizerError(Exception):
    """Custom exception for file organizer errors."""
    pass

# --- Reporter Class (Existing) ---

class FileOrganizerReporter:
    """Handles logging, reporting, and statistics for the file organizer run."""

    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.operation_log: List[Dict[str, Any]] = []
        self.start_time = datetime.now()
        self.end_time: Optional[datetime] = None

    def add_operation_result(self, result: DuplicateResolutionResult) -> None:
        """Logs a file processing result or system event to the operation log."""
        if not isinstance(result, DuplicateResolutionResult):
            self.logger.error(f"Attempted to log invalid result object: {result}")
            return

        entry = asdict(result)
        entry['source'] = str(result.source)
        entry['destination'] = str(result.destination) if result.destination else None
        entry['timestamp'] = datetime.now().isoformat()
        entry['size'] = result.size if result.size is not None else 0

        entry['operation'] = result.action_taken # Standard key for reports

        self.operation_log.append(entry)

        # Log to the main logger for console/file output
        log_message = f"{result.action_taken.upper()}: '{result.source.name if result.source else 'N/A'}'"
        if result.destination:
             dest_path = Path(result.destination)
             log_message += f" -> {str(Path(dest_path.parent.name) / dest_path.name)}" if dest_path.parent.name else f" -> {dest_path.name}"
        if result.reason:
             log_message += f" ({result.reason})"
        if result.error_info:
             log_message += f" (ERROR: {result.error_info.splitlines()[0]})"

        if result.action_taken.startswith("error"):
             self.logger.error(log_message)
        elif result.action_taken in ["skipped", "skipped_by_strategy", "dry_run", "processed_dry_run"]:
             self.logger.info(log_message)
        elif result.action_taken in ["moved", "renamed", "overwritten", "backup_created", "folder_created"]:
             self.logger.info(log_message)
        else:
             self.logger.debug(f"Logged unknown action: {log_message}")


    def finalize(self) -> None:
        """Mark the end of operations."""
        self.end_time = datetime.now()

    def get_summary_stats(self) -> Dict[str, Any]:
        """Generate summary statistics by processing the operation log."""
        total_files_processed = sum(1 for op in self.operation_log if op['operation'] not in ["backup_created", "folder_created"])
        total_moved = sum(1 for op in self.operation_log if op['operation'] in ["moved", "renamed", "overwritten"])
        total_skipped = sum(1 for op in self.operation_log if op['operation'] in ["skipped", "dry_run", "processed_dry_run", "skipped_by_strategy"])
        total_errors = sum(1 for op in self.operation_log if op['operation'].startswith("error"))
        total_size_processed_overall = sum(op.get('size', 0) for op in self.operation_log if op['operation'] not in ["backup_created", "folder_created"])
        total_size_moved = sum(op.get('size', 0) for op in self.operation_log if op['operation'] == "moved")

        recalculated_category_stats: Dict[str, Dict[str, int]] = {}
        all_categories = set() # Collect all categories encountered

        for op in self.operation_log:
            category = op.get('category', 'Unknown')
            action = op.get('operation', 'unknown')
            size = op.get('size', 0)

            all_categories.add(category) # Add this category

            if category not in recalculated_category_stats:
                 recalculated_category_stats[category] = {'count': 0, 'size': 0, 'moved': 0, 'skipped': 0, 'errors': 0}

            if action not in ["backup_created", "folder_created"]:
                recalculated_category_stats[category]['count'] += 1
                recalculated_category_stats[category]['size'] += size

            if action in ["moved", "renamed", "overwritten"]:
                recalculated_category_stats[category]['moved'] += 1
            elif action in ["skipped", "dry_run", "processed_dry_run", "skipped_by_strategy"]:
                recalculated_category_stats[category]['skipped'] += 1
            elif action.startswith("error"):
                recalculated_category_stats[category]['errors'] += 1

        # Ensure categories from config that might not have had files are included (with zero counts)
        config_categories = set(self.config.get("extension_mapping", {}).values()) | set(self.config.get("custom_patterns", {}).values())
        config_categories.add(self.config.get("extension_mapping", {}).get("no_extension", "Others"))
        config_categories.add(self.config.get("extension_mapping", {}).get("unknown", "Others"))
        config_categories.add("Unknown") # Ensure Unknown is always listed
        config_categories.add("System")  # Ensure System is always listed

        for cat in config_categories:
             if cat not in recalculated_category_stats:
                 recalculated_category_stats[cat] = {'count': 0, 'size': 0, 'moved': 0, 'skipped': 0, 'errors': 0}
             # Handle nested path categories from config (e.g., Images/2024-06)
             cat_parts = Path(cat).parts
             if len(cat_parts) > 1:
                 base_cat = cat_parts[0]
                 if base_cat not in recalculated_category_stats:
                      recalculated_category_stats[base_cat] = {'count': 0, 'size': 0, 'moved': 0, 'skipped': 0, 'errors': 0}


        duration = (self.end_time - self.start_time).total_seconds() if self.end_time and self.start_time else 0

        return {
            'total_files_processed': total_files_processed,
            'total_size_processed': total_size_processed_overall,
            'files_moved': total_moved,
            'files_skipped': total_skipped,
            'errors': total_errors,
            'total_size_moved': total_size_moved,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_seconds': duration,
            'categories': recalculated_category_stats
        }

    def export_report(self, format: str = 'text', output_path: Optional[Path] = None) -> Optional[Path]:
        """
        Export report in the specified format.

        Args:
            format: 'text', 'csv', or 'json'.
            output_path: Optional base path for the output file.

        Returns:
            Optional[Path]: Path to the created report file, or None on failure.
        """
        if not self.end_time: self.finalize() # Ensure finalized

        summary = self.get_summary_stats()
        report_file_path = None

        try:
            if not output_path:
                output_filename = f'file_organizer_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
                report_dir = Path(self.config.get("log_directory", "logs")).expanduser().resolve()
                report_dir.mkdir(parents=True, exist_ok=True)
                output_path = report_dir / output_filename

            if format == 'json':
                report_file_path = output_path.with_suffix('.json')
                with open(report_file_path, 'w', encoding='utf-8') as f:
                    json.dump(summary, f, indent=2)

            elif format == 'csv':
                report_file_path = output_path.with_suffix('.csv')
                with open(report_file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Metric', 'Value'])
                    writer.writerow(['Total Files Processed', summary['total_files_processed']])
                    writer.writerow(['Files Moved', summary['files_moved']])
                    writer.writerow(['Files Skipped', summary['files_skipped']])
                    writer.writerow(['Errors', summary['errors']])
                    writer.writerow(['Total Size Processed (MB)', f"{summary['total_size_processed'] / (1024*1024):.2f}"])
                    writer.writerow(['Total Size Moved (MB)', f"{summary['total_size_moved'] / (1024*1024):.2f}"])
                    writer.writerow(['Duration (seconds)', f"{summary['duration_seconds']:.2f}"])
                    writer.writerow([])

                    writer.writerow(['Category', 'Count', 'Size (MB)', 'Moved', 'Skipped', 'Errors'])
                    for category, stats in sorted(summary['categories'].items()):
                         if stats['count'] > 0 or stats['errors'] > 0:
                            writer.writerow([
                                category,
                                stats['count'],
                                f"{stats['size'] / (1024*1024):.2f}",
                                stats['moved'],
                                stats['skipped'],
                                stats['errors']
                            ])
                    writer.writerow([])

                    writer.writerow(['Timestamp', 'Operation', 'Source', 'Destination', 'Category', 'Size (Bytes)', 'Reason', 'Error Info'])
                    for op in self.operation_log[-50:]:
                         writer.writerow([
                             op.get('timestamp', ''), op.get('operation', ''), op.get('source', ''),
                             op.get('destination', ''), op.get('category', ''), op.get('size', 0),
                             op.get('reason', ''), op.get('error_info', '')
                         ])

            else:  # text format (default)
                report_file_path = output_path.with_suffix('.txt')
                with open(report_file_path, 'w', encoding='utf-8') as f:
                    f.write("=" * 60 + "\n")
                    f.write("FILE ORGANIZER REPORT\n")
                    f.write("=" * 60 + "\n\n")

                    f.write("SUMMARY\n")
                    f.write("-" * 60 + "\n")
                    f.write(f"Start Time:           {summary['start_time']}\n")
                    f.write(f"End Time:             {summary['end_time']}\n")
                    f.write(f"Duration:             {summary['duration_seconds']:.2f} seconds\n")
                    f.write(f"Total Files Processed:{summary['total_files_processed']:>8}\n")
                    f.write(f"Files Moved:          {summary['files_moved']:>8}\n")
                    f.write(f"Files Skipped:        {summary['files_skipped']:>8}\n")
                    f.write(f"Errors:               {summary['errors']:>8}\n")
                    f.write(f"Total Size Processed: {summary['total_size_processed'] / (1024*1024):>8.2f} MB\n")
                    f.write(f"Total Size Moved:     {summary['total_size_moved'] / (1024*1024):>8.2f} MB\n\n")

                    f.write("CATEGORY BREAKDOWN\n")
                    f.write("-" * 60 + "\n")
                    f.write(f"{'Category':<25} {'Count':>8} {'Size (MB)':>12} {'Moved':>8} {'Skipped':>8} {'Errors':>8}\n")
                    f.write("-" * 60 + "\n")

                    for category, stats in sorted(summary['categories'].items()):
                        if stats['count'] > 0 or stats['errors'] > 0:
                            f.write(f"{category:<25} {stats['count']:>8} {stats['size']/(1024*1024):>12.2f} "
                                   f"{stats['moved']:>8} {stats['skipped']:>8} {stats['errors']:>8}\n")

                    f.write("\nRECENT OPERATIONS (last 50)\n")
                    f.write("-" * 60 + "\n")
                    for op in self.operation_log[-50:]:
                        op_str = f"{op.get('timestamp', 'N/A').split('.')[0]} {op.get('operation', 'N/A').upper()}: {Path(op.get('source', 'N/A')).name}"
                        if op.get('destination'):
                            dest_path = Path(op['destination'])
                            op_str += f" -> {str(Path(dest_path.parent.name) / dest_path.name)}" if dest_path.parent.name else f" -> {dest_path.name}"
                        if op.get('reason'):
                            op_str += f" ({op['reason']})"
                        if op.get('error_info'):
                            op_str += f" (ERROR: {op['error_info'].splitlines()[0]})"
                        f.write(op_str + "\n")

            self.logger.info(f"Report exported to: {report_file_path}")
            return report_file_path

        except Exception as e:
            self.logger.error(f"Error exporting report: {e}", exc_info=True)
            return None


# --- Main Organizer Class (Existing Core Logic) ---

class EnhancedFileOrganizer:
    """Enhanced file organizer with improved error handling and features."""

    def __init__(self, config_path: Optional[str] = None):
        # Initialize logger first with a basic configuration
        self.logger = logging.getLogger('file_organizer')
        self.logger.setLevel(logging.DEBUG)

        # Clear any existing handlers before adding new ones
        for handler in self.logger.handlers[:]:
             self.logger.removeHandler(handler)
        # Add a NullHandler initially to prevent "No handlers could be found" warnings
        self.logger.addHandler(logging.NullHandler())


        self.config_path = config_path or "file_organizer_config.json"

        try:
            # Load config (basic logger is used here for early warnings/errors)
            self.config = self._load_config()

            # Now setup proper logging based on loaded config
            self.logger = self._setup_logging() # This replaces the NullHandler and sets specific handlers

            # Initialize reporter after config and logging are set up
            self.reporter = FileOrganizerReporter(self.config, self.logger)

            # Initialize overall stats (primarily for start/end time and total scanned count)
            # Detailed counts are managed by the reporter
            self.stats = OrganizationStats()

        except Exception as e:
            self.logger.critical(f"Initialization failed: {e}", exc_info=True)
            raise FileOrganizerError(f"Initialization failed: {e}") from e


    # --- Setup & Configuration ---

    def _setup_logging(self) -> logging.Logger:
        """Set up logging handlers based on loaded configuration."""
        # Get the logger instance created in __init__
        logger = logging.getLogger('file_organizer')

        # Clear any existing handlers (including the NullHandler)
        for handler in logger.handlers[:]:
            try:
                handler.flush()
                handler.close()
            except Exception:
                pass  # Ignore errors closing
            logger.removeHandler(handler)

        # Set log level
        logger.setLevel(logging.DEBUG) # Master level captures everything

        # Console handler - use INFO level by default, will be overridden by main
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO) # Default console level
        console_formatter = logging.Formatter(
             '%(asctime)s - %(levelname)-8s - %(message)s',
             datefmt='%H:%M:%S'
         )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)


        # File handler - logs *all* messages (DEBUG and above)
        log_dir_name = self.config.get("log_directory", "logs")
        log_dir = Path(log_dir_name).expanduser().resolve()

        try:
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file = log_dir / f'file_organizer_debug_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

            file_handler = logging.FileHandler(log_file, mode='w')
            file_handler.setLevel(logging.DEBUG) # Log everything to the file
            file_formatter = logging.Formatter(
                 '%(asctime)s - %(name)s - %(levelname)-8s - %(message)s'
             )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
            logger.info(f"Logging DEBUG messages to file: {log_file}")

        except Exception as e:
             logger.warning(f"Could not set up file logging in '{log_dir}': {e}")

        # Return the configured logger instance
        return logger


    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        # Default configuration - must be self-contained
        default_config = {
            "extension_mapping": {
                # Documents
                '.txt': 'Documents', '.pdf': 'Documents', '.doc': 'Documents',
                '.docx': 'Documents', '.odt': 'Documents', '.rtf': 'Documents',
                '.md': 'Documents', '.ppt': 'Documents', '.pptx': 'Documents',
                '.xls': 'Documents', '.xlsx': 'Documents', '.csv': 'Documents',
                '.epub': 'Documents', '.mobi': 'Documents', '.pages': 'Documents',
                '.numbers': 'Documents', '.key': 'Documents',

                # Images
                '.jpg': 'Images', '.jpeg': 'Images', '.png': 'Images', '.gif': 'Images',
                '.bmp': 'Images', '.tiff': 'Images', '.webp': 'Images', '.svg': 'Images',
                '.ico': 'Images', '.psd': 'Images', '.ai': 'Images', '.heic': 'Images',
                '.raw': 'Images',

                # Audio
                '.mp3': 'Audio', '.wav': 'Audio', '.flac': 'Audio', '.aac': 'Audio',
                '.ogg': 'Audio', '.wma': 'Audio', '.m4a': 'Audio', '.opus': 'Audio',

                # Video
                '.mp4': 'Videos', '.mov': 'Videos', '.avi': 'Videos', '.mkv': 'Videos',
                '.wmv': 'Videos', '.flv': 'Videos', '.webm': 'Videos', '.mpeg': 'Videos',
                '.mpg': 'Videos', '.3gp': 'Videos', '.m4v': 'Videos', '.ts': 'Videos',

                # Archives
                '.zip': 'Archives', '.rar': 'Archives', '.7z': 'Archives', '.tar': 'Archives',
                '.gz': 'Archives', '.bz2': 'Archives', '.xz': 'Archives', '.tgz': 'Archives',
                '.iso': 'Archives', '.img': 'Archives', # Disk Images sometimes treated as archives

                # Executables / Installers
                '.exe': 'Executables', '.msi': 'Executables', '.deb': 'Executables',
                '.rpm': 'Executables', '.pkg': 'Executables', '.dmg': 'Executables',
                '.app': 'Executables', # macOS applications are folders but often thought of this way

                # Code / Scripts
                '.py': 'Code', '.js': 'Code', '.html': 'Code', '.css': 'Code', '.json': 'Code',
                '.xml': 'Code', '.c': 'Code', '.cpp': 'Code', '.h': 'Code', '.hpp': 'Code',
                '.java': 'Code', '.cs': 'Code', '.sh': 'Code', '.bat': 'Code', '.ps1': 'Code',
                '.vbs': 'Code', '.php': 'Code', '.rb': 'Code', '.go': 'Code', '.swift': 'Code',
                '.kt': 'Code', '.ts': 'Code', '.pl': 'Code', '.lua': 'Code', '.sql': 'Code',
                '.r': 'Code', '.f': 'Code', '.for': 'Code', '.asm': 'Code', '.yaml': 'Code',
                '.yml': 'Code', '.toml': 'Code', '.ini': 'Code', '.cfg': 'Code', '.conf': 'Code',

                # Fonts
                '.ttf': 'Fonts', '.otf': 'Fonts', '.woff': 'Fonts', '.woff2': 'Fonts',

                # Disk Images (can be separate from Archives if preferred)
                # '.iso': 'Disk Images', '.img': 'Disk Images', '.vmdk': 'Disk Images', '.vhd': 'Disk Images',

                # Databases
                '.db': 'Databases', '.sqlite': 'Databases',

                # No extension - key is 'no_extension'
                'no_extension': 'Others',
                # Unknown extension - key is 'unknown'
                'unknown': 'Others'
            },
            "custom_patterns": {
                 # Example: {"report": "Reports", "invoice": "Invoices"} - matches substrings (case-insensitive)
            },
            "exclude_patterns": [
                "*.tmp", "*.log", ".*", "desktop.ini", "thumbs.db",
                "__pycache__", ".git", ".vscode", ".idea",
                "file_organizer_config.json" # Exclude config file itself by default
            ],
            "date_based_organization": False, # If True, adds Year/Month or Year subfolders
            "date_format": "%Y-%m",         # "%Y" for Year only, "%Y-%m" for Year/Month
            "max_file_size_mb": 1000,       # Skip files larger than this (1GB default)
            "log_directory": "logs",        # Directory to store log files and reports
            "backup_structure": True,       # Backup directory structure before organizing
            "duplicate_resolution": "rename", # Options: 'skip', 'rename', 'overwrite', 'ask'
            "hash_chunk_size": 65536,       # 64KB chunks for hashing large files
            "export_reports": True,         # Automatically export reports after run
            "report_formats": ["text", "csv"] # List of formats to export ('text', 'csv', 'json')
        }

        loaded_config = {}
        config_file_path = Path(self.config_path).expanduser().resolve()

        # Use the logger instance from self (which might only have a NullHandler initially)
        logger = self.logger


        if config_file_path.exists():
            try:
                with open(config_file_path, 'r') as f:
                    loaded_config = json.load(f)
                logger.info(f"Loaded configuration from '{config_file_path}'.") # Use logger now
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON from '{config_file_path}'. Using default mapping.")
            except Exception as e:
                logger.error(f"An unexpected error occurred loading config '{config_file_path}': {e}. Using default mapping.")


        # Merge loaded config with defaults
        config = default_config.copy()
        for key, value in loaded_config.items():
             # Simple recursive merge for nested dicts like extension_mapping
             if isinstance(value, dict) and key in config and isinstance(config[key], dict):
                 config[key].update({k.lower() if k.startswith('.') else k: v for k, v in value.items()})
             else:
                 config[key] = value

        # --- Config Validation and Harmonization ---

        # Validate duplicate_resolution strategy
        valid_strategies = [s.value for s in DuplicateStrategy]
        current_strategy = config.get("duplicate_resolution")
        if current_strategy not in valid_strategies:
            logger.warning(f"Invalid duplicate_resolution strategy '{current_strategy}'. Defaulting to 'rename'.")
            config["duplicate_resolution"] = "rename"

        # Ensure extensions in mapping are lowercase keys
        if "extension_mapping" in config:
            config["extension_mapping"] = {k.lower(): v for k, v in config["extension_mapping"].items()}

        # Ensure custom patterns are lowercase keys (values can be anything)
        if "custom_patterns" in config:
             config["custom_patterns"] = {k.lower(): v for k, v in config["custom_patterns"].items()}

        # Validate report formats
        valid_report_formats = ['text', 'csv', 'json']
        if "report_formats" in config:
             config["report_formats"] = [f.lower() for f in config["report_formats"] if f.lower() in valid_report_formats]
             if not config["report_formats"]:
                  logger.warning("No valid report formats specified in config. Defaulting to ['text', 'csv'].")
                  config["report_formats"] = ["text", "csv"]


        # If config file didn't exist or had errors/merges, save the effective one
        # Compare merged config (config dict) with initially loaded config (loaded_config dict)
        if not config_file_path.exists() or loaded_config != config:
             self._save_config(config) # Save the effective config (defaults + loaded + validated)


        return config

    def _save_config(self, config: Dict):
        """Save configuration to file."""
        try:
            config_file_path = Path(self.config_path).expanduser().resolve()
            config_file_path.parent.mkdir(parents=True, exist_ok=True) # Ensure config directory exists
            with open(config_file_path, 'w') as f:
                json.dump(config, f, indent=2)
            self.logger.debug(f"Saved configuration to '{config_file_path}'.")
        except Exception as e:
            self.logger.error(f"Could not save config file '{self.config_path}': {e}")

    # --- Helper Methods ---

    def _print_colored(self, message: str, color: str = "", style: str = "", **kwargs):
        """Print colored message if colors are available."""
        if COLORS_AVAILABLE:
            print(f"{color}{style}{message}{Style.RESET_ALL}", **kwargs)
        else:
            print(message, **kwargs)

    def _clear_progress_line(self):
         """Clears the current console line for the progress bar."""
         if sys.stdout.isatty(): # Check if connected to a terminal
             # Move cursor to the beginning of the line and clear line from cursor
             sys.stdout.write('\r' + ' ' * 100 + '\r') # Clear more space just in case
             sys.stdout.flush()

    def _show_progress(self, current: int, total: int, description: str = "Processing"):
        """Show progress bar on the console."""
        if not sys.stdout.isatty(): # Only show progress on a terminal
            return

        percent = (current / total) * 100 if total > 0 else 0
        bar_length = 30
        filled = int(bar_length * current // total)
        bar = "█" * filled + "░" * (bar_length - filled)

        # Clear the line before printing the progress bar
        self._clear_progress_line()
        print(f"{description}: [{bar}] {percent:.1f}% ({current}/{total})", end="", flush=True)

        if current == total:
            print()  # New line when complete

    def _check_disk_space(self, directory: Path, required_size: int) -> bool:
        """Check if there is enough free disk space in the target directory's partition."""
        try:
            # Use the target directory to get usage of its filesystem
            total, used, free = shutil.disk_usage(directory)
            if free >= required_size:
                self.logger.debug(f"Disk space check passed for '{directory}'. Free: {free:,} bytes, Required: {required_size:,} bytes.")
                return True
            else:
                self.logger.error(f"Insufficient disk space in '{directory.anchor}' partition. Required: {required_size:,} bytes, Available: {free:,} bytes.")
                return False
        except OSError as e:
            self.logger.error(f"Could not check disk space for '{directory}': {e}")
            return False

    def _should_skip_file(self, file_path: Path) -> Tuple[bool, str]:
        """Check if file should be skipped based on various criteria."""
        # Check if file is the script or config file itself using absolute paths
        try:
            abs_file_path = file_path.resolve()
            abs_script_path = Path(__file__).resolve()
            abs_config_path = Path(self.config_path).resolve()

            if abs_file_path == abs_script_path:
                return True, "is the script file"
            # Use is_relative_to check in case config file is in parent dir of target
            if abs_config_path == abs_file_path:
                 return True, "is the configuration file"

        except (OSError, RuntimeError) as e: # Catch OSError and symlink loop RuntimeErrors
             # If resolving path fails, skip as it might be a broken symlink or inaccessible
             self.logger.debug(f"Could not resolve path {file_path}: {e}")
             return True, "could not resolve path"


        # Check exclude patterns (using case-insensitive regex match on the filename)
        # Use glob pattern matching logic with regex conversion
        file_name_lower = file_path.name.lower()
        for pattern in self.config.get("exclude_patterns", []):
            try:
                # Escape special regex characters, then convert glob patterns (*, ?)
                escaped = re.escape(pattern)
                regex_pattern = escaped.replace(r'\*', '.*').replace(r'\?', '.')
                # Anchor the regex to match the whole filename
                regex = re.compile(f'^{regex_pattern}$', re.IGNORECASE)
                # Check if the filename matches the pattern
                if regex.match(file_name_lower):
                    self.logger.debug(f"'{file_path.name}' matches exclude pattern '{pattern}'.")
                    return True, f"matches exclude pattern: {pattern}"
            except re.error as e:
                self.logger.warning(f"Invalid regex pattern '{pattern}' in config exclude_patterns: {e}")
                continue # Continue to next pattern


        # Check file size limit
        try:
            max_size = self.config.get("max_file_size_mb", 1000) * 1024 * 1024
            if file_path.stat().st_size > max_size:
                self.logger.debug(f"'{file_path.name}' is too large ({file_path.stat().st_size} bytes).")
                return True, f"file too large (>{max_size/1024/1024:.1f}MB)"
        except OSError:
            # If stat fails, treat as potentially inaccessible or problematic
            self.logger.debug(f"Could not access metadata for '{file_path.name}'.")
            return True, "could not access file metadata (might be in use or permission issue)"

        # Check if file is in use (common heuristic, may not work everywhere)
        # rely on OS errors during the move for definitive locked files
        # This check is primarily for permissions or obvious locks before attempting move
        if not os.access(file_path, os.R_OK): # Need read permission to hash/copy
             self.logger.debug(f"Read permission denied for '{file_path.name}'.")
             return True, "read permission denied"
        if not os.access(file_path, os.W_OK): # Need write permission to move/delete original
             self.logger.debug(f"Write permission denied for '{file_path.name}'.")
             return True, "write permission denied (might be in use)"


        return False, "" # Not skipped

    def _get_file_hash(self, file_path: Path, quick_check: bool = False) -> Optional[str]:
        """
        Get hash of file for duplicate detection. Returns None on error.

        Args:
            file_path: Path to the file to hash
            quick_check: If True, hash only first/last chunks for large files

        Returns:
            Optional[str]: Hex digest of the file hash, or None on error
        """
        if not file_path.is_file():
            # Already logged warnings for non-existent files before hashing
            return None

        try:
            file_size = file_path.stat().st_size
            chunk_size = self.config.get("hash_chunk_size", 65536)  # 64KB chunks
            file_hash = hashlib.md5()

            with open(file_path, 'rb') as f:
                # Always read first chunk
                chunk1 = f.read(chunk_size)
                file_hash.update(chunk1)

                # For quick check on large files, hash last chunk too
                if quick_check and file_size > chunk_size * 2:
                    # Seek to near end of file (minus one chunk)
                    f.seek(-chunk_size, 2)
                    chunk2 = f.read(chunk_size)
                    file_hash.update(chunk2)
                    self.logger.debug(f"Hashed first and last {chunk_size} bytes for {file_path.name} (quick check).")
                else:
                     # If not quick check, read remaining chunks
                    while chunk := f.read(chunk_size): # Use walrus operator for cleaner loop
                         file_hash.update(chunk)
                    self.logger.debug(f"Hashed entire file {file_path.name}.")

            return file_hash.hexdigest()

        except (IOError, OSError, PermissionError) as e:
            self.logger.warning(f"Error hashing file {file_path}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error during hashing {file_path}: {e}", exc_info=True)
            return None


    def _get_destination_folder(self, file_path: Path) -> str:
        """
        Determine destination folder for a file based on config rules.

        Checks extension mapping, then custom patterns, then applies date logic if enabled.

        Args:
            file_path: Path to the file

        Returns:
            str: Name of the destination folder (relative path components, e.g. "Images/2024-06")
        """
        extension = file_path.suffix.lower()
        folder_name = None

        # 1. Check extension mapping
        if not extension:
            folder_name = self.config["extension_mapping"].get("no_extension", "Others")
        elif extension in self.config["extension_mapping"]:
            folder_name = self.config["extension_mapping"][extension]

        # 2. Check custom patterns (if not already mapped by extension)
        #    Custom patterns override extension mapping if they match
        if folder_name is None:
             for pattern, folder in self.config.get("custom_patterns", {}).items():
                 # Simple substring match (case-insensitive)
                 if pattern.lower() in file_path.name.lower():
                     folder_name = folder
                     break # Use the first matching pattern

        # 3. Default if no mapping/pattern matched
        if folder_name is None:
            folder_name = self.config["extension_mapping"].get("unknown", "Others")
            if extension or "no_extension" not in self.config["extension_mapping"]:
                 self.logger.debug(f"Using default 'Others' for '{file_path.name}' (extension '{extension}' unknown).")


        # 4. Add date-based organization if enabled
        if self.config.get("date_based_organization", False):
            date_format = self.config.get("date_format", "%Y-%m")
            try:
                # Use modification time
                file_date = datetime.fromtimestamp(file_path.stat().st_mtime)
                date_subfolder = file_date.strftime(date_format)
                # Append date subfolder to the determined folder name
                folder_name = Path(folder_name) / date_subfolder
            except OSError:
                self.logger.warning(f"Could not get modification date for {file_path.name}, skipping date-based organization for this file.")
                pass  # Use default folder name if date access fails
            except ValueError:
                 self.logger.error(f"Invalid date format '{date_format}' in config. Skipping date-based organization for this file.")
                 pass # Use default folder name if format is invalid


        # Return as string, joining Path components if date added nested folders
        return str(folder_name)

    # --- Duplicate Handling ---

    def _handle_duplicate(self, source_file: Path, dest_file_path: Path) -> DuplicateResolutionResult:
        """
        Handle a duplicate file by checking content and applying resolution strategy.

        Args:
            source_file: Source file path (must exist)
            dest_file_path: Intended destination path that conflicts with an existing file (must exist)

        Returns:
            DuplicateResolutionResult: Contains resolution details and outcome.
                                       action_taken will be one of: "resolved_rename",
                                       "resolved_overwrite", "resolved_skip_identical",
                                       "skipped_by_strategy", "error_duplicate_handling".
                                       The `destination` field is the path to use *if*
                                       the result indicates proceeding (rename, overwrite).
        """
        # Initialize result details (some will be updated in the try block)
        result_details = {
             'action_taken': "error_duplicate_handling", # Default in case of early error
             'source': source_file,     # Original source path
             'destination': dest_file_path, # Initial destination
             'category': self._get_destination_folder(source_file), # Determine category early
             'size': source_file.stat().st_size if source_file.exists() else 0, # Get size if possible
             'reason': "unknown error in duplicate handling",
             'error_info': None
        }

        if not dest_file_path.exists():
             # This method should only be called if dest_file_path exists, but add check
             self.logger.warning(f"_handle_duplicate called but destination '{dest_file_path}' does not exist.")
             result_details.update({'reason': "duplicate handling called on non-existent destination"})
             return DuplicateResolutionResult(**result_details)


        strategy = DuplicateStrategy(self.config.get("duplicate_resolution", "rename")) # Use Enum for validation
        source_name = source_file.name
        dest_name = dest_file_path.name


        try:
            self.logger.debug(f"Handling duplicate: Source='{source_name}', Dest='{dest_name}', Strategy='{strategy.value}'")

            # Perform quick hash check
            source_hash_quick = self._get_file_hash(source_file, quick_check=True)
            dest_hash_quick = self._get_file_hash(dest_file_path, quick_check=True)

            files_identical = False
            # Proceed to full hash only if quick hashes match AND both were calculable
            if source_hash_quick is not None and dest_hash_quick is not None and source_hash_quick == dest_hash_quick:
                self.logger.debug(f"Quick hashes match for '{source_name}' vs '{dest_name}'. Performing full hash check.")
                source_hash_full = self._get_file_hash(source_file, quick_check=False)
                dest_hash_full = self._get_file_hash(dest_file_path, quick_check=False)

                # Files are identical only if full hashes match AND both were calculable
                if source_hash_full is not None and dest_hash_full is not None and source_hash_full == dest_hash_full:
                     files_identical = True
                     self.logger.debug(f"Full hash confirmed '{source_name}' and '{dest_name}' are identical.")
                elif source_hash_full is None or dest_hash_full is None:
                     self.logger.warning(f"Could not complete full hash check for '{source_name}' or '{dest_name}'. Cannot confirm if identical.")
                     files_identical = False # Treat as non-identical if cannot verify identity
                else:
                     self.logger.debug(f"Full hash confirmed '{source_name}' and '{dest_name}' are different.")
                     files_identical = False # Full hashes differ

            elif source_hash_quick is None or dest_hash_quick is None:
                 self.logger.warning(f"Could not calculate quick hash for '{source_name}' or '{dest_name}'. Cannot confirm if identical.")
                 files_identical = False # Cannot confirm identity, treat as non-identical for safety (will rename or ask, not skip identical)
            else:
                 self.logger.debug(f"Quick hashes differ for '{source_name}' vs '{dest_name}'. Files are different.")
                 files_identical = False # Quick hashes differ


            # --- Apply resolution strategy ---

            if strategy == DuplicateStrategy.SKIP:
                action_taken = "skipped_by_strategy"
                reason = f"destination exists (strategy: {strategy.value})"
                self.logger.debug(f"'{source_name}' {action_taken}: {reason}")
                result_details.update({'action_taken': action_taken, 'reason': reason})
                return DuplicateResolutionResult(**result_details)

            elif strategy == DuplicateStrategy.RENAME:
                if files_identical:
                    action_taken = "skipped_by_strategy"
                    reason = f"identical file exists (strategy: {strategy.value})"
                    self.logger.debug(f"'{source_name}' {action_taken}: {reason}")
                    result_details.update({'action_taken': action_taken, 'reason': reason})
                    return DuplicateResolutionResult(**result_details)
                else:
                    # Files are different, generate unique name
                    new_dest_path = self._generate_unique_filename(dest_file_path)
                    action_taken = "resolved_rename"
                    reason = f"files differ, renamed to '{new_dest_path.name}' (strategy: {strategy.value})"
                    self.logger.debug(f"'{source_name}' {action_taken}: {reason}")
                    result_details.update({'action_taken': action_taken, 'destination': new_dest_path, 'reason': reason})
                    return DuplicateResolutionResult(**result_details)

            elif strategy == DuplicateStrategy.OVERWRITE:
                 # Always proceed to overwrite if destination exists
                 # Note: Overwriting an identical file is effectively a skip, but strategy says overwrite
                 action_taken = "resolved_overwrite"
                 reason = f"destination exists, will overwrite (strategy: {strategy.value}, identical: {files_identical})"
                 self.logger.debug(f"'{source_name}' {action_taken}: {reason}")
                 result_details.update({'action_taken': action_taken, 'reason': reason})
                 return DuplicateResolutionResult(**result_details)

            elif strategy == DuplicateStrategy.ASK:
                 # Interactive resolution loop
                 while True:
                     self._clear_progress_line() # Clear progress before asking
                     print(f"\n{Style.BRIGHT}{Fore.YELLOW}Conflict detected:{Style.RESET_ALL} {source_name}")
                     print(f"  Source: {source_file}")
                     print(f"  Destination: {dest_file_path}")

                     if files_identical:
                         self._print_colored("  Status: Files are identical.", Fore.YELLOW)
                     else:
                         self._print_colored("  Status: Files are different.", Fore.YELLOW)
                         # Optionally print sizes if files are different
                         try:
                            size1 = source_file.stat().st_size
                            size2 = dest_file_path.stat().st_size
                            print(f"  Size: {size1:,} bytes vs {size2:,} bytes")
                         except OSError:
                            pass # Cannot get sizes


                     print("\nOptions:")
                     print("  [s]kip        - Keep existing file, skip moving this file.")
                     print("  [r]ename      - Generate a new name for this file.")
                     if files_identical:
                         print("  [k]eep        - Keep existing file (files are identical).")
                     else:
                         print("  [o]verwrite   - Replace the existing file.")
                         print("  [d]iff        - Show differences between the files.")

                     choice = input("Choose an option: ").strip().lower()

                     if choice in ['s', 'skip']:
                         self.logger.info(f"User chose to skip '{source_name}'.")
                         action_taken = "skipped_by_strategy"
                         reason = "user chose to skip"
                         result_details.update({'action_taken': action_taken, 'reason': reason})
                         return DuplicateResolutionResult(**result_details)

                     elif choice in ['r', 'rename']:
                         new_path = self._generate_unique_filename(dest_file_path)
                         self.logger.info(f"User chose to rename '{source_name}' to '{new_path.name}'.")
                         self._print_colored(f"  → Renaming to: {new_path.name}", Fore.CYAN)
                         action_taken = "resolved_rename"
                         reason = f"user chose to rename to '{new_path.name}'"
                         result_details.update({'action_taken': action_taken, 'destination': new_path, 'reason': reason})
                         return DuplicateResolutionResult(**result_details)

                     elif choice in ['k', 'keep'] and files_identical:
                          self.logger.info(f"User chose to keep existing identical file for '{source_name}'.")
                          self._print_colored("  → Keeping existing identical file.", Fore.CYAN)
                          action_taken = "skipped_by_strategy"
                          reason = "user chose to keep existing identical file"
                          result_details.update({'action_taken': action_taken, 'reason': reason})
                          return DuplicateResolutionResult(**result_details)

                     elif choice in ['o', 'overwrite'] and not files_identical:
                         confirm = input("Are you sure you want to overwrite? (y/n): ").strip().lower()
                         if confirm == 'y':
                              self.logger.info(f"User chose to overwrite '{dest_file_path.name}' with '{source_name}'.")
                              self._print_colored("  → Overwriting existing file.", Fore.RED)
                              action_taken = "resolved_overwrite"
                              reason = "user chose to overwrite"
                              result_details.update({'action_taken': action_taken, 'reason': reason})
                              return DuplicateResolutionResult(**result_details)
                         else:
                             self.logger.info(f"User cancelled overwrite for '{source_name}'.")
                             # Re-show menu for a different choice
                             continue
                     elif choice in ['d', 'diff'] and not files_identical:
                          self.logger.info(f"User requested diff for '{source_name}' vs '{dest_file_path.name}'.")
                          self._show_file_differences(source_file, dest_file_path)
                          # Re-show menu after showing diff
                          continue
                     else:
                         print("Invalid choice. Please try again.")
                         continue # Re-show menu

        except Exception as e:
            error_msg = f"Error during duplicate handling for '{source_name}': {e}"
            self.logger.error(error_msg, exc_info=True)
            # Return as an error action
            result_details.update({
                'action_taken': "error_duplicate_handling",
                'reason': error_msg,
                'error_info': traceback.format_exc()
            })
            return DuplicateResolutionResult(**result_details)


    def _show_file_differences(self, file1: Path, file2: Path) -> None:
        """Show differences between two files (simple text diff or info for binary)"""
        self._print_colored("\n--- File Differences ---", Fore.MAGENTA)
        try:
            # Simple text diff for files that appear to be text
            if self._is_text_file(file1) and self._is_text_file(file2):
                import difflib
                try:
                    # Read files with universal newlines and ignore encoding errors
                    with open(file1, 'r', encoding='utf-8', errors='ignore', newline='') as f1, \
                         open(file2, 'r', encoding='utf-8', errors='ignore', newline='') as f2:
                        diff = difflib.unified_diff(
                            [line.rstrip() for line in f1], # rstrip to avoid diffs due to trailing whitespace
                            [line.rstrip() for line in f2],
                            fromfile=str(file1.name),
                            tofile=str(file2.name),
                            lineterm='', # Don't add newlines, handled by print
                            n=3  # Show 3 lines of context
                        )
                        diff_output = list(diff) # Read all diff lines
                        if not diff_output:
                            print("Files appear identical (based on text content).")
                        else:
                             # Print diff with potential colors if difflib supports it
                             # (depends on environment, basic print is safer cross-platform)
                             for line in diff_output:
                                 if line.startswith('+'):
                                     self._print_colored(line, Fore.GREEN)
                                 elif line.startswith('-'):
                                     self._print_colored(line, Fore.RED)
                                 elif line.startswith('@'):
                                     self._print_colored(line, Fore.CYAN)
                                 else:
                                     print(line)

                except Exception as e:
                     print(f"Could not perform text diff: {e}")

            else:
                # For binary files or diff errors, show basic info
                print("Files are likely binary or text diff failed.")
                try:
                    s1 = file1.stat()
                    s2 = file2.stat()
                    print(f"  Size: {s1.st_size:,} bytes vs {s2.st_size:,} bytes")
                    print(f"  Modified: {datetime.fromtimestamp(s1.st_mtime)} vs {datetime.fromtimestamp(s2.st_mtime)}")
                    # Add hash comparison result if available
                    # (hashes were calculated in _handle_duplicate before calling this)
                    # Re-calculating here for robustness if called elsewhere, but less efficient
                    hash1 = self._get_file_hash(file1, quick_check=False)
                    hash2 = self._get_file_hash(file2, quick_check=False)
                    if hash1 and hash2:
                         print(f"  MD5 Hash: {hash1} vs {hash2}")
                         if hash1 == hash2:
                             self._print_colored("  Files confirmed identical by full hash.", Fore.GREEN)
                         else:
                             self._print_colored("  Files confirmed different by full hash.", Fore.YELLOW)
                    elif hash1 or hash2:
                         self._print_colored("  Could not get hash for one file.", Fore.YELLOW)
                    else:
                         self._print_colored("  Could not get hash for either file.", Fore.YELLOW)

                except OSError as e:
                     print(f"  Could not get file info: {e}")

        except Exception as e:
            print(f"An unexpected error occurred during diff display: {e}")
        finally:
            self._print_colored("--- End Differences ---", Fore.MAGENTA)


    def _is_text_file(self, file_path: Path, chunk_size: int = 1024) -> bool:
        """Heuristically check if a file is a text file by sampling content."""
        if not file_path.is_file():
            return False
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(chunk_size)
                # If the chunk is empty, it's an empty file (often considered text)
                if not chunk:
                    return True
                # Check for common binary indicators (null bytes)
                if b'\x00' in chunk:
                    return False
                # Try decoding with common text encodings
                try:
                    chunk.decode('utf-8', errors='strict')
                    return True
                except UnicodeDecodeError:
                    try:
                        chunk.decode('latin-1', errors='strict')
                        return True
                    except UnicodeDecodeError:
                        pass # Not easily decodeable as UTF-8 or Latin-1
                return False # Contains non-text bytes or decoding failed
        except (IOError, PermissionError, OSError):
            return False # Cannot read file


    def _generate_unique_filename(self, dest_file: Path) -> Path:
        """Generate a unique filename by appending a number."""
        counter = 1
        name_parts = dest_file.stem, dest_file.suffix
        dest_dir = dest_file.parent

        # Handle case where original file might be like "file_1.txt"
        # If stem ends with _number, start counter from number + 1
        stem_parts = name_parts[0].rsplit('_', 1)
        if len(stem_parts) > 1 and stem_parts[-1].isdigit():
            base_name = stem_parts[0]
            counter = int(stem_parts[-1]) + 1
        else:
            base_name = name_parts[0]

        new_dest_file = dest_file # Start with original path

        # Loop until a non-existent filename is found
        while new_dest_file.exists():
            new_name = f"{base_name}_{counter}{name_parts[1]}"
            new_dest_file = dest_dir / new_name
            counter += 1
            if counter > 10000: # Safety break for extremely rare cases or bugs
                self.logger.error(f"Could not find unique name for {dest_file.name} after 10000 attempts.")
                raise FileOrganizerError(f"Could not find unique name for {dest_file.name}")

        return new_dest_file

    # --- Backup ---

    def _create_backup(self, target_path: Path):
        """Create a backup of the directory structure (metadata only)."""
        if not self.config.get("backup_structure", True):
            self.logger.info("Structure backup disabled in config.")
            return

        backup_dir_name = f"{target_path.name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_dir = target_path.parent / backup_dir_name

        try:
            self.logger.info(f"Creating structure backup in: {backup_dir}")
            # Only backup the directory structure, not the files
            structure_info = {
                "timestamp": datetime.now().isoformat(),
                "original_path": str(target_path),
                "files": [] # We'll list files and their original relative paths
            }

            # Scan all items in the target directory and its subdirectories
            # This captures *everything* before organization
            for root, dirs, files in os.walk(str(target_path), topdown=True):
                 current_dir = Path(root)
                 # Prune backup directory itself from the walk if it's inside target_path
                 if backup_dir.exists() and backup_dir.is_relative_to(current_dir):
                     # If the backup directory is a subdirectory of the current root
                     # check if any of the subdirs found are the backup dir, and remove them
                     try:
                         backup_subdir_name = backup_dir.relative_to(current_dir).parts[0]
                         if backup_subdir_name in dirs:
                              dirs.remove(backup_subdir_name)
                              self.logger.debug(f"Pruning backup directory '{backup_subdir_name}' from walk.")
                     except ValueError:
                         # backup_dir is not relative to current_dir in the expected way, continue walk
                         pass # Should not happen with is_relative_to check above, but safety


                 for name in files:
                    file_path = current_dir / name
                    try:
                         # Store relative path, size, and modified time
                        structure_info["files"].append({
                            "path": str(file_path.relative_to(target_path)),
                            "size": file_path.stat().st_size,
                            "modified": file_path.stat().st_mtime # Unix timestamp
                        })
                    except Exception as e:
                        self.logger.warning(f"Could not get info for backup structure for {file_path}: {e}")


            backup_dir.mkdir(parents=True, exist_ok=True) # Ensure backup dir exists before writing
            info_file_path = backup_dir / "directory_structure.json"
            with open(info_file_path, "w") as f:
                json.dump(structure_info, f, indent=2)

            self.logger.info(f"Structure backup created: {info_file_path}")
            # Log backup creation via reporter
            # Need to decide if backup creation is logged per file or as a system event
            # Logging as a system event seems more appropriate
            # The Reporter class doesn't have a simple 'log_system_event' - repurpose log_operation
            self.reporter.add_operation_result(DuplicateResolutionResult(
                action_taken="backup_created", source=target_path, destination=backup_dir, category="System",
                size=0, reason=f"Structure backup created at {backup_dir}"
            ))

        except Exception as e:
            self.logger.warning(f"Could not create structure backup: {e}")
            self.reporter.add_operation_result(DuplicateResolutionResult(
                action_taken="error", source=target_path, destination=None, category="System",
                size=0, reason=f"Failed to create structure backup: {e}",
                error_info=traceback.format_exc()
            ))


    # --- Core Processing Logic ---

    def _process_single_file(self, file_path: Path, target_path: Path, dry_run: bool = False) -> DuplicateResolutionResult:
        """
        Processes a single file: checks eligibility, determines destination,
        handles duplicates, and performs the move (or simulates).

        Args:
            file_path: The full Path object of the file to process (expected to be resolved).
            target_path: The root directory being organized (expected to be resolved).
            dry_run: If True, simulates the move without action.

        Returns:
            DuplicateResolutionResult: Describes the outcome (moved, skipped, renamed, error).
        """
        # Log entry point for processing this file
        self.logger.debug(f"\n{'='*80}\nProcessing file: {file_path}\nTarget path: {target_path}\nDry run: {dry_run}\n{'='*80}")

        # Initialize base result details
        # These will be updated as processing proceeds
        result_details: Dict[str, Any] = {
            'source': file_path, # Original source path
            'destination': None,
            'category': "Unknown",
            'size': 0,
            'reason': "",
            'error_info': None
        }

        try:
             # --- Initial Checks & Metadata ---
             # Ensure file still exists and get size/category early
             try:
                 if not file_path.exists():
                     result_details.update({'action_taken': "skipped", 'reason': "source file disappeared"})
                     self.logger.warning(f"Skipping '{file_path.name}': {result_details['reason']}")
                     return DuplicateResolutionResult(**result_details) # Return early

                 result_details['size'] = file_path.stat().st_size
                 result_details['category'] = self._get_destination_folder(file_path) # Determine category early
                 self.logger.debug(f"Determined category: {result_details['category']}, size: {result_details['size']} bytes.")

             except (OSError, RuntimeError) as e:
                 result_details.update({'action_taken': "error", 'reason': f"cannot access file metadata: {e}", 'error_info': traceback.format_exc()})
                 self.logger.error(f"Error processing '{file_path.name}': {result_details['reason']}", exc_info=True)
                 return DuplicateResolutionResult(**result_details) # Return early

             # Check if file should be skipped based on config rules (type, size, patterns, etc.)
             should_skip, skip_reason = self._should_skip_file(file_path)
             if should_skip:
                  result_details.update({'action_taken': "skipped", 'reason': skip_reason})
                  self.logger.info(f"Skipping '{file_path.name}': {result_details['reason']}")
                  return DuplicateResolutionResult(**result_details) # Return early

             # --- Determine Destination ---
             try:
                 dest_folder = target_path / result_details['category'] # Use the determined category
                 intended_dest_file_path = dest_folder / file_path.name
                 result_details['destination'] = intended_dest_file_path # Set initial destination in result details
                 self.logger.debug(f"Intended destination folder: {dest_folder}")
                 self.logger.debug(f"Intended destination path: {intended_dest_file_path}")

                 # Skip if the file is already exactly where it should go (resolved paths)
                 # Check if the parent of the source is the intended destination folder AND the name is the same
                 if file_path.parent.resolve() == dest_folder.resolve() and file_path.name == intended_dest_file_path.name:
                     result_details.update({'action_taken': "skipped", 'reason': "already in correct location"})
                     self.logger.info(f"Skipping '{file_path.name}': {result_details['reason']}")
                     return DuplicateResolutionResult(**result_details) # Return early

             except Exception as e:
                  result_details.update({'action_taken': "error", 'reason': f"error determining destination: {e}", 'error_info': traceback.format_exc()})
                  self.logger.error(f"Error processing '{file_path.name}': {result_details['reason']}", exc_info=True)
                  return DuplicateResolutionResult(**result_details) # Return early


             # --- Handle Dry Run ---
             if dry_run:
                 action_description = "would move"
                 reason_suffix = "simulated move"
                 final_path_for_report = intended_dest_file_path

                 if intended_dest_file_path.exists():
                      # In dry run, still check duplicates to report intended action
                      dry_run_duplicate_result = self._handle_duplicate(file_path, intended_dest_file_path)
                      action_description = f"would {dry_run_duplicate_result.action_taken.replace('resolved_', '').replace('_by_strategy', '').replace('error_', '')}" # e.g., would rename, would skip, would overwrite
                      reason_suffix = f"simulated action: {dry_run_duplicate_result.action_taken}"
                      final_path_for_report = dry_run_duplicate_result.destination # Use the simulated final path


                 result_details.update({
                     'action_taken': "dry_run",
                     'destination': final_path_for_report, # Report the simulated destination
                     'reason': reason_suffix
                 })
                 self.logger.info(f"[DRY RUN] {action_description}: '{file_path.name}' -> '{result_details['destination']}'")
                 return DuplicateResolutionResult(**result_details) # Return dry run result


             # --- Perform Actual Operations (if not dry run) ---

             # Create destination folder if needed
             try:
                 # exists_ok=True is crucial for retries and multiple files going to same folder
                 if not dest_folder.exists():
                      dest_folder.mkdir(parents=True, exist_ok=True)
                      self.stats.folders_created += 1 # This count is for UI display, reporter has detailed logs
                      self.logger.info(f"Created directory: {dest_folder}")
                      # Reporter logs folder creation separately if needed, not tied to file processing result

                 # Verify destination folder is writable
                 if not os.access(dest_folder, os.W_OK):
                      result_details.update({'action_taken': "error", 'reason': f"no write permission for destination directory: {dest_folder}", 'error_info': traceback.format_exc()})
                      self.logger.error(f"Error processing '{file_path.name}': {result_details['reason']}")
                      return DuplicateResolutionResult(**result_details) # Return early


             except (OSError, PermissionError) as e:
                 result_details.update({'action_taken': "error", 'reason': f"failed to create or check destination directory: {e}", 'error_info': traceback.format_exc()})
                 self.logger.error(f"Error processing '{file_path.name}': {result_details['reason']}", exc_info=True)
                 return DuplicateResolutionResult(**result_details) # Return early


             # --- Handle Duplicates if Destination Exists ---
             if intended_dest_file_path.exists():
                 self.logger.debug(f"Destination '{intended_dest_file_path}' exists. Handling duplicate...")
                 duplicate_resolution_result = self._handle_duplicate(file_path, intended_dest_file_path)

                 # Update result details based on duplicate resolution outcome
                 result_details.update({
                      'action_taken': duplicate_resolution_result.action_taken, # e.g., "resolved_rename", "skipped_by_strategy"
                      'reason': duplicate_resolution_result.reason,
                      'error_info': duplicate_resolution_result.error_info, # Carry forward error info if any
                      'destination': duplicate_resolution_result.destination  # Ensure destination is set
                 })
                 final_destination_path = duplicate_resolution_result.destination # Path to use if proceeding

                 # If duplicate handling resulted in skipping this file or error
                 if duplicate_resolution_result.action_taken in ["skipped_by_strategy", "error_duplicate_handling"]:
                     self.logger.warning(f"Skipping '{file_path.name}' based on duplicate handling: {duplicate_resolution_result.reason}")
                     return DuplicateResolutionResult(**result_details)  # Return the result object directly

                 # If duplicate handling resolved to rename or overwrite, update destination and proceed
                 # action_taken is now "resolved_rename" or "resolved_overwrite"
                 result_details['destination'] = final_destination_path
                 self.logger.debug(f"Duplicate resolved for '{file_path.name}': {duplicate_resolution_result.action_taken}. Final destination: {final_destination_path}")

             else:
                 # No duplicate conflict, standard move action
                 action_description = "will_move" # Indicate the intended action before attempting move
                 final_destination_path = intended_dest_file_path
                 result_details['destination'] = final_destination_path
                 self.logger.debug(f"No duplicate for '{file_path.name}'. Will move to '{final_destination_path}'.")


             # --- Perform the Move Operation ---
             # Verify source file is still accessible immediately before the move
             try:
                 # Use fstat if possible as it's faster on an open file handle, but stat is fine here
                 file_path.stat()
                 if not file_path.exists():
                     result_details.update({
                         'action_taken': "error",
                         'reason': "source file disappeared unexpectedly before move",
                         'error_info': "FileNotFoundError: source file disappeared"
                     })
                     self.logger.error(f"Error processing '{file_path.name}': {result_details['reason']}")
                     return DuplicateResolutionResult(**result_details)
             except OSError as e:
                 result_details.update({
                     'action_taken': "error",
                     'reason': f"source file inaccessible before move: {e}",
                     'error_info': traceback.format_exc()
                 })
                 self.logger.error(f"Error processing '{file_path.name}': {result_details['reason']}", exc_info=True)
                 return DuplicateResolutionResult(**result_details)


             try:
                 # shutil.move handles cross-device moves internally by copying then deleting
                 shutil.move(str(file_path), str(final_destination_path))

                 # Success! Log the final action (moved/renamed/overwritten)
                 # Determine the final action status for the reporter based on the outcome before move
                 action_taken = result_details.get('action_taken', 'moved')
                 if action_taken == "resolved_rename":
                      final_action_status = "renamed"
                      report_reason = f"Successfully renamed to '{final_destination_path.name}'"
                 elif action_taken == "resolved_overwrite":
                      final_action_status = "overwritten"
                      report_reason = f"Successfully overwrote '{final_destination_path.name}'"
                 else: # Case "will_move" or default
                      final_action_status = "moved"
                      report_reason = f"Successfully moved to '{final_destination_path.name}'"

                 # Update result details with final successful status
                 result_details.update({
                     'action_taken': final_action_status,
                     'destination': final_destination_path, # Ensure final destination is correct in result
                     'reason': report_reason,
                     'error_info': None # Clear error info on success
                 })
                 self.logger.info(f"SUCCESS ({final_action_status}): '{file_path.name}' -> '{final_destination_path}'")
                 return DuplicateResolutionResult(**result_details) # Return success result


             except (OSError, shutil.Error, PermissionError) as e:
                 error_msg = f"Failed to move '{file_path.name}': {e}"
                 self.logger.error(error_msg, exc_info=True)
                 result_details.update({
                     'action_taken': "error",
                     'destination': final_destination_path if 'final_destination_path' in locals() else intended_dest_file_path, # Use determined path or intended
                     'reason': error_msg,
                     'error_info': traceback.format_exc()
                 })

                 # Clean up potential partial copy if move failed and left one
                 # Check if the destination file exists AND the source still exists (means move failed, not copy+delete succeeded)
                 # Use the path from result_details which is final_destination_path or intended
                 current_dest_path_attempt = Path(result_details.get('destination') or '')
                 if current_dest_path_attempt.exists() and file_path.exists():
                      try:
                           self.logger.warning(f"Attempting cleanup of potential partial copy at '{current_dest_path_attempt}'...")
                           current_dest_path_attempt.unlink()
                           self.logger.warning(f"Cleaned up partial copy at '{current_dest_path_attempt}'.")
                      except Exception as cleanup_error:
                           self.logger.error(f"Failed to clean up partial copy at '{current_dest_path_attempt}': {cleanup_error}")

                 return DuplicateResolutionResult(**result_details) # Return error result

        except Exception as e:
            # Catch any other unexpected errors during the entire _process_single_file logic
            reason = f"unexpected error during processing: {e}"
            result_details.update({'action_taken': "error", 'reason': reason, 'error_info': traceback.format_exc()})
            self.logger.critical(f"Critical error processing '{file_path.name}': {result_details['reason']}", exc_info=True)
            return DuplicateResolutionResult(**result_details) # Return error result


    def _process_files_list(self, files_to_process: List[Path], target_path: Path, dry_run: bool) -> None:
        """
        Iterates through a list of files and processes each one.
        Calls _process_single_file and logs results via reporter.
        Updates overall stats (processed, moved, skipped, errors) for the final summary.
        This method orchestrates the file processing loop.
        """
        # Start the overall timer for the run (reporter also starts its time in __init__)
        self.stats.start_time = datetime.now()
        self.stats.files_processed = len(files_to_process) # Total files entering this process list

        total_files = len(files_to_process)
        self.logger.info(f"Attempting to process {total_files} files in directory: {target_path} (Dry Run: {dry_run})")

        # Add disk space check before starting the loop
        # Estimate required space *only* for files not already skipped by initial checks
        # The list `files_to_process` already excludes initial skips from _scan_directory_for_files
        estimated_size_to_move = 0
        files_eligible_for_disk_check = [] # List of files that passed initial skip checks
        for f in files_to_process:
            try:
                if f.is_file(): # Double check it's a file
                    estimated_size_to_move += f.stat().st_size
                    files_eligible_for_disk_check.append(f)
            except Exception as e:
                self.logger.warning(f"Error checking file size for disk space estimate for '{f.name}': {e}")
                # Continue estimating with other files
                # Log errors during initial size check are logged in _scan_directory_for_files

        # Add a buffer (10% or minimum 50MB)
        required_space = estimated_size_to_move + max(estimated_size_to_move // 10, 50 * 1024 * 1024)


        if not self._check_disk_space(target_path, required_space):
            self._print_colored("❌ Operation cancelled due to insufficient disk space.", Fore.RED)
            # Log cancellation via reporter
            self.reporter.add_operation_result(DuplicateResolutionResult(
                action_taken='error', source=target_path, destination=None, category='System',
                size=0, reason="Operation cancelled due to insufficient disk space"
            ))
            # Set overall stats end time and finalize reporter on cancellation
            self.stats.end_time = datetime.now()
            self.reporter.finalize() # Finalize reporter on cancellation
            self._print_results() # Print results summarizing the cancellation
            return # Stop processing

        # Now process only the files that passed initial skip checks and disk space check
        files_to_process_actual = files_eligible_for_disk_check

        processed_count = 0
        for file_path in files_to_process_actual:
            processed_count += 1
            # Note: self.stats.files_processed is total files *scanned*, not *processed*.
            # It's updated before the loop. This is okay, it indicates the scope.

            self._show_progress(processed_count, total_files) # Show progress for files actually being processed

            # Process the single file - this method returns the result object
            result = self._process_single_file(file_path, target_path, dry_run)

            # The result is already logged by the reporter inside _process_single_file's finally block.
            # However, we still need to update the *overall* stats object in self.stats
            # which is used to determine the total counts displayed at the very end.
            # These stats are simple counters updated in _process_files_list.
            # The detailed per-category stats are managed by the reporter's internal log.

            # Update overall EnhancedFileOrganizer.stats based on the result for the final summary printout
            # Detailed counts are in the reporter's summary (get_summary_stats will recalculate from log)
            if result.action_taken in ["moved", "renamed", "overwritten"]:
                 self.stats.files_moved += 1
                 self.stats.total_size_moved += result.size # Use size from result object
            elif result.action_taken in ["skipped", "dry_run", "processed_dry_run", "skipped_by_strategy"]:
                 self.stats.files_skipped += 1
            elif result.action_taken.startswith("error"):
                 self.stats.errors += 1
            # Folder created is tracked in stats.folders_created within _process_single_file


        self._clear_progress_line() # Ensure final line is clear after progress bar
        self.stats.end_time = datetime.now()

        # Finalize the reporter run (already called if cancelled, but call again for success path)
        self.reporter.finalize()

        # Print final console summary based on reporter data and export reports
        self._print_results()

        # This method does not return stats object anymore, as stats are managed by reporter


    # --- Scan and Organize Methods ---

    def _scan_directory_for_files(self, directory: Path) -> List[Path]:
        """Scan directory and return a list of files at the top level that are eligible for processing."""
        files_list = [] # List of Path objects that passed initial skip checks
        unprocessed_items_count = 0 # Count items skipped or errored during scan

        try:
            # Convert to absolute path and ensure it exists and is a directory
            abs_dir = Path(directory).expanduser().resolve()
            if not abs_dir.exists():
                 raise FileOrganizerError(f"Directory not found: '{directory}'")
            if not abs_dir.is_dir():
                 raise FileOrganizerError(f"Path is not a directory: '{directory}'")
            if not os.access(abs_dir, os.R_OK): # Need Read permission to list contents
                 raise FileOrganizerError(f"Read permission denied for directory: '{directory}'")
            if not os.access(abs_dir, os.W_OK): # Need Write permission for potential moves/deletes
                 self.logger.warning(f"Write permission denied for directory: '{directory}'. File moves may fail.")


            self.logger.info(f"Scanning directory for files: {abs_dir}")

            try:
                # Iterate only through top-level items
                for item in abs_dir.iterdir():
                    item_path = item # Use the Path object directly
                    try:
                        # We only process files at the top level of the target directory
                        if item_path.is_file():
                             # Perform ALL initial skip checks *before* adding to the list
                             # This prevents processing files that are explicitly excluded by config
                             should_skip, skip_reason = self._should_skip_file(item_path)
                             if should_skip:
                                 self.logger.debug(f"Skipping file during scan: {item_path.name} ({skip_reason})")
                                 unprocessed_items_count += 1
                                 # Log skips happening during the initial scan via reporter
                                 try:
                                      item_size = item_path.stat().st_size if item_path.exists() else 0
                                      item_cat = self._get_destination_folder(item_path) # Try to get category for logging
                                 except Exception:
                                      item_size = 0
                                      item_cat = "Unknown"

                                 self.reporter.add_operation_result(DuplicateResolutionResult(
                                     action_taken='skipped', source=item_path, destination=None, category=item_cat,
                                     size=item_size, reason=f"skipped_during_scan: {skip_reason}"
                                 ))
                                 continue # Skip this file

                             # Add eligible file to the list
                             files_list.append(item_path)

                        elif item_path.is_dir():
                             # Log directories found but skipped (as we only process top-level files)
                             self.logger.debug(f"Skipping directory during scan: {item_path.name}")
                             unprocessed_items_count += 1
                             # Log directory skip via reporter
                             self.reporter.add_operation_result(DuplicateResolutionResult(
                                action_taken='skipped', source=item_path, destination=None, category='System',
                                size=0, reason="is a directory (top-level files only)"
                             ))

                        else:
                             # Log other item types (symlinks, devices, etc.)
                             self.logger.debug(f"Skipping non-file/non-directory item during scan: {item_path.name} ({item_path.stat().st_mode})")
                             unprocessed_items_count += 1
                             # Log other type skip via reporter
                             self.reporter.add_operation_result(DuplicateResolutionResult(
                                action_taken='skipped', source=item_path, destination=None, category='System',
                                size=0, reason="is not a file or directory"
                             ))


                    except OSError as e:
                         # Handle potential permission or other OS errors while iterating items
                         self.logger.warning(f"Skipping inaccessible item during scan: {item_path.name} ({e})")
                         unprocessed_items_count += 1
                         # Log scan errors via reporter
                         self.reporter.add_operation_result(DuplicateResolutionResult(
                            action_taken='error', source=item_path, destination=None, category='System',
                            size=0, reason=f"inaccessible_during_scan: {e}",
                            error_info=traceback.format_exc()
                         ))
                         continue # Skip item with error

                    except Exception as e:
                        self.logger.warning(f"Unexpected error scanning item {item_path.name}: {e}", exc_info=True)
                        unprocessed_items_count += 1
                        self.reporter.add_operation_result(DuplicateResolutionResult(
                            action_taken='error', source=item_path, destination=None, category='System',
                             size=0, reason=f"unexpected_scan_error: {e}",
                             error_info=traceback.format_exc()
                        ))
                        continue # Continue scanning other items

            except OSError as e:
                # Handle errors accessing the directory itself (e.g., permission denied to list)
                raise FileOrganizerError(f"Error listing contents of '{abs_dir}': {e}")


            self.logger.info(f"Finished scanning. Found {len(files_list)} eligible files at top level. {unprocessed_items_count} items were skipped or errored during scan.")
            return files_list

        except FileOrganizerError:
             # Re-raise our custom error
             raise
        except Exception as e:
             # Catch any other unexpected error during scan setup
             self.logger.critical(f"An unexpected error occurred during scan setup for '{directory}': {e}", exc_info=True)
             raise FileOrganizerError(f"An unexpected error occurred during scan setup: {e}") from e


    def organize_directory(self, target_directory: str, dry_run: bool = False) -> None:
        """
        Organize all eligible files in a given directory into subfolders based on type.
        Runs in automatic mode.

        Args:
            target_directory (str): The path to the directory to organize.
            dry_run (bool): If True, simulate the organization without moving files.

        Returns:
            None. Results are printed and logged.
        """
        target_path = Path(target_directory).expanduser().resolve()

        try:
             # Create backup *before* scanning, as scan might take time on large dirs
             self._create_backup(target_path)

             # Scan for files to process (validation happens inside)
             files_to_process = self._scan_directory_for_files(target_path)

             # Process the list of files
             self._process_files_list(files_to_process, target_path, dry_run)

        except FileOrganizerError:
             # Catch validation errors from scan or listing
             # Reporter should have logged these errors already via _scan_directory_for_files
             # The _process_files_list method handles finalization and printing if called.
             # If the error happened *before* _process_files_list (e.g. in _scan_directory_for_files),
             # we need to finalize and print here.
             if not self.stats.end_time: # Check if _process_files_list didn't run/finish
                 self.stats.start_time = self.stats.start_time or datetime.now() # Ensure start time is set
                 self.stats.end_time = datetime.now() # Set end time
                 self.reporter.finalize() # Finalize reporter
                 self._print_results() # Print results summarizing the error
             # The error is already logged and printed by main, just exit
             # re-raising signals main to exit with error code

        except Exception as e:
            # Catch any other unexpected error during automatic mode setup (before file processing loop)
            self.logger.critical(f"An unexpected error occurred during automatic organization setup: {e}", exc_info=True)
            # Log the critical error via reporter
            self.reporter.add_operation_result(DuplicateResolutionResult(
                action_taken='error', source=target_path, destination=None, category='System',
                size=0, reason=f"unexpected_execution_error: {e}", error_info=traceback.format_exc()
            ))
            # Finalize reporter and print results on unexpected error
            self.stats.start_time = self.stats.start_time or datetime.now() # Ensure start time is set
            self.stats.end_time = datetime.now() # Ensure end time is set
            self.reporter.finalize() # Finalize reporter
            self._print_results()
            # re-raising signals main to exit with error code
            raise FileOrganizerError(f"An unexpected error occurred during automatic organization setup: {e}") from e


    def interactive_mode(self, target_directory: str) -> None:
        """
        Interactive mode for organizing files with preview and confirmation.

        Args:
            target_directory: Directory to organize.

        Returns:
             None. Results are printed and logged.
        """
        target_path = Path(target_directory).expanduser().resolve()

        try:
            self._print_colored("\n" + "="*50, Fore.CYAN)
            self._print_colored("  ENHANCED FILE ORGANIZER - INTERACTIVE MODE", Fore.CYAN, Style.BRIGHT)
            self._print_colored("="*50, Fore.CYAN)
            print("\nScanning directory for files...")

            # Scan for all eligible files first (validation happens inside _scan_directory_for_files)
            all_eligible_files = self._scan_directory_for_files(target_path)

            # Files skipped/errored during scan are already logged by the reporter inside _scan_directory_for_files

            if not all_eligible_files:
                print("\nℹ️  No eligible files found to organize in the specified directory.")
                # Return empty stats (reporter is already initialized)
                self.stats.start_time = datetime.now() # Set start time even if no files
                self.stats.end_time = datetime.now()
                self.reporter.finalize() # Finalize reporter
                self._print_results() # Print results including any scan errors/skips
                return

            # Categorize eligible files based on their determined destination folder
            file_categories: Dict[str, List[Path]] = {}
            # Create a mapping of file -> category for easy lookup later
            file_to_category_map: Dict[Path, str] = {}

            print("Categorizing eligible files...")
            categorized_count = 0
            # Iterate only files returned by scan, which already passed basic eligibility
            for file_path in all_eligible_files:
                 categorized_count += 1
                 self._show_progress(categorized_count, len(all_eligible_files), description="Categorizing")
                 try:
                    # Use resolve() for get_destination_folder to be consistent with processing
                    category = self._get_destination_folder(file_path.resolve())
                    if category not in file_categories:
                        file_categories[category] = []
                    file_categories[category].append(file_path)
                    file_to_category_map[file_path] = category
                    # Log categorization result (optional, primarily for debug/detail)
                    # self.reporter.add_operation_result(DuplicateResolutionResult(
                    #     action_taken='categorized', source=file_path, category=category,
                    #     size=file_path.stat().st_size, reason=f"Categorized as {category}"
                    # ))
                 except Exception as e:
                     self.logger.error(f"Error categorizing file {file_path.name}: {e}")
                     # Log categorization error via reporter
                     self.reporter.add_operation_result(DuplicateResolutionResult(
                         action_taken='error', source=file_path, destination=None, category='Unknown',
                         size=file_path.stat().st_size if file_path.exists() else 0, reason=f"categorization_error: {e}",
                         error_info=traceback.format_exc()
                     ))
                     # Don't add to file_categories for interactive processing if categorization fails

            self._clear_progress_line() # Clear after categorization progress

            if not file_categories:
                 print("\nℹ️  No eligible files could be categorized for organization.")
                 self.stats.start_time = datetime.now() # Set start time
                 self.stats.end_time = datetime.now() # Set end time
                 self.reporter.finalize() # Finalize reporter
                 self._print_results() # Print results including any categorization errors
                 return


            # Show available categories with file counts
            print("\n📂 Found the following file categories:")
            # Sort categories alphabetically for consistent display
            sorted_categories = sorted(file_categories.keys())
            for i, category in enumerate(sorted_categories, 1):
                self._print_colored(f"  {i}. {category}: {len(file_categories[category])} files", Fore.BLUE)

            # Get user selection loop
            selected_categories_names = []
            while not selected_categories_names: # Loop until valid categories are selected
                selected_input = input("\nEnter categories to organize (comma-separated numbers/names, or 'all'): ").strip()

                if selected_input.lower() == 'all':
                    selected_categories_names = sorted_categories
                    break

                selected_items = [item.strip() for item in selected_input.split(',') if item.strip()]
                temp_selected_categories = []
                invalid_inputs = []

                for item in selected_items:
                    try:
                        # Try to get by index first (1-based)
                        category_idx = int(item) - 1
                        if 0 <= category_idx < len(sorted_categories):
                            category_name = sorted_categories[category_idx]
                            if category_name not in temp_selected_categories:
                                temp_selected_categories.append(category_name)
                            continue # Go to next item
                        else:
                            invalid_inputs.append(item) # Index out of range
                    except ValueError:
                        # If not an index, try to match category name (case-insensitive)
                        item_lower = item.lower()
                        matched_categories = [name for name in sorted_categories if name.lower() == item_lower]
                        if matched_categories:
                            # Use the first match
                            category_name = matched_categories[0]
                            if category_name not in temp_selected_categories:
                                temp_selected_categories.append(category_name)
                            continue # Go to next item
                        else:
                            invalid_inputs.append(item) # No matching name found

                selected_categories_names = temp_selected_categories # Use valid selections

                if invalid_inputs:
                    self._print_colored(f"  Warning: The following inputs were not valid categories: {', '.join(invalid_inputs)}", Fore.YELLOW)
                    # Loop will continue if selected_categories_names is still empty

            # Filter files to process based on selected categories
            files_to_process_in_interactive = []
            for category_name in selected_categories_names:
                 # Ensure category name is a key in file_categories dictionary
                 if category_name in file_categories:
                    files_to_process_in_interactive.extend(file_categories[category_name])

            if not files_to_process_in_interactive:
                 print("No files found in the selected categories. Exiting.")
                 self.stats.start_time = datetime.now() # Set start time
                 self.stats.end_time = datetime.now() # Set end time
                 self.reporter.finalize() # Finalize reporter
                 self._print_results() # Print results
                 return self.stats

            # Create backup *before* processing the selected files
            self._create_backup(target_path)

            # Show preview of organization for selected files
            print("\n📋 Preview of organization for selected files:")
            preview_count = 0
            # Sort files by name for consistent preview order
            files_to_process_in_interactive.sort(key=lambda p: p.name)

            # Calculate intended destination paths for preview
            preview_list = []
            for file_path in files_to_process_in_interactive:
                 try:
                     # Get the category again for robustness, though it was mapped before
                     category_name = self._get_destination_folder(file_path)
                     dest_folder = target_path / category_name
                     intended_dest_path = dest_folder / file_path.name
                     preview_list.append((file_path, intended_dest_path, category_name))
                 except Exception as e:
                     self.logger.error(f"Error calculating preview path for {file_path.name}: {e}", exc_info=True)
                     # Files with errors during category lookup were already skipped from all_eligible_files
                     # If an error happens *now*, log it but don't add to preview_list


            for file_path, intended_dest_path, category_name in preview_list:
                 if preview_count >= 10: # Limit preview to 10 files
                      print(f"  ... and {len(preview_list) - preview_count} more files.")
                      break

                 status_icon = "➡️" # Default status
                 status_color = Fore.BLUE
                 notes = ""

                 # Check for conflicts *at the intended destination* for preview
                 if intended_dest_path.exists():
                      status_icon = "⚠️"
                      status_color = Fore.YELLOW
                      # Perform a quick duplicate check *only for preview status*
                      try:
                          source_hash_quick = self._get_file_hash(file_path, quick_check=True)
                          dest_hash_quick = self._get_file_hash(intended_dest_path, quick_check=True)
                          if source_hash_quick is not None and dest_hash_quick is not None and source_hash_quick == dest_hash_quick:
                               notes = "(identical duplicate)"
                          else:
                               notes = "(different duplicate)"
                      except Exception:
                           notes = "(duplicate, cannot check identity)"

                 self._print_colored(f"  {status_icon} '{file_path.name}' → '{intended_dest_path}' {notes}", status_color)
                 preview_count += 1


            # Get confirmation
            confirm = input(f"\nProceed with organizing {len(files_to_process_in_interactive)} files? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Operation cancelled by user.")
                self.stats.start_time = datetime.now() # Set start time
                self.stats.end_time = datetime.now() # Set end time
                self.reporter.finalize() # Finalize reporter
                self._print_results() # Print results
                return self.stats

            # Perform organization for the selected files
            self.logger.info(f"User confirmed organization of {len(files_to_process_in_interactive)} files.")
            # Interactive mode inherently doesn't dry-run the final move stage
            return self._process_files_list(files_to_process_in_interactive, target_path, dry_run=False)

        except FileOrganizerError as e:
            # Expected errors (directory issues etc.) caught by scan method
            # Reporter has logged them already
            self.stats.start_time = datetime.now() # Set start time
            self.stats.end_time = datetime.now() # Set end time
            self.reporter.finalize() # Finalize reporter
            self._print_results() # Print results summarizing the error
            # The error message is already printed by main's handler
            return self.stats
        except Exception as e:
            # Catch any other unexpected error during interactive mode setup/flow
            self.logger.critical(f"An unexpected error occurred during interactive organization: {e}", exc_info=True)
            # Log the critical error via reporter
            self.reporter.add_operation_result(DuplicateResolutionResult(
                action_taken='error', source=target_path, destination=None, category='System',
                size=0, reason=f"unexpected_execution_error: {e}", error_info=traceback.format_exc()
            ))
            self.stats.start_time = datetime.now() # Set start time
            self.stats.end_time = datetime.now() # Set end time
            self.reporter.finalize() # Finalize reporter
            self._print_results() # Print results
            # The error message is already printed by main's handler
            return self.stats


    # --- Results Reporting ---

    def _print_results(self) -> None:
        """Print a summary of the organization results from the reporter."""
        # Ensure reporter is finalized before printing (called by _process_files_list or error handlers)
        # self.reporter.finalize() # Avoid double finalize if already called

        summary = self.reporter.get_summary_stats()

        print("\n" + "="*60)
        self._print_colored("📊 ORGANIZATION SUMMARY", Fore.MAGENTA, Style.BRIGHT)
        print("="*60)

        # Basic stats
        self._print_colored(f"✅ Files Processed: {summary['total_files_processed']}", Fore.BLUE)
        self._print_colored(f"✅ Files Moved:     {summary['files_moved']}", Fore.GREEN)
        self._print_colored(f"⏭️  Files Skipped: {summary['files_skipped']}", Fore.YELLOW)

        if summary['errors'] > 0:
            self._print_colored(f"❌ Errors:          {summary['errors']}", Fore.RED)

        print("-"*60)

        # Category breakdown
        self._print_colored("📂 CATEGORY BREAKDOWN", Fore.CYAN, Style.BRIGHT)
        # Print header with fixed widths
        header = f"{'Category':<25} {'Count':>8} {'Size (MB)':>12} {'Moved':>8} {'Skipped':>8} {'Errors':>8}"
        print(header)
        print("-" * len(header)) # Match header width

        # Sort by category name
        for category, stats in sorted(summary['categories'].items()):
            # Only show categories that had at least one file processed or error
            if stats['count'] == 0 and stats['errors'] == 0:
                 continue
            # Format each line, applying color to counts
            line = (
                f"{category:<25} "
                f"{stats['count']:>8} "
                f"{stats['size']/(1024*1024):>12.2f} "
                f"{Fore.GREEN}{stats['moved']:>8}{Style.RESET_ALL} "
                f"{Fore.YELLOW}{stats['skipped']:>8}{Style.RESET_ALL} "
                f"{Fore.RED if stats['errors'] > 0 else ''}{stats['errors']:>8}{Style.RESET_ALL if stats['errors'] > 0 else ''}"
            )
            print(line)

        # Size and time summary
        print("-" * len(header)) # Match header width
        if summary['total_size_processed'] > 0:
            size_mb_processed = summary['total_size_processed'] / (1024 * 1024)
            self._print_colored(f"📦 Total size processed: {size_mb_processed:.2f} MB", Fore.BLUE)
        if summary['total_size_moved'] > 0:
             size_mb_moved = summary['total_size_moved'] / (1024 * 1024)
             self._print_colored(f"🚚 Total size moved:     {size_mb_moved:.2f} MB", Fore.BLUE)


        duration = summary['duration_seconds']
        self._print_colored(f"⏱️  Time taken:         {duration:.2f} seconds", Fore.MAGENTA)

        # Export reports if configured
        if self.config.get('export_reports', True):
            try:
                report_formats = self.config.get('report_formats', ['text', 'csv'])
                exported = []

                for fmt in report_formats:
                    if fmt in ['text', 'csv', 'json']:
                        report_path = self.reporter.export_report(format=fmt)
                        if report_path:
                             exported.append((fmt.upper(), report_path))
                if exported:
                    # Print to console after printing summary
                    print("\n📄 ", end="")
                    self._print_colored("Exported Reports:", Fore.CYAN, Style.BRIGHT, end=" ")
                    print(", ".join([f"{fmt} ({path})" for fmt, path in exported]))

            except Exception as e:
                self.logger.error(f"Error exporting reports: {e}", exc_info=True)
                self._print_colored(f"\n⚠️  Failed to export some reports: {e}", Fore.YELLOW)

        print("="*60)


# --- Main Execution Block ---

def main():
    """Main function with command-line interface"""
    # Setup basic logging first (will be replaced by EnhancedFileOrganizer setup)
    # This ensures *some* logging exists if initialization fails early
    logging.basicConfig(level=logging.INFO, format='%(message)s') # Simpler format for early prints
    # Get the logger instance that the class will use
    logger = logging.getLogger('file_organizer')

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Enhanced File Organizer - Organize files by type with safety features."
                    "\nOrganizes files at the top level of the specified directory.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("directory", nargs="?", help="Directory to organize (optional). Defaults to current directory.")
    parser.add_argument("--dry-run", action="store_true", help="Simulate the organization process without moving any files. Only works in automatic mode (--auto).")
    parser.add_argument("--config", default="file_organizer_config.json", help="Path to the JSON configuration file. Defaults to 'file_organizer_config.json'.")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging (show DEBUG messages).")
    parser.add_argument("--auto", action="store_true", help="Run in automatic mode without prompts. By default, runs in interactive mode.")

    args = parser.parse_args()

    # Initialize the organizer (this loads config and sets up logging via _setup_logging)
    organizer = None # Initialize to None
    try:
        organizer = EnhancedFileOrganizer(config_path=args.config)
    except Exception as e:
        # Catch any errors during organizer initialization (config loading, logger setup)
        # The critical error is already logged by the logger instance inside __init__
        print(f"\n❌ Failed to initialize file organizer. Please check the log files or run with -v for details.")
        return 1 # Exit on initialization failure


    # Now that organizer is initialized and logger is set up,
    # set the console handler level based on --verbose flag
    for handler in organizer.logger.handlers:
         if isinstance(handler, logging.StreamHandler):
             handler.setLevel(logging.DEBUG if args.verbose else logging.INFO)
             break # Assuming there's only one console handler


    target_dir = args.directory
    if not target_dir:
        # If no directory provided, ask the user unless in auto mode
        if args.auto:
            target_dir = "." # Default to current directory in auto mode
            organizer.logger.info("No directory specified, defaulting to current directory in auto mode.")
        else:
            # In interactive mode, prompt if directory is missing
            # Clear any progress bar before prompting
            organizer._clear_progress_line()
            target_dir = input("Enter the directory to organize: ").strip('\"\\ \'')
            if not target_dir:
                organizer.logger.error("No directory provided. Exiting.")
                return 1 # Exit if directory is empty after prompt

    # Expand user path (like ~) and resolve to absolute path
    try:
         target_path_resolved = str(Path(target_dir).expanduser().resolve())
    except Exception as e:
         organizer.logger.error(f"Invalid target directory path '{target_dir}': {e}", exc_info=args.verbose)
         print(f"❌ Error: Invalid target directory path '{target_dir}'.")
         return 1


    try:
        # --- Main Organization Logic ---
        if args.auto:
            if args.dry_run and organizer.config.get("duplicate_resolution") == "ask":
                # Warn if ask strategy is set but running dry-run auto
                organizer.logger.warning("Duplicate resolution is set to 'ask' in config, but running in automatic mode. 'ask' will be ignored. Consider changing strategy to 'skip', 'rename', or 'overwrite' for auto mode.")
                # The automatic mode (_process_files_list called by organize_directory) handles non-ask strategies correctly.

            organizer.organize_directory(target_path_resolved, dry_run=args.dry_run)

        else: # Interactive mode
            if args.dry_run:
                organizer.logger.warning("The --dry-run flag is ignored in interactive mode. The preview step is a simulation, but the final confirmation will perform real actions.")
            # Interactive mode inherently doesn't dry-run the final move stage
            organizer.interactive_mode(target_path_resolved)

        # Final message after successful run
        # _process_files_list or interactive_mode will finalize the reporter and print results
        pass

    except FileOrganizerError:
        # These are anticipated errors (bad directory, permissions, disk space etc.)
        # These errors are raised by methods like _scan_directory_for_files and caught
        # by the main organize_directory or interactive_mode try blocks, which log the error,
        # finalize the reporter, print results, and then re-raise.
        # The main block here just catches the re-raised error to exit with code 1.
        # The error message is already printed by the catching block's _print_results call.
        return 1 # Exit with error code

    except KeyboardInterrupt:
        # User cancelled the operation (e.g., during interactive prompt or progress)
        if organizer and hasattr(organizer, '_clear_progress_line'):
            organizer._clear_progress_line()  # Clear progress bar if active
        print("\nOperation cancelled by user.")
        if organizer and organizer.logger:
             organizer.logger.warning("Operation cancelled by user.")
             # Reporter might not be finalized or reflect cancellation accurately
             # For now, logging message and clean exit is okay.
             # A more advanced reporter could listen for KeyboardInterrupt.

        return 1
    except Exception as e:
        # Catch any other unexpected errors during the main execution flow
        # This should be rare with robust handling in processing methods
        if organizer and organizer.logger:
             organizer.logger.critical(f"An unexpected critical error occurred during execution: {e}", exc_info=args.verbose)
             # Log the critical error via reporter if possible
             if hasattr(organizer, 'reporter'):
                 organizer.reporter.add_operation_result(DuplicateResolutionResult(
                    action_taken='error', source=Path("."), destination=None, category='System',
                    size=0, reason=f"unexpected_execution_error: {e}", error_info=traceback.format_exc()
                 ))
                 organizer.stats.end_time = datetime.now() # Ensure end time is set
                 organizer.reporter.finalize() # Finalize reporter
                 organizer._print_results() # Print results including the error

        else:
             # If organizer/logger failed initialization, use basic print/logging
             logging.critical(f"An unexpected critical error occurred during execution: {e}", exc_info=args.verbose)

        print(f"\n❌ An unexpected critical error occurred: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    # When run directly, call the main function
    exit(main())
