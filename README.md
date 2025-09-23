# Student Performance Report Tool
Тестовое задание для трудоустройства в Workmate

## Инструмент для составления отчетов об успеваемости учащихся

Этот скрипт обрабатывает CSV-файлы с оценками учащихся и генерирует единый отчет со средними оценками для каждого учащегося, отсортированный по убыванию успеваемости. Он поддерживает несколько файлов и выводит их в консоль (табулирует таблицу) и CSV.

## Примеры использования
Запуск с файлами:
python studperf.py -f test_file1.csv -f test_file2.csv -r вывод/report.csv
Вывод текста: консольная таблица + report.csv.

Пример вывода:

![output-example](https://raw.githubusercontent.com/Haxmann/student-performance/master/.github/images/output_example.png)
