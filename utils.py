import requests
from requests.auth import HTTPBasicAuth
from config import PAYPAL_CLIENT_ID, PAYPAL_SECRET, PAYPAL_MODE

PAYPAL_API_BASE = "https://api-m.sandbox.paypal.com" if PAYPAL_MODE == "sandbox" else "https://api-m.paypal.com"

def get_paypal_token():
    url = f"{PAYPAL_API_BASE}/v1/oauth2/token"
    data = {"grant_type": "client_credentials"}
    resp = requests.post(url, data=data, auth=HTTPBasicAuth(PAYPAL_CLIENT_ID, PAYPAL_SECRET))
    resp.raise_for_status()
    return resp.json()["access_token"]

def create_paypal_order(amount: str, currency: str = "USD"):
    token = get_paypal_token()
    url = f"{PAYPAL_API_BASE}/v2/checkout/orders"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "intent": "CAPTURE",
        "purchase_units": [{"amount": {"currency_code": currency, "value": str(amount)}}],
        "application_context": {
            "return_url": "https://t.me/YourBot",
            "cancel_url": "https://t.me/YourBot"
        }
    }
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    approve_link = next((l["href"] for l in data.get("links", []) if l.get("rel") == "approve"), None)
    return {"order_id": data.get("id"), "approve_url": approve_link}
