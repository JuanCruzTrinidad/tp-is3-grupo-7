import re
import string

import nltk
from nltk.corpus import stopwords

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
