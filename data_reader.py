"""Module for reading CSV sheets from files."""

from typing import Dict, List, Any
import os
import csv

class DataReader:
    """Class for reading and processing data from CSV files."""

    def collect_files(self, paths: List[str]) -> List[str]:
        """Collect all CSV files from provided paths."""

        valid_paths = []

        for path in paths:
            if not os.path.exists(path):
                print(f'Warning: Invalid path - "{path}", skipping...')
                continue

            if not path.endswith('.csv'):
                print(f'Report file "{path}" must have a .csv extension, skipping...')
                continue

            valid_paths.append(path)

        return valid_paths

    def read_data(self, files: List[str], required_fields: List[str] = []) -> List[Dict[str, Any]]:
        """Read student grades from CSV files."""

        students: List[Dict[str, Any]] = []

        if not files:
            print("Error: No CSV files found in provided paths")

        else:
            for file in files:
                with open(file, mode='r', encoding='utf8') as csv_file:
                    input_table = csv.DictReader(csv_file)
                    fieldnames = input_table.fieldnames

                    if fieldnames is None:
                        print(f'Warning: Skipping {file} - no columns found')
                        continue

                    if required_fields and not all(field in fieldnames for field in required_fields):
                        print(f'Warning: Skipping {file} - missing required columns: {required_fields}')
                        continue

                    for line in input_table:
                        try:
                            grade = float(line['grade'])

                        except ValueError:
                            print(f"Warning: Skipping invalid grade in {file} for {line['student']}")
                            continue

                        students.append(dict(line))

        return students
