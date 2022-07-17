# Тестовое задание Онлайн-школа Тетрика
## Python 3.10

cd testtask_Tetrika && pipenv install && pipenv shell <br/>
OR <br/>
cd testtask_Tetrika && python3.10 -m venv venv && source venv/bin/activate && pip install -r requirements.txt <br/>

## /task_1
### Задача №1.
Дан массив чисел, состоящий из некоторого количества подряд идущих единиц, 
за которыми следует какое-то количество подряд идущих нулей: 
111111111111111111111111100000000.

Найти индекс первого нуля (то есть найти такое место, 
где заканчиваются единицы, и начинаются нули).

### Решение:
Несколько примеров решения и timeit для выбора более эфективного.
Лучше всего решать такие задачи через метод строки find().

> python3.10 -m task_1/main.py


## /task_2
### Задача №2.
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

### Решение:
С помощью библиотеки requests получаем последовательно списки страниц в категории
Животные по алфавиту от api ru.wikipedia.org. Чистим полученные данные, чтобы получить
название животного в одно слово без прилагательных, фамилий и т.п. Список животных 
записываем в файл (как пример) для дальнейшего использования. Считаем количество 
животных на каждую букву алфавита и выводим на печать.

> python3.10 -m task_2/main.py

## /task_3
### Задача №3.
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

### Решение:
Создаем два класса для работы с целочисленным интервалом (Interval) и списком целочисленных
интервалов (IntervalsList). Классы и их методы описаны в документации. Находим пересечение 
интервалов и выводим общую длину пересечения.

> python3.10 -m task_3/main.py