import uvicorn
from fastapi import FastAPI

from oxapay.models import PaymentWebhookEvent
from oxapay.webhook import WebhookRouter

# Create FastAPI app
app = FastAPI(title="OxaPay Webhook Example")

# Initialize the webhook router
webhook = WebhookRouter(
    app=app,
    merchant_api_key="your_merchant_api_key",  # Replace with actual key
    payout_api_key="your_payout_api_key",  # Replace with actual key
    path="/oxapay/webhook",
)


# Register payment webhook handlers
@webhook.on_payment_waiting
async def handle_payment_waiting(event: PaymentWebhookEvent) -> None:
    """Handle payments that are waiting for confirmation."""
    print(f"Payment {event.track_id} is waiting for confirmation")
    print(f"Amount: {event.amount} {event.currency}")
    print(f"Customer email: {event.email}")
    # Update order status in your system


@webhook.on_payment_confirming
async def handle_payment_confirming(event: PaymentWebhookEvent) -> None:
    """Handle payments that are being confirmed on the blockchain."""
    print(f"Payment {event.track_id} is confirming on the blockchain")
    print(f"Transaction ID: {event.tx_id}")
    # Update order status in your system


@webhook.on_payment_paid
async def handle_payment_paid(event: PaymentWebhookEvent) -> None:
    """Handle completed payments."""
    print(f"Payment {event.track_id} has been completed!")
    print(f"Amount: {event.amount} {event.currency}")
    print(f"Paid with: {event.pay_amount} {event.pay_currency}")

    # Here you would typically:
    # 1. Verify the payment matches an order in your system
    # 2. Mark the order as paid
    # 3. Trigger fulfillment process

    # Example database update (pseudo-code):
    # db.update_order(order_id=event.order_id, status="paid", payment_id=event.track_id)

    print(f"Order {event.order_id} has been marked as paid and is being fulfilled")


@webhook.on_payment_expired
def handle_payment_expired(event: PaymentWebhookEvent) -> None:
    """Handle expired payments."""
    print(f"Payment {event.track_id} has expired")
    # Update order status in your system to reflect failed payment
    # Maybe send an email to the customer


@webhook.on_payment_failed
def handle_payment_failed(event: PaymentWebhookEvent) -> None:
    """Handle failed payments."""
    print(f"Payment {event.track_id} has failed")
    print("Reason: Payment processing failed")
    # Update order status and possibly notify customer


# Add a simple status endpoint
@app.get("/status")
def status() -> dict[str, str]:
    """Check if the server is running."""
    return {"status": "online"}


if __name__ == "__main__":
    # Run the webhook server
    uvicorn.run(app, host="0.0.0.0", port=8000)

    # Note: In production, you should run this behind a reverse proxy like Nginx
    # and with a proper HTTPS certificate
