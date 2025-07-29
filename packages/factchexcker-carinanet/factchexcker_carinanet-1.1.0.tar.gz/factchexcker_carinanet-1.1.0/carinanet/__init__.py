"""
CarinaNet: Automatic detection of carina and ETT in chest X-rays using deep learning.

This package provides tools for detecting anatomical landmarks (carina and ETT) 
in chest X-ray images using a RetinaNet-based deep learning model.
"""

__version__ = "1.1.0"
__author__ = "Xiaoman Zhang"
__email__ = "xiaomanzhang.zxm@gmail.com"

from .api import predict_carina_ett, CarinaNetModel
from .utils import download_weights, get_default_weights_path, get_model_info

__all__ = [
    "predict_carina_ett",
    "CarinaNetModel", 
    "download_weights",
    "get_default_weights_path",
    "get_model_info",
] 