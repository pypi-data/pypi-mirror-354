"""
NuroMind - A comprehensive neuroscience ML library for Alzheimer's disease and microbiome research
Developed at UMass Chan Medical School, Microbiology & Microbiome Dynamics AI HUB
"""

__version__ = "0.0.2"
__author__ = "Ziyuan Huang"
__email__ = "ziyuan.huang2@umassmed.edu"
__organization__ = "UMass Chan Medical School"
__labs__ = ["Microbiology & Microbiome Dynamics AI HUB", "Haran Research Group", "Bucci Lab"]

from .core import NuroMindCore
from .config import Config, get_config

__all__ = [
    "NuroMindCore",
    "Config",
    "get_config",
    "__version__",
    "__author__",
    "__email__",
    "__organization__",
    "__labs__"
]
