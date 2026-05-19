import os


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
