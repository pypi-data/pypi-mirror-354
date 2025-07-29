"""
Utility functions for CarinaNet package
"""

import os
import requests
import shutil
from pathlib import Path
from typing import Optional
from tqdm import tqdm

try:
    from huggingface_hub import hf_hub_download
    HF_HUB_AVAILABLE = True
except ImportError:
    HF_HUB_AVAILABLE = False


def get_home_dir() -> Path:
    """Get CarinaNet home directory for storing models and config."""
    home_dir = os.environ.get("CARINANET_HOME", Path.home() / ".carinanet")
    return Path(home_dir)


def get_weights_dir() -> Path:
    """Get directory where model weights are stored."""
    weights_dir = get_home_dir() / "weights"
    weights_dir.mkdir(parents=True, exist_ok=True)
    return weights_dir


def get_default_weights_path() -> str:
    """Get path to default model weights."""
    return str(get_weights_dir() / "model.pt")


def get_package_model_path() -> str:
    """Get path to the model bundled with the package."""
    package_dir = Path(__file__).parent
    return str(package_dir / "models" / "model.pt")


def download_file(url: str, destination: str, description: str = "Downloading") -> None:
    """Download file with progress bar."""
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    
    with open(destination, 'wb') as file, tqdm(
        desc=description,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for chunk in response.iter_content(chunk_size=8192):
            size = file.write(chunk)
            progress_bar.update(size)


def download_from_huggingface(repo_id: str = "rajpurkarlab/carinanet", 
                             filename: str = "model.pt",
                             cache_dir: Optional[str] = None) -> str:
    """
    Download model from Hugging Face Hub.
    
    Args:
        repo_id: Hugging Face repository ID
        filename: Name of the file to download
        cache_dir: Cache directory (uses default if None)
        
    Returns:
        Path to downloaded file
    """
    if not HF_HUB_AVAILABLE:
        raise ImportError("huggingface_hub is required for downloading from HF Hub. Install with: pip install huggingface_hub")
    
    if cache_dir is None:
        cache_dir = str(get_weights_dir())
    
    try:
        print(f"📥 Downloading {filename} from Hugging Face Hub...")
        print(f"   Repository: {repo_id}")
        
        # Download file to cache directory
        downloaded_path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            cache_dir=cache_dir,
            local_dir=cache_dir,
            local_dir_use_symlinks=False
        )
        
        # If the file was downloaded to a subfolder, move it to the weights directory
        target_path = get_weights_dir() / filename
        if downloaded_path != str(target_path):
            shutil.move(downloaded_path, target_path)
            downloaded_path = str(target_path)
        
        print(f"✅ Downloaded successfully to: {downloaded_path}")
        return downloaded_path
        
    except Exception as e:
        raise RuntimeError(f"Failed to download from Hugging Face Hub: {e}")


def download_weights(model_name: str = "model.pt", 
                    force_download: bool = False,
                    use_huggingface: bool = True) -> str:
    """
    Download model weights from remote location.
    
    Args:
        model_name: Name of the model weights file
        force_download: Whether to force re-download if file exists
        use_huggingface: Whether to use Hugging Face Hub (recommended)
        
    Returns:
        Path to downloaded weights file
    """
    weights_dir = get_weights_dir()
    weights_path = weights_dir / model_name
    
    if weights_path.exists() and not force_download:
        print(f"Model weights already exist at {weights_path}")
        return str(weights_path)
    
    # First check if we have a bundled model
    package_model_path = get_package_model_path()
    if os.path.exists(package_model_path):
        print(f"Using bundled model from {package_model_path}")
        shutil.copy2(package_model_path, weights_path)
        return str(weights_path)
    
    # Try downloading from Hugging Face Hub (recommended)
    if use_huggingface and HF_HUB_AVAILABLE:
        try:
            return download_from_huggingface(filename=model_name)
        except Exception as e:
            print(f"⚠️  Hugging Face download failed: {e}")
            print("Falling back to direct download...")
    
    # Fallback to direct download (for backwards compatibility)
    model_urls = {
        "model.pt": "https://huggingface.co/rajpurkarlab/carinanet/resolve/main/model.pt"
    }
    
    if model_name not in model_urls:
        raise ValueError(f"Unknown model: {model_name}")
    
    url = model_urls[model_name]
    
    print(f"Downloading {model_name} from {url}...")
    try:
        download_file(url, str(weights_path), f"Downloading {model_name}")
        print(f"Successfully downloaded model weights to {weights_path}")
    except Exception as e:
        if weights_path.exists():
            weights_path.unlink()  # Remove partial download
        raise RuntimeError(f"Failed to download model weights: {e}")
    
    return str(weights_path)


def setup_model_from_existing_checkpoint(checkpoint_path: str) -> str:
    """
    Copy existing model checkpoint to the package weights directory.
    
    This is useful during development when you have a local checkpoint.
    
    Args:
        checkpoint_path: Path to existing checkpoint
        
    Returns:
        Path to copied weights file
    """
    if not os.path.exists(checkpoint_path):
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")
    
    weights_dir = get_weights_dir()
    destination = weights_dir / "model.pt"
    
    print(f"Copying {checkpoint_path} to {destination}")
    shutil.copy2(checkpoint_path, destination)
    print(f"Model weights setup complete at {destination}")
    
    return str(destination)


def list_available_models() -> list:
    """List all available model weights."""
    weights_dir = get_weights_dir()
    if not weights_dir.exists():
        return []
    
    return [f.name for f in weights_dir.iterdir() if f.suffix in ['.pt', '.pth']]


def get_model_info() -> dict:
    """Get information about installed models."""
    weights_dir = get_weights_dir()
    models = list_available_models()
    
    package_model_path = get_package_model_path()
    package_model_exists = os.path.exists(package_model_path)
    
    default_weights_path = get_default_weights_path()
    default_model_exists = os.path.exists(default_weights_path)
    
    info = {
        "weights_directory": str(weights_dir),
        "installed_models": models,
        "default_model": "model.pt",
        "default_model_exists": default_model_exists,
        "package_model_path": package_model_path,
        "package_model_exists": package_model_exists,
        "huggingface_hub_available": HF_HUB_AVAILABLE,
        "huggingface_repo": "rajpurkarlab/carinanet",
    }
    
    return info 