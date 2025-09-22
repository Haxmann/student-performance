import csv, argparse, tabulate
import os

folder = "./examples"

if os.path.exists(folder):
    files = os.listdir(folder)
    if files:
        students = {}

        for file in files:
            with open(f'{folder}/{file}', mode='r', encoding='utf8') as csv_file:
                table = csv.DictReader(csv_file)

                for line in table:
                    student = line['student_name']

                    if student not in students:
                        students[student] = [int(line['grade'])]
                        
                    else:
                        students[student] += [int(line['grade'])]

results = sorted([[student, round(sum(students[student]) / len(students[student]), 1)] for student in students], key = lambda x: (x[1]), reverse=True)
print(tabulate.tabulate(results, headers=['student_name', 'grade'], tablefmt='grid', showindex=True))