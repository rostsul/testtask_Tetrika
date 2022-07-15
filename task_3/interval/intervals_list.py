''' Содержит классы для работы со списками интервалов.

    Classes:
        IntervalsList: используется для создания и работы со списком целочисленных интервалов (intervals: list[Interval]).
'''
from __future__ import annotations

from .interval import Interval


class IntervalsList(object):
    """ Класс IntervalsList используется для обработки списков интервалов.

    Основное применение - хранение и обработка списка интервалов.

    Args:
        intervals_list: хранит список целочисленных интервалов.

    Raises:
        ValueError: при создании экземляра класса передан список list[int] из нечетного кол-ва элементов.

    Methods:
        _build_intervals_list_from_int_list(self, points: list[int]) -> list[Interval]: Создаем список интервалов из целочисленного четного списка list[int] -> list[Interval];
        validate_intervals_list(self) -> None: Проверяет список интервалов на наличие пересекающих интервалов;
        align_start_intervals_list_by_interval(self, interval: Interval) -> None: Отбрасывает интервалы или выравнивает интервал в начале списка интервалов по указаному интервалу;
        align_end_intervals_list_by_interval(self, interval: Interval) -> None: Отбрасывает интервалы или выравнивает интервал в конце списка интервалов по указаному интервалу;
        align_intervals_list_by_interval(self, interval: Interval) -> None: Отбрасывает интервалы или выравнивает интервалы в начале и конце списка интервалов по указаному интервалу;
        intersection(self, other: IntervalsList) -> None: Находит пересечение текущего экземляра IntervalsList с другим экземляром IntervalsList;
        len_intervals(self) -> list[int]: Возвращает список с длиной каждого интервала в IntervalsList;
        sum_intervals(self) -> int: Возвращает общую длинну интервалов в IntervalsList (их сумму).
    """

    __slots__ = ['intervals_list', ]

    def __init__(self, intervals: list[int], validate: bool = True) -> None:
        """ Создает экземпляр класса IntervalsList из целочисленного четного списка list[int].

        Args:
            intervals (list[int]): целочисленный четный список list[int] интервалов упорядоченный по парам;
            validate (bool): проверяет список интервалов после создания на наличие пересекающих интервалов. Defaults to True.
        """
        self.intervals_list: list[Interval] = self._build_intervals_list_from_int_list(
            intervals)
        if validate:
            self.validate_intervals_list()

    def _build_intervals_list_from_int_list(self, points: list[int]) -> list[Interval]:
        """ Создаем список интервалов из целочисленного четного списка list[int] -> list[Interval].

        Args:
            points (list[int]): список целочисленных значений int, обязательно должен содержать четное кол-во элементов.

        Raises:
            ValueError: передан список из нечетного кол-ва элементов. 

        Returns:
            list[Interval]: список интервалов созданный из списка целочисленных значений типа int.
        """
        if len(points) % 2 != 0:
            raise ValueError(
                'Кол-во элементов в передаваемом списке должно быть четным.')
        intervals: list[Interval] = []
        while points:
            intervals.append(Interval(start=points.pop(0), end=points.pop(0)))
        return intervals

    def validate_intervals_list(self) -> None:
        """ Проверяет список интервалов на наличие пересекающих интервалов. """
        clear_intervals, i, validate = [], 0, True
        while validate and self.intervals_list:
            i, validate = 0, False
            while i < len(self.intervals_list):
                if i + 1 >= len(self.intervals_list):
                    clear_intervals.append(self.intervals_list[i])
                    break
                if not self.intervals_list[i] < self.intervals_list[i+1] and\
                        not self.intervals_list[i] > self.intervals_list[i+1] and\
                        self.intervals_list[i] != self.intervals_list[i+1]:
                    interval = Interval(min(self.intervals_list[i].start, self.intervals_list[i+1].start),
                                        max(self.intervals_list[i].end, self.intervals_list[i+1].end))
                    clear_intervals.append(interval)
                    i += 2
                    validate = True
                else:
                    clear_intervals.append(self.intervals_list[i])
                    i += 1
            self.intervals_list.clear()
            self.intervals_list = clear_intervals[:]
            clear_intervals.clear()

    def align_start_intervals_list_by_interval(self, interval: Interval) -> None:
        """ Отбрасывает интервалы или выравнивает интервал в начале списка интервалов по указаному интервалу. """
        while self.intervals_list:
            if self.intervals_list[0] < interval:
                self.intervals_list.pop(0)
            elif self.intervals_list[0].start < interval.start and self.intervals_list[0].end > interval.start:
                self.intervals_list[0].start = interval.start
                break
            else:
                break

    def align_end_intervals_list_by_interval(self, interval: Interval) -> None:
        """ Отбрасывает интервалы или выравнивает интервал в конце списка интервалов по указаному интервалу. """
        while self.intervals_list:
            if self.intervals_list[-1] > interval:
                self.intervals_list.pop()
            elif self.intervals_list[-1].end > interval.end and self.intervals_list[-1].start < interval.end:
                self.intervals_list[-1].end = interval.end
                break
            else:
                break

    def align_intervals_list_by_interval(self, interval: Interval) -> None:
        """ Отбрасывает интервалы или выравнивает интервалы в начале и конце списка интервалов по указаному интервалу. """
        self.align_start_intervals_list_by_interval(interval)
        self.align_end_intervals_list_by_interval(interval)

    def intersection(self, other: IntervalsList) -> None:
        """ Находит пересечение текущего экземляра IntervalsList с другим экземляром IntervalsList.

        Args:
            other (IntervalsList): экземляр IntervalsList с которым нужно выполнить пересечение. 
        """
        result: list[Interval | None] = []
        for s in self.intervals_list:
            for t in other.intervals_list:
                result.append(Interval.intersection(s, t))
        self.intervals_list = [
            interval for interval in result if interval is not None]

    def len_intervals(self) -> list[int]:
        """ Возвращает список с длиной каждого интервала в IntervalsList. """
        len_intervals: list[int] = []
        for interval in self.intervals_list:
            len_intervals.append(len(interval))
        return len_intervals

    def sum_intervals(self) -> int:
        """ Возвращает общую длинну интервалов в IntervalsList (их сумму). """
        return sum(self.len_intervals())
