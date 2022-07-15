""" Содержит классы для работы с интервалами.

    Classes:
        Interval: используется для создания и работы с целочисленным интервалом (start: int, end: int)
"""
from __future__ import annotations


class Interval(object):
    """Класс Interval используется для создания и работы с целочисленным интервалом (start: int, end: int).

    Основное применение - обработка целочисленных интервалов, например timestamp начала и конца какого либо действия.

    Note:
        Содержит собственные методы для операций >, <, ==, !=, len(), str().

    Args:
        start (int): начало интервала;
        end (int): конец интервала.

    Raises:
        ValueError: Переданы некорректные значения начала и конца интервала при создании экземпляра класса;
        TypeError: Выполнение операций >, <, ==, != и методов с экземпляром другого типа.

    Methods:
        intersection(interval_1: Interval, interval_2: Interval) -> Interval: Находит пересечение двух интервалов ввиде нового интервала или возвращает None. 
    """

    __slots__ = ['start', 'end', ]

    def __init__(self, start: int, end: int) -> None:
        """ Создает экземпляр класса Interval.

        Args:
            start (int): начало интервала;
            end (int): конец интервала.

        Raises:
            ValueError: Переданы некорректные значения начала и конца интервала (not int or end < start).
        """
        if end < start or not isinstance(start, int) or not isinstance(end, int):
            raise ValueError(
                f'Переданы некорректные значения начала и конца интервала: Interval(start={start}, end={end}).')
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        return f'Interval(start={self.start}, end={self.end})'

    def __str__(self) -> str:
        return f'(start={self.start}, end={self.end})'

    def __gt__(self, other: object) -> bool:
        """ Находится ли интервал правее (условно больше) указаного. """
        if not isinstance(other, Interval):
            return NotImplemented
        if self.start > other.end and self.end > other.end:
            return True
        return False

    def __lt__(self, other: object) -> bool:
        """ Находится ли интервал левее (условно меньше) указаного. """
        if not isinstance(other, Interval):
            return NotImplemented
        if self.start < other.start and self.end < other.start:
            return True
        return False

    def __eq__(self, other: object) -> bool:
        """ Проверяет совпадает ли начало и конец двух интервалов. """
        if not isinstance(other, Interval):
            return NotImplemented
        if self.start == other.start or self.end == other.end:
            return True
        return False

    def __ne__(self, other: object) -> bool:
        """ Проверяет не совпадает ли начало или конец двух интервалов. """
        if not isinstance(other, Interval):
            return NotImplemented
        if self.start != other.start or self.end != other.end:
            return True
        return False

    def __len__(self) -> int:
        """ Возвращает длину интервала. """
        return self.end - self.start

    @staticmethod
    def intersection(interval_1: Interval, interval_2: Interval) -> Interval | None:
        """ Находит пересечение двух интервалов ввиде нового интервала или возвращает None.

        Args:
            interval_1 (Interval): экземляр класса Interval;
            interval_2 (Interval): экземляр класса Interval.

        Raises:
            TypeError: возникает в случае если одно из переданых значений не является экземпляром класса Interval.

        Returns:
            Interval: если пересечение интервалов существует;
            None: если пересечения интервалов нет.
        """
        if not isinstance(interval_1, Interval) or not isinstance(interval_2, Interval):
            raise TypeError(
                f'Допускается поиск пересечения интервалов между собой.')
        if interval_1 < interval_2 or interval_1 > interval_2:
            return None
        else:
            return Interval(max(interval_1.start, interval_2.start), min(interval_1.end, interval_2.end))
