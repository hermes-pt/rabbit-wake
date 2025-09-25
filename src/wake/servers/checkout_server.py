#!/usr/bin/env python3
"""
Wake Checkout MCP Server

Provides tools for managing e-commerce checkout flow including cart management,
shipping, payment, and order completion.
"""

import os
from datetime import datetime
from fastmcp import FastMCP
from typing import List, Dict, Any, Optional
from src.wake.services.checkout_service import CheckoutService
from src.wake.db import SessionLocal, CustomerToken


# Create MCP server
mcp = FastMCP("Wake Checkout Server")

# Get customer phone from environment
CUSTOMER_PHONE = os.getenv("CUSTOMER_PHONE")


def get_customer_token():
    """Get customer token from database using CUSTOMER_PHONE"""
    if not CUSTOMER_PHONE:
        raise Exception("Variável de ambiente CUSTOMER_PHONE não está configurada")
    
    with SessionLocal() as db:
        # Get the most recent token for this phone (even if expired)
        token = db.query(CustomerToken).filter(
            CustomerToken.phone == CUSTOMER_PHONE
        ).order_by(CustomerToken.valid_until.desc()).first()
        
        if token:
            now = datetime.utcnow()
            if token.valid_until > now:
                return token.token
            else:
                raise Exception("Token expirado. É necessário fazer o login novamente usando simple_login_start e simple_login_verify")
        else:
            raise Exception("Nenhum token encontrado. É necessário fazer o login usando simple_login_start e simple_login_verify")
    
    return None


def format_checkout_response(checkout_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format checkout response consistently"""
    if not checkout_data:
        return {}
    
    return {
        "checkoutId": checkout_data.get("checkoutId"),
        "total": checkout_data.get("total", 0),
        "subtotal": checkout_data.get("subtotal", 0),
        "shippingFee": checkout_data.get("shippingFee", 0),
        "discount": checkout_data.get("discount", 0),
        "couponDiscount": checkout_data.get("couponDiscount", 0),
        "completed": checkout_data.get("completed", False),
        "products": checkout_data.get("products", []),
        "customer": checkout_data.get("customer"),
        "selectedAddress": checkout_data.get("selectedAddress"),
        "selectedShipping": checkout_data.get("selectedShipping"),
        "selectedPaymentMethod": checkout_data.get("selectedPaymentMethod"),
        "coupon": checkout_data.get("coupon"),
        "orders": checkout_data.get("orders", [])
    }


@mcp.tool()
async def create_checkout(
    product_variant_ids: Optional[str] = None,
    quantities: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new checkout session
    
    Args:
        product_variant_ids: Comma-separated list of product variant IDs (e.g., "265682,265683")
        quantities: Comma-separated list of quantities (e.g., "2,1")
    
    Returns:
        Checkout object with checkoutId, total, subtotal, and products
    """
    async with CheckoutService() as service:
        products = []
        if product_variant_ids and quantities:
            # Parse comma-separated strings
            variant_ids = [id.strip() for id in product_variant_ids.split(',')]
            qty_list = [q.strip() for q in quantities.split(',')]
            
            # Validate that lists have same length
            if len(variant_ids) != len(qty_list):
                raise ValueError("product_variant_ids and quantities must have the same number of items")
            
            # Format products for the API
            for variant_id, quantity in zip(variant_ids, qty_list):
                products.append({
                    "productVariantId": int(variant_id),
                    "quantity": int(quantity)
                })
        
        try:
            result = await service.create_checkout(products)
            return format_checkout_response(result)
        except Exception as e:
            raise Exception(f"Error creating checkout: {str(e)}")


@mcp.tool()
async def add_to_checkout(
    checkout_id: str,
    product_variant_id: str,
    quantity: int = 1
) -> Dict[str, Any]:
    """
    Add products to an existing checkout
    
    Args:
        checkout_id: UUID of the checkout
        product_variant_id: ID of the product variant to add
        quantity: Number of items to add
    
    Returns:
        Updated checkout object
    """
    async with StorefrontAPIClient() as client:
        mutation = """
        mutation AddToCheckout($input: CheckoutProductInput!, $customerAccessToken: String, $recaptchaToken: String) {
            checkoutAddProduct(input: $input, customerAccessToken: $customerAccessToken, recaptchaToken: $recaptchaToken) {
                checkoutId
                total
                subtotal
                shippingFee
                discount
                products {
                    productId
                    productVariantId
                    name
                    sku
                    quantity
                    price
                    ajustedPrice
                    listPrice
                    imageUrl
                }
            }
        }
        """
        
        product_input = {
            "productVariantId": int(product_variant_id),
            "quantity": int(quantity)
        }
        
        variables = {
            "input": {
                "id": checkout_id,
                "products": [product_input]
            },
            "recaptchaToken": None
        }
        
        # Add customer token if available from database
        try:
            customer_token = get_customer_token()
            if customer_token:
                variables["customerAccessToken"] = customer_token
        except Exception as e:
            # Continue without token, but warn about the error
            print(f"Aviso: {str(e)}")
        
        try:
            result = await client.query(mutation, variables)
            if result and "checkoutAddProduct" in result:
                return format_checkout_response(result["checkoutAddProduct"])
            else:
                raise Exception("Failed to add product to checkout")
        except Exception as e:
            raise Exception(f"Error adding to checkout: {str(e)}")


@mcp.tool()
async def update_checkout_product(
    checkout_id: str,
    product_variant_id: str,
    quantity: int
) -> Dict[str, Any]:
    """
    Update product quantity in checkout
    
    NOTE: This mutation appears to succeed but doesn't actually update the quantity.
    Use remove_from_checkout and create_checkout instead.
    
    Args:
        checkout_id: UUID of the checkout
        product_variant_id: ID of the product variant
        quantity: New quantity (0 to remove)
    
    Returns:
        Updated checkout object
    """
    async with StorefrontAPIClient() as client:
        mutation = """
        mutation UpdateCheckoutProduct($input: CheckoutProductUpdateInput!, $customerAccessToken: String) {
            checkoutUpdateProduct(input: $input, customerAccessToken: $customerAccessToken) {
                checkoutId
                total
                subtotal
                shippingFee
                discount
                products {
                    productId
                    productVariantId
                    name
                    sku
                    quantity
                    price
                    ajustedPrice
                    listPrice
                    imageUrl
                }
            }
        }
        """
        
        variables = {
            "input": {
                "id": checkout_id,
                "product": {
                    "productVariantId": int(product_variant_id),
                    "quantity": int(quantity)
                }
            }
        }
        
        # Add customer token if available from database
        try:
            customer_token = get_customer_token()
            if customer_token:
                variables["customerAccessToken"] = customer_token
        except Exception as e:
            # Continue without token, but warn about the error
            print(f"Aviso: {str(e)}")
        
        try:
            result = await client.query(mutation, variables)
            if result and "checkoutUpdateProduct" in result:
                return format_checkout_response(result["checkoutUpdateProduct"])
            else:
                raise Exception("Failed to update product in checkout")
        except Exception as e:
            raise Exception(f"Error updating checkout product: {str(e)}")


@mcp.tool()
async def remove_from_checkout(
    checkout_id: str,
    product_variant_id: str,
    quantity: Optional[str] = None
) -> Dict[str, Any]:
    """
    Remove products from checkout
    
    Args:
        checkout_id: UUID of the checkout
        product_variant_id: ID of the product variant
        quantity: Number to remove (None = remove all)
    
    Returns:
        Updated checkout object
    """
    async with StorefrontAPIClient() as client:
        mutation = """
        mutation RemoveFromCheckout($input: CheckoutProductInput!, $customerAccessToken: String) {
            checkoutRemoveProduct(input: $input, customerAccessToken: $customerAccessToken) {
                checkoutId
                total
                subtotal
                shippingFee
                discount
                products {
                    productId
                    productVariantId
                    name
                    sku
                    quantity
                    price
                    ajustedPrice
                    listPrice
                    imageUrl
                }
            }
        }
        """
        
        # If quantity not specified, assume we want to remove all
        # Since get_checkout might fail, we'll use a high number
        if quantity is None:
            quantity_int = 999  # High number to ensure all items are removed
        else:
            quantity_int = int(quantity)
        
        variables = {
            "input": {
                "id": checkout_id,
                "products": [{
                    "productVariantId": int(product_variant_id),
                    "quantity": quantity_int
                }]
            }
        }
        
        # Add customer token if available from database
        try:
            customer_token = get_customer_token()
            if customer_token:
                variables["customerAccessToken"] = customer_token
        except Exception as e:
            # Continue without token, but warn about the error
            print(f"Aviso: {str(e)}")
        
        try:
            result = await client.query(mutation, variables)
            if result and "checkoutRemoveProduct" in result:
                return format_checkout_response(result["checkoutRemoveProduct"])
            else:
                raise Exception("Failed to remove product from checkout")
        except Exception as e:
            raise Exception(f"Error removing from checkout: {str(e)}")


@mcp.tool()
async def get_checkout(
    checkout_id: str,
    include_available_shipping: bool = False,
    include_available_payments: bool = False
) -> Dict[str, Any]:
    """
    Get detailed checkout information
    
    Args:
        checkout_id: UUID of the checkout
        include_available_shipping: Include shipping options
        include_available_payments: Include payment methods
    
    Returns:
        Complete checkout object with all details
    """
    async with StorefrontAPIClient() as client:
        # Build query based on requested includes
        shipping_fragment = """
            availableShippingMethods {
                shippingQuoteId
                name
                type
                value
                deadline
                shippingMethodId
                distributionCenterName
            }
        """ if include_available_shipping else ""
        
        payment_fragment = """
            availablePaymentMethods {
                paymentMethodId
                name
                installments {
                    installmentNumber
                    value
                    total
                    fees
                }
            }
        """ if include_available_payments else ""
        
        query = f"""
        query GetCheckout($checkoutId: String!, $customerAccessToken: String) {{
            checkout(checkoutId: $checkoutId, customerAccessToken: $customerAccessToken) {{
                checkoutId
                completed
                total
                subtotal
                shippingFee
                discount
                couponDiscount
                customer {{
                    customerId
                    customerName
                    email
                }}
                products {{
                    productId
                    productVariantId
                    name
                    sku
                    quantity
                    price
                    listPrice
                    totalPrice
                    imageUrl
                    brand
                    category
                    gift
                    productAttributes {{
                        name
                        value
                    }}
                }}
                selectedAddress {{
                    id
                    street
                    addressNumber
                    complement
                    neighborhood
                    city
                    state
                    cep
                    receiverName
                    referencePoint
                }}
                selectedShipping {{
                    shippingQuoteId
                    name
                    value
                    deadline
                }}
                selectedPaymentMethod {{
                    paymentMethodId
                    name
                    installments
                }}
                coupon
                {shipping_fragment}
                {payment_fragment}
            }}
        }}
        """
        
        variables = {
            "checkoutId": checkout_id
        }
        
        # Add customer token if available from database
        try:
            customer_token = get_customer_token()
            if customer_token:
                variables["customerAccessToken"] = customer_token
        except Exception as e:
            # Continue without token, but warn about the error
            print(f"Aviso: {str(e)}")
        
        try:
            result = await client.query(query, variables)
            if result and "checkout" in result:
                checkout = result["checkout"]
                # Add the available methods to the formatted response if requested
                formatted = format_checkout_response(checkout)
                if include_available_shipping:
                    formatted["availableShippingMethods"] = checkout.get("availableShippingMethods", [])
                if include_available_payments:
                    formatted["availablePaymentMethods"] = checkout.get("availablePaymentMethods", [])
                return formatted
            else:
                raise Exception("Failed to get checkout")
        except Exception as e:
            raise Exception(f"Error getting checkout: {str(e)}")


@mcp.tool()
async def associate_customer(
    checkout_id: str
) -> Dict[str, Any]:
    """
    Associate customer account with checkout using environment token
    
    Args:
        checkout_id: UUID of the checkout
    
    Returns:
        Updated checkout with customer information
    """
    async with CheckoutService() as service:
        try:
            # Get customer token from database (will be handled by service)
            result = await service.associate_customer(checkout_id)
            return format_checkout_response(result)
        except Exception as e:
            raise Exception(f"Error associating customer: {str(e)}")


@mcp.tool()
async def set_checkout_address(
    checkout_id: str,
    address_id: str
) -> Dict[str, Any]:
    """
    Set delivery address for checkout
    
    Args:
        checkout_id: UUID of the checkout
        address_id: ID of customer's saved address
    
    Returns:
        Updated checkout with selected address
    """
    async with CheckoutService() as service:
        try:
            result = await service.set_checkout_address(checkout_id, address_id)
            return format_checkout_response(result)
        except Exception as e:
            raise Exception(f"Error setting checkout address: {str(e)}")


@mcp.tool()
async def get_shipping_quotes(
    checkout_id: str
) -> List[Dict[str, Any]]:
    """
    Get available shipping quotes for checkout
    
    Args:
        checkout_id: UUID of the checkout
    
    Returns:
        List of shipping options
    """
    async with CheckoutService() as service:
        try:
            return await service.get_shipping_quotes(checkout_id)
        except Exception as e:
            raise Exception(f"Erro ao buscar cotações de frete: {str(e)}")


@mcp.tool()
async def select_shipping(
    checkout_id: str,
    shipping_quote_id: str,
    delivery_schedule_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Select shipping method for checkout
    
    Args:
        checkout_id: UUID of the checkout
        shipping_quote_id: ID from get_shipping_quotes
        delivery_schedule_id: Optional scheduled delivery
    
    Returns:
        Updated checkout with shipping selected
    """
    async with CheckoutService() as service:
        try:
            result = await service.select_shipping(checkout_id, shipping_quote_id, delivery_schedule_id)
            return format_checkout_response(result)
        except Exception as e:
            raise Exception(f"Error selecting shipping: {str(e)}")


@mcp.tool()
async def get_payment_methods(
    checkout_id: str
) -> List[Dict[str, Any]]:
    """
    Get available payment methods
    
    Args:
        checkout_id: UUID of the checkout
    
    Returns:
        List of payment methods with installment options
    """
    async with CheckoutService() as service:
        try:
            # Service already includes 5 second wait
            return await service.get_payment_methods(checkout_id)
        except Exception as e:
            raise Exception(f"Erro ao buscar métodos de pagamento: {str(e)}")

@mcp.tool()
async def select_payment(
    checkout_id: str,
    payment_method_id: str,
    installment_number: int = 1
) -> Dict[str, Any]:
    """
    Select payment method and installments
    
    Args:
        checkout_id: UUID of the checkout
        payment_method_id: ID from get_payment_methods
        installment_number: Number of installments
    
    Returns:
        Updated checkout with payment selected
    """
    async with CheckoutService() as service:
        try:
            # First select payment method
            result = await service.select_payment(checkout_id, payment_method_id)
            
            # If installments > 1, select installment
            if installment_number > 1:
                result = await service.select_installment(checkout_id, installment_number)
                
            return format_checkout_response(result)
        except Exception as e:
            raise Exception(f"Error selecting payment: {str(e)}")


@mcp.tool()
async def apply_coupon(
    checkout_id: str,
    coupon_code: str
) -> Dict[str, Any]:
    """
    Apply discount coupon to checkout
    
    Args:
        checkout_id: UUID of the checkout
        coupon_code: Discount code
    
    Returns:
        Updated checkout with coupon applied
    """
    async with CheckoutService() as service:
        try:
            result = await service.apply_coupon(checkout_id, coupon_code)
            return format_checkout_response(result)
        except Exception as e:
            raise Exception(f"Error applying coupon: {str(e)}")


@mcp.tool()
async def remove_coupon(
    checkout_id: str,
    coupon_code: str
) -> Dict[str, Any]:
    """
    Remove discount coupon from checkout
    
    Args:
        checkout_id: UUID of the checkout
        coupon_code: Coupon to remove
    
    Returns:
        Updated checkout without coupon
    """
    async with CheckoutService() as service:
        try:
            result = await service.remove_coupon(checkout_id, coupon_code)
            return format_checkout_response(result)
        except Exception as e:
            raise Exception(f"Error removing coupon: {str(e)}")


@mcp.tool()
async def list_customer_addresses() -> List[Dict[str, Any]]:
    """
    Lista os endereços salvos do cliente
    
    Returns:
        Lista de endereços do cliente
    """
    async with CheckoutService() as service:
        try:
            addresses = await service.list_customer_addresses()
            # Format addresses for better readability
            formatted_addresses = []
            for addr in addresses:
                formatted_addresses.append({
                    "addressId": addr.get("id"),
                    "street": addr.get("street"),
                    "number": addr.get("addressNumber"),
                    "complement": addr.get("addressDetails"),
                    "neighborhood": addr.get("neighborhood"),
                    "city": addr.get("city"),
                    "state": addr.get("state"),
                    "cep": addr.get("cep"),
                    "referencePoint": addr.get("referencePoint"),
                    "receiverName": addr.get("receiverName"),
                    "phone": addr.get("phone"),
                    "fullAddress": f"{addr.get('street')}, {addr.get('addressNumber')} - {addr.get('neighborhood')} - {addr.get('city')}/{addr.get('state')} - CEP: {addr.get('cep')}"
                })
            return formatted_addresses
        except Exception as e:
            raise Exception(f"Erro ao buscar endereços: {str(e)}")

@mcp.tool()
async def complete_checkout(
    checkout_id: str,
    payment_data: str,
    comments: Optional[str] = None
) -> Dict[str, Any]:
    """
    Complete checkout and create order
    
    Args:
        checkout_id: UUID of the checkout
        payment_data: Payment information (format depends on payment method)
                     - For PIX: "" (empty string)
                     - For Boleto: "cpf=12345678900&telefone=11999999999"
                     - For Credit Card: full card details
        comments: Order comments/notes
    
    Returns:
        Completion result with order details
    """
    async with CheckoutService() as service:
        try:
            result = await service.complete_checkout(checkout_id, payment_data, comments)
            
            # Include the formatted message in the response
            formatted = format_checkout_response(result)
            if "message" in result:
                formatted["message"] = result["message"]
            if "paymentLink" in result:
                formatted["paymentLink"] = result["paymentLink"]
                
            return formatted
        except Exception as e:
            raise Exception(f"Error completing checkout: {str(e)}")


if __name__ == "__main__":
    mcp.run()