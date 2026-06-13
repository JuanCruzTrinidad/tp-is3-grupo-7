import os
import sys

import pytest

# Los módulos del backend usan imports planos (ej: "from parser import parse_lines"),
# por lo que agregamos esta carpeta al sys.path para que los tests puedan importarlos.
sys.path.insert(0, os.path.dirname(__file__))

from parser import parse_lines  # noqa: E402

# Chat de ejemplo con el formato real de un export de WhatsApp.
#   - Juan y María: 2 mensajes cada uno; Pedro: 1 mensaje
#   - Fechas: 8/11/2018 (jueves) y 9/11/2018 (viernes)
#   - Emojis: 👋 (1 vez) y 😀 (2 veces)
SAMPLE_CHAT = """\
8/11/2018, 19:51 - Juan: Hola a todos 👋
8/11/2018, 19:52 - María: Buenas! 😀
8/11/2018, 20:05 - Juan: Cómo andan?
9/11/2018, 09:10 - Pedro: Todo bien 😀
9/11/2018, 09:11 - María: Genial
"""


@pytest.fixture
def sample_chat():
    """Texto crudo del chat de ejemplo, tal como saldría de load_file()."""
    return SAMPLE_CHAT


@pytest.fixture
def sample_messages():
    """Mensajes ya parseados del chat de ejemplo."""
    return parse_lines(SAMPLE_CHAT)
