import asyncio
import sys

from oxapay import OxaPayClient, OxaPayError


async def check_payment_status(track_id: str) -> None:
    """Example of checking a payment's status."""
    # Replace with your actual API key
    merchant_api_key = "your_merchant_api_key"

    async with OxaPayClient(merchant_api_key=merchant_api_key) as client:
        try:
            # Get payment information
            payment = await client.get_payment_info(track_id)

            print(f"Payment {track_id} information:")
            print(f"Status: {payment.status}")
            print(f"Amount: {payment.amount} {payment.currency}")

            if payment.status == "Paid":
                print(f"Payment completed at: {payment.pay_date}")
                print(f"Transaction ID: {payment.tx_id}")
            elif payment.status == "Expired":
                print("Payment has expired")
            elif payment.status in ["New", "Waiting", "Confirming"]:
                print("Payment is still in progress")

        except OxaPayError as e:
            print(f"API Error {e.code}: {e.message}")
        except Exception as e:
            print(f"Error checking payment: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_payment_status.py <track_id>")
        sys.exit(1)

    track_id = sys.argv[1]
    asyncio.run(check_payment_status(track_id))
