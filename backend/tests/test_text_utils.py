"""Pruebas unitarias de las funciones de text_utils.py."""

import base64

from text_utils import clean_text, generate_wordcloud_base64


# --- clean_text ----------------------------------------------------------

def test_clean_text_elimina_url_y_stopwords():
    msgs = [{"sender": "Juan", "message": "Hola el la de mundo http://x.com"}]
    # "el", "la", "de" son stopwords; la URL se elimina por completo.
    assert clean_text(msgs) == "hola mundo"


def test_clean_text_elimina_puntuacion_y_normaliza_minusculas():
    msgs = [{"sender": "A", "message": "PERRO, gato; PERRO!"}]
    assert clean_text(msgs).split() == ["perro", "gato", "perro"]


def test_clean_text_elimina_tokens_de_whatsapp():
    msgs = [{"sender": "A", "message": "foto <Multimedia omitido> video <media omitted>"}]
    tokens = clean_text(msgs).split()
    assert "omitido" not in tokens
    assert "omitted" not in tokens
    assert "foto" in tokens and "video" in tokens


def test_clean_text_une_varios_mensajes():
    msgs = [
        {"sender": "A", "message": "perro"},
        {"sender": "B", "message": "gato"},
    ]
    assert clean_text(msgs).split() == ["perro", "gato"]


# --- generate_wordcloud_base64 -------------------------------------------

def test_generate_wordcloud_base64_devuelve_png(sample_messages):
    result = generate_wordcloud_base64(sample_messages)
    assert isinstance(result, str) and result
    # El string base64 debe decodificar a un PNG válido (magic bytes).
    assert base64.b64decode(result)[:8] == b"\x89PNG\r\n\x1a\n"
