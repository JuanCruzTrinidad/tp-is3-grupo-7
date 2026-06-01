from flask import Flask, jsonify

from stats import top_days, messages_by_weekday
from text_utils import clean_text, generate_wordcloud_base64

app = Flask(__name__)

# Datos hardcodeados para verificar Task 1 antes de integrar el endpoint real
_SAMPLE_MESSAGES = [
    {"timestamp": "14/10/2018, 19:51", "sender": "Ana", "message": "hola"},
    {"timestamp": "14/10/2018, 20:00", "sender": "Luis", "message": "hey"},
    {"timestamp": "15/10/2018, 10:00", "sender": "Ana", "message": "buenos días"},
    {"timestamp": "15/10/2018, 10:05", "sender": "Luis", "message": "buen día"},
    {"timestamp": "15/10/2018, 10:10", "sender": "Ana", "message": "cómo estás"},
    {"timestamp": "16/10/2018, 09:00", "sender": "Luis", "message": "bien"},
    {"timestamp": "17/10/2018, 21:00", "sender": "Ana", "message": "jaja"},
    {"timestamp": "17/10/2018, 21:01", "sender": "Luis", "message": "😂"},
    {"timestamp": "18/10/2018, 08:00", "sender": "Ana", "message": "ok"},
    {"timestamp": "19/10/2018, 18:00", "sender": "Luis", "message": "nos vemos"},
]


@app.route("/health", methods=["GET"])
def health():
    """Verificación de estado del servidor."""
    return jsonify({"status": "ok"})


@app.route("/stats/top-days", methods=["GET"])
def stats_top_days():
    """Endpoint de prueba para Task 1 — usa datos hardcodeados."""
    return jsonify({
        "top_days": top_days(_SAMPLE_MESSAGES),
        "messages_by_weekday": messages_by_weekday(_SAMPLE_MESSAGES),
    })


@app.route("/utils/clean-text", methods=["GET"])
def utils_clean_text():
    """Endpoint de prueba para Task 2 — usa datos hardcodeados."""
    return jsonify({"clean_text": clean_text(_SAMPLE_MESSAGES)})


@app.route("/utils/wordcloud", methods=["GET"])
def utils_wordcloud():
    """Endpoint de prueba para Task 3 — usa datos hardcodeados."""
    return jsonify({"wordcloud_base64": generate_wordcloud_base64(_SAMPLE_MESSAGES)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
