import requests
import base64
import logging
import os

from .exceptions import PaymentIntentError, PaymentMethodError, AttachIntentError

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class PayMongoService:
    API_BASE_URL = "https://api.paymongo.com/v1"

    def __init__(self, secret_key=None, return_url=None):
        """
        Initialize the PayMongo service.

        Args:
            secret_key (str): Your PayMongo secret key.
            return_url (str): URL to redirect after payment confirmation.
        """
        self.secret_key = secret_key or os.getenv("PAYMONGO_SECRET_KEY")
        self.return_url = return_url or os.getenv(
            "PAYMONGO_RETURN_URL", 
            "http://127.0.0.1:8000/"
        )

        if not self.secret_key:
            raise ValueError("PayMongo secret key is required.")

        self.auth_bytes = self.secret_key.encode("ascii")
        self.base64_auth = base64.b64encode(self.auth_bytes).decode("ascii")
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.base64_auth}",
        }

    def create_payment_intent(self, amount):
        """Create a payment intent in centavos (e.g., 10000 = ₱100.00)"""
        url = f"{self.API_BASE_URL}/payment_intents"
        payload = {
            "data": {
                "attributes": {
                    "amount": int(amount * 100),
                    "payment_method_allowed": ["card", "gcash"],
                    "currency": "PHP",
                    "description": "Service Payment",
                }
            }
        }
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            logging.info(f"Payment intent created: {response.json()}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to create payment intent: {e}")
            raise PaymentIntentError(f"Error creating payment intent: {e}") from e

    def create_payment_method(self, method_type, details=None):
        url = f"{self.API_BASE_URL}/payment_methods"
        payload = {
            "data": {
                "attributes": {
                    "type": method_type,
                    **({"details": details} if details else {}),
                }
            }
        }
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            logging.info(f"Payment method created: {response.json()}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to create payment method: {e}")
            raise PaymentMethodError(f"Error creating payment method: {e}") from e

    def attach_payment_intent(self, payment_intent_id, payment_method_id):
        url = f"{self.API_BASE_URL}/payment_intents/{payment_intent_id}/attach"
        payload = {
            "data": {
                "attributes": {
                    "payment_method": payment_method_id,
                    "return_url": self.return_url,
                }
            }
        }
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            logging.info(f"Payment intent attached: {response.json()}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to attach payment intent: {e}")
            raise AttachIntentError(f"Error attaching payment method: {e}") from e
