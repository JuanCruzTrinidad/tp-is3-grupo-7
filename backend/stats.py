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
