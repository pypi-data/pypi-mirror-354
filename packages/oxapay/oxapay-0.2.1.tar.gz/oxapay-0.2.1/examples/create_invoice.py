import asyncio

from oxapay import OxaPayClient
from oxapay.models import CreateInvoiceRequest


async def create_invoice() -> None:
    """Example of creating a payment invoice."""
    # Replace with your actual API key
    merchant_api_key = "your_merchant_api_key"

    async with OxaPayClient(merchant_api_key=merchant_api_key) as client:
        # Create invoice request
        request = CreateInvoiceRequest(
            amount=100.50,
            currency="USD",  # Invoice in USD
            order_id="example-order-123",
            description="Purchase of premium widgets",
            email="customer@example.com",
            callback_url="https://your-site.com/oxapay-callback",
            return_url="https://your-site.com/thank-you",
            life_time=60,  # 60 minutes expiration
            fee_paid_by_payer=1,  # Customer pays the transaction fee
        )

        # Send the request
        try:
            response = await client.create_invoice(request)
            print(f"Payment Link: {response.pay_link}")
            print(f"Track ID: {response.track_id}")

            # You would typically store the track_id in your database
            # to associate it with the customer's order

        except Exception as e:
            print(f"Error creating invoice: {e}")


if __name__ == "__main__":
    asyncio.run(create_invoice())
