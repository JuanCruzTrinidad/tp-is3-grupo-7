from collections import Counter

import emoji

from .parser import parse_timestamp


def messages_by_hour(messages: list[dict]) -> dict[int, int]:
    """
    Agrupa los mensajes según la hora del día en que fueron enviados.

    Extrae la hora de cada timestamp usando parse_timestamp() y acumula
    la cantidad de mensajes por cada franja horaria (0–23). Las horas sin
    mensajes se incluyen con valor 0 para facilitar la visualización.

    Parámetros:
        messages (list[dict]): Lista de mensajes retornada por parse_lines().

    Retorna:
        dict[int, int]: Diccionario {hora: cantidad_de_mensajes} con las
                        24 horas del día ordenadas de 0 a 23.
    """
    counter: Counter = Counter()
    for msg in messages:
        hour = parse_timestamp(msg["timestamp"]).hour
        counter[hour] += 1
    return {hour: counter.get(hour, 0) for hour in range(24)}


def messages_by_date(messages: list[dict]) -> dict[str, int]:
    """
    Agrupa los mensajes según la fecha en que fueron enviados.

    Extrae la fecha de cada timestamp usando parse_timestamp() y acumula
    la cantidad de mensajes por día. Las fechas se representan como strings
    en formato ISO (YYYY-MM-DD) y se ordenan cronológicamente.

    Parámetros:
        messages (list[dict]): Lista de mensajes retornada por parse_lines().

    Retorna:
        dict[str, int]: Diccionario {fecha: cantidad_de_mensajes} ordenado
                        cronológicamente, con fechas en formato YYYY-MM-DD.
    """
    counter: Counter = Counter()
    for msg in messages:
        date = parse_timestamp(msg["timestamp"]).date().isoformat()
        counter[date] += 1
    return dict(sorted(counter.items()))


def peak_hour(messages: list[dict]) -> tuple[int, int]:
    """
    Identifica la franja horaria con mayor cantidad de mensajes en el chat.

    Utiliza messages_by_hour() para obtener la distribución por hora y
    retorna la hora con más actividad junto con su cantidad de mensajes.

    Parámetros:
        messages (list[dict]): Lista de mensajes retornada por parse_lines().

    Retorna:
        tuple[int, int]: Par (hora, cantidad_de_mensajes) de la franja
                         horaria más activa del chat.
    """
    by_hour = messages_by_hour(messages)
    hour = max(by_hour, key=lambda h: by_hour[h])
    return (hour, by_hour[hour])


def count_emojis_per_user(messages: list[dict]) -> dict[str, dict[str, int]]:
    """
    Extrae y cuenta los emojis usados por cada participante del chat.

    Recorre todos los mensajes agrupando los emojis por remitente. Para cada
    participante retorna un diccionario con sus emojis ordenados de mayor a
    menor frecuencia.

    Parámetros:
        messages (list[dict]): Lista de mensajes retornada por parse_lines().

    Retorna:
        dict[str, dict[str, int]]: Diccionario {participante: {emoji: cantidad}},
                                   con los emojis de cada usuario ordenados por
                                   frecuencia descendente.
    """
    counters: dict[str, Counter] = {}
    for msg in messages:
        sender = msg["sender"]
        if sender not in counters:
            counters[sender] = Counter()
        for token in emoji.analyze(msg["message"]):
            counters[sender][token.chars] += 1
    return {sender: dict(counter.most_common()) for sender, counter in counters.items()}


def most_frequent_emoji(messages: list[dict]) -> tuple[str, int] | None:
    """
    Identifica el emoji más frecuente en todo el chat.

    Recorre todos los mensajes, acumula el conteo global de emojis y retorna
    el emoji con mayor cantidad de apariciones junto con su frecuencia.
    Retorna None si el chat no contiene ningún emoji.

    Parámetros:
        messages (list[dict]): Lista de mensajes retornada por parse_lines().

    Retorna:
        tuple[str, int] | None: Par (emoji, cantidad) del más frecuente,
                                o None si no hay emojis en el chat.
    """
    counter: Counter = Counter()
    for msg in messages:
        for token in emoji.analyze(msg["message"]):
            counter[token.chars] += 1
    if not counter:
        return None
    return counter.most_common(1)[0]


def count_messages_per_user(messages: list[dict]) -> dict[str, int]:
    """
    Cuenta la cantidad de mensajes enviados por cada participante del chat.

    Recorre la lista de mensajes y acumula el total de mensajes por remitente,
    retornando el resultado ordenado de mayor a menor cantidad.

    Parámetros:
        messages (list[dict]): Lista de mensajes retornada por parse_lines().

    Retorna:
        dict[str, int]: Diccionario {participante: cantidad_de_mensajes},
                        ordenado por frecuencia descendente.
    """
    counter: Counter = Counter(msg["sender"] for msg in messages)
    return dict(counter.most_common())
