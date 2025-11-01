from flask import Flask, request, jsonify
from config import PAYPAL_CLIENT_ID, PAYPAL_SECRET
from utils import create_paypal_order

app = Flask(__name__)

@app.route("/")
def home():
    return "Payment server is running"

@app.route("/create_payment", methods=["POST"])
def create_payment():
    data = request.json
    if not data or "amount" not in data:
        return jsonify({"status": "error", "message": "Amount required"}), 400
    
    amount = data["amount"]
    
    # Создаем платеж (пример для PayPal)
    order = create_paypal_order(amount)
    if order:
        return jsonify({"status": "success", "order": order})
    else:
        return jsonify({"status": "error", "message": "Failed to create payment"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
