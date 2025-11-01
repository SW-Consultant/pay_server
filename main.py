from flask import Flask, request, jsonify
import requests
import os

app = Flask(_name_)

PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_SECRET = os.getenv("PAYPAL_SECRET")
PAYPAL_API_BASE = "https://api-m.sandbox.paypal.com"  # для теста

def get_paypal_token():
    auth = (PAYPAL_CLIENT_ID, PAYPAL_SECRET)
    headers = {"Accept": "application/json", "Accept-Language": "en_US"}
    data = {"grant_type": "client_credentials"}
    response = requests.post(f"{PAYPAL_API_BASE}/v1/oauth2/token", headers=headers, data=data, auth=auth)
    response.raise_for_status()
    return response.json()["access_token"]

@app.route("/create_payment", methods=["POST"])
def create_payment():
    data = request.json
    amount = data.get("amount")
    currency = data.get("currency", "USD")
    
    token = get_paypal_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "intent": "CAPTURE",
        "purchase_units": [{"amount": {"currency_code": currency, "value": str(amount)}}],
        "application_context": {"return_url": "https://yourapp.com/success", "cancel_url": "https://yourapp.com/cancel"}
    }
    
    response = requests.post(f"{PAYPAL_API_BASE}/v2/checkout/orders", headers=headers, json=payload)
    response.raise_for_status()
    return jsonify(response.json())

@app.route("/health")
def health():
    return "OK"

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
