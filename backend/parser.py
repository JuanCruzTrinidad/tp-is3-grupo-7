import os
import re
from collections import Counter
from datetime import datetime

import emoji
from dateutil import parser as dateutil_parser

# Patrón que identifica el inicio de una línea con timestamp de WhatsApp.
# Cubre formatos con y sin cero inicial: "8/11/2018" y "08/11/2018".
_TIMESTAMP_RE = re.compile(
    r"^(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2})\s-\s(.+?):\s(.*)$"
)
_SYSTEM_LINE_RE = re.compile(
    r"^\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s"
)


def load_file(filepath: str) -> str:
    """
    Carga el contenido de un archivo de chat de WhatsApp desde disco.

    Intenta leer con UTF-8 primero. Si falla por caracteres inválidos,
    reintenta con latin-1 para cubrir exports de dispositivos Android
    que no usan UTF-8 estándar.

    Parámetros:
        filepath (str): Ruta al archivo .txt exportado desde WhatsApp.

    Retorna:
        str: Contenido completo del archivo como texto plano.

    Lanza:
        FileNotFoundError: Si el archivo no existe en la ruta indicada.
        ValueError: Si la extensión del archivo no es .txt.
    """
    if not filepath.lower().endswith(".txt"):
        raise ValueError(f"El archivo debe tener extensión .txt: {filepath}")

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No se encontró el archivo: {filepath}")

    try:
        with open(filepath, encoding="utf-8-sig") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(filepath, encoding="latin-1") as f:
            return f.read()


def parse_lines(raw_text: str) -> list[dict]:
    """
    Divide el texto crudo del chat en una lista de mensajes estructurados.

    Cada mensaje se representa como un diccionario con las claves:
        - "timestamp": str  — fecha y hora (ej: "14/10/2018, 19:51")
        - "sender":    str  — nombre del remitente
        - "message":   str  — contenido del mensaje

    Los mensajes multilínea se unen en un único campo "message".
    Las líneas del sistema (cifrado, cambios de grupo, etc.) se omiten.

    Parámetros:
        raw_text (str): Texto completo retornado por load_file().

    Retorna:
        list[dict]: Lista de mensajes en orden cronológico.
    """
    messages = []
    current = None

    for line in raw_text.splitlines():
        match = _TIMESTAMP_RE.match(line)
        if match:
            if current:
                messages.append(current)
            timestamp, sender, message = match.groups()
            current = {
                "timestamp": timestamp.strip(),
                "sender": sender.strip(),
                "message": message.strip(),
            }
        elif _SYSTEM_LINE_RE.match(line):
            # Línea del sistema sin remitente — descartar
            if current:
                messages.append(current)
            current = None
        elif current is not None:
            # Continuación de un mensaje multilínea
            current["message"] += "\n" + line

    if current:
        messages.append(current)

    return messages


def get_participants(messages: list[dict]) -> list[str]:
    """
    Extrae la lista de participantes únicos del chat.

    Recorre los mensajes ya parseados por parse_lines() y recolecta todos
    los remitentes distintos, manteniendo el orden de primera aparición.

    Parámetros:
        messages (list[dict]): Lista de mensajes retornada por parse_lines().

    Retorna:
        list[str]: Lista de nombres de participantes sin duplicados,
                   en orden de primera aparición en el chat.
    """
    seen = set()
    participants = []
    for msg in messages:
        sender = msg["sender"]
        if sender not in seen:
            seen.add(sender)
            participants.append(sender)
    return participants


def count_emojis(messages: list[dict]) -> dict[str, int]:
    """
    Identifica y cuenta los emojis presentes en todos los mensajes del chat.

    Recorre el campo "message" de cada entrada y extrae los emojis usando
    la librería emoji. Retorna un diccionario ordenado de mayor a menor
    frecuencia.

    Parámetros:
        messages (list[dict]): Lista de mensajes retornada por parse_lines().

    Retorna:
        dict[str, int]: Diccionario {emoji: cantidad}, ordenado por frecuencia
                        descendente.
    """
    counter: Counter = Counter()
    for msg in messages:
        for token in emoji.analyze(msg["message"]):
            counter[token.chars] += 1
    return dict(counter.most_common())


def parse_timestamp(timestamp_str: str) -> datetime:
    """
    Convierte un string de timestamp de WhatsApp a un objeto datetime.

    El formato esperado es el generado por WhatsApp en Argentina:
    "DD/MM/YYYY, HH:MM", con día y mes que pueden tener uno o dos dígitos
    (ej: "8/11/2018, 9:51" o "14/10/2018, 19:51").

    Parámetros:
        timestamp_str (str): String de timestamp extraído por parse_lines().

    Retorna:
        datetime: Objeto datetime con la fecha y hora del mensaje.

    Lanza:
        ValueError: Si el string no puede interpretarse como fecha válida.
    """
    return dateutil_parser.parse(timestamp_str, dayfirst=True)


def validate_format(raw_text: str) -> bool:
    """
    Verifica que el texto corresponde al formato de exportación de WhatsApp.

    Considera válido el archivo si al menos 5 líneas presentan el patrón
    de timestamp de WhatsApp. Usar un umbral mayor a 1 evita falsos positivos
    con archivos de texto que tengan fechas por coincidencia.

    Parámetros:
        raw_text (str): Texto a validar, normalmente retornado por load_file().

    Retorna:
        bool: True si el formato es reconocible como export de WhatsApp.
    """
    if not raw_text or not raw_text.strip():
        return False

    matches = sum(
        1 for line in raw_text.splitlines()
        if _SYSTEM_LINE_RE.match(line)
    )
    return matches >= 5
