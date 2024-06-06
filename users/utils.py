from random import choice


def get_letters_numbers() -> list:
    """Создает список символов для пароля"""
    result = list(range(0, 10))
    for number in range(65, 91):
        result.append(chr(number))
    for number in range(97, 123):
        result.append(chr(number))
    return result


def fill_random(random_sequence: list, maximum_size: int) -> str:
    """Создает последовательность рандомных символов [a-zA-Z0-9]"""
    result = ''
    size = 0
    while size != maximum_size:
        symbol = choice(random_sequence)
        result += str(symbol)
        size += 1
    return result


def get_code() -> str:
    """Получить 4-х значный код"""
    return fill_random(list(range(0, 10)), 4)
