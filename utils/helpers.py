"""
Helper Functions

This module contains helper functions for the alpha generator.
"""
import json
import logging
import os
import re
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def save_alphas_to_file(alphas: List[Dict], directory: str) -> str:
    """
    Save generated alphas to a JSON file.
    
    Args:
        alphas: List of alpha dictionaries to save
        directory: Directory to save the file in
        
    Returns:
        Path to the saved file
    """
    os.makedirs(directory, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"alphas_{timestamp}.json"
    filepath = os.path.join(directory, filename)
    
    with open(filepath, 'w') as f:
        json.dump(alphas, f, indent=2)
        
    logger.info(f"Saved {len(alphas)} alphas to {filepath}")
    return filepath

def load_alphas_from_file(filepath: str) -> List[Dict]:
    """
    Load alphas from a JSON file.
    
    Args:
        filepath: Path to the JSON file
        
    Returns:
        List of alpha dictionaries
    """
    if not os.path.exists(filepath):
        logger.error(f"File not found: {filepath}")
        return []
        
    with open(filepath, 'r') as f:
        try:
            alphas = json.load(f)
            logger.info(f"Loaded {len(alphas)} alphas from {filepath}")
            return alphas
        except json.JSONDecodeError as e:
            logger.error(f"Error loading alphas from {filepath}: {e}")
            return []

def validate_expression_syntax(expression: str) -> bool:
    """
    Perform basic syntax validation on an alpha expression.
    This is a lightweight check before sending to the API.
    
    Args:
        expression: The alpha expression to validate
        
    Returns:
        True if syntax appears valid, False otherwise
    """
    if not expression or len(expression) < 5:
        return False
        
    # Check for balanced parentheses
    if expression.count('(') != expression.count(')'):
        return False
        
    # Check for common operators
    common_operators = ['rank', 'ts_', 'divide', 'subtract', 'add', 'multiply']
    if not any(op in expression for op in common_operators):
        return False
        
    return True

def extract_numeric_params(expression: str) -> List[tuple]:
    """
    Extract numeric parameters from an expression.
    
    Args:
        expression: Alpha expression to parse
        
    Returns:
        List of tuples (function_name, param_value, start_pos, end_pos)
    """
    params = []
    pattern = r'(\w+)\(([^,]+),\s*(\d+)\)'
    
    for match in re.finditer(pattern, expression):
        func_name = match.group(1)
        param_value = int(match.group(3))
        start_pos = match.start(3)
        end_pos = match.end(3)
        
        params.append((func_name, param_value, start_pos, end_pos))
        
    return params

def format_alpha_for_display(alpha: str) -> str:
    """
    Format an alpha expression for better readability.
    
    Args:
        alpha: Alpha expression to format
        
    Returns:
        Formatted alpha expression
    """
    # Add spacing around commas
    formatted = re.sub(r',\s*', ', ', alpha)
    
    # Add indentation for nested expressions
    depth = 0
    result = []
    for char in formatted:
        if char == '(':
            depth += 1
            result.append(char)
            if depth > 1:
                result.append('\n' + '  ' * (depth - 1))
        elif char == ')':
            depth -= 1
            if depth > 0:
                result.append('\n' + '  ' * depth)
            result.append(char)
        else:
            result.append(char)
    
    return ''.join(result)