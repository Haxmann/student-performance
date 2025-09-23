import os
import csv
from unittest.mock import patch
from studperf import *

import pytest

DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data")

def test_parse_arguments_valid():
    """Testing the validity of supplied arguments."""

    with patch('sys.argv', ['studperf.py', '-f', 'file1.csv', '-r', 'report.csv']):
        args = parse_arguments()
        assert args.files == ['file1.csv']
        assert args.report == 'report.csv'

def test_parse_arguments_no_files():
    """Testing the case where w/o input csvs"""

    with patch('sys.argv', ['studperf.py']):
        with pytest.raises(SystemExit):
            parse_arguments()

def test_parse_arguments_invalid_report_dir(tmp_path):
    """Testing the case for invalid report path"""

    invalid_report = str(tmp_path + '/nonexistent/report.csv')

    with patch('sys.argv', ['studperf.py', '-f', 'file1.csv', '-r', invalid_report]):
        with pytest.raises(SystemExit):
            parse_arguments()

def test_collect_files_valid_file(tmp_path):
    """Testing if input csv was correctly handled"""

    csv_path = tmp_path + "/test.csv"
    csv_path.touch()
    files = collect_files([str(csv_path)])
    assert files == [str(csv_path)]

def test_collect_files_invalid_path():
    """Testing for invalid input csv's path(s)"""

    with patch('builtins.print') as mocked_print:
        files = collect_files(['nonexistent'])
        assert not files
        mocked_print.assert_called_with('Warning: Invalid path - "nonexistent", skipping...')

def test_collect_files_non_csv(tmp_path):
    """Testing if non-csv file was supplied"""

    txt_path = tmp_path + "/test.txt"
    txt_path.touch()

    with patch('builtins.print') as mocked_print:
        files = collect_files([str(txt_path)])
        assert not files
        mocked_print.assert_called_with(
            f'Report file "{txt_path}" must have a .csv extension, skipping...')

def test_read_student_data_valid():
    """Testing for handling of valid dataset"""

    csv_path = os.path.join(DATA_DIR, "valid.csv")
    students = read_student_data([csv_path])
    assert students == {'Alice': [4.0], 'Bob': [3.0]}

def test_read_student_data_invalid_format():
    """Testing for handling of dataset with invalid header"""

    csv_path = os.path.join(DATA_DIR, "invalid.csv")

    with patch('builtins.print') as mocked_print:
        students = read_student_data([csv_path])
        assert not students
        mocked_print.assert_called_with(
            f'Warning: Skipping {csv_path} - missing "student_name" or "grade" columns')

def test_read_student_data_invalid_grade():
    """Testing dataset with invalid grade values"""

    csv_path = os.path.join(DATA_DIR, "invalid_grade.csv")

    with patch('builtins.print') as mocked_print:
        students = read_student_data([csv_path])
        assert not students
        mocked_print.assert_called_with(f"Warning: Skipping invalid grade in {csv_path} for Alice")

def test_read_student_data_no_valid_files():
    """Testing for case where no valid csv was supplied"""

    with patch('builtins.print') as mocked_print, patch('sys.exit') as mocked_exit:
        read_student_data([])
        mocked_print.assert_called_with("Error: No CSV files found in provided paths")
        mocked_exit.assert_called_with(1)

def test_compute_results():
    """Testing for handling average grades"""

    students = {'Alice': [5.0, 4.0], 'Bob': [3.0, 3.0]}
    results = compute_results(students)
    assert results == [['Alice', 4.5], ['Bob', 3.0]]

def test_write_report(tmp_path):
    """Testing if resulted report was written correctly"""

    results = [['Alice', 4.5], ['Bob', 3.0]]
    report_path = tmp_path + "/report.csv"

    with patch('builtins.print'):
        write_report(results, str(report_path)) # type: ignore

    with open(report_path, 'r', encoding='utf8') as f:
        reader = csv.DictReader(f)
        assert list(reader) == [{'student_name': 'Alice', 'grade': '4.5'},
                                {'student_name': 'Bob', 'grade': '3.0'}]

def test_main(tmp_path):
    """Testing the main module from start to finish"""

    csv_path = os.path.join(DATA_DIR, "valid.csv")
    report_path = tmp_path + "/report.csv"

    with patch('sys.argv', ['studperf.py', '-f', csv_path, '-r', str(report_path)]), \
        patch('builtins.print'):
        main()

    with open(report_path, 'r', encoding='utf8') as f:
        reader = csv.DictReader(f)
        assert list(reader) == [{'student_name': 'Alice', 'grade': '5.0'},
                                {'student_name': 'Bob', 'grade': '3.0'}]
