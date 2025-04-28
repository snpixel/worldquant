"""
Alpha Generator Core Logic

This module handles the generation of alpha expressions.
"""
import logging
import random
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class AlphaGenerator:
    def __init__(self, client):
        """Initialize the alpha generator with a WorldQuant client."""
        self.client = client

    def generate_alpha_expressions(self, count: int, mode: str, data_fields: List[Dict], 
                                 operators: List[Dict]) -> List[str]:
        """
        Generate alpha expressions based on the specified mode.
        
        Args:
            count: Number of alpha expressions to generate
            mode: Generation mode ('basic', 'creative', 'optimize')
            data_fields: List of available data fields
            operators: List of available operators
            
        Returns:
            List of alpha expressions
        """
        logger.info(f"Generating {count} alphas in {mode} mode")
        
        if mode == 'basic':
            return self.generate_basic_alphas(count, data_fields, operators)
        elif mode == 'creative':
            return self.generate_creative_alphas(count, data_fields, operators)
        elif mode == 'optimize':
            return self.generate_optimized_alphas(count, data_fields, operators)
        else:
            raise ValueError(f"Unknown generation mode: {mode}")

    def generate_basic_alphas(self, count: int, data_fields: List[Dict], 
                            operators: List[Dict]) -> List[str]:
        """Generate basic alpha expressions using simple patterns."""
        alphas = []
        
        # Group operators by category for easier use
        op_by_category = self._group_operators_by_category(operators)
        
        # Get sample fields and operators
        sample_fields = self._sample_data_fields(data_fields, min(10, len(data_fields)))
        
        # Basic patterns
        patterns = [
            # Simple rank
            lambda: f"rank({self._get_random_field(sample_fields)})",
            
            # Simple mean
            lambda: f"ts_mean({self._get_random_field(sample_fields)}, {random.randint(5, 60)})",
            
            # Simple ratio
            lambda: f"divide({self._get_random_field(sample_fields)}, {self._get_random_field(sample_fields)})",
            
            # Simple difference
            lambda: f"subtract({self._get_random_field(sample_fields)}, ts_mean({self._get_random_field(sample_fields)}, {random.randint(5, 60)}))",
            
            # Simple momentum
            lambda: f"subtract({self._get_random_field(sample_fields)}, delay({self._get_random_field(sample_fields)}, {random.randint(1, 10)}))"
        ]
        
        # Generate alphas using patterns
        for _ in range(count):
            pattern = random.choice(patterns)
            alpha = pattern()
            alphas.append(alpha)
        
        return alphas

    def generate_creative_alphas(self, count: int, data_fields: List[Dict], 
                               operators: List[Dict]) -> List[str]:
        """Generate more creative alpha expressions using complex patterns."""
        alphas = []
        
        # Group operators by category for easier use
        op_by_category = self._group_operators_by_category(operators)
        
        # Get sample fields and operators
        sample_fields = self._sample_data_fields(data_fields, min(20, len(data_fields)))
        ts_ops = op_by_category.get('Time Series', [])
        cs_ops = op_by_category.get('Cross Sectional', [])
        arith_ops = op_by_category.get('Arithmetic', [])
        
        # Advanced patterns
        patterns = [
            # Momentum with normalization
            lambda: f"rank(subtract({self._get_random_field(sample_fields)}, delay({self._get_random_field(sample_fields)}, {random.randint(1, 10)})))",
            
            # Mean reversion
            lambda: f"rank(subtract(ts_mean({self._get_random_field(sample_fields)}, {random.randint(10, 60)}), {self._get_random_field(sample_fields)}))",
            
            # Ratio with ranking
            lambda: f"rank(divide({self._get_random_field(sample_fields)}, {self._get_random_field(sample_fields)}))",
            
            # Volatility adjusted momentum
            lambda: f"divide(subtract({self._get_random_field(sample_fields)}, delay({self._get_random_field(sample_fields)}, {random.randint(1, 10)})), ts_std_dev({self._get_random_field(sample_fields)}, {random.randint(10, 60)}))",
            
            # Multi-factor combination
            lambda: f"add(multiply(rank({self._get_random_field(sample_fields)}), {random.uniform(0.4, 0.6):.2f}), multiply(rank({self._get_random_field(sample_fields)}), {random.uniform(0.4, 0.6):.2f}))"
        ]
        
        # Generate alphas using patterns
        for _ in range(count):
            pattern = random.choice(patterns)
            alpha = pattern()
            alphas.append(alpha)
        
        return alphas

    def generate_optimized_alphas(self, count: int, data_fields: List[Dict], 
                                operators: List[Dict]) -> List[str]:
        """Generate optimized alpha expressions using more sophisticated techniques."""
        # Start with creative alphas
        base_alphas = self.generate_creative_alphas(count, data_fields, operators)
        
        # Apply additional optimization techniques
        optimized_alphas = []
        for alpha in base_alphas:
            # Add industry neutralization
            if random.random() > 0.5:
                alpha = f"group_neutralize({alpha}, industry)"
            
            # Apply normalization
            if random.random() > 0.7:
                alpha = f"zscore({alpha})"
                
            optimized_alphas.append(alpha)
            
        return optimized_alphas

    def _group_operators_by_category(self, operators: List[Dict]) -> Dict[str, List[Dict]]:
        """Group operators by their category."""
        grouped = {}
        for op in operators:
            category = op.get('category', 'Other')
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(op)
        return grouped

    def _sample_data_fields(self, fields: List[Dict], n: int) -> List[Dict]:
        """Sample n data fields from the available fields."""
        return random.sample(fields, min(n, len(fields)))

    def _get_random_field(self, fields: List[Dict]) -> str:
        """Get a random data field ID."""
        field = random.choice(fields)
        return field['id']