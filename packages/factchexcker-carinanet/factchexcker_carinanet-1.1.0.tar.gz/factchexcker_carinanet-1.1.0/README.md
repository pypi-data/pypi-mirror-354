# CarinaNet

[![PyPI version](https://badge.fury.io/py/carinanet.svg)](https://badge.fury.io/py/carinanet)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Automatic detection of **carina** and **ETT (endotracheal tube)** in chest X-rays using deep learning. CarinaNet provides a simple, pip-installable package for medical image analysis with state-of-the-art accuracy.

## Features

- 🔬 **Medical AI**: Specialized for carina and ETT detection in chest X-rays
- 🚀 **Easy to Use**: Simple Python API and command-line interface
- 🎯 **High Accuracy**: Based on RetinaNet architecture optimized for medical imaging
- 📦 **Pip Installable**: Just `pip install carinanet` and you're ready to go
- 🔧 **Flexible Input**: Supports various image formats (JPG, PNG, DICOM)
- 💾 **Bundled Model**: Pre-trained weights included - no separate downloads needed

## Installation

Install CarinaNet with pip:

```bash
pip install carinanet
```

## Quick Start

### Python API

```python
import carinanet

# Simple prediction on an image file
result = carinanet.predict_carina_ett("chest_xray.jpg")
print(f"Carina: {result['carina']}")
print(f"ETT: {result['ett']}")
print(f"Carina confidence: {result['carina_confidence']}")
print(f"ETT confidence: {result['ett_confidence']}")

# Using the model class for multiple predictions
model = carinanet.CarinaNetModel()
result = model.predict("chest_xray.jpg")

# Works with PIL Images and numpy arrays too
from PIL import Image
import numpy as np

image = Image.open("chest_xray.jpg")
result = carinanet.predict_carina_ett(image)

# Or with numpy arrays
image_array = np.array(image)
result = carinanet.predict_carina_ett(image_array)
```

### Command Line Interface

```bash
# Predict on a single image
carinanet predict chest_xray.jpg

# Get package information
carinanet info

# Show help
carinanet --help
```

## Output Format

CarinaNet returns predictions as dictionaries with the following structure:

```python
{
    'carina': (x, y),           # Carina coordinates
    'ett': (x, y),              # ETT coordinates  
    'carina_confidence': 0.95,  # Confidence score (0-1)
    'ett_confidence': 0.87      # Confidence score (0-1)
}
```

Coordinates are in image pixel space (x, y) where (0, 0) is the top-left corner.

## Requirements

- Python 3.8+
- PyTorch 1.9+
- See `requirements.txt` for full dependency list

## Model Information

CarinaNet uses a RetinaNet-based architecture fine-tuned specifically for carina and ETT detection in chest X-rays. The model:

- **Architecture**: RetinaNet with ResNet backbone
- **Input Size**: 640x640 pixels (automatically resized)
- **Output**: Bounding box coordinates converted to center points
- **Training Data**: Curated medical imaging dataset
- **Performance**: High accuracy on clinical validation sets

## Use Cases

CarinaNet is designed for:

- 🏥 **Clinical Decision Support**: Assist radiologists in identifying anatomical landmarks
- 📊 **Research**: Batch processing of chest X-ray datasets
- 🎓 **Education**: Teaching anatomical landmark identification
- 🔬 **Quality Control**: Automated verification of ETT placement

## Device Support

CarinaNet automatically detects and uses:
- **GPU**: CUDA-enabled GPUs for faster inference
- **CPU**: Fallback to CPU if GPU not available
- **Apple Silicon**: Optimized for M1/M2 Macs

## Contributing

We welcome contributions! Please see our contributing guidelines for details.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Citation

If you use CarinaNet in your research, please cite:

```bibtex
@misc{heiman2025factchexckermitigatingmeasurementhallucinations,
      title={FactCheXcker: Mitigating Measurement Hallucinations in Chest X-ray Report Generation Models}, 
      author={Alice Heiman and Xiaoman Zhang and Emma Chen and Sung Eun Kim and Pranav Rajpurkar},
      year={2025},
      eprint={2411.18672},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2411.18672}, 
}
```

## Support

- 📖 **Documentation**: See this README and inline documentation
- 🐛 **Issues**: Report bugs on [GitHub Issues](https://github.com/rajpurkarlab/carinanet/issues)
- 💬 **Discussions**: Join our [GitHub Discussions](https://github.com/rajpurkarlab/carinanet/discussions)

---

**Disclaimer**: CarinaNet is intended for research and educational purposes. It should not be used as the sole basis for clinical decisions. Always consult with qualified medical professionals.
