class Interval(object):

    __slots__ = ['start', 'end', ]

    def __init__(self, start: int, end: int, *args, **kwargs) -> None:
        if end < start:
            raise ValueError(
                f'Переданы некорректные значения начала и конца интервала: Interval(start={start}, end={end}).')
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        return f'Interval(start={self.start}, end={self.end})'

    def __str__(self) -> str:
        return f'(start={self.start}, end={self.end})'

    def __gt__(self, other) -> bool:
        if not isinstance(other, Interval):
            raise TypeError(
                f'Допускается сравнение интервалов между собой.')
        if self.start > other.end and self.end > other.end:
            return True
        return False

    def __lt__(self, other) -> bool:
        if not isinstance(other, Interval):
            raise TypeError(
                f'Допускается сравнение интервалов между собой.')
        if self.start < other.start and self.end < other.start:
            return True
        return False

    def __eq__(self, other) -> bool:
        if not isinstance(other, Interval):
            raise TypeError(
                f'Допускается сравнение интервалов между собой.')
        if self.start == other.start or self.end == other.end:
            return True
        return False

    def __ne__(self, other):
        if not isinstance(other, Interval):
            raise TypeError(
                f'Допускается сравнение интервалов между собой.')
        if self.start != other.start or self.end != other.end:
            return True
        return False

    def __len__(self) -> int:
        return self.end - self.start

    @staticmethod
    def intersection(interval_1, interval_2):
        if not isinstance(interval_1, Interval) and not isinstance(interval_2, Interval):
            raise TypeError(
                f'Допускается поиск пересечения интервалов между собой.')

        if interval_1 < interval_2 or interval_1 > interval_2:
            return None

        if interval_1.start > interval_2.start and interval_1.end < interval_2.end:
            return Interval(interval_1.start, interval_1.end)
        elif interval_1.start < interval_2.start and interval_2.end < interval_1.end:
            return Interval(interval_2.start, interval_2.end)
        elif interval_1.start <= interval_2.start and interval_1.end >= interval_2.start and interval_1.end <= interval_2.end:
            return Interval(interval_2.start, interval_1.end)
        elif interval_1.start >= interval_2.start and interval_1.start <= interval_2.end and interval_1.end >= interval_2.end:
            return Interval(interval_1.start, interval_2.end)

        return None

    @staticmethod
    def build_intervals_list_from_list(points: list) -> list:
        intervals = []
        for _ in range(int(len(points) / 2)):
            try:
                intervals.append(
                    Interval(start=points.pop(0), end=points.pop(0)))
            except ValueError:
                continue
        return intervals

    @staticmethod
    def validate_intervals_list(intervals):
        clear_intervals, i, validate = [], 0, False
        while i < len(intervals):
            if i + 1 >= len(intervals):
                clear_intervals.append(intervals[i])
                break
            if not intervals[i] < intervals[i+1] and not intervals[i] > intervals[i+1] and intervals[i] != intervals[i+1]:
                interval = Interval(min(intervals[i].start, intervals[i+1].start),
                                    max(intervals[i].end, intervals[i+1].end))
                clear_intervals.append(interval)
                i += 2
                validate = True
            else:
                clear_intervals.append(intervals[i])
                i += 1
        if validate:
            return Interval.validate_intervals_list(clear_intervals)
        return clear_intervals
