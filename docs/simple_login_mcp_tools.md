# Wake Simple Login MCP Tools

This MCP server provides tools for Wake's simple login flow with security questions and token management.

## Features

- Simple login flow with security questions
- Token storage in database by phone number
- Token expiration tracking
- Support for both new and existing users

## Tools

### 1. simple_login_start

Start the simple login process for a customer.

**Parameters:**
- `email` (required): Customer email address

**Returns:**
- For existing users: Security question with answer options
- For new users: Registration token

**Example:**
```json
{
  "email": "customer@example.com",
  "type": "SIMPLE",
  "question": {
    "questionId": "abc-123",
    "question": "What year were you born?",
    "answers": [
      {"id": "ans1", "value": "1990"},
      {"id": "ans2", "value": "1995"}
    ]
  }
}
```

### 2. simple_login_verify

Verify the security question answer and obtain access token.

**Parameters:**
- `email` (required): Customer email address
- `question_id` (required): ID from the security question
- `answer_id` (required): ID of the selected answer
- `phone` (optional): Phone number to associate with token

**Returns:**
- Success: Customer access token (saved to database)
- Wrong answer: New security question

**Example:**
```json
{
  "email": "customer@example.com",
  "type": "AUTHENTICATED",
  "customerAccessToken": {
    "token": "xxx...",
    "type": "SIMPLE",
    "validUntil": "2025-01-11T12:00:00Z"
  },
  "token_saved": true,
  "phone": "11999999999"
}
```

## Configuration

Set the following environment variables in `.env`:

```env
# Default phone for token storage (optional)
DEFAULT_CUSTOMER_PHONE=11999999999
```

If `DEFAULT_CUSTOMER_PHONE` is set, tokens will be automatically saved with this phone number when no phone is provided.

## Database

Tokens are stored in the `customer_tokens` table with:
- Phone number
- Email
- Token
- Token type
- Expiration time
- Timestamps

## Usage Example

1. Start login:
```python
result = await simple_login_start(email="customer@example.com")
# Returns security question
```

2. Verify answer:
```python
result = await simple_login_verify(
    email="customer@example.com",
    question_id="abc-123",
    answer_id="ans1",
    phone="11999999999"
)
# Returns token and saves to database
```

## Running the Server

```bash
python -m src.wake.servers.simple_login_server
```