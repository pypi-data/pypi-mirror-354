# PayMongo Service (Python)

A simple and lightweight Python wrapper for the [PayMongo API](https://developers.paymongo.com/) that allows developers to create payment intents, methods, and attach them using Python code.

## Features

- Create Payment Intents
- Create Payment Methods
- Attach a Payment Method to an Intent
- Supports both `card` and `gcash`
- Supports environment variable or direct secret key assignment

## Installation

Install via pip:

```bash
pip install paymongo-wrapper
```

## Setup

You can either:

### 1. Use environment variables (recommended):

Create a `.env` file:

```env
PAYMONGO_SECRET_KEY=sk_test_your_secret_key
PAYMONGO_PUBLIC_KEY=pk_test_your_public_key
PAYMONGO_RETURN_URL=http://127.0.0.1:8000/
```

Then load them using `python-dotenv`:

```python
from dotenv import load_dotenv
load_dotenv()
```

### 2. Declartion

```python
from paymongo_wrapper import PayMongoService

paymongo = PayMongoService(
    secret_key="sk_test_your_secret_key",
    return_url="http://127.0.0.1:8000/"
)

intent = paymongo.create_payment_intent(100.00)
```


### 3(Optional). Or directly modify the variables in `service.py`:

```python
PAYMONGO_SECRET_KEY = "sk_test_your_secret_key"
PAYMONGO_PUBLIC_KEY = "pk_test_your_public_key"
PAYMONGO_RETURN_URL = "http://127.0.0.1:8000/"
```

## Usage

```python
from paymongo_wrapper import PayMongoService

paymongo = PayMongoService()

# Step 1: Create a Payment Intent
intent = paymongo.create_payment_intent(amount=100)  # PHP 100.00
payment_intent_id = intent['data']['id']

# Step 2: Create a Payment Method
method = paymongo.create_payment_method(
    method_type="gcash",
    details={"phone": "09171234567"}
)
payment_method_id = method['data']['id']

# Step 3: Attach the Payment Method to the Intent
result = paymongo.attach_payment_intent(payment_intent_id, payment_method_id)
print(result)
```

## Exception Handling

The library raises custom exceptions:

- `PaymentIntentError`
- `PaymentMethodError`
- `AttachIntentError`

Wrap your logic in try-except blocks if needed.

## Contributing

Contributions are welcome. Please open an issue or pull request.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

