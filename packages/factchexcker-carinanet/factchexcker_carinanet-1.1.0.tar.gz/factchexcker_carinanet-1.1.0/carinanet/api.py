"""
Main API for CarinaNet model inference
"""

import os
import torch
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
from typing import Union, Tuple, Dict, Optional
from pathlib import Path

from .models.carinanet_model import CarinaNetModel as _CarinaNetModel
from .utils import download_weights, get_default_weights_path, get_package_model_path


class CarinaNetModel:
    """
    CarinaNet model for detecting carina and ETT in chest X-rays.
    
    This class provides a simple interface for loading the model and making predictions.
    """
    
    def __init__(self, model_path: Optional[str] = None, device: Optional[str] = None):
        """
        Initialize CarinaNet model.
        
        Args:
            model_path (str, optional): Path to model weights. If None, will use bundled or downloaded weights.
            device (str, optional): Device to run model on ('cpu', 'cuda', 'auto'). If None, auto-detect.
        """
        self.device = self._get_device(device)
        
        if model_path is None:
            # First try the bundled model
            package_model_path = get_package_model_path()
            if os.path.exists(package_model_path):
                model_path = package_model_path
                print("Using bundled model")
            else:
                # Fall back to downloaded model
                model_path = get_default_weights_path()
                if not os.path.exists(model_path):
                    print("Downloading CarinaNet model weights...")
                    download_weights()
        
        self.model_path = model_path
        self.model = self._load_model()
        
    def _get_device(self, device: Optional[str]) -> str:
        """Get appropriate device for inference."""
        if device == 'auto' or device is None:
            return 'cuda' if torch.cuda.is_available() else 'cpu'
        return device
    
    def _load_model(self) -> _CarinaNetModel:
        """Load the CarinaNet model."""
        try:
            # Use None for update_method since we're only doing inference
            model = _CarinaNetModel(self.model_path, update_method=None)
            if self.device == 'cuda' and torch.cuda.is_available():
                model.model = model.model.cuda()
            else:
                model.model = model.model.cpu()
            return model
        except Exception as e:
            raise RuntimeError(f"Failed to load CarinaNet model: {e}")
    
    def preprocess_image(self, image_input: Union[str, Path, Image.Image, np.ndarray], 
                        target_size: int = 640) -> torch.Tensor:
        """
        Preprocess input image for model inference.
        
        Args:
            image_input: Input image (file path, PIL Image, or numpy array)
            target_size: Target size for resizing
            
        Returns:
            Preprocessed tensor ready for model input
        """
        # Handle different input types
        if isinstance(image_input, (str, Path)):
            image = Image.open(image_input).convert("RGB")
        elif isinstance(image_input, Image.Image):
            image = image_input.convert("RGB")
        elif isinstance(image_input, np.ndarray):
            image = Image.fromarray(image_input).convert("RGB")
        else:
            raise ValueError("Unsupported image input type")
        
        # Resize and convert to tensor
        image = image.resize((target_size, target_size), Image.BICUBIC)
        transform = transforms.ToTensor()
        tensor_image = transform(image)
        
        # Move to device if needed
        if self.device == 'cuda' and torch.cuda.is_available():
            tensor_image = tensor_image.cuda()
            
        return tensor_image
    
    def predict(self, image_input: Union[str, Path, Image.Image, np.ndarray], 
                return_confidence: bool = True) -> Dict[str, Union[Tuple[float, float], float]]:
        """
        Predict carina and ETT locations in chest X-ray.
        
        Args:
            image_input: Input image (file path, PIL Image, or numpy array)
            return_confidence: Whether to return confidence scores
            
        Returns:
            Dictionary containing predicted coordinates for carina and ETT
        """
        tensor_image = self.preprocess_image(image_input)
        
        # Create dummy image ID for the model
        image_id = "prediction"
        images_and_ids = [(tensor_image, image_id)]
        
        # Get predictions from model
        predictions = self.model.predict(images_and_ids)
        pred = predictions[image_id]
        
        result = {}
        
        # Extract predictions for each class (0=carina, 1=ett)
        for class_id, class_name in [(0, "carina"), (1, "ett")]:
            if class_id in pred and "pred" in pred[class_id]:
                result[class_name] = tuple(pred[class_id]["pred"])
                if return_confidence and "confidence" in pred[class_id]:
                    result[f"{class_name}_confidence"] = pred[class_id]["confidence"]
            else:
                # Default fallback if not found
                result[class_name] = (0.0, 0.0)
                if return_confidence:
                    result[f"{class_name}_confidence"] = 0.0
        
        return result


def predict_carina_ett(image_input: Union[str, Path, Image.Image, np.ndarray],
                      model_path: Optional[str] = None,
                      device: Optional[str] = None,
                      return_confidence: bool = True) -> Dict[str, Union[Tuple[float, float], float]]:
    """
    Simple function to predict carina and ETT locations in a chest X-ray.
    
    Args:
        image_input: Input image (file path, PIL Image, or numpy array)
        model_path: Optional path to model weights
        device: Device to run on ('cpu', 'cuda', 'auto')
        return_confidence: Whether to return confidence scores
        
    Returns:
        Dictionary containing predicted coordinates for carina and ETT
        
    Example:
        >>> import carinanet
        >>> result = carinanet.predict_carina_ett("chest_xray.jpg")
        >>> print(f"Carina: {result['carina']}, ETT: {result['ett']}")
    """
    model = CarinaNetModel(model_path=model_path, device=device)
    return model.predict(image_input, return_confidence=return_confidence) 