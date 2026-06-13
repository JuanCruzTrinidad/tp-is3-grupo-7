"""Pruebas unitarias de las funciones de parser.py."""

import pytest

from parser import (
    count_emojis,
    get_participants,
    load_file,
    parse_lines,
    parse_timestamp,
    validate_format,
)


# --- parse_lines ---------------------------------------------------------

def test_parse_lines_extrae_campos(sample_chat):
    messages = parse_lines(sample_chat)
    assert len(messages) == 5
    assert messages[0] == {
        "timestamp": "8/11/2018, 19:51",
        "sender": "Juan",
        "message": "Hola a todos 👋",
    }


def test_parse_lines_une_mensajes_multilinea():
    chat = "8/11/2018, 19:51 - Juan: primera\nsegunda linea\ntercera"
    messages = parse_lines(chat)
    assert len(messages) == 1
    assert messages[0]["message"] == "primera\nsegunda linea\ntercera"


def test_parse_lines_omite_lineas_de_sistema():
    chat = (
        "8/11/2018, 19:50 - Los mensajes están cifrados de extremo a extremo.\n"
        "8/11/2018, 19:51 - Juan: Hola\n"
    )
    messages = parse_lines(chat)
    assert len(messages) == 1
    assert messages[0]["sender"] == "Juan"


def test_parse_lines_texto_vacio_devuelve_lista_vacia():
    assert parse_lines("") == []


# --- get_participants ----------------------------------------------------

def test_get_participants_unicos_y_en_orden(sample_messages):
    assert get_participants(sample_messages) == ["Juan", "María", "Pedro"]


# --- parse_timestamp -----------------------------------------------------

def test_parse_timestamp_interpreta_dia_primero():
    dt = parse_timestamp("8/11/2018, 19:51")
    assert (dt.year, dt.month, dt.day) == (2018, 11, 8)
    assert (dt.hour, dt.minute) == (19, 51)


def test_parse_timestamp_formato_invalido_lanza():
    with pytest.raises(ValueError):
        parse_timestamp("no es una fecha")


# --- count_emojis --------------------------------------------------------

def test_count_emojis_cuenta_y_ordena_por_frecuencia(sample_messages):
    emojis = count_emojis(sample_messages)
    assert emojis["😀"] == 2
    assert emojis["👋"] == 1
    # El más frecuente debe quedar primero en el dict ordenado.
    assert list(emojis.keys())[0] == "😀"


def test_count_emojis_sin_emojis_devuelve_vacio():
    messages = parse_lines("8/11/2018, 19:51 - Juan: hola sin emojis")
    assert count_emojis(messages) == {}


# --- validate_format -----------------------------------------------------

def test_validate_format_reconoce_export(sample_chat):
    assert validate_format(sample_chat) is True


def test_validate_format_rechaza_texto_plano():
    assert validate_format("esto no es un chat\nsolo texto suelto") is False


def test_validate_format_rechaza_vacio():
    assert validate_format("") is False
    assert validate_format("   \n  ") is False


# --- load_file -----------------------------------------------------------

def test_load_file_rechaza_extension_invalida():
    with pytest.raises(ValueError):
        load_file("chat.zip")


def test_load_file_archivo_inexistente():
    with pytest.raises(FileNotFoundError):
        load_file("no_existe_abc123.txt")


def test_load_file_lee_contenido(tmp_path):
    archivo = tmp_path / "chat.txt"
    archivo.write_text("contenido de prueba", encoding="utf-8")
    assert load_file(str(archivo)) == "contenido de prueba"
