"""
Alpha Display

This module displays generated alphas in a user-friendly format.
"""
import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def display_alphas(alphas: List[Dict], output_file: str = None) -> None:
    """
    Display alpha expressions for manual submission.
    
    Args:
        alphas: List of alpha dictionaries
        output_file: Path to the output JSON file
    """
    if not alphas:
        print("\n=== NO VALID ALPHAS GENERATED ===\n")
        return
        
    print("\n" + "="*80)
    print("                        GENERATED ALPHAS FOR WORLDQUANT                        ")
    print("="*80 + "\n")
    
    print(f"Generated {len(alphas)} valid alpha expressions for manual submission.\n")
    print(f"These alphas have been saved to: {output_file}\n")
    
    for i, alpha_data in enumerate(alphas, 1):
        alpha = alpha_data['expression']
        print(f"Alpha #{i}:")
        print("-" * 40)
        print(alpha)
        print("-" * 40)
        print("Copy this expression to WorldQuant Brain for manual submission.\n")
    
    print("\nInstructions for manual submission:")
    print("1. Log in to WorldQuant Brain (https://platform.worldquantbrain.com)")
    print("2. Go to the Alpha Lab")
    print("3. Create a new alpha and paste the expression")
    print("4. Set parameters (region: USA, universe: TOP3000, etc.)")
    print("5. Run simulation and submit if results look good")
    
    print("\n" + "="*80)