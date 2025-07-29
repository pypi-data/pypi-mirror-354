"""Utility functions for NuroMind"""

import logging
import sys
from pathlib import Path
from typing import Optional, Union, Any
import json
import yaml


def setup_logging(
    level: Union[str, int] = "INFO",
    log_file: Optional[Path] = None,
    format_string: Optional[str] = None
) -> None:
    """
    Set up logging configuration
    
    Args:
        level: Logging level
        log_file: Optional file to write logs to
        format_string: Custom format string
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    handlers = [logging.StreamHandler(sys.stdout)]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=level,
        format=format_string,
        handlers=handlers
    )


def load_config_file(path: Union[str, Path]) -> Dict[str, Any]:
    """Load configuration from YAML or JSON file"""
    path = Path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    
    with open(path, 'r') as f:
        if path.suffix in ['.yaml', '.yml']:
            return yaml.safe_load(f)
        elif path.suffix == '.json':
            return json.load(f)
        else:
            raise ValueError(f"Unsupported config format: {path.suffix}")


def ensure_path(path: Union[str, Path]) -> Path:
    """Ensure a path exists and return as Path object"""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


class NuroMindError(Exception):
    """Base exception for NuroMind"""
    pass


class DataError(NuroMindError):
    """Exception for data-related errors"""
    pass


class ModelError(NuroMindError):
    """Exception for model-related errors"""
    pass
