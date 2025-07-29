"""Tests for NuroMind core functionality"""

import pytest
from nuromind import NuroMindConfig, check_dependencies, get_device


def test_nuromind_config():
    """Test NuroMindConfig initialization"""
    config = NuroMindConfig()
    
    assert config.device in ["cuda", "cpu"]
    assert config.model_cache_dir.exists()
    assert config.data_cache_dir.exists()
    assert config.hf_cache_dir.exists()
    assert config.organization == "UMass Chan Medical School"


def test_check_dependencies():
    """Test dependency checking"""
    deps = check_dependencies()
    
    assert isinstance(deps, dict)
    assert "PyTorch" in deps
    assert "Transformers" in deps
    assert all(isinstance(v, bool) for v in deps.values())


def test_get_device():
    """Test device detection"""
    device = get_device()
    assert device in ["cuda", "cpu"]


if __name__ == "__main__":
    pytest.main([__file__])
