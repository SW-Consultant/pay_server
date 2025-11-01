from flask import Flask, request, jsonify
from config import SECRET_KEY
from utils import create_paypal_order

app = Flask(__name__)

@app.route("/")
def home():
    return "Payment server is running"

@app.route("/create_payment", methods=["POST"])
def create_payment():
    auth = request.headers.get("Authorization", "")
    if auth != f"Bearer {SECRET_KEY}":
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    data = request.json
    if not data or "amount" not in data:
        return jsonify({"status": "error", "message": "Amount required"}), 400

    amount = data["amount"]
    try:
        order = create_paypal_order(amount)
        return jsonify({"status": "success", "order": order})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
