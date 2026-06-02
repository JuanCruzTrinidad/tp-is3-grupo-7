import zipfile
import io

from flask import Flask, jsonify, request
from flask_cors import CORS

from parser import parse_lines, validate_format
from stats import (
    count_messages_per_user,
    count_emojis_per_user,
    messages_by_hour,
    messages_by_weekday,
    most_frequent_emoji,
    top_days,
)
from text_utils import generate_wordcloud_base64

app = Flask(__name__)
CORS(app)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "No se recibió ningún archivo."}), 400

    file = request.files["file"]
    if not file.filename.endswith(".zip"):
        return jsonify({"error": "El archivo debe ser un .zip."}), 400

    try:
        with zipfile.ZipFile(io.BytesIO(file.read())) as zf:
            txt_files = [n for n in zf.namelist() if n.endswith(".txt")]
            if not txt_files:
                return jsonify({"error": "No se encontró un .txt dentro del .zip."}), 400
            raw = zf.read(txt_files[0]).decode("utf-8-sig", errors="replace")
    except zipfile.BadZipFile:
        return jsonify({"error": "El archivo .zip está corrupto."}), 400

    if not validate_format(raw):
        return jsonify({"error": "El archivo no parece un export de WhatsApp."}), 422

    messages = parse_lines(raw)
    emoji_result = most_frequent_emoji(messages)

    return jsonify({
        "total_messages": len(messages),
        "participants": list({m["sender"] for m in messages}),
        "messages_per_user": count_messages_per_user(messages),
        "messages_by_hour": messages_by_hour(messages),
        "messages_by_weekday": messages_by_weekday(messages),
        "top_days": top_days(messages),
        "emojis_per_user": count_emojis_per_user(messages),
        "most_frequent_emoji": list(emoji_result) if emoji_result else None,
        "wordcloud_base64": generate_wordcloud_base64(messages),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
