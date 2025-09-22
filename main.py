"""Main module"""
import os
import csv
from tabulate import tabulate

FOLDER = "./examples"

if os.path.exists(FOLDER):
    files = os.listdir(FOLDER)
    if files:
        students = {}

        for file in files:
            with open(f'{FOLDER}/{file}', mode='r', encoding='utf8') as csv_file:
                table = csv.DictReader(csv_file)

                for line in table:
                    student = line['student_name']

                    if student not in students:
                        students[student] = [int(line['grade'])]

                    else:
                        students[student] += [int(line['grade'])]

results = [[student, round(sum(grades) / len(grades), 1)] for student, grades in students.items()]
results = sorted(results, key = lambda x: (x[1]), reverse=True)
print(tabulate(results, headers=['student_name', 'grade'], tablefmt='grid', showindex=True))
