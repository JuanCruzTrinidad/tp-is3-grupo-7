from collections import Counter

import emoji


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
