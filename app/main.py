from flask import Flask, jsonify
import os

ENV = os.environ["APP_ENV"]
app = Flask(__name__)


@app.route("/api/")
def index():
    return jsonify({"message": "Hello", "env": ENV})


@app.route("/api/health")
def health():
    return jsonify({"status": "OK"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
