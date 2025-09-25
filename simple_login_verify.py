#!/usr/bin/env python3
"""
Verify simple login security question answer
Usage: python simple_login_verify.py <email> <question_id> <answer_id>
"""

import asyncio
import sys
from src.wake.api.storefront import StorefrontAPIClient


async def verify_security_answer(email: str, question_id: str, answer_id: str):
    """Verify the security question answer"""
    
    # Note: The mutation has a typo in the API - it's "Anwser" not "Answer"
    query = """
    mutation CustomerSimpleLoginVerifyAnwser(
        $input: String,
        $questionId: Uuid!,
        $answerId: Uuid!,
        $recaptchaToken: String
    ) {
        customerSimpleLoginVerifyAnwser(
            input: $input,
            questionId: $questionId,
            answerId: $answerId,
            recaptchaToken: $recaptchaToken
        ) {
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
                    "questionId": question_id,
                    "answerId": answer_id,
                    "recaptchaToken": None
                }
            )
            
            if result:
                response = result.get("customerSimpleLoginVerifyAnwser", {})
                response_type = response.get("type")
                token_data = response.get("customerAccessToken", {})
                
                print(f"Email: {email}")
                print(f"Response Type: {response_type}")
                
                # Check if we got a token (successful login)
                if token_data and token_data.get("token"):
                    print("\n✅ LOGIN SUCCESSFUL!")
                    token = token_data.get("token")
                    print(f"Token: {token[:50]}...")
                    print(f"Token Type: {token_data.get('type')}")
                    print(f"Valid Until: {token_data.get('validUntil')}")
                    
                    # Save token
                    with open("customer_token.txt", "w") as f:
                        f.write(token)
                    print("\nToken saved to customer_token.txt")
                    
                    # Export command
                    print(f"\nTo set as environment variable:")
                    print(f"export WAKE_CUSTOMER_TOKEN='{token}'")
                    
                elif response_type == "SIMPLE":
                    print("\n❌ WRONG ANSWER - New question received")
                    question_data = response.get("question", {})
                    if question_data:
                        print(f"\nNew Question ID: {question_data.get('questionId')}")
                        print(f"Question: {question_data.get('question')}")
                        print("\nAnswer Options:")
                        for answer in question_data.get("answers", []):
                            print(f"  ID: {answer.get('id')}")
                            print(f"  Value: {answer.get('value')}")
                            print()
                else:
                    print(f"\n❌ Unexpected response")
                    print(f"Full response: {response}")
                    
        except Exception as e:
            print(f"❌ Error: {e}")


async def main():
    if len(sys.argv) < 4:
        print("Usage: python simple_login_verify.py <email> <question_id> <answer_id>")
        print("\nExample:")
        print("python simple_login_verify.py luis@filipe.xyz 11cb3e4d-fad1-ef3f-437d-b37344e46363 de29c85e-54be-9ab1-5f78-d9a65b900a39")
        sys.exit(1)
    
    email = sys.argv[1]
    question_id = sys.argv[2]
    answer_id = sys.argv[3]
    
    await verify_security_answer(email, question_id, answer_id)


if __name__ == "__main__":
    asyncio.run(main())