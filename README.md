# Student Performance Report Tool
Тестовое задание для трудоустройства в Workmate

## Инструмент для составления отчетов об успеваемости учащихся

Скрипт обрабатывает CSV-файлы с данными об успеваемости студентов и создает отчеты. Поддерживает отчеты по студентам, преподавателям (WIP) и предметам (WIP), выводит результаты в консоль в виде таблицы. Архитектура позволяет легко добавлять новые типы отчетов.

## Примеры использования
Пример запуска:
`python studperf.py --files test_file1.csv test_file2.csv --report student-performance`

Пример вывода:

![output-example](https://raw.githubusercontent.com/Haxmann/student-performance/master/.github/images/example.png)


Результаты покрытия тестами:

[![codecov](https://codecov.io/github/Haxmann/student_performance/graph/badge.svg?token=O4NQ3F7XPK)](https://codecov.io/github/Haxmann/student_performance)