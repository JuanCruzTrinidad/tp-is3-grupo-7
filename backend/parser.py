import os
import re

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
