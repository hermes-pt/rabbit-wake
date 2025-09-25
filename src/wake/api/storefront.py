#!/usr/bin/env python3
"""
Wake Storefront GraphQL API Client
Client for interacting with Wake's GraphQL storefront API
"""

import os
import json
import time
import asyncio
import aiohttp
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
STOREFRONT_API_BASE_URL = os.getenv("STOREFRONT_API_BASE_URL", "https://storefront-api.fbits.net")
STOREFRONT_API_TOKEN = os.getenv("STOREFRONT_API_TOKEN")

if not STOREFRONT_API_TOKEN:
    raise ValueError("STOREFRONT_API_TOKEN environment variable is required")


class StorefrontAPIClient:
    """Client for interacting with Wake's GraphQL storefront API"""
    
    def __init__(self, base_url: Optional[str] = None, token: Optional[str] = None):
        self.base_url = base_url or STOREFRONT_API_BASE_URL
        self.token = token or STOREFRONT_API_TOKEN
        self.headers = {
            "TCS-Access-Token": self.token,
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        self._session: Optional[aiohttp.ClientSession] = None
        
        # Rate limiting tracking
        self._request_times: List[float] = []
        self._rate_limit_per_minute = 120
        self._blocked_until: Optional[float] = None
    
    @property
    def session(self) -> aiohttp.ClientSession:
        """Get or create session"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session
    
    async def _check_rate_limit(self):
        """Check and enforce rate limiting"""
        current_time = time.time()
        
        # Check if blocked
        if self._blocked_until and current_time < self._blocked_until:
            wait_time = self._blocked_until - current_time
            await asyncio.sleep(wait_time)
            self._blocked_until = None
        
        # Clean old requests (older than 1 minute)
        minute_ago = current_time - 60
        self._request_times = [t for t in self._request_times if t > minute_ago]
        
        # Check if we're at the limit
        if len(self._request_times) >= self._rate_limit_per_minute:
            # Wait until the oldest request is more than a minute old
            oldest_request = min(self._request_times)
            wait_time = 60 - (current_time - oldest_request) + 0.1  # Add small buffer
            if wait_time > 0:
                await asyncio.sleep(wait_time)
        
        # Record this request
        self._request_times.append(current_time)
    
    async def query(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        operation_name: Optional[str] = None
    ) -> Any:
        """
        Execute a GraphQL query
        
        Args:
            query: GraphQL query string
            variables: Optional query variables
            operation_name: Optional operation name
        
        Returns:
            Response data
        
        Raises:
            Exception: If the API returns an error
        """
        # Check rate limit before making request
        await self._check_rate_limit()
        
        url = f"{self.base_url}/graphql"
        
        # Build request body
        body = {"query": query}
        if variables:
            body["variables"] = variables
        if operation_name:
            body["operationName"] = operation_name
        
        async with self.session.post(
            url=url,
            headers=self.headers,
            json=body
        ) as response:
            # Handle response
            text = await response.text()
            
            if response.status >= 400:
                # Handle rate limiting
                if response.status == 429:
                    retry_after = response.headers.get("Retry-After")
                    if retry_after:
                        retry_seconds = int(retry_after)
                        self._blocked_until = time.time() + retry_seconds
                        raise Exception(f"Rate limit exceeded. Retry after {retry_seconds} seconds")
                
                try:
                    error_data = json.loads(text) if text else {}
                    error_msg = error_data.get("message", f"Unknown error - HTTP {response.status}")
                except:
                    error_msg = f"HTTP {response.status}: {text[:200]}"
                raise Exception(f"Storefront API Error: {error_msg}")
            
            # Parse response
            if not text:
                return None
            
            try:
                data = json.loads(text)
                
                # Check for GraphQL errors
                if "errors" in data and data["errors"]:
                    errors = data["errors"]
                    error_messages = [e.get("message", "Unknown error") for e in errors]
                    raise Exception(f"GraphQL errors: {'; '.join(error_messages)}")
                
                return data.get("data")
            except json.JSONDecodeError:
                raise Exception(f"Invalid JSON response: {text[:200]}")
    
    async def test_connection(self) -> bool:
        """Test if the API connection is working"""
        try:
            # Simple introspection query to test connection
            test_query = """
            query TestConnection {
                __typename
            }
            """
            result = await self.query(test_query)
            return result is not None
        except Exception as e:
            print(f"Connection test failed: {e}")
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
storefront_client = StorefrontAPIClient()