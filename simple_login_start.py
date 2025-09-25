#!/usr/bin/env python3
"""
Start simple login and get the security question
Usage: python simple_login_start.py <email>
"""

import asyncio
import sys
from src.wake.api.storefront import StorefrontAPIClient


async def get_security_question(email: str):
    """Start simple login and return the security question"""
    
    query = """
    mutation CustomerSimpleLoginStart($input: String!, $recaptchaToken: String) {
        customerSimpleLoginStart(input: $input, recaptchaToken: $recaptchaToken) {
            customerAccessToken {
                token
                type
                validUntil
                isMaster
            }
            type
            question {
                questionId
                question
                answers {
                    id
                    value
                }
            }
        }
    }
    """
    
    async with StorefrontAPIClient() as client:
        try:
            result = await client.query(
                query,
                variables={
                    "input": email,
                    "recaptchaToken": None
                }
            )
            
            if result:
                simple_login = result.get("customerSimpleLoginStart", {})
                login_type = simple_login.get("type")
                
                print(f"Email: {email}")
                print(f"Type: {login_type}")
                
                if login_type == "NEW":
                    print("\n✅ NEW USER - Ready for registration")
                    token_data = simple_login.get("customerAccessToken", {})
                    if token_data:
                        print(f"Registration Token: {token_data.get('token')[:50]}...")
                        
                elif login_type == "SIMPLE":
                    print("\n✅ EXISTING USER - Security question required")
                    question_data = simple_login.get("question", {})
                    if question_data:
                        print(f"\nQuestion ID: {question_data.get('questionId')}")
                        print(f"Question: {question_data.get('question')}")
                        print("\nAnswer Options:")
                        for answer in question_data.get("answers", []):
                            print(f"  ID: {answer.get('id')}")
                            print(f"  Value: {answer.get('value')}")
                            print()
                
        except Exception as e:
            print(f"❌ Error: {e}")


async def main():
    if len(sys.argv) < 2:
        print("Usage: python simple_login_start.py <email>")
        sys.exit(1)
    
    email = sys.argv[1]
    await get_security_question(email)


if __name__ == "__main__":
    asyncio.run(main())