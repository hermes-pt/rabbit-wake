#!/usr/bin/env python3
"""
Wake E-commerce API Base Client
Base connection module for Wake e-commerce API
"""

import os
import json
import time
import asyncio
from collections import defaultdict
import aiohttp
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
WAKE_API_BASE_URL = os.getenv("WAKE_API_BASE_URL", "https://api.fbits.net")
WAKE_API_TOKEN = os.getenv("WAKE_API_TOKEN")

if not WAKE_API_TOKEN:
    raise ValueError("WAKE_API_TOKEN environment variable is required")

# Create authorization header
AUTH_HEADER = f"Basic {WAKE_API_TOKEN}"


class WakeAPIClient:
    """Base client for interacting with Wake e-commerce API"""
    
    def __init__(self, base_url: Optional[str] = None, token: Optional[str] = None):
        self.base_url = base_url or WAKE_API_BASE_URL
        self.token = token or WAKE_API_TOKEN
        self.headers = {
            "Authorization": f"Basic {self.token}",
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        self._session: Optional[aiohttp.ClientSession] = None
        
        # Rate limiting tracking
        self._request_times = defaultdict(list)  # endpoint_group -> list of timestamps
        self._rate_limit_per_minute = 120
        self._blocked_until = {}  # endpoint_group -> unblock timestamp
    
    @property
    def session(self) -> aiohttp.ClientSession:
        """Get or create session"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session
    
    def _get_endpoint_group(self, endpoint: str) -> str:
        """Extract endpoint group from endpoint path"""
        # Common endpoint groups
        groups = [
            "produtos", "usuarios", "pedidos", "categorias",
            "centrosdistribuicao", "estoque", "preco"
        ]
        
        # Extract first part of endpoint
        parts = endpoint.strip("/").split("/")
        if parts:
            first_part = parts[0].lower()
            for group in groups:
                if group in first_part:
                    return group
        
        return "default"
    
    async def _check_rate_limit(self, endpoint_group: str):
        """Check and enforce rate limiting"""
        current_time = time.time()
        
        # Check if blocked
        if endpoint_group in self._blocked_until:
            if current_time < self._blocked_until[endpoint_group]:
                wait_time = self._blocked_until[endpoint_group] - current_time
                await asyncio.sleep(wait_time)
            else:
                del self._blocked_until[endpoint_group]
        
        # Clean old requests (older than 1 minute)
        minute_ago = current_time - 60
        self._request_times[endpoint_group] = [
            t for t in self._request_times[endpoint_group] if t > minute_ago
        ]
        
        # Check if we're at the limit
        if len(self._request_times[endpoint_group]) >= self._rate_limit_per_minute:
            # Wait until the oldest request is more than a minute old
            oldest_request = min(self._request_times[endpoint_group])
            wait_time = 60 - (current_time - oldest_request) + 0.1  # Add small buffer
            if wait_time > 0:
                await asyncio.sleep(wait_time)
        
        # Record this request
        self._request_times[endpoint_group].append(current_time)
    
    async def make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Any:
        """
        Make an HTTP request to Wake API
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint path (e.g., "/usuarios")
            params: Query parameters
            json_data: JSON body data
            headers: Additional headers to merge with defaults
        
        Returns:
            Response data as dictionary
        
        Raises:
            Exception: If the API returns an error status
        """
        # Check rate limit before making request
        endpoint_group = self._get_endpoint_group(endpoint)
        await self._check_rate_limit(endpoint_group)
        
        url = f"{self.base_url}{endpoint}"
        
        # Merge headers if provided
        request_headers = self.headers.copy()
        if headers:
            request_headers.update(headers)
        
        # Clean params - convert booleans to strings
        if params:
            clean_params = {}
            for k, v in params.items():
                if isinstance(v, bool):
                    clean_params[k] = "true" if v else "false"
                elif v is not None:
                    clean_params[k] = v
            params = clean_params
        
        async with self.session.request(
            method=method,
            url=url,
            headers=request_headers,
            params=params,
            json=json_data
        ) as response:
            # Handle empty responses
            text = await response.text()
            
            if response.status >= 400:
                # Handle rate limiting specifically
                if response.status == 429:
                    retry_after = response.headers.get("Retry-After")
                    if retry_after:
                        retry_seconds = int(retry_after)
                        self._blocked_until[endpoint_group] = time.time() + retry_seconds
                        raise Exception(f"Rate limit exceeded. Retry after {retry_seconds} seconds")
                
                try:
                    error_data = json.loads(text) if text else {}
                    error_msg = error_data.get("message", "Unknown error")
                except:
                    error_msg = "Unknown error"
                raise Exception(f"Wake API Error ({response.status}): {error_msg}")
            
            # Parse response
            if not text or text == "null":
                return None
            
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return text
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Convenience method for GET requests"""
        return await self.make_request("GET", endpoint, params=params)
    
    async def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convenience method for POST requests"""
        raise NotImplementedError("POST requests are temporarily disabled for production safety")
        # return await self.make_request("POST", endpoint, json_data=data)
    
    async def put(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convenience method for PUT requests"""
        raise NotImplementedError("PUT requests are temporarily disabled for production safety")
        # return await self.make_request("PUT", endpoint, json_data=data)
    
    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """Convenience method for DELETE requests"""
        raise NotImplementedError("DELETE requests are temporarily disabled for production safety")
        # return await self.make_request("DELETE", endpoint)
    
    async def test_connection(self) -> bool:
        """Test if the API connection is working"""
        try:
            # Try to access a simple endpoint
            await self.get("/usuarios", params={"limite": 1})
            return True
        except Exception:
            return False
    
    async def close(self):
        """Close the session"""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()


# Singleton instance
wake_client = WakeAPIClient()