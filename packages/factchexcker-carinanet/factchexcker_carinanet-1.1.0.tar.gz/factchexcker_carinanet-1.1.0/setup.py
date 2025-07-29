from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="factchexcker-carinanet",
    version="1.1.0",
    author="Xiaoman Zhang",
    author_email="xiaomanzhang.zxm@gmail.com",
    description="Automatic detection of carina and ETT in chest X-rays using deep learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rajpurkarlab/carinanet",
    project_urls={
        "Homepage": "https://github.com/rajpurkarlab/carinanet",
        "Repository": "https://github.com/rajpurkarlab/carinanet",
        "Issues": "https://github.com/rajpurkarlab/carinanet/issues",
        "Documentation": "https://github.com/rajpurkarlab/carinanet#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Healthcare Industry",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Image Processing",
    ],
    python_requires=">=3.8",
    install_requires=[
        "torch>=1.9.0",
        "torchvision>=0.10.0",
        "Pillow>=8.0.0",
        "numpy>=1.19.0",
        "requests>=2.25.0",
        "tqdm>=4.60.0",
        "kwcoco>=0.2.0",
        "pandas>=1.3.0",
        "scikit-image>=0.18.0",
        "pycocotools>=2.0.0",
        "huggingface_hub>=0.15.0",
    ],
    extras_require={
        "dev": ["wandb", "pytest", "black", "isort", "mypy"],
    },
    entry_points={
        "console_scripts": [
            "carinanet=carinanet.cli:main",
        ],
    },
    include_package_data=True,
    keywords=["medical", "ai", "chest-xray", "carina", "ett", "deep-learning", "computer-vision", "medical-imaging"],
) 