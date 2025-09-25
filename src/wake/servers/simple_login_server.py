#!/usr/bin/env python3
"""
MCP Server for Wake Simple Login
Handles customer authentication using simple login flow with security questions
"""

import os
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
from fastmcp import FastMCP
from sqlalchemy import and_

from ..api.storefront import StorefrontAPIClient
from ..db import SessionLocal, CustomerToken

# Load environment variables
load_dotenv()

# Customer phone for token storage
CUSTOMER_PHONE = os.getenv("CUSTOMER_PHONE", "")

mcp = FastMCP("Wake Simple Login")


@mcp.tool()
async def simple_login_start(
    email: str
) -> Dict[str, Any]:
    """
    Start simple login process for a customer
    
    Args:
        email: Customer email address
    
    Returns:
        Dict with login type and security question if existing user,
        or registration token if new user
    """
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
            
            if not result:
                return {"error": "Nenhuma resposta da API"}
            
            simple_login = result.get("customerSimpleLoginStart", {})
            login_type = simple_login.get("type")
            
            response = {
                "email": email,
                "type": login_type
            }
            
            if login_type == "NEW":
                # New user - return registration token
                token_data = simple_login.get("customerAccessToken", {})
                if token_data:
                    response["customerAccessToken"] = token_data
                    response["message"] = "Novo usuário detectado. Use o token para registro."
                    
            elif login_type == "SIMPLE":
                # Existing user - return security question
                question_data = simple_login.get("question", {})
                if question_data:
                    response["question"] = question_data
                    response["message"] = "Pergunta de segurança necessária. Use simple_login_verify para responder."
            
            return response
            
        except Exception as e:
            return {"error": str(e)}


@mcp.tool()
async def simple_login_verify(
    email: str,
    question_id: str,
    answer_id: str
) -> Dict[str, Any]:
    """
    Verify security question answer and get customer access token
    
    Args:
        email: Customer email address
        question_id: ID of the security question
        answer_id: ID of the selected answer
    
    Returns:
        Dict with login result and token if successful
    """
    # Check if CUSTOMER_PHONE is set
    if not CUSTOMER_PHONE:
        return {"error": "Variável de ambiente CUSTOMER_PHONE não está configurada"}
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
            
            if not result:
                return {"error": "Nenhuma resposta da API"}
            
            response_data = result.get("customerSimpleLoginVerifyAnwser", {})
            response_type = response_data.get("type")
            token_data = response_data.get("customerAccessToken", {})
            
            response = {
                "email": email,
                "type": response_type
            }
            
            # Check if we got a token (successful login)
            if token_data and token_data.get("token"):
                token = token_data.get("token")
                token_type = token_data.get("type")
                valid_until_str = token_data.get("validUntil")
                
                # Parse valid_until date
                try:
                    # Parse ISO format with timezone
                    valid_until = datetime.fromisoformat(valid_until_str.replace('Z', '+00:00'))
                except:
                    # Fallback to current time + 3 hours if parsing fails
                    from datetime import timedelta
                    valid_until = datetime.utcnow() + timedelta(hours=3)
                
                response["customerAccessToken"] = token_data
                response["message"] = "Login realizado com sucesso!"
                
                # Save token to database with CUSTOMER_PHONE
                if CUSTOMER_PHONE:
                    try:
                        with SessionLocal() as db:
                            # Check if token exists for this phone/email
                            existing_token = db.query(CustomerToken).filter(
                                and_(
                                    CustomerToken.phone == CUSTOMER_PHONE,
                                    CustomerToken.email == email
                                )
                            ).first()
                            
                            if existing_token:
                                # Update existing token
                                existing_token.token = token
                                existing_token.token_type = token_type
                                existing_token.valid_until = valid_until
                                existing_token.updated_at = datetime.utcnow()
                            else:
                                # Create new token
                                new_token = CustomerToken(
                                    phone=CUSTOMER_PHONE,
                                    email=email,
                                    token=token,
                                    token_type=token_type,
                                    valid_until=valid_until
                                )
                                db.add(new_token)
                            
                            db.commit()
                            response["token_saved"] = True
                            response["phone"] = CUSTOMER_PHONE
                    except Exception as e:
                        response["token_saved"] = False
                        response["save_error"] = str(e)
                
            elif response_type == "SIMPLE":
                # Wrong answer, got a new question
                question_data = response_data.get("question", {})
                if question_data:
                    response["question"] = question_data
                    response["message"] = "Resposta incorreta. Nova pergunta de segurança fornecida."
            else:
                response["message"] = "Resposta inesperada da API"
            
            return response
            
        except Exception as e:
            return {"error": str(e)}




if __name__ == "__main__":
    mcp.run()