"""Base model classes for NuroMind"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Union, List
from pathlib import Path
import json
import torch
import torch.nn as nn

logger = logging.getLogger(__name__)


class BaseModel(ABC):
    """Abstract base class for all NuroMind models"""
    
    def __init__(
        self,
        model_name: str,
        device: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize base model
        
        Args:
            model_name: Name identifier for the model
            device: Computing device (cuda/cpu/auto)
            config: Model configuration dictionary
        """
        self.model_name = model_name
        self.config = config or {}
        self.device = self._setup_device(device)
        self.model = None
        self.is_trained = False
        
        logger.info(f"Initializing {self.__class__.__name__}: {model_name}")
    
    def _setup_device(self, device: Optional[str]) -> torch.device:
        """Set up computing device"""
        if device == "auto" or device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            
        device_obj = torch.device(device)
        logger.info(f"Using device: {device_obj}")
        return device_obj
    
    @abstractmethod
    def forward(self, *args, **kwargs) -> Any:
        """Forward pass of the model"""
        pass
    
    @abstractmethod
    def predict(self, *args, **kwargs) -> Any:
        """Make predictions"""
        pass
    
    def save(self, path: Union[str, Path]) -> None:
        """
        Save model to disk
        
        Args:
            path: Path to save model
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        checkpoint = {
            'model_name': self.model_name,
            'model_state_dict': self.model.state_dict() if self.model else None,
            'config': self.config,
            'is_trained': self.is_trained,
            'model_class': self.__class__.__name__
        }
        
        torch.save(checkpoint, path)
        logger.info(f"Model saved to {path}")
    
    def load(self, path: Union[str, Path]) -> None:
        """
        Load model from disk
        
        Args:
            path: Path to load model from
        """
        path = Path(path)
        
        if not path.exists():
            raise FileNotFoundError(f"Model file not found: {path}")
        
        checkpoint = torch.load(path, map_location=self.device)
        
        self.model_name = checkpoint['model_name']
        self.config = checkpoint['config']
        self.is_trained = checkpoint['is_trained']
        
        if self.model and checkpoint['model_state_dict']:
            self.model.load_state_dict(checkpoint['model_state_dict'])
        
        logger.info(f"Model loaded from {path}")
    
    def get_params(self) -> Dict[str, Any]:
        """Get model parameters"""
        return {
            'model_name': self.model_name,
            'config': self.config,
            'device': str(self.device),
            'is_trained': self.is_trained,
            'n_parameters': self.count_parameters() if self.model else 0
        }
    
    def count_parameters(self) -> int:
        """Count number of trainable parameters"""
        if not self.model:
            return 0
        return sum(p.numel() for p in self.model.parameters() if p.requires_grad)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.model_name}', device='{self.device}')"


class BaseNeuralNetwork(BaseModel, nn.Module):
    """Base class for neural network models"""
    
    def __init__(self, model_name: str, input_dim: int, output_dim: int, **kwargs):
        """
        Initialize neural network base
        
        Args:
            model_name: Model identifier
            input_dim: Input dimension
            output_dim: Output dimension
            **kwargs: Additional arguments
        """
        nn.Module.__init__(self)
        BaseModel.__init__(self, model_name, **kwargs)
        
        self.input_dim = input_dim
        self.output_dim = output_dim
        self._build_model()
    
    @abstractmethod
    def _build_model(self) -> None:
        """Build the neural network architecture"""
        pass
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass
        
        Args:
            x: Input tensor
            
        Returns:
            Output tensor
        """
        if self.model is None:
            raise RuntimeError("Model not built. Call _build_model() first.")
        return self.model(x)


class EnsembleModel(BaseModel):
    """Base class for ensemble models"""
    
    def __init__(
        self,
        model_name: str,
        base_models: List[BaseModel],
        aggregation: str = "mean",
        **kwargs
    ):
        """
        Initialize ensemble model
        
        Args:
            model_name: Ensemble model name
            base_models: List of base models
            aggregation: Aggregation method (mean/weighted/voting)
            **kwargs: Additional arguments
        """
        super().__init__(model_name, **kwargs)
        
        self.base_models = base_models
        self.aggregation = aggregation
        self.weights = None
        
        if aggregation == "weighted":
            self.weights = nn.Parameter(torch.ones(len(base_models)) / len(base_models))
    
    def forward(self, *args, **kwargs) -> Any:
        """Ensemble forward pass"""
        outputs = []
        
        for model in self.base_models:
            output = model.forward(*args, **kwargs)
            outputs.append(output)
        
        return self._aggregate(outputs)
    
    def _aggregate(self, outputs: List[torch.Tensor]) -> torch.Tensor:
        """Aggregate outputs from base models"""
        if self.aggregation == "mean":
            return torch.stack(outputs).mean(dim=0)
        elif self.aggregation == "weighted":
            weights = torch.softmax(self.weights, dim=0)
            weighted_outputs = [w * out for w, out in zip(weights, outputs)]
            return torch.stack(weighted_outputs).sum(dim=0)
        elif self.aggregation == "voting":
            # For classification
            votes = torch.stack(outputs).argmax(dim=-1)
            return torch.mode(votes, dim=0).values
        else:
            raise ValueError(f"Unknown aggregation method: {self.aggregation}")
    
    def predict(self, *args, **kwargs) -> Any:
        """Make ensemble predictions"""
        self.eval()
        with torch.no_grad():
            return self.forward(*args, **kwargs)
