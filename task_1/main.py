"""
Задача №1.
Дан массив чисел, состоящий из некоторого количества подряд идущих единиц, 
за которыми следует какое-то количество подряд идущих нулей: 
111111111111111111111111100000000.

Найти индекс первого нуля (то есть найти такое место, 
где заканчиваются единицы, и начинаются нули).

Решение:
Несколько примеров решения и timeit для выбора более эфективного.
Лучше всего решать такие задачи через метод строки find().
"""
import timeit


def example_1(array: str) -> int:
    return array.index('0')


def example_2(array: str) -> int:
    return len(bin(int(array[::-1], 2))) - 2


def example_3(array: str) -> int:
    return array.count('1')


def example_4(array: str) -> int:
    return array.find('0')


def example_5(array: str) -> int:
    return sum([int(a) for a in array.split()])


test_example_1 = """
def example_1(array = '111111111110000000000000000'):    
    return array.index('0')
"""

test_example_2 = """
def example_2(array = '111111111110000000000000000'):
    return len(bin(int(array[::-1], 2))) - 2
"""

test_example_3 = """
def example_3(array = '111111111110000000000000000'):
    return array.count('1')
"""

test_example_4 = """
def example_4(array = '111111111110000000000000000'):
    return array.find('0')
"""

test_example_5 = """
def example_5(array = '111111111110000000000000000'):
    return sum([int(a) for a in array.split()])
"""


if __name__ == '__main__':
    array = '111111111110000000000000000'

    print('Example 1: Через метод str index() - ', example_1(array))
    print('Timeit:', timeit.timeit(stmt=test_example_1, number=10000), end='\n'*2)

    print('Example 2: Через разворот строки и приведение к битам - ', example_2(array))
    print('Timeit:', timeit.timeit(stmt=test_example_2, number=10000), end='\n'*2)

    print('Example 3: Через метод str count() - ', example_3(array))
    print('Timeit:', timeit.timeit(stmt=test_example_3, number=10000), end='\n'*2)

    print('Example 4: Через метод str find() - ', example_3(array))
    print('Timeit:', timeit.timeit(stmt=test_example_4, number=10000), end='\n'*2)

    print('Example 5: Через распаковку и сумму элементов списка - ', example_3(array))
    print('Timeit:', timeit.timeit(stmt=test_example_5, number=10000), end='\n'*2)
