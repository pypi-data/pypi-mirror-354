from typing import Any, Dict, Optional, TypeVar
import json
from json.decoder import JSONDecodeError
import logging
from cognite.client import CogniteClient

T = TypeVar('T')
logger = logging.getLogger(__name__)


class APIBase:
    """
    Base class for API clients.
    
    Args:
        cognite_client: The CogniteClient to use for authentication and API calls.
    """
    
    _RESOURCE_PATH = ""
    # Define the required API version header
    _API_VERSION = "alpha" # Update if needed
    
    def __init__(self, cognite_client: CogniteClient):
        self._cognite_client = cognite_client
        # Construct default headers once
        self._default_headers = {
            "cdf-version": self._API_VERSION,
            "Accept": "application/json"
        }
    
    def _get_base_url(self) -> str:
        """
        Get the base URL for API requests.
        
        Returns:
            str: The base URL.
        """
        return f"/api/v1/projects/{self._cognite_client.config.project}{self._RESOURCE_PATH}"
    
    def _post(self, url_path: str, json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a POST request to the API, automatically adding required headers.
        
        Args:
            url_path: The URL path to append to the base URL.
            json: The JSON body to send.
            
        Returns:
            Dict[str, Any]: The response JSON. Handles potential JSON parsing errors.
        """
        url = f"{self._get_base_url()}{url_path}"
        # Use the pre-constructed default headers
        response = self._cognite_client.post(url, json=json, headers=self._default_headers)
        
        # If the response is a Response object, try to extract the JSON data
        if hasattr(response, 'json'):
            try:
                return response.json()
            except (JSONDecodeError, ValueError) as e:
                # Log the error and response content for debugging
                logger.error(f"Failed to decode JSON response: {e}")
                logger.debug(f"Response content: {response.text}")
                
                # Try to extract just the first JSON object if there's extra data
                if hasattr(response, 'text'):
                    try:
                        # Find the first valid JSON object in the response
                        text = response.text.strip()
                        # Look for the end of the first JSON object
                        brace_count = 0
                        for i, char in enumerate(text):
                            if char == '{':
                                brace_count += 1
                            elif char == '}':
                                brace_count -= 1
                                if brace_count == 0:
                                    # Found the end of the first JSON object
                                    return json.loads(text[:i+1])
                    except Exception as e2:
                        logger.error(f"Failed to extract partial JSON: {e2}")
                
                # If all else fails, return the raw response
                return {"raw_response": response.text if hasattr(response, 'text') else str(response)}
        
        return response
    
    def _get(self, url_path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a GET request to the API, automatically adding required headers.
        
        Args:
            url_path: The URL path to append to the base URL.
            params: The query parameters to send.
            
        Returns:
            Dict[str, Any]: The response JSON. Handles potential JSON parsing errors.
        """
        url = f"{self._get_base_url()}{url_path}"
        # Use the pre-constructed default headers
        response = self._cognite_client.get(url, params=params, headers=self._default_headers)
        
        # If the response is a Response object, try to extract the JSON data
        if hasattr(response, 'json'):
            try:
                return response.json()
            except (JSONDecodeError, ValueError) as e:
                # Log the error and response content for debugging
                logger.error(f"Failed to decode JSON response: {e}")
                logger.debug(f"Response content: {response.text}")
                
                # Return the raw response if JSON parsing fails
                return {"raw_response": response.text if hasattr(response, 'text') else str(response)}
        
        return response 