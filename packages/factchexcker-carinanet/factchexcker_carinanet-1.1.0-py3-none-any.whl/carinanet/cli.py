"""
Command line interface for CarinaNet
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from . import predict_carina_ett
from .utils import download_weights, setup_model_from_existing_checkpoint, get_model_info


def predict_command(args):
    """Run prediction on input image."""
    try:
        result = predict_carina_ett(
            args.input,
            model_path=args.model_path,
            device=args.device,
            return_confidence=not args.no_confidence
        )
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Results saved to {args.output}")
        else:
            print(json.dumps(result, indent=2))
            
    except Exception as e:
        print(f"Error during prediction: {e}", file=sys.stderr)
        sys.exit(1)


def download_command(args):
    """Download model weights."""
    try:
        weights_path = download_weights(force_download=args.force)
        print(f"Model weights downloaded to: {weights_path}")
    except Exception as e:
        print(f"Error downloading weights: {e}", file=sys.stderr)
        sys.exit(1)


def info_command(args):
    """Show package information."""
    info = get_model_info()
    print(json.dumps(info, indent=2))


def setup_command(args):
    """Setup model from existing checkpoint."""
    try:
        weights_path = setup_model_from_existing_checkpoint(args.checkpoint)
        print(f"Model setup complete: {weights_path}")
    except Exception as e:
        print(f"Error setting up model: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="CarinaNet: Automatic detection of carina and ETT in chest X-rays",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Predict on a single image
  carinanet predict chest_xray.jpg
  
  # Save results to file
  carinanet predict chest_xray.jpg -o results.json
  
  # Use CPU only
  carinanet predict chest_xray.jpg --device cpu
  
  # Download model weights
  carinanet download-weights
  
  # Show package info
  carinanet info
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Predict command
    predict_parser = subparsers.add_parser('predict', help='Run prediction on chest X-ray')
    predict_parser.add_argument('input', help='Input image path')
    predict_parser.add_argument('-o', '--output', help='Output JSON file path')
    predict_parser.add_argument('--model-path', help='Path to model weights file')
    predict_parser.add_argument('--device', choices=['cpu', 'cuda', 'auto'], default='auto',
                               help='Device to use for inference')
    predict_parser.add_argument('--no-confidence', action='store_true',
                               help='Do not return confidence scores')
    predict_parser.set_defaults(func=predict_command)
    
    # Download weights command
    download_parser = subparsers.add_parser('download-weights', help='Download model weights')
    download_parser.add_argument('--force', action='store_true',
                                help='Force re-download even if weights exist')
    download_parser.set_defaults(func=download_command)
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show package information')
    info_parser.set_defaults(func=info_command)
    
    # Setup command (for development)
    setup_parser = subparsers.add_parser('setup', help='Setup model from existing checkpoint')
    setup_parser.add_argument('checkpoint', help='Path to existing checkpoint file')
    setup_parser.set_defaults(func=setup_command)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == '__main__':
    main() 