"""Main module"""
import argparse
import os
import csv
import sys
from tabulate import tabulate

parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter,
                                 prog = "studperf",
                                 usage='%(prog)s [-fr]',
                                 description = "Student Performance Report Tool")
parser.add_argument("-f", "--files", action='extend', nargs="+", type=str,
    help = """\
A file containing grade data, or a folder containing such file(s) (non-recursive).\n
Examples:
%(prog)s -f file1.csv -f /folder/file2.csv file3.csv\n
""")
parser.add_argument("-r", "--report", type=str, default='./report.csv',
                     help = "Full path to report file. (default: ./report.csv)")

try:
    args = parser.parse_args()
    if not args.files:
        raise ValueError("At least one file must be provided via --files")

    report_dir = os.path.dirname(args.report) or '.'
    if not os.path.isdir(report_dir):
        raise ValueError(f"Directory for report file {args.report} does not exist")

except ValueError as e:
    parser.error(str(e))

paths = []

for path in args.files:
    if not os.path.exists(path):
        print(f'Warning: Invalid path provided -  "{path}", skipping...')
        continue

    if not str(os.path).endswith('.csv'):
        print(f'Report file "{path}" must have a .csv extension, skipping...')
        continue

    paths.append(path)

if paths:
    students = {}

    for file in paths:
        with open(file, mode='r', encoding='utf8') as csv_file:
            input_table = csv.DictReader(csv_file)

            if not all(field in [input_table.fieldnames] for field in ['student_name', 'grade']):
                print(f"Warning: Skipping {file} - missing 'student_name' or 'grade' columns")
                continue

            for line in input_table:
                student = line['student_name']

                try:
                    grade = float(line['grade'])
                except ValueError:
                    print(f"Warning: Skipping invalid grade in {file} for {student}")
                    continue

                if student not in students:
                    students[student] = [int(line['grade'])]

                else:
                    students[student] += [int(line['grade'])]

else:
    print("Error: No CSV files found in provided paths")
    sys.exit(1)

results = [[student, round(sum(grades) / len(grades), 1)] for student, grades in students.items()]
results = sorted(results, key = lambda x: (x[1]), reverse=True)

with open(args.report, 'w', newline='', encoding='utf8') as reportfile:
    headers = ['student_name', 'grade']
    output_table = csv.DictWriter(reportfile, fieldnames=headers)
    output_table.writeheader()
    output_table.writerows([{'student_name': name, 'grade': grade} for name, grade in results])

print(tabulate(results, headers=headers, tablefmt='grid', showindex=range(1, len(results) + 1)))
