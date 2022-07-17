"""
Задача №2.
В нашей школе мы не можем разглашать персональные данные пользователей, 
но чтобы преподаватель и ученик смогли объяснить нашей поддержке, 
кого они имеют в виду (у преподавателей, например, часто учится несколько Саш),
мы генерируем пользователям уникальные и легко произносимые имена. 
Имя у нас состоит из прилагательного, имени животного и двузначной цифры. 
В итоге получается, например, "Перламутровый лосось 77". Для генерации 
таких имен мы и решали следующую задачу:

Получить с русской википедии список всех животных (https://inlnk.ru/jElywR) 
и вывести количество животных на каждую букву алфавита. 

Результат должен получиться в следующем виде:
А: 642
Б: 412
В: ...
...

Решение:
С помощью библиотеки requests получаем последовательно списки страниц в категории
Животные по алфавиту от api ru.wikipedia.org. Чистим полученные данные, чтобы получить
название животного в одно слово без прилагательных, фамилий и т.п. Список животных 
записываем в файл (как пример) для дальнейшего использования. Считаем количество 
животных на каждую букву алфавита и выводим на печать.
"""
import os
import re
import locale
from collections import Counter

import requests
from requests.exceptions import HTTPError


def print_animals_by_letter_count():
    """ Выводит количество животных на каждую букву алфавита. """
    count = count_animals_by_first_letter()
    for key, value in count.items():
        print(f'{key.upper()}: {value}')


def count_animals_by_first_letter() -> Counter:
    """ Читает список животных из файла и считает количество животных 
    на каждую букву алфавита. """
    count: Counter = Counter()
    with open(f'{os.getcwd()}/task_2/animals.list.txt', 'r', encoding='utf-8') as file:
        animals: list[str] = [animal for animal in file]
    for animal in animals:
        count[animal[0]] += 1
    return count


def write_animals_to_file() -> None:
    """ Получаем, чистим, сортируем и записываем список животных в файл. """
    animals: list[str] = [animal.get('title', '_')
                          for animal in animals_from_ruwiki()]
    animal_names = _clear_and_sort_animals_name(animals)
    with open(f'{os.getcwd()}/task_2/animals.list.txt', 'w', encoding='utf-8') as file:
        for animal in animal_names:
            # откидываем остаток животных на латинице
            if re.match(r'^[а-яА-ЯёЁ]', animal) is not None:
                file.write(f'{animal}\n')


def _clear_and_sort_animals_name(animals: list[str]) -> list[str]:
    """ Чистит список названий животных избавляясь от прилагательных, фамилий открывателей,
    повторов, страниц видов, родов и т.п., оставляя одно слово или слово через дефис с
    названием животного, сортирует по алфавиту.

    Note:
        В ОС должна быть доступна русская локаль для корректной работы регулярных выражений
        и сортировки по алфавиту.

    TODO:
        Полностью избавиться от названий динозавров.

    Args:
        animals (list[str]): список названий животных.
    Returns:
        animals (list[str]): список названий животных отсортированный по алфавиту.
    """
    locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))
    template = r"[а-яё-]*(и|й|е|ы|я|икс|опс|нис|дон|тек|иль|тор|рус|авр|тис|фал)(\s|$)|^([а-яё-])*\s\((.+)\)$"
    animals_clear: set[str] = set(map(lambda animal: re.sub(
        template, '', animal.lower()), animals))
    # отбрасываем фамилии в названии животного
    animals_clear = set(
        map(lambda animal: animal.strip().split(' ')[0], animals_clear))
    # сортруем названия животных
    animals = sorted(list(animals_clear), key=locale.strxfrm)
    return animals


def animals_from_ruwiki() -> list[dict]:
    """ Загружает страницы из категории животные по алфавиту с ru.wikipedia.org 
    пока есть страницы или не начинаются страницы животных с латинскими названиями.

    Returns:
        list: список страниц из категории животные по алфавиту
    """
    animals: list[dict] = []
    next_page: str | None = None

    while next_page is not None or not animals:
        page: dict = animals_page_from_ruwiki(next_page)
        next_page = page.get('continue', {}).get('cmcontinue', None)
        new_animals: list[dict] = page.get(
            'query', {}).get('categorymembers', [])
        animals.extend(new_animals)
        if re.match(r'^[а-яА-ЯёЁ]', new_animals[-1].get('title', '')) is None:
            break

    return animals


def animals_page_from_ruwiki(cmcontinue: str | None) -> dict:
    """ Формирует набор аргументов для api и загружает первую или указанную 
    в cmcontinue страницу категории Животные_по_алфавиту.

    Note:
        Судя по докуметации api ru.wikipedia.org список всех страниц в 
        категории не получить, следующую страницу мы узнаем из полученной.

    Args:
        cmcontinue (str | None, optional): следующая страница в категории. 
                                           Defaults to None.
    Returns:
        dict: страница с животными по алфавиту.
    """
    action = 'query'  # action api ru.wikipedia.org
    url_args = {'list': 'categorymembers',  # тип возвращаемого списка
                'cmtitle': 'Category:Животные_по_алфавиту',  # категория
                'cmtype': 'page',  # тип элементов в списке, чтобы не захватить подкатегории
                'cmlimit': 100, }  # кол-во элементов в списке, от 10 до 500 согласно документации
    if cmcontinue is not None:
        url_args['cmcontinue'] = cmcontinue  # страница списка
    url_args['format'] = 'json'  # формат ответа (должно быть в таком порядке)
    response: dict = request_data_from_ruwiki(action, **url_args)
    return response


def request_data_from_ruwiki(action: str, **kwargs) -> dict:
    """ Запрашивает данные от api ru.wikipedia.org по указанному action 
    и набору аргументов.

    Обертка для получения данных в формате json от api ru.wikipedia.org.

    Args:
        action (str): обязательный аргумент для api ru.wikipedia.org;
        **kwargs (dict[str, str]): прочие необязательные аргументы api endpoint.
    Raises:
        Exception: в случае если сервер возвращает ошибку или возникает ошибка 
                   при обращении к серверу.
    Returns:
        dict: ответ от указанного api endpoint.
    """
    url = [f'https://ru.wikipedia.org/w/api.php?action={action}', ]
    for key, value in kwargs.items():
        url.append(f'&{key}={value}')
    response = _request_json(''.join(url))
    if response.get('error', None) is not None:
        raise Exception(response.get('error'))
    return response


def _request_json(url: str) -> dict:
    """ Запрашивает json по указанному адрессу api.

    Args:
        url (str): api endpoint.

    Returns:
        dict: ответ api ввиде словаря.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return {'error': http_err}

    except Exception as err:
        print(f'Other error occurred: {err}')
        return {'error': {err}}


if __name__ == '__main__':
    write_animals_to_file()
    print_animals_by_letter_count()
