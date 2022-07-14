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
"""
from collections import Counter

import requests
from requests.exceptions import HTTPError


def print_animal_by_letter_count():
    count = animals_by_letter_count()
    for key, value in count.items():
        print(f'{key}: {value}')
    exit(0)


def animals_by_letter_count() -> Counter:
    count = Counter()
    animals = _animals_from_ruwiki()
    for animal in animals:
        animal_name: str = animal.get('title', '_')
        count[animal_name[0].upper()] += 1
    return count


def _animals_from_ruwiki() -> list:
    animals: list = []

    def _read_page(animals: list, next_page: str = None):
        page = animals_page_from_ruwiki(next_page)
        next_page = page.get('continue', {}).get('cmcontinue', None)
        new_animals = [*animals,
                       *page.get('query', {}).get('categorymembers', []), ]
        if next_page is not None:
            return new_animals + _read_page(animals, next_page)
        else:
            return new_animals

    return _read_page(animals)


def animals_page_from_ruwiki(cmcontinue: str = None) -> dict:
    action = 'query'
    url_args = {'list': 'categorymembers',
                'cmtitle': 'Category:Животные_по_алфавиту',
                'cmtype': 'page',
                'cmlimit': 200, }
    if cmcontinue is not None:
        url_args['cmcontinue'] = cmcontinue
    url_args['format'] = 'json'
    response: dict = request_data_from_ruwiki(action, **url_args)
    return response


def request_data_from_ruwiki(action: str, **kwargs) -> dict:
    """  """
    url = [f'https://ru.wikipedia.org/w/api.php?action={action}', ]
    for key, value in kwargs.items():
        url.append(f'&{key}={value}')
    response = _request_json(''.join(url))
    if response.get('error', None) is not None:
        print(response.get('error'))
        exit(1)
    return response


def _request_json(url: str) -> dict:
    """  """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return {'error': http_err}

    except Exception as err:
        print(f'Other error occurred: {err}')
        return {'error': {err}}


if __name__ == '__main__':
    print_animal_by_letter_count()
