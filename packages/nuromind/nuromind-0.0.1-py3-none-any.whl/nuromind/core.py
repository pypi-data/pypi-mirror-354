"""Core functionality for NuroMind"""

import logging
from typing import Optional, Dict, Any
from .config import Config
from .utils import setup_logging

logger = logging.getLogger(__name__)


class NuroMindCore:
    """Main entry point for NuroMind functionality"""
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize NuroMind core
        
        Args:
            config: Configuration object. If None, uses default config.
        """
        self.config = config or Config()
        setup_logging(self.config.log_level)
        logger.info(f"Initializing NuroMind v{__import__('nuromind').__version__}")
        
    def check_dependencies(self) -> Dict[str, bool]:
        """Check if all required dependencies are installed"""
        dependencies = {
            "torch": "PyTorch",
            "transformers": "Transformers",
            "monai": "MONAI",
            "langchain": "LangChain",
        }
        
        status = {}
        for module, name in dependencies.items():
            try:
                __import__(module)
                status[name] = True
                logger.debug(f"{name} is available")
            except ImportError:
                status[name] = False
                logger.warning(f"{name} is not installed")
        
        return status
    
    def __repr__(self) -> str:
        return f"NuroMindCore(config={self.config})"
