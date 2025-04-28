"""
Alpha Optimizer

This module optimizes generated alpha expressions.
"""
import logging
import random
import re
from typing import List, Dict, Any, Tuple

logger = logging.getLogger(__name__)

class AlphaOptimizer:
    def __init__(self, client):
        """Initialize the optimizer with a WorldQuant client."""
        self.client = client

    def optimize_batch(self, alphas: List[str]) -> List[str]:
        """
        Optimize a batch of alpha expressions.
        
        Args:
            alphas: List of alpha expressions to optimize
            
        Returns:
            List of optimized alpha expressions
        """
        logger.info(f"Optimizing batch of {len(alphas)} alphas")
        optimized_alphas = []
        
        for alpha in alphas:
            optimized_alpha = self.optimize_alpha(alpha)
            optimized_alphas.append(optimized_alpha)
            
        return optimized_alphas

    def optimize_alpha(self, alpha: str) -> str:
        """
        Optimize a single alpha expression.
        
        Args:
            alpha: The alpha expression to optimize
            
        Returns:
            Optimized alpha expression
        """
        # Parse numeric parameters
        params = self._extract_numeric_params(alpha)
        
        # Optimize each parameter
        for param, value, start, end in params:
            new_value = self._optimize_parameter(param, value, alpha)
            alpha = alpha[:start] + str(new_value) + alpha[end:]
        
        return alpha
        
    def _extract_numeric_params(self, expression: str) -> List[Tuple[str, int, int, int]]:
        """
        Extract numeric parameters from an expression.
        
        Returns list of tuples: (param_name, value, start_pos, end_pos)
        """
        params = []
        # Match pattern like: function_name(field, 20)
        # Captures the function name, parameter value, and positions
        pattern = r'(\w+)\(([^,]+),\s*(\d+)\)'
        
        for match in re.finditer(pattern, expression):
            func_name = match.group(1)
            param_value = int(match.group(3))
            start_pos = match.start(3)
            end_pos = match.end(3)
            
            # Store as tuple (param_name, value, start_pos, end_pos)
            params.append((func_name, param_value, start_pos, end_pos))
            
        return params
        
    def _optimize_parameter(self, param_name: str, value: int, alpha: str) -> int:
        """
        Optimize a numeric parameter based on its function context.
        
        Args:
            param_name: Name of the function using this parameter
            value: Current parameter value
            alpha: Full alpha expression (for context)
            
        Returns:
            Optimized parameter value
        """
        # Lookback window optimization
        if param_name in ['ts_mean', 'ts_std_dev', 'ts_rank', 'ts_min', 'ts_max']:
            # For time series functions, optimize the lookback period
            if value < 10:
                return max(5, value)  # Minimum window of 5
            elif value > 250:
                return min(250, value)  # Maximum window of 250
            elif 50 <= value <= 100:
                return value  # These are generally good values
            else:
                # Nudge toward common effective values
                common_periods = [5, 10, 20, 60, 120, 252]
                closest = min(common_periods, key=lambda x: abs(x - value))
                # Gradually move toward closest common value
                return value + (1 if closest > value else -1)
                
        # Delay optimization
        elif param_name == 'delay':
            # For delay functions, keep delays reasonable
            return min(20, max(1, value))  # Between 1 and 20
            
        # Default case: return original value
        return value