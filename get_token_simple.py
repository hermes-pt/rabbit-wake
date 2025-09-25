#!/usr/bin/env python3
"""
Simple script to get access token - outputs only the token
"""

import asyncio
import sys
import getpass
from src.wake.api import StorefrontAPIClient


async def get_token(email: str, password: str):
    """Get access token and print it"""
    async with StorefrontAPIClient() as client:
        query = """
        mutation {
            customerAuthenticatedLogin(input: {input: "%s", password: "%s"}) {
                isMaster
                token
                type
            }
        }
        """ % (email, password)
        
        try:
            result = await client.query(query)
            if result and "customerAuthenticatedLogin" in result:
                auth_result = result["customerAuthenticatedLogin"]
                token = auth_result.get("token")
                if token:
                    print(f"isMaster: {auth_result.get('isMaster')}")
                    print(f"token: {token}")
                    print(f"type: {auth_result.get('type')}")
                    return True
        except:
            pass
    return False


if __name__ == "__main__":
    email = input("Email: ") if len(sys.argv) < 2 else sys.argv[1]
    password = getpass.getpass("Password: ") if len(sys.argv) < 3 else sys.argv[2]
    
    if not asyncio.run(get_token(email, password)):
        sys.exit(1)