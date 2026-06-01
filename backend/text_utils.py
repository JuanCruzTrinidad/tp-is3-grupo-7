import base64
import io
import re
import string

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud

nltk.download("stopwords", quiet=True)

# Tokens propios de WhatsApp que no aportan información
_WHATSAPP_TOKENS = re.compile(
    r"<[^>]+omitido>|<[^>]+omitted>", re.IGNORECASE
)
_URL_RE = re.compile(r"https?://\S+|www\.\S+")


def clean_text(messages: list[dict], lang: str = "spanish") -> str:
    """
    Retorna un string con el texto limpio de todos los mensajes:
    sin URLs, sin tokens de WhatsApp, sin puntuación y sin stop words.

    Parámetros:
        messages (list[dict]): Lista de mensajes de parse_lines().
        lang (str): Idioma para las stop words de nltk. Por defecto "spanish".

    Retorna:
        str: Texto limpio listo para generar word cloud u otros análisis.
    """
    stop_words = set(stopwords.words(lang))
    tokens = []

    for msg in messages:
        text = msg["message"]
        text = _WHATSAPP_TOKENS.sub(" ", text)
        text = _URL_RE.sub(" ", text)
        text = text.translate(str.maketrans("", "", string.punctuation))
        for word in text.lower().split():
            if word and word not in stop_words:
                tokens.append(word)

    return " ".join(tokens)


def generate_wordcloud_base64(messages: list[dict]) -> str:
    """
    Genera una imagen PNG de word cloud a partir de los mensajes y la retorna
    como string base64.

    Parámetros:
        messages (list[dict]): Lista de mensajes de parse_lines().

    Retorna:
        str: Imagen PNG codificada en base64.
    """
    text = clean_text(messages)
    wc = WordCloud(width=800, height=400, background_color="white").generate(text)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)

    return base64.b64encode(buf.getvalue()).decode("utf-8")
