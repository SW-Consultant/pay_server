from flask import Flask, request, jsonify
import requests
from requests.auth import HTTPBasicAuth
import os

app = Flask(__name__)

PAYPAL_CLIENT_ID = os.environ.get("PAYPAL_SANDBOX_CLIENT_ID")
PAYPAL_SECRET = os.environ.get("PAYPAL_SANDBOX_SECRET")
PAYPAL_API_BASE = "https://api-m.sandbox.paypal.com"

@app.route("/create-payment", methods=["POST"])
def create_payment():
    data = request.json
    amount = data.get("amount", "5.00")
    description = data.get("description", "Тестовая подписка")

    # Получаем токен Sandbox
    token_resp = requests.post(
        f"{PAYPAL_API_BASE}/v1/oauth2/token",
        auth=HTTPBasicAuth(PAYPAL_CLIENT_ID, PAYPAL_SECRET),
        headers={"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"},
        data="grant_type=client_credentials"
    )
    token_resp.raise_for_status()
    access_token = token_resp.json()["access_token"]

    # Создаём заказ
    payment_resp = requests.post(
        f"{PAYPAL_API_BASE}/v2/checkout/orders",
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"},
        json={
            "intent": "CAPTURE",
            "purchase_units": [{"amount": {"currency_code": "USD", "value": amount}, "description": description}],
            "application_context": {
                "return_url": "https://t.me/SWConsultant",
                "cancel_url": "https://t.me/SWConsultant"
            }
        }
    )
    payment_resp.raise_for_status()
    payment_data = payment_resp.json()

    approve_link = next(link["href"] for link in payment_data["links"] if link["rel"] == "approve")
    return jsonify({"payment_url": approve_link})
