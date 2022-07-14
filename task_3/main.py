"""
Задача №3.
Когда пользователь заходит на страницу урока, мы сохраняем время его захода. 
Когда пользователь выходит с урока (или закрывает вкладку, браузер – 
в общем как-то разрывает соединение с сервером), мы фиксируем время выхода с урока. 
Время присутствия каждого пользователя на уроке хранится у нас в виде интервалов. 
В функцию передается словарь, содержащий три списка с таймстемпами (время в секундах):

lesson – начало и конец урока
pupil – интервалы присутствия ученика
tutor – интервалы присутствия учителя

Интервалы устроены следующим образом – это всегда список из четного количества элементов. 
Под четными индексами (начиная с 0) время входа на урок, под нечетными - время выхода с урока.
Нужно написать функцию, которая получает на вход словарь с интервалами и 
возвращает время общего присутствия ученика и учителя на уроке (в секундах).
"""
from interval import Interval


def _fix_person_start_interval(lesson: Interval, person: list[Interval]) -> list[Interval]:
    if person[0].start < lesson.start and person[0].end > lesson.start:
        person[0].start = lesson.start
        return person
    elif person[0].start < lesson.start and person[0].end < lesson.start:
        person = person[1:]
        return _fix_person_start_interval(lesson, person)
    return person


def _fix_person_end_interval(lesson: Interval, person: list[Interval]) -> list[Interval]:
    if person[-1].end > lesson.end and person[-1].start < lesson.end:
        person[-1].end = lesson.end
        return person
    elif person[-1].end > lesson.end and person[-1].start > lesson.end:
        person = person[:-1]
        return _fix_person_end_interval(lesson, person)
    return person


def _fix_person_start_end_interval(lesson: Interval, person: list[Interval]) -> list[Interval]:
    person: list = _fix_person_start_interval(lesson, person)
    person: list = _fix_person_end_interval(lesson, person)
    return person


def _intersection(student: list[Interval], teacher: list[Interval]) -> list[int]:
    intervals, intersections = [], []
    for s in student:
        for t in teacher:
            intervals.append(Interval.intersection(s, t))
    for interval in intervals:
        intersections.append(len(interval)) if interval is not None else 0
    return intersections


def appearance(intervals: dict) -> int:
    lesson: Interval = Interval(*intervals.get('lesson', []))
    student: list[Interval] = Interval.build_intervals_list_from_list(
        intervals.get('pupil', []))
    teacher: list[Interval] = Interval.build_intervals_list_from_list(
        intervals.get('tutor', []))

    student: list[Interval] = Interval.validate_intervals_list(student)
    student: list[Interval] = _fix_person_start_end_interval(lesson, student)

    teacher: list[Interval] = _fix_person_start_end_interval(lesson, teacher)
    return sum(_intersection(student, teacher))


if __name__ == '__main__':
    tests = [{'data': {'lesson': [1594663200, 1594666800],
                       'pupil': [1594663340, 1594663389,
                                 1594663390, 1594663395,
                                 1594663396, 1594666472],
                       'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
              'answer': 3117
              },
             {'data': {'lesson': [1594692000, 1594695600],
                       'pupil': [1594692033, 1594696347],
                       'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
              'answer': 3565
              },
             # пересекаются интервалы у студента
             {'data': {'lesson': [1594702800, 1594706400],
                       'pupil': [1594702789, 1594704500,
                                 1594702807, 1594704542,
                                 1594704512, 1594704513,
                                 1594704564, 1594705150,
                                 1594704581, 1594704582,
                                 1594704734, 1594705009,
                                 1594705095, 1594705096,
                                 1594705106, 1594706480,
                                 1594705158, 1594705773,
                                 1594705849, 1594706480,
                                 1594706500, 1594706875,
                                 1594706502, 1594706503,
                                 1594706524, 1594706524,
                                 1594706579, 1594706641],
                       'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
              'answer': 3577
              }, ]

    for i, test in enumerate(tests):
        test_answer = appearance(test['data'])

        assert test_answer == test['answer'],\
            f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'

'''

'''
