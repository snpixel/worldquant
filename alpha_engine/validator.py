"""
Alpha Validator

This module validates generated alpha expressions.
"""
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class AlphaValidator:
    def __init__(self, client):
        """Initialize the validator with a WorldQuant client."""
        self.client = client

    def validate_batch(self, alphas: List[str]) -> List[Dict]:
        """
        Validate a batch of alpha expressions.
        
        Args:
            alphas: List of alpha expressions to validate
            
        Returns:
            List of dictionaries with validated alphas and their metadata
        """
        logger.info(f"Validating {len(alphas)} alpha expressions")
        
        validated_results = []
        for alpha in alphas:
            result = self.validate_alpha(alpha)
            validated_results.append(result)
            
        # Filter out invalid alphas
        valid_results = [r for r in validated_results if r['is_valid']]
        logger.info(f"{len(valid_results)} of {len(alphas)} alphas are valid")
        
        return valid_results

    def validate_alpha(self, alpha: str) -> Dict:
        """
        Validate a single alpha expression.
        
        Args:
            alpha: The alpha expression to validate
            
        Returns:
            Dictionary with validation results
        """
        try:
            # Check if alpha is empty or too short
            if not alpha or len(alpha) < 5:
                return {
                    'expression': alpha,
                    'is_valid': False,
                    'error': 'Alpha expression is too short',
                    'details': {}
                }
            
            # Check for syntax validity using the WorldQuant API
            validation_result = self.client.validate_expression(alpha)
            
            if validation_result.get('status') == 'valid':
                return {
                    'expression': alpha,
                    'is_valid': True,
                    'details': validation_result.get('details', {})
                }
            else:
                return {
                    'expression': alpha,
                    'is_valid': False,
                    'error': validation_result.get('error', 'Unknown error'),
                    'details': validation_result.get('details', {})
                }
                
        except Exception as e:
            logger.error(f"Error validating alpha {alpha}: {str(e)}")
            return {
                'expression': alpha,
                'is_valid': False,
                'error': str(e),
                'details': {}
            }