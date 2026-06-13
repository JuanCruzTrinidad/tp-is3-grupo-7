"""Pruebas unitarias de las funciones de stats.py."""

from stats import (
    count_emojis_per_user,
    count_messages_per_user,
    messages_by_date,
    messages_by_hour,
    messages_by_weekday,
    most_frequent_emoji,
    peak_hour,
    top_days,
)


# --- count_messages_per_user ---------------------------------------------

def test_count_messages_per_user(sample_messages):
    result = count_messages_per_user(sample_messages)
    assert result == {"Juan": 2, "María": 2, "Pedro": 1}
    # El participante con menos mensajes queda último (orden descendente).
    assert list(result.keys())[-1] == "Pedro"


# --- messages_by_hour ----------------------------------------------------

def test_messages_by_hour_devuelve_24_horas(sample_messages):
    by_hour = messages_by_hour(sample_messages)
    assert len(by_hour) == 24
    assert by_hour[19] == 2  # 19:51 y 19:52
    assert by_hour[20] == 1  # 20:05
    assert by_hour[9] == 2   # 09:10 y 09:11
    assert by_hour[0] == 0   # hora sin mensajes


# --- peak_hour -----------------------------------------------------------

def test_peak_hour_devuelve_franja_mas_activa(sample_messages):
    hour, count = peak_hour(sample_messages)
    assert count == 2
    assert hour in (9, 19)  # ambas franjas tienen 2 mensajes


# --- messages_by_weekday -------------------------------------------------

def test_messages_by_weekday_devuelve_7_dias(sample_messages):
    by_weekday = messages_by_weekday(sample_messages)
    assert len(by_weekday) == 7
    assert by_weekday[3] == 3  # jueves 8/11/2018
    assert by_weekday[4] == 2  # viernes 9/11/2018
    assert by_weekday[0] == 0  # lunes sin mensajes


# --- messages_by_date ----------------------------------------------------

def test_messages_by_date_iso_y_cronologico(sample_messages):
    by_date = messages_by_date(sample_messages)
    assert by_date == {"2018-11-08": 3, "2018-11-09": 2}
    assert list(by_date.keys()) == ["2018-11-08", "2018-11-09"]


# --- top_days ------------------------------------------------------------

def test_top_days_ordenado_descendente(sample_messages):
    assert top_days(sample_messages) == [["2018-11-08", 3], ["2018-11-09", 2]]


def test_top_days_respeta_n(sample_messages):
    assert top_days(sample_messages, n=1) == [["2018-11-08", 3]]


# --- most_frequent_emoji -------------------------------------------------

def test_most_frequent_emoji(sample_messages):
    assert most_frequent_emoji(sample_messages) == ("😀", 2)


def test_most_frequent_emoji_sin_emojis_devuelve_none():
    assert most_frequent_emoji([]) is None


# --- count_emojis_per_user -----------------------------------------------

def test_count_emojis_per_user(sample_messages):
    result = count_emojis_per_user(sample_messages)
    assert result["Juan"] == {"👋": 1}
    assert result["María"] == {"😀": 1}
    assert result["Pedro"] == {"😀": 1}
