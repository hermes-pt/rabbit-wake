"""Checkout service for managing the checkout flow"""
import time
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..api import StorefrontAPIClient
from ..db import SessionLocal, CustomerToken
from .auth_service import AuthService


class CheckoutService:
    """Service for managing checkout operations"""
    
    def __init__(self):
        self.client: Optional[StorefrontAPIClient] = None
        
    async def __aenter__(self):
        self.client = StorefrontAPIClient()
        await self.client.__aenter__()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.__aexit__(exc_type, exc_val, exc_tb)
    
    def get_customer_token(self) -> str:
        """Get valid customer token from database"""
        import os
        
        customer_phone = os.getenv("CUSTOMER_PHONE", "11999999999")
        
        with SessionLocal() as db:
            token = db.query(CustomerToken).filter(
                CustomerToken.phone == customer_phone
            ).order_by(CustomerToken.valid_until.desc()).first()
            
            if not token:
                raise Exception("Nenhum token encontrado. Faça login primeiro.")
            
            if token.valid_until <= datetime.utcnow():
                raise Exception("Token expirado. Faça login novamente.")
                
            return token.token
    
    async def create_checkout(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a new checkout
        
        Args:
            products: List of products with productVariantId and quantity
            
        Returns:
            Checkout data with checkoutId, total, subtotal, etc.
        """
        mutation = """
        mutation CreateCheckout($products: [CheckoutProductItemInput]) {
            createCheckout(products: $products) {
                checkoutId
                total
                subtotal
                products {
                    productVariantId
                    quantity
                    name
                    imageUrl
                    ajustedPrice
                    price
                    sku
                }
            }
        }
        """
        
        result = await self.client.query(mutation, {"products": products})
        
        if result and "createCheckout" in result:
            return result["createCheckout"]
        else:
            raise Exception("Failed to create checkout")
    
    async def associate_customer(self, checkout_id: str, customer_token: Optional[str] = None) -> Dict[str, Any]:
        """
        Associate customer to checkout
        
        Args:
            checkout_id: UUID of the checkout
            customer_token: Optional customer token (will get from DB if not provided)
            
        Returns:
            Updated checkout data
        """
        if not customer_token:
            customer_token = self.get_customer_token()
            
        mutation = """
        mutation AssociateCustomer($customerAccessToken: String!, $checkoutId: Uuid!) {
            checkoutCustomerAssociate(
                customerAccessToken: $customerAccessToken
                checkoutId: $checkoutId
            ) {
                checkoutId
                cep
                total
                subtotal
                customer {
                    customerId
                    customerName
                    email
                    phoneNumber
                }
                selectedAddress {
                    id
                    street
                    addressNumber
                    neighborhood
                    city
                    state
                    cep
                }
                products {
                    productVariantId
                    quantity
                }
            }
        }
        """
        
        variables = {
            "checkoutId": checkout_id,
            "customerAccessToken": customer_token
        }
        
        result = await self.client.query(mutation, variables)
        
        if result and "checkoutCustomerAssociate" in result:
            return result["checkoutCustomerAssociate"]
        else:
            raise Exception("Failed to associate customer")
    
    async def list_customer_addresses(self, customer_token: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List customer saved addresses
        
        Args:
            customer_token: Optional customer token (will get from DB if not provided)
            
        Returns:
            List of customer addresses
        """
        if not customer_token:
            customer_token = self.get_customer_token()
            
        query = """
        query GetCustomerAddresses($customerAccessToken: String!) {
            customer(customerAccessToken: $customerAccessToken) {
                addresses {
                    id
                    street
                    addressNumber
                    addressDetails
                    neighborhood
                    city
                    state
                    cep
                    referencePoint
                    receiverName
                    phone
                }
            }
        }
        """
        
        result = await self.client.query(query, {"customerAccessToken": customer_token})
        
        if result and "customer" in result and "addresses" in result["customer"]:
            return result["customer"]["addresses"]
        else:
            return []
    
    async def set_checkout_address(self, checkout_id: str, address_id: str, 
                                  customer_token: Optional[str] = None) -> Dict[str, Any]:
        """
        Set delivery address for checkout
        
        Args:
            checkout_id: UUID of the checkout
            address_id: ID of customer's saved address
            customer_token: Optional customer token
            
        Returns:
            Updated checkout data
        """
        if not customer_token:
            customer_token = self.get_customer_token()
            
        mutation = """
        mutation SetAddress($customerAccessToken: String!, $addressId: ID!, $checkoutId: Uuid!) {
            checkoutAddressAssociate(
                customerAccessToken: $customerAccessToken
                addressId: $addressId
                checkoutId: $checkoutId
            ) {
                cep
                checkoutId
                url
                updateDate
            }
        }
        """
        
        variables = {
            "checkoutId": checkout_id,
            "addressId": address_id,
            "customerAccessToken": customer_token
        }
        
        result = await self.client.query(mutation, variables)
        
        if result and "checkoutAddressAssociate" in result:
            return result["checkoutAddressAssociate"]
        else:
            raise Exception("Failed to set address")
    
    async def get_shipping_quotes(self, checkout_id: str) -> List[Dict[str, Any]]:
        """
        Get available shipping quotes
        
        Args:
            checkout_id: UUID of the checkout
            
        Returns:
            List of shipping options
        """
        query = """
        query GetShippingQuotes($checkoutId: Uuid!) {
            shippingQuotes(checkoutId: $checkoutId, useSelectedAddress: true) {
                deadline
                name
                shippingQuoteId
                type
                value
            }
        }
        """
        
        result = await self.client.query(query, {"checkoutId": checkout_id})
        
        if result and "shippingQuotes" in result:
            return result["shippingQuotes"]
        else:
            return []
    
    async def select_shipping(self, checkout_id: str, shipping_quote_id: str,
                            delivery_schedule_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Select shipping method
        
        Args:
            checkout_id: UUID of the checkout
            shipping_quote_id: ID from get_shipping_quotes
            delivery_schedule_id: Optional scheduled delivery
            
        Returns:
            Updated checkout data
        """
        mutation = """
        mutation SelectShipping($checkoutId: Uuid!, $shippingQuoteId: Uuid!, $recaptchaToken: String) {
            checkoutSelectShippingQuote(
                checkoutId: $checkoutId
                shippingQuoteId: $shippingQuoteId
                recaptchaToken: $recaptchaToken
            ) {
                checkoutId
                shippingFee
                total
            }
        }
        """
        
        variables = {
            "checkoutId": checkout_id,
            "shippingQuoteId": shipping_quote_id,
            "recaptchaToken": None
        }
        
        result = await self.client.query(mutation, variables)
        
        if result and "checkoutSelectShippingQuote" in result:
            return result["checkoutSelectShippingQuote"]
        else:
            raise Exception("Failed to select shipping")
    
    async def get_checkout_info(self, checkout_id: str) -> Dict[str, Any]:
        """
        Get basic checkout information
        
        Args:
            checkout_id: UUID of the checkout
            
        Returns:
            Checkout data with customer info
        """
        query = """
        query GetCheckout($checkoutId: String!) {
            checkout(checkoutId: $checkoutId) {
                checkoutId
                customer {
                    customerId
                    customerName
                    email
                }
                completed
            }
        }
        """
        
        result = await self.client.query(query, {"checkoutId": checkout_id})
        
        if result and "checkout" in result:
            return result["checkout"]
        else:
            return {}
    
    async def get_assisted_sale_token(self) -> str:
        """
        Get assisted sale token for current customer
        
        Returns:
            Assisted sale (impersonate) token
            
        Raises:
            Exception: If unable to get token with clear error message in Portuguese
        """
        # Get customer email from token
        try:
            customer_token = self.get_customer_token()
        except Exception as e:
            raise Exception(f"Erro ao obter token do cliente: {str(e)}")
        
        customer_query = """
        query GetCustomer($customerAccessToken: String!) {
            customer(customerAccessToken: $customerAccessToken) {
                email
                customerName
            }
        }
        """
        
        result = await self.client.query(
            customer_query,
            {"customerAccessToken": customer_token}
        )
        
        if not result or "customer" not in result:
            raise Exception("Não foi possível obter informações do cliente")
        
        customer_email = result["customer"].get("email")
        if not customer_email:
            raise Exception("Cliente não possui email cadastrado")
        
        # Get assisted sale token
        async with AuthService() as auth:
            return await auth.get_assisted_sale_token(customer_email)
    
    async def get_payment_methods(self, checkout_id: str, wait_time: int = 5) -> List[Dict[str, Any]]:
        """
        Get available payment methods
        
        Args:
            checkout_id: UUID of the checkout
            wait_time: Seconds to wait before querying (default 5s)
            
        Returns:
            List of payment methods
        """
        # Wait to ensure checkout is ready for payment methods
        if wait_time > 0:
            time.sleep(wait_time)
        
        # Get assisted sale token
        assisted_token = await self.get_assisted_sale_token()
        
        query = """
        query GetPaymentMethods($checkoutId: Uuid!, $customerAccessToken: String) {
            paymentMethods(checkoutId: $checkoutId, customerAccessToken: $customerAccessToken) {
                id
                name
                type
            }
        }
        """
        
        variables = {
            "checkoutId": checkout_id,
            "customerAccessToken": assisted_token
        }
        
        result = await self.client.query(query, variables)
        
        if result and "paymentMethods" in result:
            # Filter out credit card payment methods
            payment_methods = result["paymentMethods"]
            filtered_methods = [
                method for method in payment_methods 
                if method.get("type") != "CartaoTransparente" and 
                   "cartão" not in method.get("name", "").lower() and
                   "credit" not in method.get("name", "").lower()
            ]
            return filtered_methods
        else:
            return []
    
    async def select_payment(self, checkout_id: str, payment_method_id: str) -> Dict[str, Any]:
        """
        Select payment method
        
        Args:
            checkout_id: UUID of the checkout
            payment_method_id: ID from get_payment_methods
            
        Returns:
            Updated checkout data
        """
        mutation = """
        mutation SelectPayment($checkoutId: Uuid!, $paymentMethodId: ID!, $recaptchaToken: String) {
            checkoutSelectPaymentMethod(
                checkoutId: $checkoutId
                paymentMethodId: $paymentMethodId
                recaptchaToken: $recaptchaToken
            ) {
                checkoutId
                total
            }
        }
        """
        
        variables = {
            "checkoutId": checkout_id,
            "paymentMethodId": payment_method_id,
            "recaptchaToken": None
        }
        
        result = await self.client.query(mutation, variables)
        
        if result and "checkoutSelectPaymentMethod" in result:
            return result["checkoutSelectPaymentMethod"]
        else:
            raise Exception("Failed to select payment method")
    
    async def select_installment(self, checkout_id: str, installment_number: int) -> Dict[str, Any]:
        """
        Select payment installment
        
        Args:
            checkout_id: UUID of the checkout
            installment_number: Number of installments
            
        Returns:
            Updated checkout data
        """
        mutation = """
        mutation SelectInstallment($checkoutId: Uuid!, $selectedInstallmentNumber: Int!, 
                                  $recaptchaToken: String) {
            checkoutSelectInstallment(
                checkoutId: $checkoutId
                selectedInstallmentNumber: $selectedInstallmentNumber
                recaptchaToken: $recaptchaToken
            ) {
                checkoutId
                total
                selectedPaymentMethod {
                    selectedInstallment {
                        installmentNumber
                        value
                        total
                    }
                }
            }
        }
        """
        
        variables = {
            "checkoutId": checkout_id,
            "selectedInstallmentNumber": installment_number,
            "recaptchaToken": None
        }
        
        result = await self.client.query(mutation, variables)
        
        if result and "checkoutSelectInstallment" in result:
            return result["checkoutSelectInstallment"]
        else:
            raise Exception("Failed to select installment")
    
    async def apply_coupon(self, checkout_id: str, coupon_code: str, 
                          customer_token: Optional[str] = None) -> Dict[str, Any]:
        """
        Apply discount coupon
        
        Args:
            checkout_id: UUID of the checkout
            coupon_code: Discount code
            customer_token: Optional customer token
            
        Returns:
            Updated checkout data
        """
        if not customer_token:
            customer_token = self.get_customer_token()
            
        mutation = """
        mutation ApplyCoupon($checkoutId: Uuid!, $coupon: String!, $customerAccessToken: String) {
            checkoutAddCoupon(
                checkoutId: $checkoutId
                coupon: $coupon
                customerAccessToken: $customerAccessToken
            ) {
                checkoutId
                coupon
                total
                subtotal
            }
        }
        """
        
        variables = {
            "checkoutId": checkout_id,
            "coupon": coupon_code,
            "customerAccessToken": customer_token
        }
        
        result = await self.client.query(mutation, variables)
        
        if result and "checkoutAddCoupon" in result:
            return result["checkoutAddCoupon"]
        else:
            raise Exception("Failed to apply coupon")
    
    async def remove_coupon(self, checkout_id: str, coupon_code: str) -> Dict[str, Any]:
        """
        Remove discount coupon
        
        Args:
            checkout_id: UUID of the checkout
            coupon_code: Coupon to remove
            
        Returns:
            Updated checkout data
        """
        mutation = """
        mutation RemoveCoupon($checkoutId: Uuid!, $coupon: String!) {
            checkoutRemoveCoupon(
                checkoutId: $checkoutId
                coupon: $coupon
            ) {
                checkoutId
                total
                subtotal
            }
        }
        """
        
        variables = {
            "checkoutId": checkout_id,
            "coupon": coupon_code
        }
        
        result = await self.client.query(mutation, variables)
        
        if result and "checkoutRemoveCoupon" in result:
            return result["checkoutRemoveCoupon"]
        else:
            raise Exception("Failed to remove coupon")
    
    async def complete_checkout(self, checkout_id: str, payment_data: str,
                              comments: Optional[str] = None) -> Dict[str, Any]:
        """
        Complete checkout and create order
        
        Args:
            checkout_id: UUID of the checkout
            payment_data: Payment information (format depends on payment method)
                        - For PIX: "" (empty string)
                        - For Boleto: "cpf=12345678900&telefone=11999999999"
                        - For Credit Card: "number=0000%200000%200000%200000&name=Name&month=09&year=2024&expiry=09%2F2024&cvc=531&cpf=12345678900"
            comments: Order comments/notes
            
        Returns:
            Completion result with order details
        """
        # Get assisted sale token
        token_to_use = await self.get_assisted_sale_token()
            
        mutation = """
        mutation CompleteCheckout($checkoutId: Uuid!, $paymentData: String!, 
                                 $customerAccessToken: String, $comments: String, $recaptchaToken: String) {
            checkoutComplete(
                checkoutId: $checkoutId
                paymentData: $paymentData
                customerAccessToken: $customerAccessToken
                comments: $comments
                recaptchaToken: $recaptchaToken
            ) {
                checkoutId
                completed
                orders {
                    orderId
                    orderStatus
                    date
                    totalValue
                    payment {
                        name
                        invoice {
                            digitableLine
                            paymentLink
                        }
                        pix {
                            qrCode
                            qrCodeExpirationDate
                            qrCodeUrl
                        }
                    }
                }
            }
        }
        """
        
        variables = {
            "checkoutId": checkout_id,
            "paymentData": payment_data,
            "customerAccessToken": token_to_use,
            "comments": comments,
            "recaptchaToken": None
        }
        
        result = await self.client.query(mutation, variables)
        
        if result and "checkoutComplete" in result:
            checkout_data = result["checkoutComplete"]
            
            # Add payment link to the response
            checkout_data["paymentLink"] = f"https://www.camys.com.br/checkout/confirmation?checkoutId={checkout_id}"
            
            # Format a natural language message
            if checkout_data.get("orders"):
                order = checkout_data["orders"][0]
                order_id = order.get("orderId")
                total = order.get("totalValue")
                payment = order.get("payment", {})
                payment_name = payment.get("name", "")
                
                message = f"✅ Pedido #{order_id} finalizado com sucesso!\n"
                message += f"Valor total: R$ {total}\n"
                message += f"Forma de pagamento: {payment_name}\n\n"
                
                # PIX payment details
                if payment.get("pix"):
                    pix = payment["pix"]
                    message += "📱 **Dados do PIX:**\n"
                    message += f"- Código PIX (copia e cola): `{pix.get('qrCode')}`\n"
                    message += f"- QR Code: {pix.get('qrCodeUrl')}\n"
                    message += f"- Validade: {pix.get('qrCodeExpirationDate')}\n\n"
                
                message += f"🔗 **Link de acompanhamento do pedido:**\n"
                message += f"{checkout_data['paymentLink']}\n\n"
                
                # Add payment guide for non-Link payment methods
                if payment_name and "link" not in payment_name.lower():
                    message += "💡 **Como pagar:**\n"
                    message += "1. Acesse o link acima\n"
                    message += "2. Clique em 'Finalizar pagamento'\n"
                    message += "3. Escolha a forma de pagamento desejada\n"
                    message += "4. Complete os dados e finalize\n\n"
                
                message += "Obrigado pela sua compra! 🛍️"
                
                checkout_data["message"] = message
            
            return checkout_data
        else:
            raise Exception("Falha ao finalizar o pedido")