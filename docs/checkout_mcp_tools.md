# Checkout MCP Tools Documentation

## Overview
This document outlines the MCP tools needed for checkout functionality in the Wake e-commerce system. These tools follow the existing pattern established by the products server and integrate with the Storefront GraphQL API.

## Architecture Pattern
- Location: `src/wake/servers/checkout_server.py`
- Framework: FastMCP
- API Client: Reuse `StorefrontAPIClient` for GraphQL operations
- Database: May need checkout state persistence (optional)

## Proposed MCP Tools

### 1. create_checkout
**Purpose**: Initialize a new checkout session
```python
@mcp.tool()
async def create_checkout(
    products: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Create a new checkout session
    
    Args:
        products: Optional list of products to add initially
            Each product dict should contain:
            - productVariantId: int (required)
            - quantity: int (required)
            - customization: List[Dict] (optional)
            - metadata: List[Dict] (optional)
    
    Returns:
        Checkout object with:
        - checkoutId: UUID string
        - total: float
        - subtotal: float
        - products: List of products added
    """
```

### 2. add_to_checkout
**Purpose**: Add products to existing checkout
```python
@mcp.tool()
async def add_to_checkout(
    checkout_id: str,
    product_variant_id: int,
    quantity: int = 1,
    customization: Optional[List[Dict[str, Any]]] = None,
    metadata: Optional[List[Dict[str, str]]] = None
) -> Dict[str, Any]:
    """
    Add products to an existing checkout
    
    Args:
        checkout_id: UUID of the checkout
        product_variant_id: ID of the product variant to add
        quantity: Number of items to add
        customization: Product customizations
        metadata: Key-value pairs for custom data
    
    Returns:
        Updated checkout object
    """
```

### 3. update_checkout_product
**Purpose**: Update product quantity in checkout
```python
@mcp.tool()
async def update_checkout_product(
    checkout_id: str,
    product_variant_id: int,
    quantity: int
) -> Dict[str, Any]:
    """
    Update product quantity in checkout
    
    Args:
        checkout_id: UUID of the checkout
        product_variant_id: ID of the product variant
        quantity: New quantity (0 to remove)
    
    Returns:
        Updated checkout object
    """
```

### 4. remove_from_checkout
**Purpose**: Remove products from checkout
```python
@mcp.tool()
async def remove_from_checkout(
    checkout_id: str,
    product_variant_id: int,
    quantity: Optional[int] = None
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
```

### 5. get_checkout
**Purpose**: Retrieve current checkout state
```python
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
        Complete checkout object with:
        - checkoutId, total, subtotal
        - products with details
        - customer info (if associated)
        - selectedAddress, selectedShipping
        - availableShipping (if requested)
        - availablePayments (if requested)
    """
```

### 6. associate_customer
**Purpose**: Link customer account to checkout
```python
@mcp.tool()
async def associate_customer(
    checkout_id: str,
    customer_token: str
) -> Dict[str, Any]:
    """
    Associate customer account with checkout
    
    Args:
        checkout_id: UUID of the checkout
        customer_token: Customer access token
    
    Returns:
        Updated checkout with customer information
    """
```

### 7. set_checkout_address
**Purpose**: Set delivery address
```python
@mcp.tool()
async def set_checkout_address(
    checkout_id: str,
    address_id: str,
    customer_token: str
) -> Dict[str, Any]:
    """
    Set delivery address for checkout
    
    Args:
        checkout_id: UUID of the checkout
        address_id: ID of customer's saved address
        customer_token: Customer access token
    
    Returns:
        Updated checkout with selected address
    """
```

### 8. get_shipping_quotes
**Purpose**: Get available shipping options
```python
@mcp.tool()
async def get_shipping_quotes(
    checkout_id: str
) -> List[Dict[str, Any]]:
    """
    Get available shipping quotes for checkout
    
    Args:
        checkout_id: UUID of the checkout
    
    Returns:
        List of shipping options with:
        - shippingQuoteId: ID to select
        - name: Shipping method name
        - value: Shipping cost
        - deadline: Delivery estimate
        - shippingMethodId: Method ID
    """
```

### 9. select_shipping
**Purpose**: Choose shipping method
```python
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
```

### 10. get_payment_methods
**Purpose**: Get available payment options
```python
@mcp.tool()
async def get_payment_methods(
    checkout_id: str
) -> List[Dict[str, Any]]:
    """
    Get available payment methods
    
    Args:
        checkout_id: UUID of the checkout
    
    Returns:
        List of payment methods with:
        - paymentMethodId: ID to select
        - name: Payment method name
        - installments: Available installment plans
    """
```

### 11. select_payment
**Purpose**: Choose payment method
```python
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
```

### 12. apply_coupon
**Purpose**: Apply discount coupon
```python
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
        Updated checkout with:
        - coupon: Applied coupon details
        - couponDiscount: Discount amount
        - New total with discount
    """
```

### 13. remove_coupon
**Purpose**: Remove discount coupon
```python
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
```

### 14. complete_checkout
**Purpose**: Finalize purchase
```python
@mcp.tool()
async def complete_checkout(
    checkout_id: str,
    payment_data: str,
    customer_token: Optional[str] = None,
    comments: Optional[str] = None
) -> Dict[str, Any]:
    """
    Complete checkout and create order
    
    Args:
        checkout_id: UUID of the checkout
        payment_data: Encrypted payment information
        customer_token: Optional customer access token
        comments: Order comments/notes
    
    Returns:
        Completion result with:
        - completed: bool
        - orders: List of created orders
          - orderId: Order number
          - orderStatus: Current status
          - total: Order total
    """
```

## Implementation Notes

### GraphQL Operations
Each tool will use the corresponding GraphQL mutation/query:
- `createCheckout` mutation
- `checkoutAddProduct` mutation
- `checkoutUpdateProduct` mutation
- `checkoutRemoveProduct` mutation
- `checkout` query
- `checkoutCustomerAssociate` mutation
- `checkoutAddressAssociate` mutation
- `checkoutSelectShippingQuote` mutation
- `checkoutSelectPaymentMethod` mutation
- `checkoutAddCoupon` mutation
- `checkoutRemoveCoupon` mutation
- `checkoutComplete` mutation

### Error Handling
- Invalid checkout ID: Return clear error message
- Product not available: Include available quantity in error
- Invalid coupon: Return coupon validation error
- Missing required fields: Validate before API call
- API errors: Pass through with context

### Data Validation
- Validate UUID format for checkout_id
- Ensure positive integers for quantity
- Validate required fields based on checkout state
- Check token validity for authenticated operations

### Response Consistency
All tools should return consistent checkout structure:
```json
{
    "checkoutId": "uuid",
    "total": 100.00,
    "subtotal": 90.00,
    "shippingFee": 10.00,
    "discount": 0.00,
    "products": [...],
    "customer": {...},
    "selectedAddress": {...},
    "selectedShipping": {...},
    "selectedPaymentMethod": {...}
}
```

## Example Usage Flow

```python
# 1. Create checkout
checkout = await create_checkout()
checkout_id = checkout["checkoutId"]

# 2. Add products
await add_to_checkout(checkout_id, product_variant_id=12345, quantity=2)

# 3. Associate customer (if logged in)
await associate_customer(checkout_id, customer_token)

# 4. Set delivery address
await set_checkout_address(checkout_id, address_id, customer_token)

# 5. Get and select shipping
quotes = await get_shipping_quotes(checkout_id)
await select_shipping(checkout_id, quotes[0]["shippingQuoteId"])

# 6. Get and select payment
payments = await get_payment_methods(checkout_id)
await select_payment(checkout_id, payments[0]["paymentMethodId"])

# 7. Apply coupon (optional)
await apply_coupon(checkout_id, "DISCOUNT10")

# 8. Complete checkout
result = await complete_checkout(checkout_id, payment_data)
order_id = result["orders"][0]["orderId"]
```

## Testing Considerations

1. **Unit Tests**: Mock GraphQL responses for each operation
2. **Integration Tests**: Test full checkout flow with test data
3. **Error Cases**: Invalid IDs, unavailable products, expired tokens
4. **Edge Cases**: Empty cart, multiple shipping groups, partial quantities
5. **Performance**: Concurrent checkouts, large product quantities

## Future Enhancements

1. **Checkout persistence**: Store checkout state in local DB for recovery
2. **Webhook support**: Listen for checkout status changes
3. **Batch operations**: Add/update multiple products in one call
4. **Guest checkout**: Support anonymous checkouts
5. **Saved carts**: List and manage multiple saved checkouts
6. **Checkout templates**: Pre-configured product sets
7. **Inventory validation**: Real-time stock checking
8. **Price monitoring**: Alert on price changes during checkout