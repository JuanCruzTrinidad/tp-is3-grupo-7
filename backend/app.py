from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    """Verificación de estado del servidor."""
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
