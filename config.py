import os

# Секрет для проверки запросов от Albato
SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key")

# PayPal sandbox credentials
PAYPAL_CLIENT_ID = os.environ.get("PAYPAL_SANDBOX_CLIENT_ID")
PAYPAL_SECRET = os.environ.get("PAYPAL_SANDBOX_SECRET")
PAYPAL_MODE = os.environ.get("PAYPAL_MODE", "sandbox").lower()
