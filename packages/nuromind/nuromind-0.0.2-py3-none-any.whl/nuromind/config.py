"""Configuration management for NuroMind"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, field


@dataclass
class Config:
    """NuroMind configuration"""
    
    # Device settings
    device: str = "auto"
    
    # Path settings
    cache_dir: Optional[Path] = None
    data_dir: Optional[Path] = None
    model_dir: Optional[Path] = None
    
    # Logging
    log_level: str = "INFO"
    log_file: Optional[Path] = None
    
    # Model settings
    default_model: str = "base"
    batch_size: int = 32
    
    # API settings
    openai_api_key: Optional[str] = field(default=None, repr=False)
    hf_token: Optional[str] = field(default=None, repr=False)
    
    def __post_init__(self):
        """Initialize paths and load environment variables"""
        # Set up default paths
        home = Path.home()
        base_dir = home / ".nuromind"
        
        self.cache_dir = self.cache_dir or base_dir / "cache"
        self.data_dir = self.data_dir or base_dir / "data"
        self.model_dir = self.model_dir or base_dir / "models"
        
        # Create directories
        for dir_path in [self.cache_dir, self.data_dir, self.model_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Load from environment
        self.openai_api_key = self.openai_api_key or os.getenv("OPENAI_API_KEY")
        self.hf_token = self.hf_token or os.getenv("HF_TOKEN")
        
        # Auto-detect device
        if self.device == "auto":
            self.device = self._detect_device()
    
    def _detect_device(self) -> str:
        """Detect available computing device"""
        try:
            import torch
            return "cuda" if torch.cuda.is_available() else "cpu"
        except ImportError:
            return "cpu"


# Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get global configuration instance"""
    global _config
    if _config is None:
        _config = Config()
    return _config


def set_config(config: Config) -> None:
    """Set global configuration"""
    global _config
    _config = config
