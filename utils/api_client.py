"""
WorldQuant API Client

This module handles interactions with the WorldQuant Brain API.
"""
import json
import logging
import random
import time
from typing import List, Dict, Any

import requests
from requests.auth import HTTPBasicAuth

from config.settings import (
    API_BASE_URL, AUTH_ENDPOINT, DATA_FIELDS_ENDPOINT,
    OPERATORS_ENDPOINT, SIMULATIONS_ENDPOINT, PARSE_ENDPOINT,
    DEFAULT_SIMULATION_SETTINGS, DEFAULT_DATASETS,
    RATE_LIMIT_SLEEP, MAX_RETRIES
)

logger = logging.getLogger(__name__)

class WorldQuantClient:
    def __init__(self, credentials_path: str):
        """Initialize the client with credentials."""
        self.sess = requests.Session()
        self.credentials_path = credentials_path
        self.setup_auth(credentials_path)
        
    def setup_auth(self, credentials_path: str) -> None:
        """Set up authentication with WorldQuant Brain."""
        logger.info(f"Loading credentials from {credentials_path}")
        with open(credentials_path) as f:
            credentials = json.load(f)
        
        username, password = credentials
        self.sess.auth = HTTPBasicAuth(username, password)
        
        logger.info("Authenticating with WorldQuant Brain...")
        response = self.sess.post(f"{API_BASE_URL}{AUTH_ENDPOINT}")
        logger.info(f"Authentication response status: {response.status_code}")
        
        if response.status_code != 201:
            logger.error(f"Authentication failed: {response.text}")
            raise Exception(f"Authentication failed: {response.text}")
        logger.info("Authentication successful")

    def get_data_fields(self) -> List[Dict]:
        """Fetch available data fields from WorldQuant Brain."""
        all_fields = []
        
        base_params = {
            'delay': 1,
            'instrumentType': 'EQUITY',
            'limit': 20,
            'region': 'USA',
            'universe': 'TOP3000'
        }
        
        try:
            logger.info("Requesting data fields from multiple datasets...")
            for dataset in DEFAULT_DATASETS:
                params = base_params.copy()
                params['dataset.id'] = dataset
                
                logger.info(f"Getting fields for dataset: {dataset}")
                response = self.sess.get(f"{API_BASE_URL}{DATA_FIELDS_ENDPOINT}", params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    fields = data.get('results', [])
                    logger.info(f"Found {len(fields)} fields in {dataset}")
                    all_fields.extend(fields)
                else:
                    logger.error(f"Failed to fetch fields for {dataset}: {response.text[:500]}")
            
            # Remove duplicates
            unique_fields = {field['id']: field for field in all_fields}.values()
            logger.info(f"Total unique fields found: {len(unique_fields)}")
            return list(unique_fields)
            
        except Exception as e:
            logger.error(f"Failed to fetch data fields: {e}")
            return []

    def get_operators(self) -> List[Dict]:
        """Fetch available operators from WorldQuant Brain."""
        logger.info("Requesting operators...")
        response = self.sess.get(f"{API_BASE_URL}{OPERATORS_ENDPOINT}")
        logger.info(f"Operators response status: {response.status_code}")
        
        if response.status_code != 200:
            logger.error(f"Failed to get operators: {response.text}")
            raise Exception(f"Failed to get operators: {response.text}")
        
        data = response.json()
        if isinstance(data, list):
            return data
        elif 'results' in data:
            return data['results']
        else:
            logger.error(f"Unexpected operators response format: {data}")
            raise Exception(f"Unexpected operators response format")
            
    def validate_expression(self, expression: str) -> Dict:
        """
        Validate an alpha expression using the WorldQuant API.
        
        Args:
            expression: The alpha expression to validate
            
        Returns:
            Dictionary with validation status and details
        """
        try:
            logger.info(f"Validating expression: {expression}")
            
            # In a real implementation, we'd use their parse endpoint
            simulation_data = {
                'type': 'REGULAR',
                'settings': DEFAULT_SIMULATION_SETTINGS,
                'regular': expression
            }
            
            response = self.sess.post(f"{API_BASE_URL}{PARSE_ENDPOINT}", json=simulation_data)
            if response.status_code == 200:
                return {'status': 'valid', 'details': response.json()}
            else:
                return {'status': 'invalid', 'error': response.text, 'details': {}}
                
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            return {'status': 'invalid', 'error': str(e), 'details': {}}
            
    def test_alpha(self, alpha_expression: str) -> Dict:
        """
        Submit an alpha for testing simulation.
        
        Args:
            alpha_expression: The alpha expression to test
            
        Returns:
            Dictionary with test results
        """
        try:
            logger.info(f"Testing alpha: {alpha_expression}")
            
            simulation_data = {
                'type': 'REGULAR',
                'settings': DEFAULT_SIMULATION_SETTINGS,
                'regular': alpha_expression
            }
            
            # Apply retry logic for simulation submission
            for attempt in range(MAX_RETRIES):
                try:
                    sim_resp = self.sess.post(f"{API_BASE_URL}{SIMULATIONS_ENDPOINT}", json=simulation_data)
                    
                    if sim_resp.status_code == 429:  # Rate limited
                        wait_time = int(sim_resp.headers.get('Retry-After', RATE_LIMIT_SLEEP))
                        logger.warning(f"Rate limited. Waiting {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                        
                    if sim_resp.status_code == 401:  # Auth expired
                        logger.warning("Authentication expired, refreshing...")
                        self.setup_auth(self.credentials_path)
                        continue
                        
                    if sim_resp.status_code == 201:
                        sim_progress_url = sim_resp.headers.get('location')
                        return {
                            "status": "success", 
                            "sim_url": sim_progress_url,
                            "message": "Simulation submitted successfully"
                        }
                    else:
                        return {
                            "status": "error",
                            "message": f"Simulation submission failed: {sim_resp.text}"
                        }
                        
                except requests.exceptions.RequestException as e:
                    logger.error(f"Request error on attempt {attempt+1}: {e}")
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(5)  # Short delay before retry
                    else:
                        return {
                            "status": "error",
                            "message": f"Request failed after {MAX_RETRIES} attempts: {e}"
                        }
                        
            return {
                "status": "error",
                "message": f"Max retries exceeded"
            }
                
        except Exception as e:
            logger.error(f"Error testing alpha: {str(e)}")
            return {"status": "error", "message": str(e)}