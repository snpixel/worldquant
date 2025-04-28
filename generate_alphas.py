#!/usr/bin/env python3
"""
Alpha Generator for WorldQuant

This script generates alpha expressions that can be manually submitted to WorldQuant.
"""
import argparse
import json
import logging
import os
import sys
from datetime import datetime

from alpha_engine.generator import AlphaGenerator
from alpha_engine.optimizer import AlphaOptimizer
from alpha_engine.validator import AlphaValidator
from ui.display import display_alphas
from utils.api_client import WorldQuantClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('alpha_generator.log')
    ]
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Generate alphas for WorldQuant')
    parser.add_argument('--credentials', type=str, default='./data/credentials.json',
                      help='Path to credentials file (default: ./data/credentials.json)')
    parser.add_argument('--output-dir', type=str, default='./data/generated_alphas',
                      help='Directory to save results (default: ./data/generated_alphas)')
    parser.add_argument('--count', type=int, default=5,
                      help='Number of alpha expressions to generate (default: 5)')
    parser.add_argument('--mode', type=str, choices=['basic', 'creative', 'optimize'], 
                      default='creative', help='Generation mode (default: creative)')
    parser.add_argument('--optimize', action='store_true',
                      help='Optimize generated alphas before display')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    try:
        # Initialize WorldQuant client
        client = WorldQuantClient(args.credentials)
        
        # Initialize alpha generator
        logger.info("Initializing alpha generator...")
        generator = AlphaGenerator(client)
        
        # Fetch data fields and operators
        data_fields = client.get_data_fields()
        operators = client.get_operators()
        
        # Generate alpha expressions
        logger.info(f"Generating {args.count} alpha expressions in {args.mode} mode...")
        alphas = generator.generate_alpha_expressions(
            count=args.count,
            mode=args.mode,
            data_fields=data_fields,
            operators=operators
        )
        
        # Optimize if requested
        if args.optimize:
            logger.info("Optimizing alpha expressions...")
            optimizer = AlphaOptimizer(client)
            alphas = optimizer.optimize_batch(alphas)
        
        # Validate alphas
        logger.info("Validating alpha expressions...")
        validator = AlphaValidator(client)
        validated_alphas = validator.validate_batch(alphas)
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(args.output_dir, f'alphas_{timestamp}.json')
        with open(output_file, 'w') as f:
            json.dump(validated_alphas, f, indent=2)
        logger.info(f"Saved {len(validated_alphas)} alphas to {output_file}")
        
        # Display alphas for manual submission
        display_alphas(validated_alphas, output_file)
        
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        return 0
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())