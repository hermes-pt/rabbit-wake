Processo de Fechamento de Pedido através do Storefront API
Suggest Edits
Etapas
Cadastro de Usuário: Criação de um novo usuário
Cadastro de Endereço de Usuário: Cadastro de um endereço do usuário
Criando um Carrinho:
3.1 Adicionando ou Removendo Produtos ao Carrinho: Inserindo ou Removendo um produto ao carrinho.
3.2 Adicionando produto com assinatura ao Carrinho: Inserindo um produto de assinatura ao carrinho.
3.3 Adicionando produto com personalização ao Carrinho: Inserindo um produto com personalização ao carrinho.
Realizando Login Autenticado : e-mail e senha: Criando um token de acesso às informações de um usuário.
Associando o Cliente ao Carrinho: Criação de um novo carrinho e posterior associação ao cliente.
Selecionando Endereço de Entrega: Selecionando um endereço de entrega para o checkout.
Listagem das Formas de Envio: A API retorna as opções de envio disponíveis para o carrinho.
Seleção da Forma de Envio: A opção de envio é selecionada.
8.1 Agendamento de Entrega: Opção de agendar a entrega do produto.
8.2 Retirada na Loja(com informações adicionais): Opção de retirar o produto na loja.
Aplicando um Cupom de Desconto: Adicionando um cupom de desconto ao carrinho.
Listagem das Formas de Pagamento: A API retorna todas as opções de pagamento disponíveis para o carrinho.
Seleção da Forma de Pagamento: A opção de pagamento é selecionada.
Seleção do Parcelamento de Forma de Pagamento: Selecionando um parcelamento conforme configurado na loja.
Fechamento do Carrinho: O carrinho é fechado e o pedido é concluído.
Cadastrando um usuário
Para realizar o cadastro de um usuário, basta enviar a requisição com os parâmetros necessários.

Request

mutation($input: CustomerCreateInput) {
  customerCreate(input: $input) {
    customerId
    customerName
    customerType
  }
}
Variáveis

{
  "input": {
    "address": "Rua das Flores",
    "addressNumber": "111",
    "cep": "80200-000",
    "city": "Curitiba",
    "cpf": "070.347.090-68",
    "email": "teste2023@gmail.com",
    "fullName": "Feliciano da Silva",
    "gender": "MALE",
    "state": "PR",
    "neighborhood": "Fioravante Marino",
    "primaryPhoneAreaCode": "41",
    "primaryPhoneNumber": "99111-0001",
    "password": "123456",
    "passwordConfirmation": "123456",
    "customerType": "PERSON",
    "birthDate": "10/01/1980",
    "receiverName": "Joaquim Pereira"
  }
}
Response

{
  "data": {
    "customerCreate": {
      "customerId": 407675,
      "customerName": "Feliciano da Silva",
      "customerType": "Física"
    }
  }
}
Realizando o Login Autenticado
Para realizar o Login é necessário realizar a requisição conforme exemplo abaixo.

Request

mutation {
  customerAuthenticatedLogin(input:{input: $input, password: $pass}) {
    isMaster
    token
    type
    validuntil
  }
}
Variáveis

{
  "input": "meuemail@teste.com.br",
  "pass": "123456",
}
Response

{
  "data": {
    "customerAuthenticatedLogin": {
      "isMaster": true,
      "token": "token",
      "type": "AUTHENTICATED",
      "validUntil": "2023-12-07-18T15:27:36.087-03:00"
    }
  }
}
Cadastrando o Endereço do Usuário
Para realizar o cadastro de um endereço do usuário, basta enviar a requisição com os parâmetros necessários.

Request

mutation($address: CreateCustomerAddressInput!, $customerAccessToken: String!) {
  customerAddressCreate(
    address: $address
    customerAccessToken: $customerAccessToken
  ) {
    id
    name
    addressDetails
  }
}
Variáveis

{
  "address": 
  {
    "addressNumber": "120",
    "cep": "05707-001",
    "city": "São Paulo",
    "country": "BR",
    "email": "teste2023@gmail.com",
    "name": "Vanderléia dos Santos",
    "neighborhood": "Novo Horizonte",
    "phone": "1199122-0001",
    "state": "SP",
    "street": "Rua Itapaiuna"
  },
  "customerAccessToken": "CFyqybUNFBllxImseZwTKiS2d7405lpiC9Ph3YtqGiCB+6cWEkFZfA2Xgw1YAZCiqocNxMFGrI5PVjirwXJuRDwmPJoHSJnV1MflmTqtpVw7WdE/1RRmo8uMHhit7Guw63gCxKj+ilPd77Y9YcAetv/QfRk3l9/54tnYRF31A5s6oBmqFIBtaU3dx42WbKTX"
}
Response

{
  "data": {
    "customerAddressCreate": {
      "id": "eyJFbnRpdHkiOiJDdXN0b21lckFkZHJlc3MiLCJJZCI6NjgwNDg0fQ==",
      "name": "Vanderléia dos Santos",
      "addressDetails": null
    }
  }
}
Criando um Carrinho
A primeira requisição é uma mutation que cria um novo carrinho. A requisição deve conter a lista de produtos que devem ser adicionados ao carrinho. A resposta da API será um objeto que representa o carrinho criado.

Request

mutation($products: [CheckoutProductItemInput]) {
  createCheckout(products: $products) {
    ...checkoutFields
  }
}

fragment checkoutFields on Checkout {
  checkoutId
  products {
    productVariantId
    quantity
  }
}
Variáveis

{
	"products": [
		{
			"productVariantId": 258198,
			"quantity": 1
		}
	]
}
Response

{
  "data": {
    "createCheckout": {
      "checkoutId": "ce8ac3c3-c8f9-4393-9a0a-ac80e2aee438",
      "products": [
        {
          "productVariantId": 258198,
          "quantity": 1
        }
      ]
    }
  }
}
Associando o usuário ao carrinho
A próxima requisição é uma mutation que associa um cliente ao carrinho criado. A requisição deve conter o ID do carrinho e o token do cliente.

Request

mutation($customerAccessToken: String!, $checkoutId: Uuid!) {
  checkoutCustomerAssociate(
    customerAccessToken: $customerAccessToken
    checkoutId: $checkoutId
  ) {
    ...checkoutFields
  }
}

fragment checkoutFields on Checkout {
  cep
  checkoutId
  customer {
    cnpj
    cpf
    creditLimit
    creditLimitBalance
    customerId
    customerName
    email
    phoneNumber
  }
  selectedAddress {
    addressNumber
    cep
    city
    complement
    id
    neighborhood
    referencePoint
    state
    street
  }
}
Variáveis

{
	"checkoutId": "ce8ac3c3-c8f9-4393-9a0a-ac80e2aee438",
	"customerAccessToken": "CFyqybUNFBllxImseZwTKiS2d7405lpiC9Ph3YtqGiCB+6cWEkFZfA2Xgw1YAZCiqocNxMFGrI5PVjirwXJuRDwmPJoHSJnV1MflmTqtpVw7WdE/1RRmo8uMHhit7Guw63gCxKj+ilPd77Y9YcAetv/QfRk3l9/54tnYRF31A5s6oBmqFIBtaU3dx42WbKTX"
}
Response

{
  "data": {
    "checkoutCustomerAssociate": {
      "cep": 5707001,
      "checkoutId": "ce8ac3c3-c8f9-4393-9a0a-ac80e2aee438",
      "customer": {
        "cnpj": "",
        "cpf": "07034709068",
        "creditLimit": 0,
        "creditLimitBalance": 0,
        "customerId": 407675,
        "customerName": "Feliciano da Silva",
        "email": "teste2023@gmail.com",
        "phoneNumber": "4199111-0001"
      },
      "selectedAddress": {
        "addressNumber": "120",
        "cep": 5707001,
        "city": "São Paulo",
        "complement": null,
        "id": "680484",
        "neighborhood": "Novo Horizonte",
        "referencePoint": null,
        "state": "SP",
        "street": "Rua Itapaiuna"
      }
    }
  }
}
Selecionando Endereço de Entrega
Para selecionar um endereço para entrega, basta enviar a requisição com os parâmetros necessários.

Request

mutation($customerAccessToken: String!, $addressId: ID!, $checkoutId: Uuid!) {
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
Variáveis

{
  "customerAccessToken": "CFyqybUNFBllxImseZwTKiS2d7405lpiC9Ph3YtqGiCB+6cWEkFZfA2Xgw1YAZCiqocNxMFGrI5PVjirwXJuRDwmPJoHSJnV1MflmTqtpVw7WdE/1RRmo8uMHhit7Guw63gCxKj+ilPd77Y9YcAetv/QfRk3l9/54tnYRF31A5s6oBmqFIBtaU3dx42WbKTX",
  "addressId":"eyJFbnRpdHkiOiJDdXN0b21lckFkZHJlc3MiLCJJZCI6NjgwNDg0fQ==",
  "checkoutId":"ce8ac3c3-c8f9-4393-9a0a-ac80e2aee438"
}
Response

{
  "data": {
    "checkoutAddressAssociate": {
      "cep": 5707001,
      "checkoutId": "ce8ac3c3-c8f9-4393-9a0a-ac80e2aee438",
      "url": "https://lojacss.checkout.fbits.store/",
      "updateDate": "2023-07-06T15:53:48.820-03:00"
    }
  }
}
Listando as Formas de Envio
A seguinte requisição é uma query que retorna todas as opções de envio disponíveis para o carrinho. A requisição deve conter o ID do carrinho. A resposta da API será uma lista de opções de envio.

Request

query($checkoutId: Uuid!) {
  shippingQuotes(checkoutId: $checkoutId, useSelectedAddress: true) {
    deadline
    name
    products {
      productVariantId
      value
    }
    shippingQuoteId
    type
    value
  }
}
Variáveis

{
	"checkoutId": "ce8ac3c3-c8f9-4393-9a0a-ac80e2aee438"
}
Response

{
  "data": {
    "shippingQuotes": [
      {
        "deadline": 0,
        "name": "Teste 859",
        "products": [
          {
            "productVariantId": 258198,
            "value": 0
          }
        ],
        "shippingQuoteId": "0f1ddf45-4feb-4a7d-a8b3-2bd7cd83d126",
        "type": "Retirada",
        "value": 0
      },
      {
        "deadline": 0,
        "name": "Tray Corp - Macapá",
        "products": [
          {
            "productVariantId": 258198,
            "value": 0
          }
        ],
        "shippingQuoteId": "503a4fb8-dfff-4d3f-952d-9b6f3403495d",
        "type": "Retirada",
        "value": 0
      },
      {
        "deadline": 13,
        "name": "Transportadora Ágil",
        "products": [
          {
            "productVariantId": 258198,
            "value": 25.12
          }
        ],
        "shippingQuoteId": "d455624d-aa1a-40ae-be89-5ef52b4d0e37",
        "type": "Tabela",
        "value": 25.12
      },
      {
        "deadline": 3,
        "name": "Teste contrato 1",
        "products": [
          {
            "productVariantId": 258198,
            "value": 106
          }
        ],
        "shippingQuoteId": "476151ee-682d-4f82-b7ed-465d5641a4ef",
        "type": "Tabela",
        "value": 106
      }
    ]
  }
}
Selecionando a Forma de Envio com informações adicionais
A próxima requisição é uma mutation que seleciona a opção de envio para o carrinho.

Request

mutation(
  $checkoutId: Uuid!
  $shippingQuoteId: Uuid!
  $additionalInformation: InStorePickupAdditionalInformationInput
) {
  checkoutSelectShippingQuote(
    checkoutId: $checkoutId
    shippingQuoteId: $shippingQuoteId
    additionalInformation: $additionalInformation
  ) {
    ...checkoutFields
  }
}

fragment checkoutFields on Checkout {
  cep
  checkoutId
  shippingFee
  total
  subtotal
  selectedShipping {
    deadline
    name
    shippingQuoteId
    type
    value
    deliverySchedule {
      date
      endDateTime
      endTime
      startDateTime
      startTime
    }
  }
}
Variáveis

{
  "shippingQuoteId": "503a4fb8-dfff-4d3f-952d-9b6f3403495d",
  "checkoutId": "ce8ac3c3-c8f9-4393-9a0a-ac80e2aee438",
  "additionalInformation": {
    "document": "123456",
    "name": "Armando"
  }
}
Response

{
  "data": {
    "checkoutSelectShippingQuote": {
      "cep": 5707001,
      "checkoutId": "ce8ac3c3-c8f9-4393-9a0a-ac80e2aee438",
      "shippingFee": 0,
      "total": 8721.7,
      "subtotal": 670.9,
      "selectedShipping": {
        "deadline": 0,
        "name": "Tray Corp - Macapá",
        "shippingQuoteId": "503a4fb8-dfff-4d3f-952d-9b6f3403495d",
        "type": "Retirada",
        "value": 0,
        "deliverySchedule": null
      }
    }
  }
}
Aplicando um Cupom de Desconto
Para aplicar um cupom de desconto a um carrinho, basta enviar a requisição com os parâmetros necessários.

Request

mutation($checkoutId: Uuid!, $coupon: String!, $customerAccessToken: String) {
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
Variáveis

{
  "checkoutId": "ce8ac3c3-c8f9-4393-9a0a-ac80e2aee438",
  "coupon": "promo1",
  "customerAccessToken":"CFyqybUNFBllxImseZwTKiS2d7405lpiC9Ph3YtqGiCB+6cWEkFZfA2Xgw1YAZCiqocNxMFGrI5PVjirwXJuRDwmPJoHSJnV1MflmTqtpVw7WdE/1RRmo8uMHhit7Guw63gCxKj+ilPd77Y9YcAetv/QfRk3l9/54tnYRF31A5s6oBmqFIBtaU3dx42WbKTX"
  }
Response

{
  "data": {
    "checkoutAddCoupon": {
      "checkoutId": "ce8ac3c3-c8f9-4393-9a0a-ac80e2aee438",
      "coupon": "promo1",
      "total": 8721.7,
      "subtotal": 670.9
    }
  }
}
Listagem das Formas de Pagamento
Para obter a listagem das formas de pagamento, basta realizar a consulta conforme exemplo da requisição abaixo.

Request

query($checkoutId: Uuid!) {
  paymentMethods(checkoutId: $checkoutId) {
    id
    name
    imageUrl
  }
}
Variáveis

{
  "checkoutId": "ce8ac3c3-c8f9-4393-9a0a-ac80e2aee438"
}
Response

{
  "data": {
    "paymentMethods": [
      {
        "id": "eyJFbnRpdHkiOiJQYXltZW50TWV0aG9kIiwiSWQiOjM3Nzd9",
        "name": "Boleto",
        "imageUrl": "https://conector.ecommercegateway.com.br/Recursos/Imagens/055b3df3-d185-438b-8e1a-b0b9c5d639d2.png"
      }
    ]
  }
}
Selecionando a Forma de Pagamento
A próxima requisição é uma mutation que seleciona a opção de pagamento para o carrinho.

Request

mutation($checkoutId: Uuid!, $paymentMethodId: ID!) {
  checkoutSelectPaymentMethod(
    checkoutId: $checkoutId
    paymentMethodId: $paymentMethodId
  ) {
    ...checkoutFields
  }
}

fragment checkoutFields on Checkout {
  checkoutId
  total
  subtotal
  selectedPaymentMethod {
    id
    installments {
      adjustment
      number
      total
      value
    }
    selectedInstallment {
      adjustment
      number
      total
      value
    }
  }
}
Varáveis

{
  "checkoutId": "ce8ac3c3-c8f9-4393-9a0a-ac80e2aee438",
  "paymentMethodId": "eyJFbnRpdHkiOiJQYXltZW50TWV0aG9kIiwiSWQiOjM3Nzd9"
}
Response

{
  "data": {
    "checkoutSelectPaymentMethod": {
      "checkoutId": "ce8ac3c3-c8f9-4393-9a0a-ac80e2aee438",
      "total": 8721.7,
      "subtotal": 670.9,
      "selectedPaymentMethod": {
        "id": "25a95a84-5013-42a8-ae5e-7f7710f91238",
        "installments": [
          {
            "adjustment": -0.1,
            "number": 1,
            "total": 7849.53,
            "value": 7849.53
          }
        ],
        "selectedInstallment": {
          "adjustment": -0.1,
          "number": 1,
          "total": 7849.53,
          "value": 7849.53
        }
      }
    }
  }
}
Concluindo o Pedido
Finalmente, concluímos o pedido. Essa mutation fecha o carrinho, e é nesse momento que o pedido é efetivamente criado no sistema. É importante notar que, dependendo do método de pagamento selecionado, informações adicionais de pagamento podem ser necessárias.

Request

mutation (
  $checkoutId: Uuid!
  $paymentData: String!
  $comments: String
  $customerAccessToken: String
) {
  checkoutComplete(
    checkoutId: $checkoutId
    paymentData: $paymentData
    comments: $comments
    customerAccessToken: $customerAccessToken
  ) {
    ...checkoutFields
  }
}

fragment checkoutFields on Checkout {
  checkoutId
  completed
  orders {
    adjustments {
      name
      type
      value
    }
    date
    discountValue
    interestValue
    orderId
    orderStatus
    products {
      adjustments {
        name
        additionalInformation
        type
        value
      }
      attributes {
        name
        value
      }
      imageUrl
      name
      productVariantId
      quantity
      value
    }
    shippingValue
    totalValue
    delivery {
      address {
        address
        cep
        city
        complement
        name
        isPickupStore
        neighborhood
        pickupStoreText
      }
      cost
      deliveryTime
      name
    }
    dispatchTimeText
    payment {
      invoice {
        digitableLine
        paymentLink
      }
      name
      pix {
        qrCode
        qrCodeExpirationDate
        qrCodeUrl
      }
    }
  }
}
Variáveis

{
  "paymentData": "cpf=72628449030&telefone=11912345674",
  "comments": "Observação do Pedido",
  "checkoutId": "ce8ac3c3-c8f9-4393-9a0a-ac80e2aee438",
  "customerAccessToken": "CFyqybUNFBllxImseZwTKiS2d7405lpiC9Ph3YtqGiCB+6cWEkFZfA2Xgw1YAZCiqocNxMFGrI5PVjirwXJuRDwmPJoHSJnV1MflmTqtpVw7WdE/1RRmo8uMHhit7Guw63gCxKj+ilPd77Y9YcAetv/QfRk3l9/54tnYRF31A5s6oBmqFIBtaU3dx42WbKTX"
}
Response

{
  "data": {
    "checkoutComplete": {
      "checkoutId": "ce8ac3c3-c8f9-4393-9a0a-ac80e2aee438",
      "completed": true,
      "orders": [
        {
          "adjustments": [
            {
              "name": "IPI PR",
              "type": "Formula",
              "value": 8050.8
            }
          ],
          "date": "2023-07-06T16:35:40.007-03:00",
          "discountValue": -872.17,
          "interestValue": 0,
          "orderId": 346266,
          "orderStatus": "AWAITING_PAYMENT",
          "products": [
            {
              "adjustments": [
                {
                  "name": "Tray Corp - Macapá",
                  "additionalInformation": "Tray Corp - Macapá - 503a4fb8-dfff-4d3f-952d-9b6f3403495d",
                  "type": "Frete",
                  "value": 0
                },
                {
                  "name": "Promoção",
                  "additionalInformation": "{\"id\":10590, \"nome\": \"vale presente\", \"cupom\": \"\"}",
                  "type": "PromocaoProduto",
                  "value": -499
                },
                {
                  "name": "IPI PR",
                  "additionalInformation": "{\"ChaveAjuste\":\"3c31f902-a117-4118-afe1-8fc360b6896e\",\"Formula\":\"Testes Postman (NÃO INATIVAR!)\",\"Matriz\":\"PR\",\"EndPoint\":null,\"Expressao\":\"(@subtotalCarrinho  *  5) / 100 + @matriz \",\"ExpressaoInterpretada\":\"@670.9 *@12\",\"Valor\":8050.8,\"Nome\":\"Testes Postman (NÃO INATIVAR!) PR\",\"ProdutoVarianteId\":258198}",
                  "type": "Formula",
                  "value": 8050.8
                },
                {
                  "name": "",
                  "additionalInformation": "Pagamento rateado",
                  "type": "FormaPagamento",
                  "value": -872.17
                }
              ],
              "attributes": [
                {
                  "name": "COR",
                  "value": "Vermelho"
                }
              ],
              "imageUrl": "https://lojacss.fbitsstatic.net/img/p/sem-foto.jpg",
              "name": "Poltrona Cadeira Decorativa Chesterfield Suede Vermelho Recepção Sala de Estar - AM Decor",
              "productVariantId": 258198,
              "quantity": 1,
              "value": 670.9
            }
          ],
          "shippingValue": 0,
          "totalValue": 7849.53,
          "delivery": {
            "address": {
              "address": "Avenida Diógenes Silva, 100",
              "cep": "68901-326",
              "city": "Macapá - AP",
              "complement": null,
              "name": null,
              "isPickupStore": true,
              "neighborhood": "Santa Rita",
              "pickupStoreText": null
            },
            "cost": 0,
            "deliveryTime": 0,
            "name": "Tray Corp - Macapá"
          },
          "dispatchTimeText": "(após pedido ser despachado):",
          "payment": {
            "invoice": {
              "digitableLine": "23790.00124  60010.020216  68123.456706  1  94080000784953",
              "paymentLink": "https://intermediador-sandbox.yapay.com.br/orders/billet/0c53a156b93246e7a712c245af6268d8"
            },
            "name": "Boleto",
            "pix": null
          }
        }
      ]
    }
  }
}