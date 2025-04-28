"""
Configuration Settings

This module contains configuration settings for the alpha generator.
"""

# API endpoints
API_BASE_URL = "https://api.worldquantbrain.com"
AUTH_ENDPOINT = "/authentication"
DATA_FIELDS_ENDPOINT = "/data-fields"
OPERATORS_ENDPOINT = "/operators"
SIMULATIONS_ENDPOINT = "/simulations"
PARSE_ENDPOINT = "/simulations/parse"
ALPHAS_ENDPOINT = "/alphas"

# Default simulation settings
DEFAULT_SIMULATION_SETTINGS = {
    'instrumentType': 'EQUITY',
    'region': 'USA',
    'universe': 'TOP3000',
    'delay': 1,
    'decay': 0,
    'neutralization': 'INDUSTRY',
    'truncation': 0.08,
    'pasteurization': 'ON',
    'unitHandling': 'VERIFY',
    'nanHandling': 'OFF',
    'language': 'FASTEXPR',
    'visualization': False,
}

# Default datasets to check for data fields
DEFAULT_DATASETS = [
    'fundamental6', 
    'fundamental2', 
    'analyst4', 
    'model16', 
    'model51', 
    'news12'
]

# API rate limiting settings
RATE_LIMIT_SLEEP = 60  # seconds to wait when hitting rate limits
MAX_RETRIES = 3  # maximum number of retries for API calls