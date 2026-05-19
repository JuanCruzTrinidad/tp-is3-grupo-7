from collections import Counter


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
