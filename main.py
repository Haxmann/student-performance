"""Main module"""
from typing import Dict, List, Tuple

import argparse
import os
import csv
import sys

from tabulate import tabulate

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""

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

    return args

def collect_files(paths: List[str]) -> List[str]:
    """Collect all CSV files from provided paths."""

    valid_paths = []

    for path in paths:
        if not os.path.exists(path):
            print(f'Warning: Invalid path provided -  "{path}", skipping...')
            continue

        if not path.endswith('.csv'):
            print(f'Report file "{path}" must have a .csv extension, skipping...')
            continue

        valid_paths.append(path)

    return valid_paths

def read_student_data(files: List[str]) -> Dict[str, List[float]]:
    """Read student grades from CSV files."""

    if files:
        students = {}

        for file in files:
            with open(file, mode='r', encoding='utf8') as csv_file:
                input_table = csv.DictReader(csv_file)

                if not all(field in input_table.fieldnames # type: ignore (not a sequenced str)
                        for field in ['student_name', 'grade']):
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
                        students[student] = [grade]

                    else:
                        students[student] += [grade]

    else:
        print("Error: No CSV files found in provided paths")
        sys.exit(1)

    return students

def compute_results(students: Dict[str, List[float]]) -> List[Tuple[str, float]]:
    """Compute average grades and sort by performance."""

    results = [[student, round(sum(grades) / len(grades), 1)]
               for student, grades in students.items()]
    return sorted(results, key = lambda x: (x[1]), reverse=True) # type: ignore (all is valid)

def write_report(results: List[Tuple[str, float]], report_path: str) -> None:
    """Write results to CSV report, then print as formatted table."""

    with open(report_path, 'w', newline='', encoding='utf8') as reportfile:
        headers = ['student_name', 'grade']
        output_table = csv.DictWriter(reportfile, fieldnames=headers)
        output_table.writeheader()
        output_table.writerows([{'student_name': name, 'grade': grade} for name, grade in results])

    print(tabulate(results, headers=headers, tablefmt='grid', showindex=range(1, len(results) + 1)))

def main() -> None:
    """Main function to run the student performance report tool."""
    args = parse_arguments()
    files = collect_files(args.files)
    students = read_student_data(files)
    results = compute_results(students)
    write_report(results, args.report)

if __name__ == "__main__":
    main()
