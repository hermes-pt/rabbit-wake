"""
Authentication service for admin and impersonate tokens
"""
import os
from typing import Dict, Any, Optional
from src.wake.api.storefront import StorefrontAPIClient


class AuthService:
    def __init__(self):
        self.client = None
        
    async def __aenter__(self):
        self.client = StorefrontAPIClient()
        await self.client.__aenter__()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.__aexit__(exc_type, exc_val, exc_tb)
    
    async def admin_login(self, email: str, password: str) -> Optional[str]:
        """
        Login as admin user and get access token
        
        Args:
            email: Admin email
            password: Admin password
            
        Returns:
            Admin access token or None if login failed
        """
        mutation = """
        mutation CustomerAuthenticatedLogin($input: String!, $password: String!) {
            customerAuthenticatedLogin(input: {input: $input, password: $password}) {
                isMaster
                token
                type
                validUntil
            }
        }
        """
        
        variables = {
            "input": email,
            "password": password
        }
        
        result = await self.client.query(mutation, variables)
        
        if result and "customerAuthenticatedLogin" in result:
            auth_data = result["customerAuthenticatedLogin"]
            if auth_data and auth_data.get("isMaster"):
                return auth_data.get("token")
            else:
                raise Exception("User is not admin (isMaster=false)")
        
        return None
    
    async def customer_impersonate(self, admin_token: str, customer_email: str) -> Optional[str]:
        """
        Generate impersonate token for customer using admin token
        
        Args:
            admin_token: Admin access token
            customer_email: Customer email to impersonate
            
        Returns:
            Impersonate token or None if failed
        """
        mutation = """
        mutation CustomerImpersonate($customerAccessToken: String!, $input: String!) {
            customerImpersonate(customerAccessToken: $customerAccessToken, input: $input) {
                isMaster
                token
                validUntil
            }
        }
        """
        
        variables = {
            "customerAccessToken": admin_token,
            "input": customer_email
        }
        
        result = await self.client.query(mutation, variables)
        
        if result and "customerImpersonate" in result:
            impersonate_data = result["customerImpersonate"]
            if impersonate_data:
                return impersonate_data.get("token")
        
        return None
    
    async def get_assisted_sale_token(self, customer_email: str) -> str:
        """
        Get assisted sale token for a customer
        
        This performs the full flow:
        1. Login as admin
        2. Generate impersonate token for customer
        
        Args:
            customer_email: Customer email to impersonate
            
        Returns:
            Assisted sale token
        """
        # Get admin credentials from environment
        admin_email = os.getenv("ADMIN_EMAIL")
        admin_password = os.getenv("ADMIN_PASSWORD")
        
        if not admin_email or not admin_password:
            raise Exception("ADMIN_EMAIL and ADMIN_PASSWORD must be set in environment")
        
        # Step 1: Login as admin
        admin_token = await self.admin_login(admin_email, admin_password)
        if not admin_token:
            raise Exception("Failed to login as admin")
        
        # Step 2: Generate impersonate token
        impersonate_token = await self.customer_impersonate(admin_token, customer_email)
        if not impersonate_token:
            raise Exception(f"Failed to generate impersonate token for {customer_email}")
        
        return impersonate_token