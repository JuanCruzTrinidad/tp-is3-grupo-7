"""Pruebas de integración end-to-end del endpoint /analyze (app.py).

A diferencia de los tests unitarios, estas pruebas ejercitan el stack completo
(Flask + parser + stats + text_utils) a través de peticiones HTTP reales usando
el test client de Flask, posteando un .zip armado en memoria.
"""

import io
import zipfile

import pytest

from app import app
from conftest import SAMPLE_CHAT


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def _make_zip(content=SAMPLE_CHAT, filename="_chat.txt"):
    """Arma en memoria un .zip con un .txt adentro, como el export de WhatsApp."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr(filename, content)
    buf.seek(0)
    return buf


def _post_zip(client, file_obj, filename="chat.zip"):
    return client.post(
        "/analyze",
        data={"file": (file_obj, filename)},
        content_type="multipart/form-data",
    )


# --- /health -------------------------------------------------------------

def test_health_ok(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


# --- /analyze: flujo completo --------------------------------------------

def test_analyze_flujo_completo(client):
    res = _post_zip(client, _make_zip())
    assert res.status_code == 200

    body = res.get_json()
    assert body["total_messages"] == 5
    assert set(body["participants"]) == {"Juan", "María", "Pedro"}
    assert body["messages_per_user"] == {"Juan": 2, "María": 2, "Pedro": 1}
    assert body["most_frequent_emoji"] == ["😀", 2]
    assert body["top_days"][0] == ["2018-11-08", 3]
    assert len(body["messages_by_hour"]) == 24
    assert len(body["messages_by_weekday"]) == 7
    assert body["emojis_per_user"]["Juan"] == {"👋": 1}
    assert body["wordcloud_base64"]  # string no vacío


# --- /analyze: caminos de error ------------------------------------------

def test_analyze_sin_archivo(client):
    res = client.post("/analyze", data={}, content_type="multipart/form-data")
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_analyze_archivo_no_zip(client):
    res = _post_zip(client, io.BytesIO(b"texto plano"), filename="chat.txt")
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_analyze_zip_sin_txt(client):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("foto.jpg", b"contenido binario")
    buf.seek(0)
    res = _post_zip(client, buf)
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_analyze_formato_invalido(client):
    # ZIP válido con un .txt, pero el contenido no es un export de WhatsApp.
    res = _post_zip(client, _make_zip(content="solo texto cualquiera\nsin formato"))
    assert res.status_code == 422
    assert "error" in res.get_json()


def test_analyze_zip_corrupto(client):
    res = _post_zip(client, io.BytesIO(b"esto no es un zip valido"))
    assert res.status_code == 400
    assert "error" in res.get_json()
