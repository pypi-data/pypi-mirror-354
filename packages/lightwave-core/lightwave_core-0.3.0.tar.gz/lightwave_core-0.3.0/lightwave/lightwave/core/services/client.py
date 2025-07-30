"""API client for the Lightwave ecosystem."""

import json
import logging
from typing import Any, Dict, List, Optional, Type, TypeVar, Union
from urllib.parse import urljoin, urlparse

import httpx
from pydantic import BaseModel, ValidationError

from ..models.base import BaseModel as LightwaveBaseModel

T = TypeVar('T', bound=BaseModel)

logger = logging.getLogger(__name__)


class ApiClientError(Exception):
    """Base exception for API client errors."""
    pass


class ApiConnectionError(ApiClientError):
    """Raised when connection to API fails."""
    pass


class ApiAuthenticationError(ApiClientError):
    """Raised when authentication fails."""
    pass


class ApiValidationError(ApiClientError):
    """Raised when response validation fails."""
    pass


class ApiServerError(ApiClientError):
    """Raised when server returns 5xx error."""
    pass


class ApiClient:
    """HTTP client for Lightwave API services.
    
    Provides:
    - Automatic JSON serialization/deserialization
    - Pydantic model validation
    - Authentication handling
    - Error handling and retries
    - Request/response logging
    """
    
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        headers: Optional[Dict[str, str]] = None
    ):
        """Initialize API client.
        
        Args:
            base_url: Base URL for the API
            api_key: API key for authentication
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            headers: Additional headers to send with requests
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        
        # Setup default headers
        self.default_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Lightwave-Client/1.0"
        }
        
        if headers:
            self.default_headers.update(headers)
        
        if api_key:
            self.default_headers["Authorization"] = f"Bearer {api_key}"
        
        # Create HTTP client
        self.client = httpx.Client(
            timeout=timeout,
            headers=self.default_headers
        )
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
    
    def close(self) -> None:
        """Close the HTTP client."""
        self.client.close()
    
    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint."""
        return urljoin(self.base_url + '/', endpoint.lstrip('/'))
    
    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle HTTP response and extract JSON data.
        
        Args:
            response: HTTP response object
            
        Returns:
            Response data as dictionary
            
        Raises:
            ApiAuthenticationError: For 401/403 responses
            ApiServerError: For 5xx responses
            ApiClientError: For other error responses
        """
        try:
            # Log response for debugging
            logger.debug(
                f"API Response: {response.status_code} {response.url} "
                f"({len(response.content)} bytes)"
            )
            
            # Handle specific status codes
            if response.status_code == 401:
                raise ApiAuthenticationError("Authentication failed - invalid API key")
            elif response.status_code == 403:
                raise ApiAuthenticationError("Access forbidden - insufficient permissions")
            elif 500 <= response.status_code < 600:
                raise ApiServerError(f"Server error: {response.status_code}")
            elif not (200 <= response.status_code < 300):
                error_msg = f"HTTP {response.status_code}"
                try:
                    error_data = response.json()
                    if isinstance(error_data, dict) and 'message' in error_data:
                        error_msg += f": {error_data['message']}"
                except Exception:
                    pass
                raise ApiClientError(error_msg)
            
            # Parse JSON response
            try:
                return response.json()
            except json.JSONDecodeError as e:
                raise ApiClientError(f"Invalid JSON response: {e}")
                
        except httpx.RequestError as e:
            raise ApiConnectionError(f"Connection error: {e}")
    
    def request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], BaseModel]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint path
            data: Request data (dict or Pydantic model)
            params: Query parameters
            headers: Additional headers
            
        Returns:
            Response data as dictionary
        """
        url = self._build_url(endpoint)
        
        # Prepare request data
        json_data = None
        if data is not None:
            if isinstance(data, BaseModel):
                json_data = data.model_dump(mode="json")
            else:
                json_data = data
        
        # Merge headers
        request_headers = self.default_headers.copy()
        if headers:
            request_headers.update(headers)
        
        # Log request for debugging
        logger.debug(f"API Request: {method} {url}")
        if json_data:
            logger.debug(f"Request data: {json.dumps(json_data, indent=2)}")
        
        # Make request with retries
        last_exception = None
        for attempt in range(self.max_retries + 1):
            try:
                response = self.client.request(
                    method=method,
                    url=url,
                    json=json_data,
                    params=params,
                    headers=request_headers
                )
                return self._handle_response(response)
                
            except (httpx.RequestError, ApiConnectionError) as e:
                last_exception = e
                if attempt < self.max_retries:
                    logger.warning(f"Request failed (attempt {attempt + 1}), retrying: {e}")
                    continue
                else:
                    break
            except (ApiAuthenticationError, ApiServerError, ApiClientError):
                # Don't retry these errors
                raise
        
        # All retries failed
        raise last_exception or ApiConnectionError("Request failed after all retries")
    
    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        response_model: Optional[Type[T]] = None
    ) -> Union[Dict[str, Any], T]:
        """Make GET request.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            response_model: Pydantic model to validate response
            
        Returns:
            Response data (dict or validated model instance)
        """
        data = self.request("GET", endpoint, params=params)
        
        if response_model:
            return self._validate_response(data, response_model)
        return data
    
    def post(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], BaseModel]] = None,
        response_model: Optional[Type[T]] = None
    ) -> Union[Dict[str, Any], T]:
        """Make POST request.
        
        Args:
            endpoint: API endpoint
            data: Request data
            response_model: Pydantic model to validate response
            
        Returns:
            Response data (dict or validated model instance)
        """
        response_data = self.request("POST", endpoint, data=data)
        
        if response_model:
            return self._validate_response(response_data, response_model)
        return response_data
    
    def put(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], BaseModel]] = None,
        response_model: Optional[Type[T]] = None
    ) -> Union[Dict[str, Any], T]:
        """Make PUT request.
        
        Args:
            endpoint: API endpoint
            data: Request data
            response_model: Pydantic model to validate response
            
        Returns:
            Response data (dict or validated model instance)
        """
        response_data = self.request("PUT", endpoint, data=data)
        
        if response_model:
            return self._validate_response(response_data, response_model)
        return response_data
    
    def patch(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], BaseModel]] = None,
        response_model: Optional[Type[T]] = None
    ) -> Union[Dict[str, Any], T]:
        """Make PATCH request.
        
        Args:
            endpoint: API endpoint
            data: Request data
            response_model: Pydantic model to validate response
            
        Returns:
            Response data (dict or validated model instance)
        """
        response_data = self.request("PATCH", endpoint, data=data)
        
        if response_model:
            return self._validate_response(response_data, response_model)
        return response_data
    
    def delete(
        self,
        endpoint: str,
        response_model: Optional[Type[T]] = None
    ) -> Union[Dict[str, Any], T, None]:
        """Make DELETE request.
        
        Args:
            endpoint: API endpoint
            response_model: Pydantic model to validate response
            
        Returns:
            Response data (dict, validated model instance, or None)
        """
        response_data = self.request("DELETE", endpoint)
        
        # DELETE requests may return empty responses
        if not response_data:
            return None
        
        if response_model:
            return self._validate_response(response_data, response_model)
        return response_data
    
    def _validate_response(self, data: Dict[str, Any], model_class: Type[T]) -> T:
        """Validate response data against Pydantic model.
        
        Args:
            data: Response data
            model_class: Pydantic model class
            
        Returns:
            Validated model instance
            
        Raises:
            ApiValidationError: If validation fails
        """
        try:
            if issubclass(model_class, LightwaveBaseModel):
                return model_class.from_api_response(data)
            else:
                return model_class(**data)
        except ValidationError as e:
            raise ApiValidationError(f"Response validation failed: {e}")
    
    def paginate(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        response_model: Optional[Type[T]] = None,
        page_size: int = 50,
        max_pages: Optional[int] = None
    ) -> List[Union[Dict[str, Any], T]]:
        """Paginate through API results.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            response_model: Pydantic model for individual items
            page_size: Number of items per page
            max_pages: Maximum number of pages to fetch
            
        Returns:
            List of all items from all pages
        """
        all_items = []
        page = 1
        
        request_params = params.copy() if params else {}
        request_params['page_size'] = page_size
        
        while True:
            if max_pages and page > max_pages:
                break
            
            request_params['page'] = page
            response = self.get(endpoint, params=request_params)
            
            # Extract items from response
            if isinstance(response, dict):
                items = response.get('items', response.get('results', []))
                total_pages = response.get('total_pages', response.get('page_count', 1))
            else:
                items = response if isinstance(response, list) else [response]
                total_pages = page
            
            # Validate items if model provided
            if response_model and items:
                validated_items = [
                    self._validate_response(item, response_model) 
                    if isinstance(item, dict) else item
                    for item in items
                ]
                all_items.extend(validated_items)
            else:
                all_items.extend(items)
            
            # Check if we've reached the last page
            if page >= total_pages or not items:
                break
            
            page += 1
        
        return all_items