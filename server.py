from flask import Flask, request, jsonify
import os

app = Flask(_name_)

@app.route("/")
def index():
    return "OK"
