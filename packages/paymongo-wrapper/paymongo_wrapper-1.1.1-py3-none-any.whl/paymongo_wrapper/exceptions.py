# paymongo_wrapper/exceptions.py

class PayMongoError(Exception):
    """Base class for all PayMongo-related errors."""
    pass


class PaymentIntentError(PayMongoError):
    """Raised when creating a payment intent fails."""

    pass


class PaymentMethodError(PayMongoError):
    """Raised when creating a payment method fails."""

    pass


class AttachIntentError(PayMongoError):
    """Raised when attaching a payment method to an intent fails."""

    pass
