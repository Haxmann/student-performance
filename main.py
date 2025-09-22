"""Main module"""
import argparse
import os
import csv
from tabulate import tabulate

parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter,
                                 prog = "studperf",
                                 usage='%(prog)s [-fr]',
                                 description = "Student Performance Report Tool")
parser.add_argument("-f", "--files", action='extend', nargs="+", type=str, help = """\
A file containing grade data, or a folder containing such file(s) (non-recursive).\n
Valid examples:
%(prog)s -f file1.csv -f /folder/file2.csv file3.csv
%(prog)s -f /folder/ file4.csv\n
""")
parser.add_argument("-r", "--report", type=str, default='./report.csv', help = "Full path to report file. (default: ./report.csv)")
args = parser.parse_args()

assert args.files, "A valid path to file or folder must be provided"
paths = {'files': [], 'folders': []}

for path in args.files:
    assert os.path.exists(path), "A valid path to file or folder must be provided"

    if os.path.isdir(path):
        paths['folders'] += [path]

    else:
        paths['files'] += [path]

files = paths['files'] + [os.path.join(dirname, filename) for dirname in paths['folders']
                          for filename in os.listdir(dirname) if filename.endswith('.csv')]

if files:
    students = {}

    for file in files:
        with open(file, mode='r', encoding='utf8') as csv_file:
            input_table = csv.DictReader(csv_file)

            for line in input_table:
                student = line['student_name']

                if student not in students:
                    students[student] = [int(line['grade'])]

                else:
                    students[student] += [int(line['grade'])]

results = [[student, round(sum(grades) / len(grades), 2)] for student, grades in students.items()]
results = sorted(results, key = lambda x: (x[1]), reverse=True)

with open(args.report, 'w', newline='') as reportfile:
    headers = ['student_name', 'grade']
    output_table = csv.DictWriter(reportfile, fieldnames=headers)
    output_table.writeheader()
    output_table.writerows([{'student_name': student, 'grade': grade} for student, grade in results])

    print(tabulate(results, headers=headers, tablefmt='grid', showindex=range(1, len(results) + 1)))
