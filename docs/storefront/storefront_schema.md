# Wake Storefront GraphQL Schema

## Queries

### `address`
Get informations about an address.

**Arguments:**
- `cep`: CEP - The address zip code.

**Returns:** `AddressNode`

---

### `autocomplete`
Get query completion suggestion.

**Arguments:**
- `limit`: Int
- `partnerAccessToken`: String - The partner access token.
- `query`: String

**Returns:** `Autocomplete`

---

### `banners`
List of banners.

**Arguments:**
- `after`: String - Returns the elements in the list that come after the specified cursor.
- `bannerIds`: [Long!] - Filter the list by specific banner ids.
- `before`: String - Returns the elements in the list that come before the specified cursor.
- `first`: Int - Returns the first _n_ elements from the list.
- `last`: Int - Returns the last _n_ elements from the list.
- `partnerAccessToken`: String
- `sortDirection`: SortDirection!
- `sortKey`: BannerSortKeys!

**Returns:** `BannersConnection`

---

### `brands`
List of brands

**Arguments:**
- `after`: String - Returns the elements in the list that come after the specified cursor.
- `before`: String - Returns the elements in the list that come before the specified cursor.
- `brandInput`: BrandFilterInput - Brand input
- `first`: Int - Returns the first _n_ elements from the list.
- `last`: Int - Returns the last _n_ elements from the list.
- `sortDirection`: SortDirection!
- `sortKey`: BrandSortKeys!

**Returns:** `BrandsConnection`

---

### `buyList`
Retrieve a buylist by the given id.

**Arguments:**
- `id`: Long! - The list ID.
- `partnerAccessToken`: String - The partner access token.

**Returns:** `BuyList`

---

### `calculatePrices`
Prices informations

**Arguments:**
- `partnerAccessToken`: String - The partner access token.
- `products`: [CalculatePricesProductsInput]!

**Returns:** `Prices`

---

### `categories`
List of categories.

**Arguments:**
- `after`: String - Returns the elements in the list that come after the specified cursor.
- `before`: String - Returns the elements in the list that come before the specified cursor.
- `categoryIds`: [Long!] - Filter the list by specific category ids.
- `first`: Int - Returns the first _n_ elements from the list.
- `last`: Int - Returns the last _n_ elements from the list.
- `onlyRoot`: Boolean! - Filter only root categories
- `sortDirection`: SortDirection!
- `sortKey`: CategorySortKeys!
- `urls`: [String] - Filter the list by specific urls

**Returns:** `CategoriesConnection`

---

### `checkout`
Get info from the checkout cart corresponding to the given ID.

**Arguments:**
- `checkoutId`: String! - The cart ID used for checkout operations.
- `customerAccessToken`: String - The customer access token.

**Returns:** `Checkout`

---

### `checkoutLite`
Retrieve essential checkout details for a specific cart.

**Arguments:**
- `checkoutId`: Uuid! - The cart ID

**Returns:** `CheckoutLite`

---

### `contents`
List of contents.

**Arguments:**
- `after`: String - Returns the elements in the list that come after the specified cursor.
- `before`: String - Returns the elements in the list that come before the specified cursor.
- `contentIds`: [Long!] - Filter the list by specific content ids.
- `first`: Int - Returns the first _n_ elements from the list.
- `last`: Int - Returns the last _n_ elements from the list.
- `sortDirection`: SortDirection!
- `sortKey`: ContentSortKeys!

**Returns:** `ContentsConnection`

---

### `customer`
Get informations about a customer from the store.

**Arguments:**
- `customerAccessToken`: String - The customer access token.

**Returns:** `Customer`

---

### `customerAccessTokenDetails`
Get informations about a customer access token.

**Arguments:**
- `customerAccessToken`: String - The customer access token.

**Returns:** `CustomerAccessTokenDetails`

---

### `eventList`
Retrieve an event list by the token.

**Arguments:**
- `eventListToken`: String - The event list token.

**Returns:** `EventList`

---

### `eventListType`
Retrieves event types

**Returns:** `[EventListType]`

---

### `eventLists`
Retrieves a list of store events.

**Arguments:**
- `eventDate`: DateTime - The event date.
- `eventName`: String - The event name.
- `eventType`: String - The event type name.

**Returns:** `[EventListStore]`

---

### `hotsite`
Retrieve a single hotsite. A hotsite consists of products, banners and contents.

**Arguments:**
- `hotsiteId`: Long
- `partnerAccessToken`: String
- `url`: String

**Returns:** `SingleHotsite`

---

### `hotsites`
List of the shop's hotsites. A hotsite consists of products, banners and contents.

**Arguments:**
- `after`: String - Returns the elements in the list that come after the specified cursor.
- `before`: String - Returns the elements in the list that come before the specified cursor.
- `first`: Int - Returns the first _n_ elements from the list.
- `hotsiteIds`: [Long!] - Filter the list by specific hotsite ids.
- `last`: Int - Returns the last _n_ elements from the list.
- `partnerAccessToken`: String
- `sortDirection`: SortDirection!
- `sortKey`: HotsiteSortKeys!

**Returns:** `HotsitesConnection`

---

### `informationGroupFields`
Get information group fields.

**Arguments:**
- `type`: EnumInformationGroup!

**Returns:** `[InformationGroupFieldNode]`

---

### `menuGroups`
List of menu groups.

**Arguments:**
- `partnerAccessToken`: String
- `position`: String
- `url`: String!

**Returns:** `[MenuGroup]`

---

### `newsletterInformationGroupFields`
Get newsletter information group fields.

**Returns:** `[InformationGroupFieldNode]`

---

### `node`
**Arguments:**
- `id`: ID!

**Returns:** `Node`

---

### `nodes`
**Arguments:**
- `ids`: [ID!]!

**Returns:** `[Node]`

---

### `partner`
Get single partner.

**Arguments:**
- `partnerAccessToken`: String! - Filter the partner by access token.

**Returns:** `Partner`

---

### `partnerByCoordinates`
Get partner by Coordinates.

**Arguments:**
- `input`: PartnerByCoordinatesInput! - Filter the partner by Coordinates.

**Returns:** `Partner`

---

### `partnerByRegion`
Get partner by region.

**Arguments:**
- `input`: PartnerByRegionInput! - Filter the partner by cep or region ID.

**Returns:** `Partner`

---

### `partners`
List of partners.

**Arguments:**
- `after`: String - Returns the elements in the list that come after the specified cursor.
- `alias`: [String] - Filter the list by specific alias.
- `before`: String - Returns the elements in the list that come before the specified cursor.
- `first`: Int - Returns the first _n_ elements from the list.
- `last`: Int - Returns the last _n_ elements from the list.
- `names`: [String] - Filter the list by specific names.
- `priceTableIds`: [Int!] - Filter the list by specific price table ids.
- `sortDirection`: SortDirection!
- `sortKey`: PartnerSortKeys!

**Returns:** `PartnersConnection`

---

### `paymentMethods`
Returns the available payment methods for a given cart ID

**Arguments:**
- `checkoutId`: Uuid! - The cart ID used for checking available payment methods.
- `customerAccessToken`: String - The customer access token.

**Returns:** `[paymentMethod]`

---

### `product`
Retrieve a product by the given id.

**Arguments:**
- `ignoreDisplayRules`: Boolean - Ignore product display rules.
- `partnerAccessToken`: String - The partner access token.
- `productId`: Long! - The product ID.

**Returns:** `SingleProduct`

---

### `productAIRecommendationsByCart`
Retrieve a list of product recommendations based on the customer's cart.

**Arguments:**
- `checkoutId`: Uuid! - The cart ID
- `partnerAccessToken`: String - The partner access token.
- `quantity`: Int! - The number of product recommendations.

**Returns:** `[Product]`

---

### `productAIRecommendationsByOrder`
Retrieve a list of product recommendations based on the customer's orders.

**Arguments:**
- `customerAccessToken`: String - The customer access token.
- `partnerAccessToken`: String - The partner access token.
- `quantity`: Int! - The number of product recommendations.

**Returns:** `[Product]`

---

### `productOptions`
Options available for the given product.

**Arguments:**
- `productId`: Long!

**Returns:** `ProductOption`

---

### `productRecommendations`
Retrieve a list of recommended products by product id.

**Arguments:**
- `algorithm`: ProductRecommendationAlgorithm! - Algorithm type.
- `partnerAccessToken`: String - The partner access token.
- `productId`: Long! - The product identifier.
- `quantity`: Int! - The number of product recommendations.

**Returns:** `[Product]`

---

### `products`
Retrieve a list of products by specific filters.

**Arguments:**
- `after`: String - Returns the elements in the list that come after the specified cursor.
- `before`: String - Returns the elements in the list that come before the specified cursor.
- `filters`: ProductExplicitFiltersInput! - The product filters to apply.
- `first`: Int - Returns the first _n_ elements from the list.
- `last`: Int - Returns the last _n_ elements from the list.
- `partnerAccessToken`: String - The partner access token.
- `sortDirection`: SortDirection!
- `sortKey`: ProductSortKeys!

**Returns:** `ProductsConnection`

---

### `scripts`
Retrieve a list of scripts.

**Arguments:**
- `id`: Long - The script Id.
- `name`: String - The script name.
- `pageType`: [ScriptPageType!] - The script page type list.
- `position`: ScriptPosition - The script position.
- `url`: String - Url for available scripts.

**Returns:** `[Script]`

---

### `search`
Search products with cursor pagination.

**Arguments:**
- `autoSecondSearch`: Boolean! - Toggle to perform second search automatically when the primary search returns no products.
- `ignoreDisplayRules`: Boolean! - Ignore product display rules.
- `operation`: Operation! - The operation to perform between query terms.
- `partnerAccessToken`: String - The partner access token.
- `query`: String - The search query.
- `useAI`: Boolean! - Toggle to perform additional research using GenAI.

**Returns:** `Search`

---

### `sellers`
List of sellers

**Arguments:**
- `after`: String - Returns the elements in the list that come after the specified cursor.
- `before`: String - Returns the elements in the list that come before the specified cursor.
- `first`: Int - Returns the first _n_ elements from the list.
- `last`: Int - Returns the last _n_ elements from the list.
- `sellerName`: String - Seller's name or corporate name
- `sortDirection`: SortDirection!
- `sortKey`: ResellerSortKeys!

**Returns:** `SellersConnection`

---

### `shippingQuoteGroups`
Get the shipping quote groups by providing CEP and checkout or products.

**Arguments:**
- `cep`: CEP - CEP to get the shipping quotes.
- `checkoutId`: Uuid! - Checkout identifier to get the shipping quotes.
- `useSelectedAddress`: Boolean - Use the selected address to get the shipping quotes.

**Returns:** `[ShippingQuoteGroup]`

---

### `shippingQuotes`
Get the shipping quotes by providing CEP and checkout or product identifier.

**Arguments:**
- `cep`: CEP - CEP to get the shipping quotes.
- `checkoutId`: Uuid - Checkout identifier to get the shipping quotes.
- `kits`: [kitsInput] - List of kits to get the shipping quotes.
- `productVariantId`: Long - Product identifier to get the shipping quotes.
- `products`: [productsInput] - List of Products to get the shipping quotes.
- `quantity`: Int - Quantity of the product to get the shipping quotes.
- `useSelectedAddress`: Boolean - Use the selected address to get the shipping quotes.

**Returns:** `[ShippingQuote]`

---

### `shop`
Store informations

**Returns:** `Shop`

---

### `shopSetting`
Returns a single store setting

**Arguments:**
- `settingName`: String - Setting name

**Returns:** `ShopSetting`

---

### `shopSettings`
Store settings

**Arguments:**
- `settingNames`: [String] - Setting names

**Returns:** `[ShopSetting]`

---

### `uri`
Get the URI kind.

**Arguments:**
- `partnerAccessToken`: String
- `url`: String!

**Returns:** `Uri`

---


## Mutations

### `checkoutAddCoupon`
Add coupon to checkout


### `checkoutAddKit`
Add kit to an existing checkout


### `checkoutAddMetadata`
Add metadata to checkout


### `checkoutAddMetadataForProductVariant`
Add metadata to a checkout product


### `checkoutAddProduct`
Add products to an existing checkout


### `checkoutAddressAssociate`
Associate the address with a checkout.


### `checkoutClone`
Clones a cart by the given checkout ID, returns the newly created checkout ID


### `checkoutComplete`
Completes a checkout


### `checkoutCustomerAssociate`
Associate the customer with a checkout.


### `checkoutDeleteSuggestedCard`
Delete a suggested card


### `checkoutGiftVariantSelection`
Selects the variant of a gift product


### `checkoutPartnerAssociate`
Associate the partner with a checkout.


### `checkoutPartnerDisassociate`
Disassociates the checkout from the partner and returns a new checkout.


### `checkoutRemoveCoupon`
Remove coupon to checkout


### `checkoutRemoveKit`
Remove kit from an existing checkout


### `checkoutRemoveMetadata`
Removes metadata keys from a checkout


### `checkoutRemoveProduct`
Remove products from an existing checkout


### `checkoutRemoveProductCustomization`
Remove Customization to Checkout


### `checkoutRemoveProductSubscription`
Remove Subscription to Checkout


### `checkoutReset`
Resets a specific area of a checkout


### `checkoutSelectInstallment`
Select installment.


### `checkoutSelectPaymentMethod`
Select payment method.


### `checkoutSelectShippingQuote`
Select shipping quote


### `checkoutUpdateProduct`
Update a product of an existing checkout


### `checkoutUseCheckingAccount`
Use balance checking account checkout


### `createCheckout`
Create a new checkout


### `createNewsletterRegister`
Register an email in the newsletter.


### `createProductReview`
Adds a review to a product variant.


### `createSearchTermRecord`
Record a searched term for admin reports


### `customerAccessTokenCreate`
Creates a new customer access token with an expiration time.


### `customerAccessTokenRenew`
Renews the expiration time of a customer access token. The token must not be expired.


### `customerAddressCreate`
Create an address.


### `customerAddressRemove`
Delete an existing address, if it is not the only registered address


### `customerAddressUpdate`
Change an existing address


### `customerAuthenticateAccessKey`
Authenticate using the provided email and access key.


### `customerAuthenticatedLogin`
Creates a new customer access token with an expiration time.


### `customerCompletePartialRegistration`
Allows the user to complete the required information for a partial registration.


### `customerCreate`
Creates a new customer register.


### `customerEmailChange`
Changes user email.


### `customerImpersonate`
Impersonates a customer, generating an access token with expiration time.


### `customerPasswordChange`
Changes user password.


### `customerPasswordChangeByRecovery`
Change user password by recovery.


### `customerPasswordRecovery`
Sends a password recovery email to the user.


### `customerSendAccessKeyEmail`
Sends an email containing an access key for authentication.


### `customerSimpleLoginStart`
Returns the user associated with a simple login (CPF or Email) if exists, else return a New user.


### `customerSimpleLoginVerifyAnwser`
Verify if the answer to a simple login question is correct, returns a new question if the answer is incorrect


### `customerSocialLoginFacebook`
Returns the user associated with a Facebook account if exists, else return a New user.


### `customerSocialLoginGoogle`
Returns the user associated with a Google account if exists, else return a New user.


### `customerSubscriptionAddressChange`
Allows a customer to change the delivery address for an existing subscription.


### `customerSubscriptionProductAdd`
Add products to an existing subscription


### `customerSubscriptionProductRemove`
Remove products to an existing subscription


### `customerSubscriptionUpdateStatus`
Allows a customer to change an existing subscription status.


### `customerUpdate`
Updates a customer register.


### `eventListAddProduct`
Adds products to the event list.


### `orderChangePayment`
Allows changing the payment method of a specific order


### `partnerAccessTokenCreate`
Creates a new closed scope partner access token with an expiration time.


### `productCounterOfferSubmit`
Submits a counteroffer for a product.


### `productFriendRecommend`
Mutation to recommend a product to a friend


### `productPriceAlert`
Add a price alert.


### `productRestockAlert`
Creates an alert to notify when the product is back in stock.


### `sendGenericForm`
Send a generic form.


### `updateAddress`
Change an existing address


### `wishlistAddProduct`
Adds a product to the customer's wishlist.


### `wishlistRemoveProduct`
Removes a product from the customer's wishlist.



## Types

### AddressNode
| Field | Type | Description |
|-------|------|-------------|
| `cep` | `String` | Zip code. |
| `city` | `String` | Address city. |
| `country` | `String` | Address country. |
| `neighborhood` | `String` | Address neighborhood. |
| `state` | `String` | Address state. |
| `street` | `String` | Address street. |

### Answer
| Field | Type | Description |
|-------|------|-------------|
| `id` | `String` |  |
| `value` | `String` |  |

### Attribute
Attributes available for the variant products from the given productId.

| Field | Type | Description |
|-------|------|-------------|
| `attributeId` | `Long!` | The id of the attribute. |
| `displayType` | `String` | The display type of the attribute. |
| `id` | `ID` | The node unique identifier. |
| `name` | `String` | The name of the attribute. |
| `type` | `String` | The type of the attribute. |
| `values` | `[AttributeValue]` | The values of the attribute. |

### AttributeMatrix
| Field | Type | Description |
|-------|------|-------------|
| `column` | `AttributeMatrixInfo` | Information about the column attribute. |
| `data` | `[[AttributeMatrixProduct]]` | The matrix products data. List of rows. |
| `row` | `AttributeMatrixInfo` | Information about the row attribute. |

### AttributeMatrixInfo
| Field | Type | Description |
|-------|------|-------------|
| `displayType` | `String` |  |
| `name` | `String` |  |
| `values` | `[AttributeMatrixRowColumnInfoValue]` |  |

### AttributeMatrixProduct
| Field | Type | Description |
|-------|------|-------------|
| `available` | `Boolean!` |  |
| `productVariantId` | `Long!` |  |
| `stock` | `Long!` |  |

### AttributeMatrixRowColumnInfoValue
| Field | Type | Description |
|-------|------|-------------|
| `printUrl` | `String` |  |
| `value` | `String` |  |

### AttributeSelection
Attributes available for the variant products from the given productId.

| Field | Type | Description |
|-------|------|-------------|
| `canBeMatrix` | `Boolean!` | Check if the current product attributes can be rendered as a matrix. |
| `candidateVariant` | `ProductVariant` | The candidate variant given the current input filters. Variant may be from brother product Id. |
| `matrix` | `AttributeMatrix` | Informations about the attribute matrix. |
| `selectedVariant` | `ProductVariant` | The selected variant given the current input filters. Variant may be from brother product Id. |
| `selections` | `[AttributeSelectionOption]` | Attributes available for the variant products from the given productId. |

### AttributeSelectionOption
Attributes available for the variant products from the given productId.

| Field | Type | Description |
|-------|------|-------------|
| `attributeId` | `Long!` | The id of the attribute. |
| `displayType` | `String` | The display type of the attribute. |
| `name` | `String` | The name of the attribute. |
| `values` | `[AttributeSelectionOptionValue]` | The values of the attribute. |
| `varyByParent` | `Boolean!` | If the attributes varies by parent. |

### AttributeSelectionOptionValue
| Field | Type | Description |
|-------|------|-------------|
| `alias` | `String` |  |
| `available` | `Boolean!` |  |
| `printUrl` | `String` |  |
| `selected` | `Boolean!` |  |
| `value` | `String` | The value of the attribute. |

### AttributeValue
Attributes values with variants

| Field | Type | Description |
|-------|------|-------------|
| `productVariants` | `[ProductVariant]` | Product variants that have the attribute. |
| `value` | `String` | The value of the attribute. |

### Autocomplete
Get query completion suggestion.

| Field | Type | Description |
|-------|------|-------------|
| `products` | `[Product]` | Suggested products based on the current query. |
| `suggestions` | `[String]` | List of possible query completions. |

### Banner
A banner is usually an image used to show sales, highlight products, announcements or to redirect to another page or hotsite on click.

| Field | Type | Description |
|-------|------|-------------|
| `altText` | `String` | Banner's alternative text. |
| `bannerId` | `Long!` | Banner unique identifier. |
| `bannerName` | `String` | Banner's name. |
| `bannerUrl` | `String` | URL where the banner is stored. |
| `creationDate` | `DateTime` | The date the banner was created. |
| `displayOnAllPages` | `Boolean!` | Field to check if the banner should be displayed on all pages. |
| `displayOnCategories` | `Boolean!` | Field to check if the banner should be displayed on category pages. |
| `displayOnSearches` | `Boolean!` | Field to check if the banner should be displayed on search pages. |
| `displayOnWebsite` | `Boolean!` | Field to check if the banner should be displayed on the website. |
| `displayToPartners` | `Boolean!` | Field to check if the banner should be displayed to partners. |
| `height` | `Int` | The banner's height in px. |
| `id` | `ID` | The node unique identifier. |
| `openNewTab` | `Boolean!` | Field to check if the banner URL should open in another tab on click. |
| `order` | `Int!` | The displaying order of the banner. |
| `position` | `String` | The displaying position of the banner. |
| `searchTerms` | `[String]` | A list of terms to display the banner on search. |
| `title` | `String` | The banner's title. |
| `urlOnClick` | `String` | URL to be redirected on click. |
| `width` | `Int` | The banner's width in px. |

### BannersConnection
A connection to a list of items.

| Field | Type | Description |
|-------|------|-------------|
| `edges` | `[BannersEdge!]` | A list of edges. |
| `nodes` | `[Banner]` | A flattened list of the nodes. |
| `pageInfo` | `PageInfo!` | Information to aid in pagination. |

### BannersEdge
An edge in a connection.

| Field | Type | Description |
|-------|------|-------------|
| `cursor` | `String!` | A cursor for use in pagination. |
| `node` | `Banner` | The item at the end of the edge. |

### BestInstallment
| Field | Type | Description |
|-------|------|-------------|
| `discount` | `Boolean!` | Wether the installment has discount. |
| `displayName` | `String` | The custom display name of the best installment plan option. |
| `fees` | `Boolean!` | Wether the installment has fees. |
| `name` | `String` | The name of the best installment plan option. |
| `number` | `Int!` | The number of installments. |
| `totalValue` | `Decimal!` | The total value representing the combined amount of all installments. |
| `value` | `Decimal!` | The value of the installment. |

### Brand
Informations about brands and its products.

| Field | Type | Description |
|-------|------|-------------|
| `active` | `Boolean!` | If the brand is active at the platform. |
| `alias` | `String` | The alias for the brand's hotsite. |
| `brandId` | `Long!` | Brand unique identifier. |
| `createdAt` | `DateTime!` | The date the brand was created in the database. |
| `fullUrlLogo` | `String` | The full brand logo URL. |
| `id` | `ID` | The node unique identifier. |
| `name` | `String` | The brand's name. |
| `products` | `ProductsConnection` | A list of products from the brand. |
| `updatedAt` | `DateTime!` | The last update date. |
| `urlCarrossel` | `String` | A web address to be redirected. |
| `urlLink` | `String` | A web address linked to the brand. |
| `urlLogo` | `String` | The url of the brand's logo. |

### BrandsConnection
A connection to a list of items.

| Field | Type | Description |
|-------|------|-------------|
| `edges` | `[BrandsEdge!]` | A list of edges. |
| `nodes` | `[Brand]` | A flattened list of the nodes. |
| `pageInfo` | `PageInfo!` | Information to aid in pagination. |
| `totalCount` | `Int!` |  |

### BrandsEdge
An edge in a connection.

| Field | Type | Description |
|-------|------|-------------|
| `cursor` | `String!` | A cursor for use in pagination. |
| `node` | `Brand` | The item at the end of the edge. |

### Breadcrumb
Informations about breadcrumb.

| Field | Type | Description |
|-------|------|-------------|
| `link` | `String` | Breadcrumb link. |
| `text` | `String` | Breadcrumb text. |

### BuyBox
BuyBox informations.

| Field | Type | Description |
|-------|------|-------------|
| `installmentPlans` | `[InstallmentPlan]` | List of the possibles installment plans. |
| `maximumPrice` | `Decimal` | Maximum price among sellers. |
| `minimumPrice` | `Decimal` | Minimum price among sellers. |
| `quantityOffers` | `Int` | Quantity of offers. |
| `sellers` | `[Seller]` | List of sellers. |

### BuyList
A buy list represents a list of items for sale in the store.

| Field | Type | Description |
|-------|------|-------------|
| `addToCartFromSpot` | `Boolean` | Check if the product can be added to cart directly from spot. |
| `alias` | `String` | The product url alias. |
| `aliasComplete` | `String` | The complete product url alias. |
| `attributeSelections` | `AttributeSelection` | Information about the possible selection attributes. |
| `attributes` | `[ProductAttribute]` | List of the product attributes. |
| `author` | `String` | The product author. |
| `available` | `Boolean` | Field to check if the product is available in stock. |
| `averageRating` | `Int` | The product average rating. From 0 to 5. |
| `averageRatingFloat` | `Float` | The average rating of the product. From 0 to 5 with two decimal places. |
| `breadcrumbs` | `[Breadcrumb]` | List of product breadcrumbs. |
| `buyBox` | `BuyBox` | BuyBox informations. |
| `buyListId` | `Long` | The unique identifier if the node is a Buy List. |
| `buyListProducts` | `[BuyListProduct]` |  |
| `buyTogether` | `[ProductBuyTogetherNode]` | Buy together products. |
| `buyTogetherGroups` | `[BuyTogetherGroup]` | Buy together groups products. |
| `collection` | `String` | The product collection. |
| `condition` | `String` | The product condition. |
| `counterOffer` | `Boolean` | Checks if the product allows counteroffers. |
| `createdAt` | `DateTime` | The product creation date. |
| `customizations` | `[Customization]` | A list of customizations available for the given products. |
| `deadline` | `Int` | The product delivery deadline. |
| `deadlineAlert` | `DeadlineAlert` | Product deadline alert informations. |
| `display` | `Boolean` | Check if the product should be displayed. |
| `displayOnlyPartner` | `Boolean` | Check if the product should be displayed only for partners. |
| `displaySearch` | `Boolean` | Check if the product should be displayed on search. |
| `ean` | `String` | The product's unique EAN. |
| `freeShipping` | `Boolean` | Check if the product offers free shipping. |
| `gender` | `String` | The product gender. |
| `height` | `Float` | The height of the product. |
| `id` | `ID` | The node unique identifier. |
| `images` | `[Image]` | List of the product images. |
| `informations` | `[Information]` | List of the product insformations. |
| `kit` | `Boolean!` |  |
| `length` | `Float` | The length of the product. |
| `mainVariant` | `Boolean` | Check if its the main variant. |
| `maximumOrderQuantity` | `Int` | The product maximum quantity for an order. |
| `minimumOrderQuantity` | `Int` | The product minimum quantity for an order. |
| `newRelease` | `Boolean` | Check if the product is a new release. |
| `numberOfVotes` | `Int` | The number of votes that the average rating consists of. |
| `parallelOptions` | `[String]` | Product parallel options information. |
| `parentId` | `Long` | Parent product unique identifier. |
| `prices` | `Prices` | The product prices. |
| `productBrand` | `ProductBrand` | Summarized informations about the brand of the product. |
| `productCategories` | `[ProductCategory]` | Summarized informations about the categories of the product. |
| `productId` | `Long` | Product unique identifier. |
| `productName` | `String` | The product name. |
| `productSubscription` | `ProductSubscription` | Summarized informations about the subscription of the product. |
| `productVariantId` | `Long` | Variant unique identifier. |
| `promotions` | `[Promotion]` | List of promotions this product belongs to. |
| `publisher` | `String` | The product publisher |
| `reviews` | `[Review]` | List of customer reviews for this product. |
| `seller` | `Seller` | The product seller. |
| `seo` | `[SEO]` | Product SEO informations. |
| `similarProducts` | `[SimilarProduct]` | List of similar products.  |
| `sku` | `String` | The product's unique SKU. |
| `spotAttributes` | `[String]` | The values of the spot attribute. |
| `spotInformation` | `String` | The product spot information. |
| `spotlight` | `Boolean` | Check if the product is on spotlight. |
| `stock` | `Long` | The available aggregated product stock (all variants) at the default distribution center. |
| `stocks` | `[Stock]` | List of the product stocks on different distribution centers. |
| `subscriptionGroups` | `[SubscriptionGroup]` | List of subscription groups this product belongs to. |
| `telesales` | `Boolean` | Check if the product is a telesale. |
| `updatedAt` | `DateTime` | The product last update date. |
| `urlVideo` | `String` | The product video url. |
| `variantName` | `String` | The variant name. |
| `variantStock` | `Long` | The available aggregated variant stock at the default distribution center. |
| `weight` | `Float` | The weight of the product. |
| `width` | `Float` | The width of the product. |

### BuyListProduct
Contains the id and quantity of a product in the buy list.

| Field | Type | Description |
|-------|------|-------------|
| `addToCartFromSpot` | `Boolean` | Check if the product can be added to cart directly from spot. |
| `alias` | `String` | The product url alias. |
| `aliasComplete` | `String` | The complete product url alias. |
| `attributes` | `[ProductAttribute]` | List of the product attributes. |
| `author` | `String` | The product author. |
| `available` | `Boolean` | Field to check if the product is available in stock. |
| `averageRating` | `Int` | The product average rating. From 0 to 5. |
| `averageRatingFloat` | `Float` | The average rating of the product. From 0 to 5 with two decimal places. |
| `buyBox` | `BuyBox` | BuyBox informations. |
| `buyListId` | `Long` | The unique identifier if the node is a Buy List. |
| `buyListProducts` | `[BuyListProduct]` |  |
| `collection` | `String` | The product collection. |
| `condition` | `String` | The product condition. |
| `counterOffer` | `Boolean` | Checks if the product allows counteroffers. |
| `createdAt` | `DateTime` | The product creation date. |
| `deadline` | `Int` | The product delivery deadline. |
| `display` | `Boolean` | Check if the product should be displayed. |
| `displayOnlyPartner` | `Boolean` | Check if the product should be displayed only for partners. |
| `displaySearch` | `Boolean` | Check if the product should be displayed on search. |
| `ean` | `String` | The product's unique EAN. |
| `freeShipping` | `Boolean` | Check if the product offers free shipping. |
| `gender` | `String` | The product gender. |
| `height` | `Float` | The height of the product. |
| `id` | `ID` | The node unique identifier. |
| `images` | `[Image]` | List of the product images. |
| `includeSameParent` | `Boolean!` |  |
| `informations` | `[Information]` | List of the product insformations. |
| `length` | `Float` | The length of the product. |
| `mainVariant` | `Boolean` | Check if its the main variant. |
| `maximumOrderQuantity` | `Int` | The product maximum quantity for an order. |
| `minimumOrderQuantity` | `Int` | The product minimum quantity for an order. |
| `newRelease` | `Boolean` | Check if the product is a new release. |
| `numberOfVotes` | `Int` | The number of votes that the average rating consists of. |
| `parentId` | `Long` | Parent product unique identifier. |
| `price` | `Decimal` |  |
| `prices` | `Prices` | The product prices. |
| `productBrand` | `ProductBrand` | Summarized informations about the brand of the product. |
| `productCategories` | `[ProductCategory]` | Summarized informations about the categories of the product. |
| `productId` | `Long` | Product unique identifier. |
| `productName` | `String` | The product name. |
| `productSubscription` | `ProductSubscription` | Summarized informations about the subscription of the product. |
| `productVariantId` | `Long` | Variant unique identifier. |
| `promotions` | `[Promotion]` | List of promotions this product belongs to. |
| `publisher` | `String` | The product publisher |
| `quantity` | `Int!` |  |
| `seller` | `Seller` | The product seller. |
| `similarProducts` | `[SimilarProduct]` | List of similar products.  |
| `sku` | `String` | The product's unique SKU. |
| `spotAttributes` | `[String]` | The values of the spot attribute. |
| `spotInformation` | `String` | The product spot information. |
| `spotlight` | `Boolean` | Check if the product is on spotlight. |
| `stock` | `Long` | The available aggregated product stock (all variants) at the default distribution center. |
| `stocks` | `[Stock]` | List of the product stocks on different distribution centers. |
| `subscriptionGroups` | `[SubscriptionGroup]` | List of subscription groups this product belongs to. |
| `telesales` | `Boolean` | Check if the product is a telesale. |
| `updatedAt` | `DateTime` | The product last update date. |
| `urlVideo` | `String` | The product video url. |
| `variantName` | `String` | The variant name. |
| `variantStock` | `Long` | The available aggregated variant stock at the default distribution center. |
| `weight` | `Float` | The weight of the product. |
| `width` | `Float` | The width of the product. |

### BuyTogetherGroup
BuyTogetherGroups informations.

| Field | Type | Description |
|-------|------|-------------|
| `name` | `String` | BuyTogether name |
| `products` | `[ProductBuyTogetherNode]` | BuyTogether products |
| `type` | `BuyTogetherType!` | BuyTogether type |

### CategoriesConnection
A connection to a list of items.

| Field | Type | Description |
|-------|------|-------------|
| `edges` | `[CategoriesEdge!]` | A list of edges. |
| `nodes` | `[Category]` | A flattened list of the nodes. |
| `pageInfo` | `PageInfo!` | Information to aid in pagination. |

### CategoriesEdge
An edge in a connection.

| Field | Type | Description |
|-------|------|-------------|
| `cursor` | `String!` | A cursor for use in pagination. |
| `node` | `Category` | The item at the end of the edge. |

### Category
Categories are used to arrange your products into different sections by similarity.

| Field | Type | Description |
|-------|------|-------------|
| `categoryId` | `Long!` | Category unique identifier. |
| `children` | `[Category]` | A list of child categories, if it exists. |
| `description` | `String` | A description to the category. |
| `displayMenu` | `Boolean!` | Field to check if the category is displayed in the store's menu. |
| `hotsiteAlias` | `String` | The hotsite alias. |
| `hotsiteUrl` | `String` | The URL path for the category. |
| `id` | `ID` | The node unique identifier. |
| `imageUrl` | `String` | The url to access the image linked to the category. |
| `imageUrlLink` | `String` | The web address to access the image linked to the category. |
| `name` | `String` | The category's name. |
| `parent` | `Category` | The parent category, if it exists. |
| `parentCategoryId` | `Long!` | The parent category unique identifier. |
| `position` | `Int!` | The position the category will be displayed. |
| `products` | `ProductsConnection` | A list of products associated with the category. |
| `urlLink` | `String` | A web address linked to the category. |

### Checkout
| Field | Type | Description |
|-------|------|-------------|
| `cep` | `Int` | The CEP. |
| `checkingAccountActive` | `Boolean!` | Indicates if the checking account is being used. |
| `checkingAccountValue` | `Decimal` | Total used from checking account. |
| `checkoutId` | `Uuid!` | The checkout unique identifier. |
| `completed` | `Boolean!` | Indicates if the checkout is completed. |
| `coupon` | `String` | The coupon for discounts. |
| `couponDiscount` | `Decimal!` | The total coupon discount applied at checkout. |
| `customer` | `CheckoutCustomer` | The customer associated with the checkout. |
| `customizationValue` | `Decimal!` | The total value of customizations added to the products. |
| `discount` | `Decimal!` | The discount applied at checkout excluding any coupons. |
| `id` | `ID` | The node unique identifier. |
| `kits` | `[CheckoutKit]` | A list of kits associated with the checkout. |
| `login` | `String` |  |
| `metadata` | `[Metadata]` | The metadata related to this checkout. |
| `minimumRequirements` | `MinimumRequirementsCheckoutNode` | Indicates the minimum requirements for completing the checkout. |
| `orders` | `[CheckoutOrder]` | The checkout orders informations. |
| `paymentFees` | `Decimal!` | The additional fees applied based on the payment method. |
| `products` | `[CheckoutProductNode]` | A list of products associated with the checkout. |
| `selectedAddress` | `CheckoutAddress` | The selected delivery address for the checkout. |
| `selectedPaymentMethod` | `SelectedPaymentMethod` | The selected payment method |
| `selectedShipping` | `ShippingNode` | Selected Shipping. |
| `selectedShippingGroups` | `[CheckoutShippingQuoteGroupNode]` | Selected shipping quote groups. |
| `shippingFee` | `Decimal!` | The shipping fee. |
| `subtotal` | `Decimal!` | The subtotal value. |
| `total` | `Decimal!` | The total value. |
| `totalDiscount` | `Decimal!` | The total discount applied at checkout. |
| `updateDate` | `DateTime!` | The last update date. |
| `url` | `String` | Url for the current checkout id. |

### CheckoutAddress
Represents an address node in the checkout.

| Field | Type | Description |
|-------|------|-------------|
| `addressNumber` | `String` | The street number of the address. |
| `cep` | `Int!` | The ZIP code of the address. |
| `city` | `String` | The city of the address. |
| `complement` | `String` | The additional address information. |
| `id` | `ID` | The node unique identifier. |
| `neighborhood` | `String` | The neighborhood of the address. |
| `receiverName` | `String` | Receiver's name |
| `referencePoint` | `String` | The reference point for the address. |
| `state` | `String` | The state of the address. |
| `street` | `String` | The street name of the address. |

### CheckoutCustomer
Represents a customer node in the checkout.

| Field | Type | Description |
|-------|------|-------------|
| `checkingAccountBalance` | `Decimal` | Customer's checking account balance. |
| `cnpj` | `String` | Taxpayer identification number for businesses. |
| `cpf` | `String` | Brazilian individual taxpayer registry identification. |
| `creditLimit` | `Decimal!` | Customer's credit limit. |
| `creditLimitBalance` | `Decimal!` | Customer's credit balance. |
| `customerId` | `Long!` | Customer's unique identifier. |
| `customerName` | `String` | Customer's name. |
| `email` | `String` | The email address of the customer. |
| `phoneNumber` | `String` | Customer's phone number. |

### CheckoutKit
| Field | Type | Description |
|-------|------|-------------|
| `ajustedPrice` | `Decimal!` | The price adjusted with promotions and other price changes |
| `alias` | `String` | The kit alias |
| `imageUrl` | `String` | The kit URL image |
| `kitGroupId` | `String` | The kit unique identifier |
| `kitId` | `Long!` | The kit identifier |
| `listPrice` | `Decimal!` | The kit list price |
| `name` | `String` | The kit name |
| `price` | `Decimal!` | The kit price |
| `products` | `[CheckoutProductNode]` | The products contained in this kit |
| `quantity` | `Int!` | The kit quantity |
| `totalAdjustedPrice` | `Decimal!` | The total price adjusted with promotions and other price changes |
| `totalListPrice` | `Decimal!` | The total list price |

### CheckoutLite
| Field | Type | Description |
|-------|------|-------------|
| `completed` | `Boolean!` | Indicates if the checkout is completed. |
| `customerId` | `Long` | The customer ID associated with the checkout. |

### CheckoutOrder
Represents a node in the checkout order.

| Field | Type | Description |
|-------|------|-------------|
| `adjustments` | `[CheckoutOrderAdjustment]` | The list of adjustments applied to the order. |
| `date` | `DateTime!` | The date of the order. |
| `delivery` | `CheckoutOrderDelivery` | Details of the delivery or store pickup. |
| `discountValue` | `Decimal!` | The discount value of the order. |
| `dispatchTimeText` | `String` | The dispatch time text from the shop settings. |
| `interestValue` | `Decimal!` | The interest value of the order. |
| `orderId` | `Long!` | The ID of the order. |
| `orderStatus` | `OrderStatus!` | The order status. |
| `orderStatusDisplay` | `String` | The order status display. |
| `payment` | `CheckoutOrderPayment` | The payment information. |
| `products` | `[CheckoutOrderProduct]` | The list of products in the order. |
| `shippingValue` | `Decimal!` | The shipping value of the order. |
| `totalValue` | `Decimal!` | The total value of the order. |

### CheckoutOrderAddress
The delivery or store Pickup Address.

| Field | Type | Description |
|-------|------|-------------|
| `address` | `String` | The street address. |
| `cep` | `String` | The ZIP code. |
| `city` | `String` | The city. |
| `complement` | `String` | Additional information or details about the address. |
| `isPickupStore` | `Boolean!` | Indicates whether the order is for store pickup. |
| `name` | `String` | The name. |
| `neighborhood` | `String` | The neighborhood. |
| `pickupStoreText` | `String` | . |

### CheckoutOrderAdjustment
Represents an adjustment applied to checkout.

| Field | Type | Description |
|-------|------|-------------|
| `name` | `String` | The name of the adjustment. |
| `type` | `String` | The type of the adjustment. |
| `value` | `Decimal!` | The value of the adjustment. |

### CheckoutOrderCardPayment
This represents a Card payment node in the checkout order.

| Field | Type | Description |
|-------|------|-------------|
| `brand` | `String` | The brand card. |
| `cardInterest` | `Decimal!` | The interest generated by the card. |
| `installments` | `Int!` | The installments generated for the card. |
| `name` | `String` | The cardholder name. |
| `number` | `String` | The final four numbers on the card. |

### CheckoutOrderDelivery
The delivery or store pickup details.

| Field | Type | Description |
|-------|------|-------------|
| `address` | `CheckoutOrderAddress` | The delivery or store pickup address. |
| `cost` | `Decimal!` | The cost of delivery or pickup. |
| `deliveryTime` | `Int!` | The estimated delivery or pickup time, in days. |
| `deliveryTimeInHours` | `Int` | The estimated delivery or pickup time, in hours. |
| `name` | `String` | The name of the recipient. |

### CheckoutOrderInvoicePayment
The invoice payment information.

| Field | Type | Description |
|-------|------|-------------|
| `digitableLine` | `String` | The digitable line. |
| `paymentLink` | `String` | The payment link. |

### CheckoutOrderPayment
The checkout order payment.

| Field | Type | Description |
|-------|------|-------------|
| `card` | `CheckoutOrderCardPayment` | The card payment information. |
| `invoice` | `CheckoutOrderInvoicePayment` | The bank invoice payment information. |
| `name` | `String` | The name of the payment method. |
| `pix` | `CheckoutOrderPixPayment` | The Pix payment information. |
| `type` | `String` | The type of payment method. |

### CheckoutOrderPixPayment
This represents a Pix payment node in the checkout order.

| Field | Type | Description |
|-------|------|-------------|
| `qrCode` | `String` | The QR code. |
| `qrCodeExpirationDate` | `DateTime` | The expiration date of the QR code. |
| `qrCodeUrl` | `String` | The image URL of the QR code. |

### CheckoutOrderProduct
Represents a node in the checkout order products.

| Field | Type | Description |
|-------|------|-------------|
| `adjustments` | `[CheckoutOrderProductAdjustment]` | The list of adjustments applied to the product. |
| `attributes` | `[CheckoutOrderProductAttribute]` | The list of attributes of the product. |
| `imageUrl` | `String` | The image URL of the product. |
| `name` | `String` | The name of the product. |
| `productVariantId` | `Long!` | The ID of the product variant. |
| `quantity` | `Int!` | The quantity of the product. |
| `unitValue` | `Decimal!` | The unit value of the product. |
| `value` | `Decimal!` | The value of the product. |

### CheckoutOrderProductAdjustment
Represents an adjustment applied to a product in the checkout order.

| Field | Type | Description |
|-------|------|-------------|
| `additionalInformation` | `String` | Additional information about the adjustment. |
| `name` | `String` | The name of the adjustment. |
| `type` | `String` | The type of the adjustment. |
| `value` | `Decimal!` | The value of the adjustment. |

### CheckoutOrderProductAttribute
Represents an attribute of a product.

| Field | Type | Description |
|-------|------|-------------|
| `name` | `String` | The name of the attribute. |
| `value` | `String` | The value of the attribute. |

### CheckoutProductAdjustmentNode
| Field | Type | Description |
|-------|------|-------------|
| `observation` | `String` | The observation referent adjustment in Product |
| `type` | `String` | The type that was applied in product adjustment |
| `value` | `Decimal!` | The value that was applied to the product adjustment |

### CheckoutProductAttributeNode
| Field | Type | Description |
|-------|------|-------------|
| `name` | `String` | The attribute name |
| `type` | `Int!` | The attribute type |
| `value` | `String` | The attribute value |

### CheckoutProductCustomizationNode
| Field | Type | Description |
|-------|------|-------------|
| `availableCustomizations` | `[Customization]` | The available product customizations. |
| `id` | `ID` | The product customization unique identifier. |
| `values` | `[CheckoutProductCustomizationValueNode]` | The product customization values. |

### CheckoutProductCustomizationValueNode
| Field | Type | Description |
|-------|------|-------------|
| `cost` | `Decimal!` | The product customization cost. |
| `customizationId` | `Long!` | The customization unique identifier. |
| `name` | `String` | The product customization name. |
| `value` | `String` | The product customization value. |

### CheckoutProductNode
| Field | Type | Description |
|-------|------|-------------|
| `adjustments` | `[CheckoutProductAdjustmentNode]` | The product adjustment information |
| `ajustedPrice` | `Decimal!` | The price adjusted with promotions and other price changes |
| `attributeSelections` | `AttributeSelection` | Information about the possible selection attributes. |
| `brand` | `String` | The product brand |
| `category` | `String` | The product category |
| `customization` | `CheckoutProductCustomizationNode` | The product customization. |
| `gift` | `Boolean!` | If the product is a gift |
| `googleCategory` | `[String]` | The product Google category |
| `imageUrl` | `String` | The product URL image |
| `informations` | `[String]` | The product informations |
| `installmentFee` | `Boolean!` | The product installment fee |
| `installmentValue` | `Decimal!` | The product installment value |
| `kit` | `Boolean!` | The product has a kit |
| `listPrice` | `Decimal!` | The product list price |
| `metadata` | `[Metadata]` | The metadata related to this checkout. |
| `name` | `String` | The product name |
| `numberOfInstallments` | `Int!` | The product number of installments |
| `price` | `Decimal!` | The product price |
| `productAttributes` | `[CheckoutProductAttributeNode]` | The product attributes |
| `productId` | `Long!` | The product unique identifier |
| `productVariantId` | `Long!` | The product variant unique identifier |
| `quantity` | `Int!` | The product quantity |
| `seller` | `CheckoutProductSellerNode` | The product seller. |
| `shippingDeadline` | `CheckoutShippingDeadlineNode` | The product shipping deadline |
| `sku` | `String` | The product SKU |
| `subscription` | `CheckoutProductSubscription` | The product subscription information |
| `totalAdjustedPrice` | `Decimal!` | The total price adjusted with promotions and other price changes |
| `totalListPrice` | `Decimal!` | The total list price |
| `url` | `String` | The product URL |

### CheckoutProductSellerNode
| Field | Type | Description |
|-------|------|-------------|
| `distributionCenterId` | `String` | The distribution center ID. |
| `sellerName` | `String` | The seller name. |

### CheckoutProductSubscription
Information for the subscription of a product in checkout.

| Field | Type | Description |
|-------|------|-------------|
| `availableSubscriptions` | `[CheckoutProductSubscriptionItemNode]` | The available subscriptions. |
| `selected` | `CheckoutProductSubscriptionItemNode` | The selected subscription. |

### CheckoutProductSubscriptionItemNode
| Field | Type | Description |
|-------|------|-------------|
| `name` | `String` | Display text. |
| `recurringDays` | `Int!` | The number of days of the recurring type. |
| `recurringTypeId` | `Long!` | The recurring type id. |
| `selected` | `Boolean!` | If selected. |
| `subscriptionGroupDiscount` | `Decimal!` | Subscription group discount value. |
| `subscriptionGroupId` | `Long!` | The subscription group id. |

### CheckoutShippingDeadlineNode
| Field | Type | Description |
|-------|------|-------------|
| `deadline` | `Int!` | The shipping deadline |
| `description` | `String` | The shipping description |
| `secondDescription` | `String` | The shipping second description |
| `secondTitle` | `String` | The shipping second title |
| `title` | `String` | The shipping title |

### CheckoutShippingQuoteGroupNode
| Field | Type | Description |
|-------|------|-------------|
| `distributionCenter` | `DistributionCenter` | The distribution center. |
| `products` | `[ShippingQuoteGroupProduct]` | The products related to the shipping quote group. |
| `selectedShipping` | `ShippingNode` | Selected Shipping. |

### Content
Contents are used to show things to the user.

| Field | Type | Description |
|-------|------|-------------|
| `content` | `String` | The content in html to be displayed. |
| `contentId` | `Long!` | Content unique identifier. |
| `creationDate` | `DateTime` | The date the content was created. |
| `height` | `Int` | The content's height in px. |
| `id` | `ID` | The node unique identifier. |
| `position` | `String` | The content's position. |
| `searchTerms` | `[String]` | A list of terms to display the content on search. |
| `title` | `String` | The content's title. |
| `width` | `Int` | The content's width in px. |

### ContentsConnection
A connection to a list of items.

| Field | Type | Description |
|-------|------|-------------|
| `edges` | `[ContentsEdge!]` | A list of edges. |
| `nodes` | `[Content]` | A flattened list of the nodes. |
| `pageInfo` | `PageInfo!` | Information to aid in pagination. |

### ContentsEdge
An edge in a connection.

| Field | Type | Description |
|-------|------|-------------|
| `cursor` | `String!` | A cursor for use in pagination. |
| `node` | `Content` | The item at the end of the edge. |

### Customer
A customer from the store.

| Field | Type | Description |
|-------|------|-------------|
| `address` | `CustomerAddressNode` | A specific customer's address. |
| `addresses` | `[CustomerAddressNode]` | Customer's addresses. |
| `birthDate` | `DateTime!` | Customer's birth date. |
| `businessPhoneNumber` | `String` | Customer's business phone number. |
| `checkingAccountBalance` | `Decimal` | Customer's checking account balance. |
| `checkingAccountHistory` | `[CustomerCheckingAccountHistoryNode]` | Customer's checking account History. |
| `cnpj` | `String` | Taxpayer identification number for businesses. |
| `companyName` | `String` | Entities legal name. |
| `cpf` | `String` | Brazilian individual taxpayer registry identification. |
| `creationDate` | `DateTime!` | Creation Date. |
| `customerId` | `Long!` | Customer's unique identifier. |
| `customerName` | `String` | Customer's name. |
| `customerType` | `String` | Indicates if it is a natural person or company profile. |
| `deliveryAddress` | `CustomerAddressNode` | Customer's delivery address. |
| `digitalProducts` | `[OrderDigitalProductNode]` | Customer's digital products. |
| `email` | `String` | Customer's email address. |
| `gender` | `String` | Customer's gender. |
| `id` | `ID` | The node unique identifier. |
| `informationGroups` | `[CustomerInformationGroupNode]` | Customer information groups. |
| `mobilePhoneNumber` | `String` | Customer's mobile phone number. |
| `order` | `order` | A specific order placed by the customer. |
| `orders` | `CustomerOrderCollectionSegment` | List of orders placed by the customer. |
| `ordersStatistics` | `CustomerOrdersStatistics` | Statistics about the orders the customer made in a specific timeframe. |
| `partners` | `[Partner]` | Get info about the associated partners. |
| `phoneNumber` | `String` | Customer's phone number. |
| `residentialAddress` | `CustomerAddressNode` | Customer's residential address. |
| `responsibleName` | `String` | Responsible's name. |
| `rg` | `String` | Registration number Id. |
| `stateRegistration` | `String` | State registration number. |
| `subscriptions` | `[CustomerSubscription]` | Customer's subscriptions. |
| `updateDate` | `DateTime!` | Date of the last update. |
| `wishlist` | `wishlist` | Customer wishlist. |

### CustomerAccessToken
| Field | Type | Description |
|-------|------|-------------|
| `accessKey` | `Boolean!` |  |
| `isMaster` | `Boolean!` |  |
| `legacyToken` | `String` |  |
| `token` | `String` |  |
| `type` | `LoginType` | The user login type |
| `validUntil` | `DateTime!` |  |

### CustomerAccessTokenDetails
| Field | Type | Description |
|-------|------|-------------|
| `accessKey` | `Boolean!` | If authenticated with access key |
| `customerId` | `Long!` | The customer id |
| `identifier` | `String` | The identifier linked to the access token |
| `isMaster` | `Boolean!` | Specifies whether the user is a master user |
| `origin` | `LoginOrigin` | The user login origin |
| `type` | `LoginType` | The user login type |
| `validUntil` | `DateTime!` |  |

### CustomerAddressNode
| Field | Type | Description |
|-------|------|-------------|
| `address` | `String` | Address street. |
| `address2` | `String` | Address street 2. |
| `addressDetails` | `String` | Address details. |
| `addressNumber` | `String` | Address number. |
| `cep` | `String` | zip code. |
| `city` | `String` | address city. |
| `country` | `String` | Country. |
| `email` | `String` | The email of the customer address. |
| `id` | `ID` | The node unique identifier. |
| `name` | `String` | The name of the customer address. |
| `neighborhood` | `String` | Address neighborhood. |
| `phone` | `String` | The phone of the customer address. |
| `receiverName` | `String` | The name of the customer address. |
| `referencePoint` | `String` | Address reference point. |
| `state` | `String` | State. |
| `street` | `String` | Address street. |

### CustomerCheckingAccountHistoryNode
| Field | Type | Description |
|-------|------|-------------|
| `date` | `DateTime!` | Customer's checking account history date. |
| `historic` | `String` | Description of the customer's checking account history. |
| `type` | `TypeCheckingAccount!` | Type of customer's checking account history. |
| `value` | `Decimal!` | Value of customer's checking account history. |

### CustomerInformationGroupFieldNode
| Field | Type | Description |
|-------|------|-------------|
| `name` | `String` | The field name. |
| `order` | `Int!` | The field order. |
| `required` | `Boolean!` | If the field is required. |
| `value` | `String` | The field value. |

### CustomerInformationGroupNode
| Field | Type | Description |
|-------|------|-------------|
| `exibitionName` | `String` | The group exibition name. |
| `fields` | `[CustomerInformationGroupFieldNode]` | The group fields. |
| `name` | `String` | The group name. |

### CustomerOrderCollectionSegment
| Field | Type | Description |
|-------|------|-------------|
| `items` | `[order]` |  |
| `page` | `Int!` |  |
| `pageSize` | `Int!` |  |
| `totalCount` | `Int!` |  |

### CustomerOrdersStatistics
| Field | Type | Description |
|-------|------|-------------|
| `productsQuantity` | `Int!` | The number of products the customer made from the number of orders. |
| `quantity` | `Int!` | The number of orders the customer made. |

### CustomerSubscription
| Field | Type | Description |
|-------|------|-------------|
| `billingAddress` | `CustomerAddressNode` | Subscription billing address. |
| `cancellationDate` | `DateTime` | The date when the subscription was cancelled. |
| `coupon` | `String` | The coupon code applied to the subscription. |
| `date` | `DateTime!` | The date of the subscription. |
| `deliveryAddress` | `CustomerAddressNode` | Subscription delivery address. |
| `intercalatedRecurrenceDate` | `DateTime` | The date of intercalated recurring payments. |
| `nextRecurrenceDate` | `DateTime` | The date of the next recurring payment. |
| `orders` | `[order]` | Subscription orders. |
| `pauseDate` | `DateTime` | The date when the subscription was paused. |
| `payment` | `CustomerSubscriptionPayment` | The payment details for the subscription. |
| `products` | `[CustomerSubscriptionProduct]` | The list of products associated with the subscription. |
| `recurring` | `CustomerSubscriptionRecurring` | The details of the recurring subscription. |
| `status` | `String` | The subscription status. |
| `subscriptionGroupId` | `Long!` | The subscription group id. |
| `subscriptionId` | `Long!` | Subscription unique identifier. |

### CustomerSubscriptionPayment
| Field | Type | Description |
|-------|------|-------------|
| `card` | `CustomerSubscriptionPaymentCard` | The details of the payment card associated with the subscription. |
| `type` | `String` | The type of payment for the subscription. |

### CustomerSubscriptionPaymentCard
| Field | Type | Description |
|-------|------|-------------|
| `brand` | `String` | The brand of the payment card (e.g., Visa, MasterCard). |
| `expiration` | `String` | The expiration date of the payment card. |
| `number` | `String` | The masked or truncated number of the payment card. |

### CustomerSubscriptionProduct
| Field | Type | Description |
|-------|------|-------------|
| `productVariantId` | `Long!` | The id of the product variant associated with the subscription. |
| `quantity` | `Int!` | The quantity of the product variant in the subscription. |
| `removed` | `Boolean!` | Indicates whether the product variant is removed from the subscription. |
| `subscriptionProductId` | `Long!` | The id of the subscription product. |
| `value` | `Decimal!` | The monetary value of the product variant in the subscription. |

### CustomerSubscriptionRecurring
| Field | Type | Description |
|-------|------|-------------|
| `days` | `Int!` | The number of days between recurring payments. |
| `description` | `String` | The description of the recurring subscription. |
| `name` | `String` | The name of the recurring subscription. |
| `recurringId` | `Long!` | The recurring subscription id. |
| `removed` | `Boolean!` | Indicates whether the recurring subscription is removed. |

### Customization
Some products can have customizations, such as writing your name on it or other predefined options.

| Field | Type | Description |
|-------|------|-------------|
| `cost` | `Decimal!` | Cost of customization. |
| `customizationId` | `Long!` | Customization unique identifier. |
| `groupName` | `String` | Customization group's name. |
| `id` | `ID` | The node unique identifier. |
| `maxLength` | `Int!` | Maximum allowed size of the field. |
| `name` | `String` | The customization's name. |
| `order` | `Int!` | Priority order of customization. |
| `required` | `Boolean!` | Customization is required. |
| `type` | `String` | Type of customization. |
| `values` | `[String]` | Value of customization. |

### DeadlineAlert
Deadline alert informations.

| Field | Type | Description |
|-------|------|-------------|
| `deadline` | `Int` | Deadline alert time |
| `description` | `String` | Deadline alert description |
| `secondDeadline` | `Int` | Second deadline alert time |
| `secondDescription` | `String` | Second deadline alert description |
| `secondTitle` | `String` | Second deadline alert title |
| `title` | `String` | Deadline alert title |

### DeliveryScheduleDetail
The delivery schedule detail.

| Field | Type | Description |
|-------|------|-------------|
| `date` | `String` | The date of the delivery schedule. |
| `endDateTime` | `DateTime!` | The end date and time of the delivery schedule. |
| `endTime` | `String` | The end time of the delivery schedule. |
| `startDateTime` | `DateTime!` | The start date and time of the delivery schedule. |
| `startTime` | `String` | The start time of the delivery schedule. |

### DistributionCenter
A distribution center.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `ID` | The distribution center unique identifier. |
| `sellerName` | `String` | The distribution center seller name. |

### EventList
Represents a list of events with their details.

| Field | Type | Description |
|-------|------|-------------|
| `coverUrl` | `String` | URL of the event's cover image |
| `date` | `DateTime` | Date of the event |
| `eventType` | `String` | Type of the event |
| `isOwner` | `Boolean!` | Indicates if the token is from the owner of this event list |
| `logoUrl` | `String` | URL of the event's logo |
| `ownerName` | `String` | Name of the event owner |
| `products` | `[Product]` | A list of products associated with the event. |
| `title` | `String` | Event title |
| `url` | `String` | URL of the event |

### EventListStore
Represents a list of store events.

| Field | Type | Description |
|-------|------|-------------|
| `date` | `DateTime` | Date of the event |
| `eventType` | `String` | Event type name of the event |
| `logoUrl` | `String` | URL of the event's logo |
| `name` | `String` | The name of the event. |
| `url` | `String` | The URL of the event. |

### EventListType
Represents a list of events types.

| Field | Type | Description |
|-------|------|-------------|
| `logoUrl` | `String` | The URL of the event's logo. |
| `name` | `String` | The name of the event. |
| `urlPath` | `String` | The URL path of the event. |

### GroupShippingQuote
The shipping quotes for group.

| Field | Type | Description |
|-------|------|-------------|
| `deadline` | `Int!` | The shipping deadline. |
| `deadlineInHours` | `Int` | The shipping deadline, in hours. |
| `name` | `String` | The shipping name. |
| `shippingQuoteId` | `Uuid!` | The shipping quote unique identifier. |
| `type` | `String` | The shipping type. |
| `value` | `Float!` | The shipping value. |

### Hotsite
A hotsite is a group of products used to organize them or to make them easier to browse.

| Field | Type | Description |
|-------|------|-------------|
| `banners` | `[Banner]` | A list of banners associated with the hotsite. |
| `contents` | `[Content]` | A list of contents associated with the hotsite. |
| `endDate` | `DateTime` | The hotsite will be displayed until this date. |
| `expression` | `String` | Expression used to associate products to the hotsite. |
| `hotsiteId` | `Long!` | Hotsite unique identifier. |
| `id` | `ID` | The node unique identifier. |
| `name` | `String` | The hotsite's name. |
| `pageSize` | `Int!` | Set the quantity of products displayed per page. |
| `products` | `ProductsConnection` | A list of products associated with the hotsite. |
| `sorting` | `HotsiteSorting` | Sorting information to be used by default on the hotsite. |
| `startDate` | `DateTime` | The hotsite will be displayed from this date. |
| `subtype` | `HotsiteSubtype` | The subtype of the hotsite. |
| `template` | `String` | The template used for the hotsite. |
| `url` | `String` | The hotsite's URL. |

### HotsiteSorting
| Field | Type | Description |
|-------|------|-------------|
| `direction` | `SortDirection` |  |
| `field` | `ProductSortKeys` |  |

### HotsitesConnection
A connection to a list of items.

| Field | Type | Description |
|-------|------|-------------|
| `edges` | `[HotsitesEdge!]` | A list of edges. |
| `nodes` | `[Hotsite]` | A flattened list of the nodes. |
| `pageInfo` | `PageInfo!` | Information to aid in pagination. |

### HotsitesEdge
An edge in a connection.

| Field | Type | Description |
|-------|------|-------------|
| `cursor` | `String!` | A cursor for use in pagination. |
| `node` | `Hotsite` | The item at the end of the edge. |

### Image
Informations about an image of a product.

| Field | Type | Description |
|-------|------|-------------|
| `fileName` | `String` | The name of the image file. |
| `mini` | `Boolean!` | Check if the image is used for the product main image. |
| `order` | `Int!` | Numeric order the image should be displayed. |
| `print` | `Boolean!` | Check if the image is used for the product prints only. |
| `url` | `String` | The url to retrieve the image |

### Information
Information registred to the product.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `Long!` | The information id. |
| `title` | `String` | The information title. |
| `type` | `String` | The information type. |
| `value` | `String` | The information value. |

### InformationGroupFieldNode
| Field | Type | Description |
|-------|------|-------------|
| `displayType` | `String` | The information group field display type. |
| `fieldName` | `String` | The information group field name. |
| `id` | `ID` | The node unique identifier. |
| `order` | `Int!` | The information group field order. |
| `required` | `Boolean!` | If the information group field is required. |
| `values` | `[InformationGroupFieldValueNode]` | The information group field preset values. |

### InformationGroupFieldValueNode
| Field | Type | Description |
|-------|------|-------------|
| `order` | `Int!` | The information group field value order. |
| `value` | `String` | The information group field value. |

### Installment
| Field | Type | Description |
|-------|------|-------------|
| `discount` | `Boolean!` | Wether the installment has discount. |
| `fees` | `Boolean!` | Wether the installment has fees. |
| `number` | `Int!` | The number of installments. |
| `totalValue` | `Decimal!` | The total value representing the combined amount of all installments. |
| `value` | `Decimal!` | The value of the installment. |

### InstallmentPlan
| Field | Type | Description |
|-------|------|-------------|
| `displayName` | `String` | The custom display name of this installment plan. |
| `installments` | `[Installment]` | List of the installments. |
| `name` | `String` | The name of this installment plan. |

### Menu
Informations about menu items.

| Field | Type | Description |
|-------|------|-------------|
| `cssClass` | `String` | Menu css class to apply. |
| `fullImageUrl` | `String` | The full image URL. |
| `id` | `ID` | The node unique identifier. |
| `imageUrl` | `String` | Menu image url address. |
| `level` | `Int!` | Menu hierarchy level. |
| `link` | `String` | Menu link address. |
| `menuGroupId` | `Int!` | Menu group identifier. |
| `menuId` | `Int!` | Menu identifier. |
| `name` | `String!` | Menu name. |
| `openNewTab` | `Boolean!` | Menu hierarchy level. |
| `order` | `Int!` | Menu position order. |
| `parentMenuId` | `Int` | Parent menu identifier. |
| `text` | `String` | Menu extra text. |

### MenuGroup
Informations about menu groups.

| Field | Type | Description |
|-------|------|-------------|
| `fullImageUrl` | `String` | The full image URL. |
| `id` | `ID` | The node unique identifier. |
| `imageUrl` | `String` | Menu group image url. |
| `menuGroupId` | `Int!` | Menu group identifier. |
| `menus` | `[Menu]` | List of menus associated with the current group |
| `name` | `String` | Menu group name. |
| `partnerId` | `Int` | Menu group partner id. |
| `position` | `String` | Menu group position. |

### Metadata
Some products can have metadata, like diferent types of custom information. A basic key value pair.

| Field | Type | Description |
|-------|------|-------------|
| `key` | `String` | Metadata key. |
| `value` | `String` | Metadata value. |

### MinimumRequirementsCheckoutNode
| Field | Type | Description |
|-------|------|-------------|
| `isMinimumOrderValueReached` | `Boolean!` | Indicates whether the minimum order value has been reached for the checkout. |
| `isMinimumProductQuantityReached` | `Boolean!` | Indicates whether the minimum product quantity has been reached for the checkout. |
| `minimumOrderValue` | `Decimal` | The minimum order value required for the checkout. |
| `minimumProductQuantity` | `Int` | The minimum quantity of products required for the checkout. |
| `minimumProductQuantityMessage` | `String` | The message indicating the minimum product quantity requirement for the checkout. |

### NewsletterNode
| Field | Type | Description |
|-------|------|-------------|
| `createDate` | `DateTime!` | Newsletter creation date. |
| `email` | `String` | The newsletter receiver email. |
| `gender` | `Gender` | Newsletter receiver gender. |
| `name` | `String` | The newsletter receiver name. |
| `updateDate` | `DateTime` | Newsletter update date. |

### OperationResult
Result of the operation.

| Field | Type | Description |
|-------|------|-------------|
| `isSuccess` | `Boolean!` | If the operation is a success. |

### OrderAdjustNode
| Field | Type | Description |
|-------|------|-------------|
| `name` | `String` | The adjust name. |
| `note` | `String` | Note about the adjust. |
| `type` | `Long` | Type of adjust. |
| `value` | `Decimal!` | Amount to be adjusted. |

### OrderAttributeNode
| Field | Type | Description |
|-------|------|-------------|
| `name` | `String` | The attribute name. |
| `value` | `String` | The attribute value. |

### OrderCustomizationNode
| Field | Type | Description |
|-------|------|-------------|
| `cost` | `Float` | The customization cost. |
| `name` | `String` | The customization name. |
| `value` | `String` | The customization value. |

### OrderDeliveryAddressNode
| Field | Type | Description |
|-------|------|-------------|
| `addressNumber` | `String` | The street number of the address. |
| `cep` | `String` | The ZIP code of the address. |
| `city` | `String` | The city of the address. |
| `complement` | `String` | The additional address information. |
| `country` | `String` | The country of the address. |
| `neighboorhood` | `String` | The neighborhood of the address. |
| `receiverName` | `String` | The receiver's name. |
| `referencePoint` | `String` | The reference point for the address. |
| `state` | `String` | The state of the address, abbreviated. |
| `street` | `String` | The street name of the address. |

### OrderDigitalProductNode
| Field | Type | Description |
|-------|------|-------------|
| `content` | `String` | The content of the digital product. |
| `date` | `DateTime!` | The order date. |
| `name` | `String` | The product name. |
| `orderId` | `Long!` | Order unique identifier. |
| `salePrice` | `Decimal!` | The product sale price. |

### OrderInvoiceNode
| Field | Type | Description |
|-------|------|-------------|
| `accessKey` | `String` | The invoice access key. |
| `invoiceCode` | `String` | The invoice identifier code. |
| `serialDigit` | `String` | The invoice serial digit. |
| `url` | `String` | The invoice URL. |

### OrderKitNode
| Field | Type | Description |
|-------|------|-------------|
| `alias` | `String` | The kit alias |
| `imageUrl` | `String` | The kit URL image |
| `kitGroupId` | `String` | The kit unique identifier |
| `kitId` | `Long!` | The kit identifier |
| `listPrice` | `Decimal!` | The kit list price |
| `name` | `String` | The kit name |
| `price` | `Decimal!` | The kit price |
| `products` | `[OrderProductNode]` | The products contained in this kit |
| `quantity` | `Int!` | The kit quantity |
| `totalListPrice` | `Decimal!` | The total list price |

### OrderNoteNode
| Field | Type | Description |
|-------|------|-------------|
| `date` | `DateTime` | Date the note was added to the order. |
| `note` | `String` | The note added to the order. |
| `user` | `String` | The user who added the note to the order. |

### OrderPackagingNode
| Field | Type | Description |
|-------|------|-------------|
| `cost` | `Decimal!` | The packaging cost. |
| `description` | `String` | The packaging description. |
| `message` | `String` | The message added to the packaging. |
| `name` | `String` | The packaging name. |

### OrderPaymentAdditionalInfoNode
| Field | Type | Description |
|-------|------|-------------|
| `key` | `String` | Additional information key. |
| `value` | `String` | Additional information value. |

### OrderPaymentBoletoNode
| Field | Type | Description |
|-------|------|-------------|
| `digitableLine` | `String` | The digitable line. |
| `paymentLink` | `String` | The payment link. |

### OrderPaymentCardNode
| Field | Type | Description |
|-------|------|-------------|
| `brand` | `String` | The brand of the card. |
| `maskedNumber` | `String` | The masked credit card number with only the last 4 digits displayed. |

### OrderPaymentNode
| Field | Type | Description |
|-------|------|-------------|
| `additionalInfo` | `[OrderPaymentAdditionalInfoNode]` | Additional information for the payment. |
| `boleto` | `OrderPaymentBoletoNode` | The boleto information. |
| `card` | `OrderPaymentCardNode` | The card information. |
| `discount` | `Decimal` | Order discounted value. |
| `fees` | `Decimal` | Order additional fees value. |
| `installmentValue` | `Decimal` | Value per installment. |
| `installments` | `Long` | Number of installments. |
| `message` | `String` | Message about payment transaction. |
| `paymentOption` | `String` | The chosen payment option for the order. |
| `pix` | `OrderPaymentPixNode` | The pix information. |
| `status` | `String` | Current payment status. |
| `total` | `Decimal` | Order total value. |

### OrderPaymentPixNode
| Field | Type | Description |
|-------|------|-------------|
| `qrCode` | `String` | The QR code. |
| `qrCodeExpirationDate` | `DateTime` | The expiration date of the QR code. |
| `qrCodeUrl` | `String` | The image URL of the QR code. |

### OrderProductNode
| Field | Type | Description |
|-------|------|-------------|
| `adjusts` | `[OrderAdjustNode]` | List of adjusts on the product price, if any. |
| `attributes` | `[OrderAttributeNode]` | The product attributes. |
| `customizationPrice` | `Decimal!` | The cost of the customizations, if any. |
| `customizations` | `[OrderCustomizationNode]` | List of customizations for the product. |
| `discount` | `Decimal!` | Amount of discount in the product price, if any. |
| `gift` | `Boolean` | If the product is a gift. |
| `image` | `String` | The product image. |
| `kit` | `Boolean!` | The product has a kit |
| `listPrice` | `Decimal!` | The product list price. |
| `name` | `String` | The product name. |
| `packagingPrice` | `Decimal!` | The cost of the packagings, if any. |
| `packagings` | `[OrderPackagingNode]` | List of packagings for the product. |
| `price` | `Decimal!` | The product price. |
| `productSeller` | `OrderSellerNode` | Information about the product seller. |
| `productVariantId` | `Long!` | Variant unique identifier. |
| `quantity` | `Long!` | Quantity of the given product in the order. |
| `salePrice` | `Decimal!` | The product sale price. |
| `sku` | `String` | The product SKU. |
| `trackings` | `[OrderTrackingNode]` | List of trackings for the order. |
| `unitaryValue` | `Decimal!` | Value of an unit of the product. |

### OrderSellerNode
| Field | Type | Description |
|-------|------|-------------|
| `name` | `String` | The seller's name. |

### OrderShippingNode
| Field | Type | Description |
|-------|------|-------------|
| `deadline` | `Int` | Limit date of delivery, in days. |
| `deadlineInHours` | `Int` | Limit date of delivery, in hours. |
| `deadlineText` | `String` | Deadline text message. |
| `distributionCenterId` | `Int` | Distribution center unique identifier. |
| `pickUpId` | `Int` | The order pick up unique identifier. |
| `products` | `[OrderShippingProductNode]` | The products belonging to the order. |
| `promotion` | `Decimal` | Amount discounted from shipping costs, if any. |
| `refConnector` | `String` | Shipping company connector identifier code. |
| `scheduleFrom` | `DateTime` | Start date of shipping schedule. |
| `scheduleUntil` | `DateTime` | Limit date of shipping schedule. |
| `shippingFee` | `Decimal` | Shipping fee value. |
| `shippingName` | `String` | The shipping name. |
| `shippingTableId` | `Int` | Shipping rate table unique identifier. |
| `total` | `Decimal` | The total value. |
| `volume` | `Decimal` | Order package size. |
| `weight` | `Decimal` | The order weight, in grams. |

### OrderShippingProductNode
| Field | Type | Description |
|-------|------|-------------|
| `distributionCenterId` | `Long` | Distribution center unique identifier. |
| `price` | `Decimal` | The product price. |
| `productVariantId` | `Long` | Variant unique identifier. |
| `quantity` | `Int!` | Quantity of the given product. |

### OrderStatusNode
| Field | Type | Description |
|-------|------|-------------|
| `changeDate` | `DateTime` | The date when status has changed. |
| `status` | `String` | Order status. |
| `statusId` | `Long` | Status unique identifier. |

### OrderSubscriptionNode
| Field | Type | Description |
|-------|------|-------------|
| `recurringDays` | `Int` | The length of the order signature period. |
| `recurringName` | `String` | The order subscription period type. |
| `subscriptionGroupId` | `Long` | The order signing group identifier. |
| `subscriptionId` | `Long` | subscription unique identifier. |
| `subscriptionOrderId` | `Long` | The subscription's order identifier. |
| `value` | `Decimal` | The subscription fee for the order. |

### OrderTrackingNode
| Field | Type | Description |
|-------|------|-------------|
| `code` | `String` | The tracking code. |
| `url` | `String` | The URL for tracking. |

### PageInfo
Information about pagination in a connection.

| Field | Type | Description |
|-------|------|-------------|
| `endCursor` | `String` | When paginating forwards, the cursor to continue. |
| `hasNextPage` | `Boolean!` | Indicates whether more edges exist following the set defined by the clients arguments. |
| `hasPreviousPage` | `Boolean!` | Indicates whether more edges exist prior the set defined by the clients arguments. |
| `startCursor` | `String` | When paginating backwards, the cursor to continue. |

### Partner
Partners are used to assign specific products or price tables depending on its scope.

| Field | Type | Description |
|-------|------|-------------|
| `alias` | `String` | The partner alias. |
| `endDate` | `DateTime!` | The partner is valid until this date. |
| `fullUrlLogo` | `String` | The full partner logo URL. |
| `id` | `ID` | The node unique identifier. |
| `logoUrl` | `String` | The partner logo's URL. |
| `name` | `String` | The partner's name. |
| `origin` | `String` | The partner's origin. |
| `partnerAccessToken` | `String` | The partner's access token. |
| `partnerId` | `Long!` | Partner unique identifier. |
| `portfolioId` | `Int!` | Portfolio identifier assigned to this partner. |
| `priceTableId` | `Int!` | Price table identifier assigned to this partner. |
| `startDate` | `DateTime!` | The partner is valid from this date. |
| `type` | `String` | The type of scoped the partner is used. |

### PartnerAccessToken
| Field | Type | Description |
|-------|------|-------------|
| `token` | `String` |  |
| `validUntil` | `DateTime` |  |

### PartnersConnection
A connection to a list of items.

| Field | Type | Description |
|-------|------|-------------|
| `edges` | `[PartnersEdge!]` | A list of edges. |
| `nodes` | `[Partner]` | A flattened list of the nodes. |
| `pageInfo` | `PageInfo!` | Information to aid in pagination. |

### PartnersEdge
An edge in a connection.

| Field | Type | Description |
|-------|------|-------------|
| `cursor` | `String!` | A cursor for use in pagination. |
| `node` | `Partner` | The item at the end of the edge. |

### PhysicalStore
Informations about the physical store.

| Field | Type | Description |
|-------|------|-------------|
| `additionalText` | `String` | Additional text. |
| `address` | `String` | Physical store address. |
| `addressDetails` | `String` | Physical store address details. |
| `addressNumber` | `String` | Physical store address number. |
| `city` | `String` | Physical store address city. |
| `country` | `String` | Physical store country. |
| `ddd` | `Int!` | Physical store DDD. |
| `deliveryDeadline` | `Int!` | Delivery deadline. |
| `email` | `String` | Physical store email. |
| `latitude` | `Float` | Physical store latitude. |
| `longitude` | `Float` | Physical store longitude. |
| `name` | `String` | Physical store name. |
| `neighborhood` | `String` | Physical store address neighborhood. |
| `phoneNumber` | `String` | Physical store phone number. |
| `physicalStoreId` | `Int!` | Physical store ID. |
| `pickup` | `Boolean!` | If the physical store allows pickup. |
| `pickupDeadline` | `Int!` | Pickup deadline. |
| `state` | `String` | Physical store state. |
| `zipCode` | `String` | Physical store zip code. |

### PickupShippingQuote
The pickup shipping quote.

| Field | Type | Description |
|-------|------|-------------|
| `deadline` | `Int!` | The shipping deadline. |
| `deadlineInHours` | `Int` | The shipping deadline, in hours. |
| `distributionCenter` | `DistributionCenter` | The distribution center. |
| `name` | `String` | The shipping name. |
| `shippingQuoteId` | `Uuid!` | The shipping quote unique identifier. |
| `value` | `Float!` | The shipping value. |

### PriceRange
Range of prices for this product.

| Field | Type | Description |
|-------|------|-------------|
| `quantity` | `Int!` | The quantity of products in this range. |
| `range` | `String` | The price range. |

### PriceTable
| Field | Type | Description |
|-------|------|-------------|
| `discountPercentage` | `Decimal!` | The amount of discount in percentage. |
| `id` | `Long!` | The id of this price table. |
| `listPrice` | `Decimal` | The listed regular price of this table. |
| `price` | `Decimal!` | The current working price of this table. |

### Prices
The prices of the product.

| Field | Type | Description |
|-------|------|-------------|
| `bestInstallment` | `BestInstallment` | The best installment option available. |
| `discountPercentage` | `Decimal!` | The amount of discount in percentage. |
| `discounted` | `Boolean!` | Wether the current price is discounted. |
| `installmentPlans` | `[InstallmentPlan]` | List of the possibles installment plans. |
| `listPrice` | `Decimal` | The listed regular price of the product. |
| `multiplicationFactor` | `Float!` | The multiplication factor used for items that are sold by quantity. |
| `price` | `Decimal!` | The current working price. |
| `priceTables` | `[PriceTable]` | List of the product different price tables.    Only returned when using the partnerAccessToken or public price tables. |
| `wholesalePrices` | `[WholesalePrices]` | Lists the different price options when buying the item over the given quantity. |

### Product
A product represents an item for sale in the store.

| Field | Type | Description |
|-------|------|-------------|
| `addToCartFromSpot` | `Boolean` | Check if the product can be added to cart directly from spot. |
| `alias` | `String` | The product url alias. |
| `aliasComplete` | `String` | The complete product url alias. |
| `attributes` | `[ProductAttribute]` | List of the product attributes. |
| `author` | `String` | The product author. |
| `available` | `Boolean` | Field to check if the product is available in stock. |
| `averageRating` | `Int` | The product average rating. From 0 to 5. |
| `averageRatingFloat` | `Float` | The average rating of the product. From 0 to 5 with two decimal places. |
| `buyBox` | `BuyBox` | BuyBox informations. |
| `buyListId` | `Long` | The unique identifier if the node is a Buy List. |
| `buyListProducts` | `[BuyListProduct]` |  |
| `collection` | `String` | The product collection. |
| `condition` | `String` | The product condition. |
| `counterOffer` | `Boolean` | Checks if the product allows counteroffers. |
| `createdAt` | `DateTime` | The product creation date. |
| `deadline` | `Int` | The product delivery deadline. |
| `display` | `Boolean` | Check if the product should be displayed. |
| `displayOnlyPartner` | `Boolean` | Check if the product should be displayed only for partners. |
| `displaySearch` | `Boolean` | Check if the product should be displayed on search. |
| `ean` | `String` | The product's unique EAN. |
| `freeShipping` | `Boolean` | Check if the product offers free shipping. |
| `gender` | `String` | The product gender. |
| `height` | `Float` | The height of the product. |
| `id` | `ID` | The node unique identifier. |
| `images` | `[Image]` | List of the product images. |
| `informations` | `[Information]` | List of the product insformations. |
| `length` | `Float` | The length of the product. |
| `mainVariant` | `Boolean` | Check if its the main variant. |
| `maximumOrderQuantity` | `Int` | The product maximum quantity for an order. |
| `minimumOrderQuantity` | `Int` | The product minimum quantity for an order. |
| `newRelease` | `Boolean` | Check if the product is a new release. |
| `numberOfVotes` | `Int` | The number of votes that the average rating consists of. |
| `parentId` | `Long` | Parent product unique identifier. |
| `prices` | `Prices` | The product prices. |
| `productBrand` | `ProductBrand` | Summarized informations about the brand of the product. |
| `productCategories` | `[ProductCategory]` | Summarized informations about the categories of the product. |
| `productId` | `Long` | Product unique identifier. |
| `productName` | `String` | The product name. |
| `productSubscription` | `ProductSubscription` | Summarized informations about the subscription of the product. |
| `productVariantId` | `Long` | Variant unique identifier. |
| `promotions` | `[Promotion]` | List of promotions this product belongs to. |
| `publisher` | `String` | The product publisher |
| `seller` | `Seller` | The product seller. |
| `similarProducts` | `[SimilarProduct]` | List of similar products.  |
| `sku` | `String` | The product's unique SKU. |
| `spotAttributes` | `[String]` | The values of the spot attribute. |
| `spotInformation` | `String` | The product spot information. |
| `spotlight` | `Boolean` | Check if the product is on spotlight. |
| `stock` | `Long` | The available aggregated product stock (all variants) at the default distribution center. |
| `stocks` | `[Stock]` | List of the product stocks on different distribution centers. |
| `subscriptionGroups` | `[SubscriptionGroup]` | List of subscription groups this product belongs to. |
| `telesales` | `Boolean` | Check if the product is a telesale. |
| `updatedAt` | `DateTime` | The product last update date. |
| `urlVideo` | `String` | The product video url. |
| `variantName` | `String` | The variant name. |
| `variantStock` | `Long` | The available aggregated variant stock at the default distribution center. |
| `weight` | `Float` | The weight of the product. |
| `width` | `Float` | The width of the product. |

### ProductAggregations
| Field | Type | Description |
|-------|------|-------------|
| `filters` | `[SearchFilter]` | List of product filters which can be used to filter subsequent queries. |
| `maximumPrice` | `Decimal!` | Minimum price of the products. |
| `minimumPrice` | `Decimal!` | Maximum price of the products. |
| `priceRanges` | `[PriceRange]` | List of price ranges for the selected products. |

### ProductAttribute
The attributes of the product.

| Field | Type | Description |
|-------|------|-------------|
| `attributeId` | `Long!` | The id of the attribute. |
| `displayType` | `String` | The display type of the attribute. |
| `id` | `ID` | The node unique identifier. |
| `name` | `String` | The name of the attribute. |
| `type` | `String` | The type of the attribute. |
| `value` | `String` | The value of the attribute. |

### ProductBrand
| Field | Type | Description |
|-------|------|-------------|
| `alias` | `String` | The hotsite url alias fot this brand. |
| `fullUrlLogo` | `String` | The full brand logo URL. |
| `id` | `Long!` | The brand id. |
| `logoUrl` | `String` | The url that contains the brand logo image. |
| `name` | `String` | The name of the brand. |

### ProductBuyTogetherNode
| Field | Type | Description |
|-------|------|-------------|
| `addToCartFromSpot` | `Boolean` | Check if the product can be added to cart directly from spot. |
| `alias` | `String` | The product url alias. |
| `aliasComplete` | `String` | The complete product url alias. |
| `attributeSelections` | `AttributeSelection` | Field disabled in the buy together query, to retrieve this information try using the product query |
| `attributes` | `[ProductAttribute]` | List of the product attributes. |
| `author` | `String` | The product author. |
| `available` | `Boolean` | Field to check if the product is available in stock. |
| `averageRating` | `Int` | The product average rating. From 0 to 5. |
| `averageRatingFloat` | `Float` | The average rating of the product. From 0 to 5 with two decimal places. |
| `breadcrumbs` | `[Breadcrumb]` | Field disabled in the buy together query, to retrieve this information try using the product query |
| `buyBox` | `BuyBox` | BuyBox informations. |
| `buyListId` | `Long` | The unique identifier if the node is a Buy List. |
| `buyListProducts` | `[BuyListProduct]` |  |
| `buyTogether` | `[ProductBuyTogetherNode]` | Field disabled in the buy together query, to retrieve this information try using the product query |
| `buyTogetherGroups` | `[BuyTogetherGroup]` | Field disabled in the buy together query, to retrieve this information try using the product query |
| `collection` | `String` | The product collection. |
| `condition` | `String` | The product condition. |
| `counterOffer` | `Boolean` | Checks if the product allows counteroffers. |
| `createdAt` | `DateTime` | The product creation date. |
| `customizations` | `[Customization]` | Field disabled in the buy together query, to retrieve this information try using the product query |
| `deadline` | `Int` | The product delivery deadline. |
| `deadlineAlert` | `DeadlineAlert` | Field disabled in the buy together query, to retrieve this information try using the product query |
| `display` | `Boolean` | Check if the product should be displayed. |
| `displayOnlyPartner` | `Boolean` | Check if the product should be displayed only for partners. |
| `displaySearch` | `Boolean` | Check if the product should be displayed on search. |
| `ean` | `String` | The product's unique EAN. |
| `freeShipping` | `Boolean` | Check if the product offers free shipping. |
| `gender` | `String` | The product gender. |
| `height` | `Float` | The height of the product. |
| `id` | `ID` | The node unique identifier. |
| `images` | `[Image]` | List of the product images. |
| `informations` | `[Information]` | List of the product insformations. |
| `length` | `Float` | The length of the product. |
| `mainVariant` | `Boolean` | Check if its the main variant. |
| `maximumOrderQuantity` | `Int` | The product maximum quantity for an order. |
| `minimumOrderQuantity` | `Int` | The product minimum quantity for an order. |
| `newRelease` | `Boolean` | Check if the product is a new release. |
| `numberOfVotes` | `Int` | The number of votes that the average rating consists of. |
| `parallelOptions` | `[String]` | Field disabled in the buy together query, to retrieve this information try using the product query |
| `parentId` | `Long` | Parent product unique identifier. |
| `prices` | `Prices` | The product prices. |
| `productBrand` | `ProductBrand` | Summarized informations about the brand of the product. |
| `productCategories` | `[ProductCategory]` | Summarized informations about the categories of the product. |
| `productId` | `Long` | Product unique identifier. |
| `productName` | `String` | The product name. |
| `productSubscription` | `ProductSubscription` | Summarized informations about the subscription of the product. |
| `productVariantId` | `Long` | Variant unique identifier. |
| `promotions` | `[Promotion]` | List of promotions this product belongs to. |
| `publisher` | `String` | The product publisher |
| `reviews` | `[Review]` | Field disabled in the buy together query, to retrieve this information try using the product query |
| `seller` | `Seller` | The product seller. |
| `seo` | `[SEO]` | Field disabled in the buy together query, to retrieve this information try using the product query |
| `similarProducts` | `[SimilarProduct]` | List of similar products.  |
| `sku` | `String` | The product's unique SKU. |
| `spotAttributes` | `[String]` | The values of the spot attribute. |
| `spotInformation` | `String` | The product spot information. |
| `spotlight` | `Boolean` | Check if the product is on spotlight. |
| `stock` | `Long` | The available aggregated product stock (all variants) at the default distribution center. |
| `stocks` | `[Stock]` | List of the product stocks on different distribution centers. |
| `subscriptionGroups` | `[SubscriptionGroup]` | List of subscription groups this product belongs to. |
| `telesales` | `Boolean` | Check if the product is a telesale. |
| `updatedAt` | `DateTime` | The product last update date. |
| `urlVideo` | `String` | The product video url. |
| `variantName` | `String` | The variant name. |
| `variantStock` | `Long` | The available aggregated variant stock at the default distribution center. |
| `weight` | `Float` | The weight of the product. |
| `width` | `Float` | The width of the product. |

### ProductCategory
Information about the category of a product.

| Field | Type | Description |
|-------|------|-------------|
| `active` | `Boolean!` | Wether the category is currently active. |
| `googleCategories` | `String` | The categories in google format. |
| `hierarchy` | `String` | The category hierarchy. |
| `id` | `Int!` | The id of the category. |
| `main` | `Boolean!` | Wether this category is the main category for this product. |
| `name` | `String` | The category name. |
| `url` | `String` | The category hotsite url alias. |

### ProductCollectionSegment
| Field | Type | Description |
|-------|------|-------------|
| `items` | `[Product]` |  |
| `page` | `Int!` |  |
| `pageSize` | `Int!` |  |
| `totalCount` | `Int!` |  |

### ProductOption
Options available for the given product.

| Field | Type | Description |
|-------|------|-------------|
| `attributes` | `[Attribute]` | A list of attributes available for the given product and its variants. |
| `customizations` | `[Customization]` | A list of customizations available for the given products. |
| `id` | `ID` | The node unique identifier. |

### ProductPriceAlert
A product price alert.

| Field | Type | Description |
|-------|------|-------------|
| `email` | `String` | The alerted's email. |
| `name` | `String` | The alerted's name. |
| `priceAlertId` | `Long!` | The price alert ID. |
| `productVariantId` | `Long!` | The product variant ID. |
| `requestDate` | `DateTime!` | The request date. |
| `targetPrice` | `Decimal!` | The target price. |

### ProductSubscription
| Field | Type | Description |
|-------|------|-------------|
| `discount` | `Decimal!` | The amount of discount if this product is sold as a subscription. |
| `price` | `Decimal` | The price of the product when sold as a subscription. |
| `subscriptionOnly` | `Boolean!` | Wether this product is sold only as a subscrition. |

### ProductVariant
Product variants that have the attribute.

| Field | Type | Description |
|-------|------|-------------|
| `aggregatedStock` | `Long` | The available stock at the default distribution center. |
| `alias` | `String` | The product alias. |
| `attributes` | `[ProductAttribute]` | List of the selected variant attributes. |
| `available` | `Boolean` | Field to check if the product is available in stock. |
| `ean` | `String` | The product's EAN. |
| `id` | `ID` | The node unique identifier. |
| `images` | `[Image]` | The product's images. |
| `offers` | `[SellerOffer]` | The seller's product offers. |
| `prices` | `Prices` | The product prices. |
| `productId` | `Long` | Product unique identifier. |
| `productVariantId` | `Long` | Variant unique identifier. |
| `productVariantName` | `String` | Product variant name. |
| `promotions` | `[Promotion]` | List of promotions this product variant belongs to. |
| `sku` | `String` | The product's unique SKU. |
| `stock` | `Long` | The available stock at the default distribution center. |
| `stocks` | `[Stock]` | Stocks at each distribution center. |

### ProductsConnection
A connection to a list of items.

| Field | Type | Description |
|-------|------|-------------|
| `edges` | `[ProductsEdge!]` | A list of edges. |
| `nodes` | `[Product]` | A flattened list of the nodes. |
| `pageInfo` | `PageInfo!` | Information to aid in pagination. |
| `totalCount` | `Int!` |  |

### ProductsEdge
An edge in a connection.

| Field | Type | Description |
|-------|------|-------------|
| `cursor` | `String!` | A cursor for use in pagination. |
| `node` | `Product` | The item at the end of the edge. |

### Promotion
Information about promotions of a product.

| Field | Type | Description |
|-------|------|-------------|
| `content` | `String` | The promotion html content. |
| `disclosureType` | `String` | Where the promotion is shown (spot, product page, etc..). |
| `endDate` | `DateTime!` | The end date for the promotion. |
| `fullStampUrl` | `String` | The stamp URL of the promotion. |
| `id` | `Long!` | The promotion id. |
| `stamp` | `String` | The stamp of the promotion. |
| `title` | `String` | The promotion title. |

### Question
| Field | Type | Description |
|-------|------|-------------|
| `answers` | `[Answer]` |  |
| `question` | `String` |  |
| `questionId` | `String` |  |

### ResellerNode
| Field | Type | Description |
|-------|------|-------------|
| `cnpj` | `String` | Taxpayer identification number for businesses |
| `corporateName` | `String` | The registered name of the company |
| `name` | `String` | The seller's name |
| `sellerId` | `Long!` | Seller unique identifier |

### RestockAlertNode
| Field | Type | Description |
|-------|------|-------------|
| `email` | `String` | Email to be notified. |
| `name` | `String` | Name of the person to be notified. |
| `productVariantId` | `Long!` | The product variant id. |
| `requestDate` | `DateTime!` | Date the alert was requested. |

### Review
A product review written by a customer.

| Field | Type | Description |
|-------|------|-------------|
| `customer` | `String` | The reviewer name. |
| `email` | `String` | The reviewer e-mail. |
| `rating` | `Int!` | The review rating. |
| `review` | `String` | The review content. |
| `reviewDate` | `DateTime!` | The review date. |

### SEO
Entity SEO information.

| Field | Type | Description |
|-------|------|-------------|
| `content` | `String` | Content of SEO. |
| `httpEquiv` | `String` | Equivalent SEO type for HTTP. |
| `name` | `String` | Name of SEO. |
| `scheme` | `String` | Scheme for SEO. |
| `type` | `String` | Type of SEO. |

### Script
Returns the scripts registered in the script manager.

| Field | Type | Description |
|-------|------|-------------|
| `content` | `String` | The script content. |
| `id` | `Long!` | The script id. |
| `name` | `String` | The script name. |
| `pageType` | `ScriptPageType!` | The script page type. |
| `position` | `ScriptPosition!` | The script position. |
| `priority` | `Int!` | The script priority. |

### Search
Search for relevant products to the searched term.

| Field | Type | Description |
|-------|------|-------------|
| `aggregations` | `ProductAggregations` | Aggregations from the products. |
| `banners` | `[Banner]` | A list of banners displayed in search pages. |
| `breadcrumbs` | `[Breadcrumb]` | List of search breadcrumbs. |
| `contents` | `[Content]` | A list of contents displayed in search pages. |
| `forbiddenTerm` | `forbiddenTerm` | Information about forbidden term. |
| `pageSize` | `Int!` | The quantity of products displayed per page. |
| `products` | `ProductsConnection` | A cursor based paginated list of products from the search. |
| `productsByOffset` | `ProductCollectionSegment` | An offset based paginated list of products from the search. |
| `redirectUrl` | `String` | Redirection url in case a term in the search triggers a redirect. |
| `searchTime` | `String` | Time taken to perform the search. |

### SearchFilter
Aggregated filters of a list of products.

| Field | Type | Description |
|-------|------|-------------|
| `field` | `String` | The name of the field. |
| `origin` | `String` | The origin of the field. |
| `values` | `[SearchFilterItem]` | List of the values of the field. |

### SearchFilterItem
Details of a filter value.

| Field | Type | Description |
|-------|------|-------------|
| `name` | `String` | The name of the value. |
| `quantity` | `Int!` | The quantity of product with this value. |

### SearchRecord
The response data

| Field | Type | Description |
|-------|------|-------------|
| `date` | `DateTime!` | The date time of the processed request |
| `isSuccess` | `Boolean!` | If the record was successful |
| `query` | `String` | The searched query |

### SelectedPaymentMethod
The selected payment method details.

| Field | Type | Description |
|-------|------|-------------|
| `html` | `String` | The payment html. |
| `id` | `Uuid!` | The unique identifier for the selected payment method. |
| `installments` | `[SelectedPaymentMethodInstallment]` | The list of installments associated with the selected payment method. |
| `paymentMethodId` | `ID` | The payment Method Id. |
| `scripts` | `[String]` | Payment related scripts. |
| `selectedInstallment` | `SelectedPaymentMethodInstallment` | The selected installment. |
| `suggestedCards` | `[SuggestedCard]` | The suggested cards. To return this field, the authenticated user's customerAccessToken must be provided. |

### SelectedPaymentMethodInstallment
Details of an installment of the selected payment method.

| Field | Type | Description |
|-------|------|-------------|
| `adjustment` | `Float!` | The adjustment value applied to the installment. |
| `number` | `Int!` | The installment number. |
| `total` | `Float!` | The total value of the installment. |
| `value` | `Float!` | The individual value of each installment. |

### Seller
Seller informations.

| Field | Type | Description |
|-------|------|-------------|
| `name` | `String` | Seller name |

### SellerInstallment
| Field | Type | Description |
|-------|------|-------------|
| `discount` | `Boolean!` | Wether the installment has discount. |
| `fees` | `Boolean!` | Wether the installment has fees. |
| `number` | `Int!` | The number of installments. |
| `value` | `Decimal!` | The value of the installment. |

### SellerInstallmentPlan
| Field | Type | Description |
|-------|------|-------------|
| `displayName` | `String` | The custom display name of this installment plan. |
| `installments` | `[SellerInstallment]` | List of the installments. |

### SellerOffer
The seller's product offer

| Field | Type | Description |
|-------|------|-------------|
| `name` | `String` |  |
| `prices` | `SellerPrices` | The product prices. |
| `productVariantId` | `Long` | Variant unique identifier. |
| `stock` | `Int!` | The stock of the product variant. |

### SellerPrices
The prices of the product.

| Field | Type | Description |
|-------|------|-------------|
| `installmentPlans` | `[SellerInstallmentPlan]` | List of the possibles installment plans. |
| `listPrice` | `Decimal` | The listed regular price of the product. |
| `price` | `Decimal` | The current working price. |

### SellersConnection
A connection to a list of items.

| Field | Type | Description |
|-------|------|-------------|
| `edges` | `[SellersEdge!]` | A list of edges. |
| `nodes` | `[ResellerNode]` | A flattened list of the nodes. |
| `pageInfo` | `PageInfo!` | Information to aid in pagination. |
| `totalCount` | `Int!` |  |

### SellersEdge
An edge in a connection.

| Field | Type | Description |
|-------|------|-------------|
| `cursor` | `String!` | A cursor for use in pagination. |
| `node` | `ResellerNode` | The item at the end of the edge. |

### ShippingNode
| Field | Type | Description |
|-------|------|-------------|
| `deadline` | `Int!` | The shipping deadline. |
| `deadlineInHours` | `Int` | The shipping deadline in hours. |
| `deliverySchedule` | `DeliveryScheduleDetail` | The delivery schedule detail. |
| `name` | `String` | The shipping name. |
| `shippingQuoteId` | `Uuid!` | The shipping quote unique identifier. |
| `type` | `String` | The shipping type. |
| `value` | `Float!` | The shipping value. |

### ShippingProduct
The product informations related to the shipping.

| Field | Type | Description |
|-------|------|-------------|
| `distributionCenterId` | `Int` | The ID of distribution center. |
| `productVariantId` | `Int!` | The product unique identifier. |
| `value` | `Float!` | The shipping value related to the product. |

### ShippingQuote
A shipping quote.

| Field | Type | Description |
|-------|------|-------------|
| `deadline` | `Int!` | The shipping deadline. |
| `deadlineInHours` | `Int` | The shipping deadline in hours. |
| `deliverySchedules` | `[deliverySchedule]` | The available time slots for scheduling the delivery of the shipping quote. |
| `distributionCenterId` | `Int` | The ID of distribution center. |
| `id` | `ID` | The node unique identifier. |
| `name` | `String` | The shipping name. |
| `products` | `[ShippingProduct]` | The products related to the shipping. |
| `shippingQuoteId` | `Uuid!` | The shipping quote unique identifier. |
| `type` | `String` | The shipping type. |
| `value` | `Float!` | The shipping value. |

### ShippingQuoteGroup
A shipping quote group.

| Field | Type | Description |
|-------|------|-------------|
| `distributionCenter` | `DistributionCenter` | The distribution center. |
| `pickups` | `[PickupShippingQuote]` | List of available pickup shipping quotes. |
| `products` | `[ShippingQuoteGroupProduct]` | The products related to the shipping quote group. |
| `shippingQuotes` | `[GroupShippingQuote]` | Shipping quotes to group. |

### ShippingQuoteGroupProduct
The product informations related to the shipping.

| Field | Type | Description |
|-------|------|-------------|
| `productVariantId` | `Int!` | The product unique identifier. |

### Shop
Informations about the store.

| Field | Type | Description |
|-------|------|-------------|
| `checkoutUrl` | `String` | Checkout URL |
| `cookieDomain` | `String` | Specifies the domain for which cookies will be set |
| `googleRecaptchaSiteKey` | `String` | The Google Recaptcha Site Key for reCAPTCHA validation |
| `mainUrl` | `String` | Store main URL |
| `mobileCheckoutUrl` | `String` | Mobile checkout URL |
| `mobileUrl` | `String` | Mobile URL |
| `modifiedName` | `String` | Store modified name |
| `name` | `String` | Store name |
| `physicalStores` | `[PhysicalStore]` | Physical stores |
| `sitemapImagesUrl` | `String` | The URL to obtain the SitemapImagens.xml file |
| `sitemapUrl` | `String` | The URL to obtain the Sitemap.xml file |

### ShopSetting
Store setting.

| Field | Type | Description |
|-------|------|-------------|
| `name` | `String` | Setting name |
| `value` | `String` | Setting value |

### SimilarProduct
Information about a similar product.

| Field | Type | Description |
|-------|------|-------------|
| `alias` | `String` | The url alias of this similar product. |
| `image` | `String` | The file name of the similar product image. |
| `imageUrl` | `String` | The URL of the similar product image. |
| `name` | `String` | The name of the similar product. |

### SimpleLogin
| Field | Type | Description |
|-------|------|-------------|
| `customerAccessToken` | `CustomerAccessToken` | The customer access token |
| `question` | `Question` | The simple login question to answer |
| `type` | `SimpleLoginType!` | The simple login type |

### SingleHotsite
A hotsite is a group of products used to organize them or to make them easier to browse.

| Field | Type | Description |
|-------|------|-------------|
| `aggregations` | `ProductAggregations` | Aggregations from the products. |
| `banners` | `[Banner]` | A list of banners associated with the hotsite. |
| `breadcrumbs` | `[Breadcrumb]` | A list of breadcrumbs for the hotsite. |
| `contents` | `[Content]` | A list of contents associated with the hotsite. |
| `endDate` | `DateTime` | The hotsite will be displayed until this date. |
| `expression` | `String` | Expression used to associate products to the hotsite. |
| `hotsiteId` | `Long!` | Hotsite unique identifier. |
| `id` | `ID` | The node unique identifier. |
| `name` | `String` | The hotsite's name. |
| `pageSize` | `Int!` | Set the quantity of products displayed per page. |
| `products` | `ProductsConnection` | A list of products associated with the hotsite. Cursor pagination. |
| `productsByOffset` | `ProductCollectionSegment` | A list of products associated with the hotsite. Offset pagination. |
| `seo` | `[SEO]` | A list of SEO contents associated with the hotsite. |
| `sorting` | `HotsiteSorting` | Sorting information to be used by default on the hotsite. |
| `startDate` | `DateTime` | The hotsite will be displayed from this date. |
| `subtype` | `HotsiteSubtype` | The subtype of the hotsite. |
| `template` | `String` | The template used for the hotsite. |
| `url` | `String` | The hotsite's URL. |

### SingleProduct
A product represents an item for sale in the store.

| Field | Type | Description |
|-------|------|-------------|
| `addToCartFromSpot` | `Boolean` | Check if the product can be added to cart directly from spot. |
| `alias` | `String` | The product url alias. |
| `aliasComplete` | `String` | The complete product url alias. |
| `attributeSelections` | `AttributeSelection` | Information about the possible selection attributes. |
| `attributes` | `[ProductAttribute]` | List of the product attributes. |
| `author` | `String` | The product author. |
| `available` | `Boolean` | Field to check if the product is available in stock. |
| `averageRating` | `Int` | The product average rating. From 0 to 5. |
| `averageRatingFloat` | `Float` | The average rating of the product. From 0 to 5 with two decimal places. |
| `breadcrumbs` | `[Breadcrumb]` | List of product breadcrumbs. |
| `buyBox` | `BuyBox` | BuyBox informations. |
| `buyListId` | `Long` | The unique identifier if the node is a Buy List. |
| `buyListProducts` | `[BuyListProduct]` |  |
| `buyTogether` | `[ProductBuyTogetherNode]` | Buy together products. |
| `buyTogetherGroups` | `[BuyTogetherGroup]` | Buy together groups products. |
| `collection` | `String` | The product collection. |
| `condition` | `String` | The product condition. |
| `counterOffer` | `Boolean` | Checks if the product allows counteroffers. |
| `createdAt` | `DateTime` | The product creation date. |
| `customizations` | `[Customization]` | A list of customizations available for the given products. |
| `deadline` | `Int` | The product delivery deadline. |
| `deadlineAlert` | `DeadlineAlert` | Product deadline alert informations. |
| `display` | `Boolean` | Check if the product should be displayed. |
| `displayOnlyPartner` | `Boolean` | Check if the product should be displayed only for partners. |
| `displaySearch` | `Boolean` | Check if the product should be displayed on search. |
| `ean` | `String` | The product's unique EAN. |
| `freeShipping` | `Boolean` | Check if the product offers free shipping. |
| `gender` | `String` | The product gender. |
| `height` | `Float` | The height of the product. |
| `id` | `ID` | The node unique identifier. |
| `images` | `[Image]` | List of the product images. |
| `informations` | `[Information]` | List of the product insformations. |
| `length` | `Float` | The length of the product. |
| `mainVariant` | `Boolean` | Check if its the main variant. |
| `maximumOrderQuantity` | `Int` | The product maximum quantity for an order. |
| `minimumOrderQuantity` | `Int` | The product minimum quantity for an order. |
| `newRelease` | `Boolean` | Check if the product is a new release. |
| `numberOfVotes` | `Int` | The number of votes that the average rating consists of. |
| `parallelOptions` | `[String]` | Product parallel options information. |
| `parentId` | `Long` | Parent product unique identifier. |
| `prices` | `Prices` | The product prices. |
| `productBrand` | `ProductBrand` | Summarized informations about the brand of the product. |
| `productCategories` | `[ProductCategory]` | Summarized informations about the categories of the product. |
| `productId` | `Long` | Product unique identifier. |
| `productName` | `String` | The product name. |
| `productSubscription` | `ProductSubscription` | Summarized informations about the subscription of the product. |
| `productVariantId` | `Long` | Variant unique identifier. |
| `promotions` | `[Promotion]` | List of promotions this product belongs to. |
| `publisher` | `String` | The product publisher |
| `reviews` | `[Review]` | List of customer reviews for this product. |
| `seller` | `Seller` | The product seller. |
| `seo` | `[SEO]` | Product SEO informations. |
| `similarProducts` | `[SimilarProduct]` | List of similar products.  |
| `sku` | `String` | The product's unique SKU. |
| `spotAttributes` | `[String]` | The values of the spot attribute. |
| `spotInformation` | `String` | The product spot information. |
| `spotlight` | `Boolean` | Check if the product is on spotlight. |
| `stock` | `Long` | The available aggregated product stock (all variants) at the default distribution center. |
| `stocks` | `[Stock]` | List of the product stocks on different distribution centers. |
| `subscriptionGroups` | `[SubscriptionGroup]` | List of subscription groups this product belongs to. |
| `telesales` | `Boolean` | Check if the product is a telesale. |
| `updatedAt` | `DateTime` | The product last update date. |
| `urlVideo` | `String` | The product video url. |
| `variantName` | `String` | The variant name. |
| `variantStock` | `Long` | The available aggregated variant stock at the default distribution center. |
| `weight` | `Float` | The weight of the product. |
| `width` | `Float` | The width of the product. |

### Stock
Information about a product stock in a particular distribution center.

| Field | Type | Description |
|-------|------|-------------|
| `aggregated` | `Long!` | The available stock at this distribution center. |
| `id` | `Long!` | The id of the distribution center. |
| `items` | `Long!` | The number of physical items in stock at this DC. |
| `name` | `String` | The name of the distribution center. |
| `reserved` | `Long!` | The number of items reserved at this distribution center. |

### SubscriptionGroup
| Field | Type | Description |
|-------|------|-------------|
| `recurringTypes` | `[SubscriptionRecurringType]` | The recurring types for this subscription group. |
| `status` | `String` | The status name of the group. |
| `statusId` | `Int!` | The status id of the group. |
| `subscriptionGroupId` | `Long!` | The subscription group id. |
| `subscriptionOnly` | `Boolean!` | Wether the product is only avaible for subscription. |

### SubscriptionRecurringType
| Field | Type | Description |
|-------|------|-------------|
| `days` | `Int!` | The number of days of the recurring type. |
| `name` | `String` | The recurring type display name. |
| `recurringTypeId` | `Long!` | The recurring type id. |

### SuggestedCard
| Field | Type | Description |
|-------|------|-------------|
| `brand` | `String` | Credit card brand. |
| `key` | `String` | Credit card key. |
| `name` | `String` | Customer name on credit card. |
| `number` | `String` | Credit card number. |

### Uri
Node of URI Kind.

| Field | Type | Description |
|-------|------|-------------|
| `hotsiteSubtype` | `HotsiteSubtype` | The origin of the hotsite. |
| `kind` | `UriKind!` | Path kind. |
| `partnerSubtype` | `PartnerSubtype` | The partner subtype. |
| `productAlias` | `String` | Product alias. |
| `productCategoriesIds` | `[Int!]` | Product categories IDs. |
| `redirectCode` | `String` | Redirect status code. |
| `redirectUrl` | `String` | Url to redirect. |

### WholesalePrices
| Field | Type | Description |
|-------|------|-------------|
| `price` | `Decimal!` | The wholesale price. |
| `quantity` | `Int!` | The minimum quantity required for the wholesale price to be applied |

### deliverySchedule
A representation of available time slots for scheduling a delivery.

| Field | Type | Description |
|-------|------|-------------|
| `date` | `DateTime!` | The date of the delivery schedule. |
| `periods` | `[period]` | The list of time periods available for scheduling a delivery. |

### forbiddenTerm
Informations about a forbidden search term.

| Field | Type | Description |
|-------|------|-------------|
| `suggested` | `String` | The suggested search term instead. |
| `text` | `String` | The text to display about the term. |

### order
| Field | Type | Description |
|-------|------|-------------|
| `checkingAccount` | `Decimal!` | Checking account value used for the order. |
| `checkoutId` | `Uuid!` | The checkout unique identifier. |
| `coupon` | `String` | The coupon for discounts. |
| `date` | `DateTime!` | The date when te order was placed. |
| `deliveryAddress` | `OrderDeliveryAddressNode` | The address where the order will be delivered. |
| `discount` | `Decimal!` | Order discount amount, if any. |
| `interestFee` | `Decimal!` | Order interest fee, if any. |
| `invoices` | `[OrderInvoiceNode]` | Information about order invoices. |
| `kits` | `[OrderKitNode]` | A list of kits belonging to the order. |
| `notes` | `[OrderNoteNode]` | Information about order notes. |
| `orderId` | `Long!` | Order unique identifier. |
| `paymentDate` | `DateTime` | The date when the order was payed. |
| `payments` | `[OrderPaymentNode]` | Information about payments. |
| `products` | `[OrderProductNode]` | Products belonging to the order. |
| `promotions` | `[Int!]` | List of promotions applied to the order. |
| `shippingFee` | `Decimal!` | The shipping fee. |
| `shippings` | `[OrderShippingNode]` | Information about order shippings. |
| `status` | `OrderStatusNode` | The order current status. |
| `statusHistory` | `[OrderStatusNode]` | List of the order status history. |
| `subscriptions` | `[OrderSubscriptionNode]` | List of order subscriptions. |
| `subtotal` | `Decimal!` | Order subtotal value. |
| `total` | `Decimal!` | Order total value. |
| `trackings` | `[OrderTrackingNode]` | Information about order trackings. |

### paymentMethod
| Field | Type | Description |
|-------|------|-------------|
| `id` | `ID` | The node unique identifier. |
| `imageUrl` | `String` | The url link that displays for the payment. |
| `name` | `String` | The name of the payment method. |
| `type` | `String` | The type of payment method. |

### period
Represents a time period available for scheduling a delivery.

| Field | Type | Description |
|-------|------|-------------|
| `end` | `String` | The end time of the time period. |
| `id` | `Long!` | The unique identifier of the time period. |
| `start` | `String` | The start time of the time period. |

### wishlist
| Field | Type | Description |
|-------|------|-------------|
| `products` | `[Product]` | Wishlist products. |


## Enums

### ApplyPolicy
Values:
- `BEFORE_RESOLVER`
- `AFTER_RESOLVER`

### BannerSortKeys
Define the banner attribute which the result set will be sorted on.

Values:
- `ID` - The banner's unique identifier.
- `CREATION_DATE` - The banner's creation date.

### BrandSortKeys
Define the brand attribute which the result set will be sorted on.

Values:
- `ID` - The brand unique identifier.
- `NAME` - The brand name.
- `GROUP_ORDER` - The order on the group. Only available when using group id or group name filter.

### BuyTogetherType
Values:
- `PRODUCT`
- `CAROUSEL`

### CategorySortKeys
Define the category attribute which the result set will be sorted on.

Values:
- `ID` - The category unique identifier.
- `NAME` - The category name.

### CheckoutResetType
The checkout areas available to reset

Values:
- `PAYMENT`

### ContentSortKeys
Define the content attribute which the result set will be sorted on.

Values:
- `ID` - The content's unique identifier.
- `CreationDate` - The content's creation date.

### CustomerOrderSortKeys
Define the order attribute which the result set will be sorted on.

Values:
- `ID` - The order ID.
- `DATE` - The date the order was placed.
- `STATUS` - The order current status.
- `AMOUNT` - The total order value.

### EntityType
Define the entity type of the customer registration.

Values:
- `PERSON` - An individual person, a physical person.
- `COMPANY` - Legal entity, a company, business, organization.
- `INTERNATIONAL` - An international person, a legal international entity.

### EnumInformationGroup
Values:
- `PESSOA_FISICA`
- `PESSOA_JURIDICA`
- `NEWSLETTER`

### FilterPosition
Values:
- `VERTICAL` - Vertical filter position.
- `HORIZONTAL` - Horizontal filter position.
- `BOTH` - Both filter position.

### Gender
The customer's gender.

Values:
- `OTHER`
- `MALE`
- `FEMALE`

### HotsiteSortKeys
Define the hotsite attribute which the result set will be sorted on.

Values:
- `ID` - The hotsite id.
- `NAME` - The hotsite name.
- `URL` - The hotsite url.

### HotsiteSubtype
Values:
- `CATEGORY` - Hotsite created from a category.
- `BRAND` - Hotsite created from a brand.
- `PORTFOLIO` - Hotsite created from a portfolio.
- `BUY_LIST` - Hotsite created from a buy list (lista de compra).

### LoginOrigin
The user login origin.

Values:
- `SOCIAL`
- `SIMPLE`

### LoginType
The user login type.

Values:
- `NEW`
- `SIMPLE`
- `AUTHENTICATED`

### Operation
Types of operations to perform between query terms.

Values:
- `AND` - Performs AND operation between query terms.
- `OR` - Performs OR operation between query terms.

### OrderSortDirection
Define the sort orientation of the result set.

Values:
- `DESC` - The results will be sorted in an descending order.
- `ASC` - The results will be sorted in an ascending order.

### OrderStatus
Represents the status of an order.

Values:
- `PAID` - Order has been paid.
- `AWAITING_PAYMENT` - Order is awaiting payment.
- `CANCELLED_TEMPORARILY_DENIED_CARD` - Order has been cancelled - Card Temporarily Denied.
- `CANCELLED_DENIED_CARD` - Order has been cancelled - Card Denied.
- `CANCELLED_FRAUD` - Order has been cancelled - Fraud.
- `CANCELLED_SUSPECT_FRAUD` - Order has been cancelled - Suspected Fraud.
- `CANCELLED_ORDER_CANCELLED` - Order has been cancelled.
- `CANCELLED` - Order has been cancelled.
- `SENT` - Order has been sent.
- `AUTHORIZED` - Order has been authorized.
- `SENT_INVOICED` - Order has been sent - Invoiced.
- `RETURNED` - Order has been returned.
- `DOCUMENTS_FOR_PURCHASE` - Documents needed for purchase.
- `APPROVED_ANALYSIS` - Order has been approved in analysis.
- `RECEIVED_GIFT_CARD` - Order has been received - Gift Card.
- `SEPARATED` - Order has been separated.
- `ORDERED` - Order has been placed.
- `DELIVERED` - Order has been delivered.
- `AWAITING_PAYMENT_CHANGE` - Order is awaiting change of payment method.
- `CHECKED_ORDER` - Order has been checked.
- `PICK_UP_IN_STORE` - Available for pick-up in store.
- `DENIED_PAYMENT` - Payment denied, but the order has not been cancelled.
- `CREDITED` - Order has been credited.

### PartnerSortKeys
Define the partner attribute which the result set will be sorted on.

Values:
- `ID` - The partner unique identifier.
- `NAME` - The partner name.

### PartnerSubtype
Values:
- `OPEN` - Partner 'open' subtype.
- `CLOSED` - Partner 'closed' subtype.
- `CLIENT` - Partner 'client' subtype.

### ProductRecommendationAlgorithm
Values:
- `DEFAULT`

### ProductSearchSortKeys
Define the product attribute which the result set will be sorted on.

Values:
- `RELEVANCE` - The relevance that the search engine gave to the possible result item based on own criteria.
- `NAME` - The product name.
- `SALES` - The sales number on a period of time.
- `PRICE` - The product variant price.
- `DISCOUNT` - The applied discount to the product variant price.
- `RANDOM` - Sort in a random way.
- `RELEASE_DATE` - The date the product was released.
- `STOCK` - The quantity in stock of the product variant.

### ProductSortKeys
Define the product attribute which the result set will be sorted on.

Values:
- `NAME` - The product name.
- `SALES` - The sales number on a period of time.
- `PRICE` - The product variant price.
- `DISCOUNT` - The applied discount to the product variant price.
- `RANDOM` - Sort in a random way.
- `RELEASE_DATE` - The date the product was released.
- `STOCK` - The quantity in stock of the product variant.

### ResellerSortKeys
Define the reseller attribute which the result set will be sorted on.

Values:
- `ID` - Reseller unique identifier
- `NAME` - The reseller's name

### ScriptPageType
Values:
- `ALL`
- `HOME`
- `SEARCH`
- `CATEGORY`
- `BRAND`
- `PRODUCT`

### ScriptPosition
Values:
- `HEADER_START`
- `HEADER_END`
- `BODY_START`
- `BODY_END`
- `FOOTER_START`
- `FOOTER_END`

### SimpleLoginType
The simple login type.

Values:
- `NEW`
- `SIMPLE`

### SortDirection
Define the sort orientation of the result set.

Values:
- `ASC` - The results will be sorted in an ascending order.
- `DESC` - The results will be sorted in an descending order.

### Status
The subscription status to update.

Values:
- `ACTIVE`
- `PAUSED`
- `CANCELED`

### TypeCheckingAccount
Represents the Type of Customer's Checking Account.

Values:
- `Credit` - Credit
- `Debit` - Debit

### UriKind
Values:
- `PRODUCT`
- `HOTSITE`
- `REDIRECT`
- `NOT_FOUND`
- `PARTNER`
- `BUY_LIST`

