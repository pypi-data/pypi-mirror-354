# OxaPay Python Client

[![PyPI version](https://badge.fury.io/py/oxapay.svg)](https://badge.fury.io/py/oxapay)
[![Python Version](https://img.shields.io/pypi/v/oxapay)](https://pypi.org/project/oxapay/)
[![License](https://img.shields.io/pypi/l/oxapay)](https://codeberg.org/TheKaram/PyOxapay/src/branch/main/LICENSE)

A fully-typed Python client for interacting with the [OxaPay](https://oxapay.com/) cryptocurrency payment gateway. This client provides both asynchronous and synchronous interfaces, comprehensive model typing, and webhook handling integration.

## Features

- 🚀 Async-first design with synchronous wrappers
- 🔒 Comprehensive type hints and Pydantic models
- 🌐 Complete API coverage (Merchant, Payout, Exchange, System)
- 🔄 FastAPI webhook integration
- 📚 Full documentation and examples

## Installation

```bash
pip install oxapay
```

For webhook handling with FastAPI:

```bash
pip install "oxapay[webhook]"
```

## Quick Start

### Async Client

```python
import asyncio
from oxapay import OxaPayClient
from oxapay.models import CreateInvoiceRequest

async def main():
    # Initialize client with your API keys
    async with OxaPayClient(
        merchant_api_key="your_merchant_api_key",
        payout_api_key="your_payout_api_key",
        general_api_key="your_general_api_key"
    ) as client:
        # Create a payment invoice
        invoice_request = CreateInvoiceRequest(
            amount=100,
            currency="USD",
            order_id="order_123",
            email="customer@example.com",
            description="Payment for Order #123"
        )

        response = await client.create_invoice(invoice_request)
        print(f"Payment URL: {response.pay_link}")
        print(f"Track ID: {response.track_id}")

        # Check system status
        status = await client.check_system_status()
        print(f"System status: {status}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Synchronous Client

```python
from oxapay.sync import SyncOxaPayClient
from oxapay.models import CreateInvoiceRequest

# Initialize client with your API keys
client = SyncOxaPayClient(
    merchant_api_key="your_merchant_api_key"
)

# Create a payment invoice
invoice_request = CreateInvoiceRequest(
    amount=100,
    currency="USD",
    order_id="order_123",
    email="customer@example.com",
    description="Payment for Order #123"
)

response = client.create_invoice(invoice_request)
print(f"Payment URL: {response.pay_link}")
print(f"Track ID: {response.track_id}")
```

### Webhook Handling with FastAPI

```python
from fastapi import FastAPI
from oxapay.webhook import WebhookRouter
from oxapay.models import PaymentWebhookEvent, PayoutWebhookEvent

app = FastAPI()

# Initialize webhook router
webhook = WebhookRouter(
    app=app,
    merchant_api_key="your_merchant_api_key",
    payout_api_key="your_payout_api_key",
    path="/oxapay/webhook"
)

# Register payment handlers
@webhook.on_payment_paid
async def handle_payment_paid(event: PaymentWebhookEvent):
    print(f"Payment {event.track_id} received: {event.amount} {event.currency}")
    # Process order fulfillment here

@webhook.on_payment_expired
def handle_payment_expired(event: PaymentWebhookEvent):
    print(f"Payment {event.track_id} expired")
    # Handle expired payment

# Register payout handlers
@webhook.on_payout_complete
async def handle_payout_complete(event: PayoutWebhookEvent):
    print(f"Payout {event.track_id} completed: {event.amount} {event.currency}")
    # Update payout status in your system

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## API Documentation

The client provides access to all OxaPay API endpoints:

### Merchant API
- Creating payment invoices
- Managing white-label payments
- Creating and managing static wallets
- Retrieving payment information and history

### Payout API
- Creating payouts to cryptocurrency addresses
- Retrieving payout information and history
- Managing account balances

### Exchange API
- Getting exchange rates and pairs
- Calculating exchange amounts
- Creating and tracking exchange requests

### System API
- Retrieving cryptocurrency prices
- Getting supported currencies and networks
- Checking system status

## Detailed Examples

### Creating a Payment Invoice

```python
from oxapay import OxaPayClient
from oxapay.models import CreateInvoiceRequest

async def create_payment():
    async with OxaPayClient(merchant_api_key="your_api_key") as client:
        invoice = CreateInvoiceRequest(
            amount=100.50,
            currency="USD",
            order_id="order_12345",
            email="customer@example.com",
            description="Premium subscription",
            callback_url="https://your-website.com/oxapay/callback",
            return_url="https://your-website.com/thank-you",
            life_time=60,  # 60 minutes expiration
            fee_paid_by_payer=1  # 1 = payer pays fees, 0 = merchant pays fees
        )

        response = await client.create_invoice(invoice)
        return response.pay_link, response.track_id
```

### Creating a Payout

```python
from oxapay import OxaPayClient
from oxapay.models import CreatePayoutRequest

async def send_payout():
    async with OxaPayClient(payout_api_key="your_payout_api_key") as client:
        payout = CreatePayoutRequest(
            address="3FZbgi29cpjq2GjdwV8eyHuJJnkLtktZc5",
            amount=0.001,
            currency="BTC",
            network="bitcoin",
            description="Affiliate payment",
            callback_url="https://your-website.com/payout-callback"
        )

        response = await client.create_payout(payout)
        return response.track_id
```

### Getting Account Balance

```python
from oxapay import OxaPayClient

async def check_balances():
    async with OxaPayClient(payout_api_key="your_payout_api_key") as client:
        # Get all balances
        all_balances = await client.get_account_balance()
        print(all_balances.data)

        # Get specific currency balance
        btc_balance = await client.get_account_balance(currency="BTC")
        print(f"BTC Balance: {btc_balance.data['BTC']}")
```

### Verifying Webhook Signatures

```python
from oxapay import OxaPayClient

def verify_webhook(signature, payload, is_payment=True):
    client = OxaPayClient(
        merchant_api_key="your_merchant_api_key",
        payout_api_key="your_payout_api_key"
    )

    is_valid = client.verify_webhook_signature(
        signature=signature,
        payload=payload,
        is_payment=is_payment  # True for payment webhooks, False for payout webhooks
    )

    return is_valid
```

## Error Handling

The library provides specific exception classes for error handling:

```python
from oxapay import OxaPayClient, OxaPayError, OxaPayValidationError

async def handle_errors():
    try:
        async with OxaPayClient(merchant_api_key="invalid_key") as client:
            await client.get_accepted_coins()
    except OxaPayError as e:
        print(f"API Error: {e.code} - {e.message}")
    except OxaPayValidationError as e:
        print(f"Validation Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
