#!/usr/bin/env python3
"""
Generate customer access token for testing
Uses email/password authentication
"""

import asyncio
import os
import sys
from datetime import datetime
from src.wake.api import StorefrontAPIClient


async def get_access_token(email: str, password: str):
    """Get customer access token using email/password"""
    async with StorefrontAPIClient() as client:
        query = """
        mutation CustomerLogin($input: CustomerAuthenticateInput!) {
            customerAuthenticatedLogin(input: $input) {
                token
                validUntil
                type
            }
        }
        """
        
        variables = {
            "input": {
                "input": email,
                "password": password
            }
        }
        
        try:
            result = await client.query(query, variables)
            
            if result and "customerAuthenticatedLogin" in result:
                token_data = result["customerAuthenticatedLogin"]
                
                if token_data and token_data.get("token"):
                    print(f"✅ Authentication successful!")
                    print(f"\nToken: {token_data['token']}")
                    print(f"Valid until: {token_data['validUntil']}")
                    print(f"Type: {token_data.get('type', 'N/A')}")
                    
                    # Parse and show expiration time
                    if token_data.get('validUntil'):
                        try:
                            # Parse ISO format timestamp
                            valid_until = datetime.fromisoformat(token_data['validUntil'].replace('Z', '+00:00'))
                            now = datetime.now(valid_until.tzinfo)
                            time_left = valid_until - now
                            hours_left = time_left.total_seconds() / 3600
                            print(f"Expires in: {hours_left:.1f} hours")
                        except:
                            pass
                    
                    return token_data['token']
                else:
                    print("❌ Authentication failed: No token returned")
                    return None
            else:
                print("❌ Authentication failed: Invalid response")
                return None
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return None


async def test_token(token: str):
    """Test if token works by fetching customer info"""
    async with StorefrontAPIClient() as client:
        query = """
        query GetCustomer($token: String!) {
            customer(customerAccessToken: $token) {
                customerId
                customerName
                email
            }
        }
        """
        
        variables = {
            "token": token
        }
        
        try:
            result = await client.query(query, variables)
            
            if result and "customer" in result:
                customer = result["customer"]
                print(f"\n📋 Customer Info:")
                print(f"ID: {customer.get('customerId', 'N/A')}")
                print(f"Name: {customer.get('customerName', 'N/A')}")
                print(f"Email: {customer.get('email', 'N/A')}")
                return True
            else:
                print("\n❌ Token validation failed")
                return False
                
        except Exception as e:
            print(f"\n❌ Token test error: {e}")
            return False


async def main():
    """Main function"""
    # Check for environment variables first
    email = os.getenv("WAKE_TEST_EMAIL")
    password = os.getenv("WAKE_TEST_PASSWORD")
    
    # If not in env, prompt user
    if not email:
        email = input("Email: ").strip()
    if not password:
        import getpass
        password = getpass.getpass("Password: ")
    
    if not email or not password:
        print("❌ Email and password are required")
        sys.exit(1)
    
    print(f"\n🔐 Authenticating as {email}...")
    
    # Get token
    token = await get_access_token(email, password)
    
    if token:
        # Test the token
        print("\n🧪 Testing token...")
        await test_token(token)
        
        print("\n💡 To use this token in other scripts:")
        print(f'export WAKE_CUSTOMER_TOKEN="{token}"')
    else:
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)