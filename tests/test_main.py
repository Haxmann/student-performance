import pytest
import os
import csv
from unittest.mock import patch
from studperf import parse_arguments, collect_files, read_student_data, compute_results, write_report

DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data")

def test_parse_arguments_valid():
    with patch('sys.argv', ['studperf.py', '-f', 'file1.csv', '-r', 'report.csv']):
        args = parse_arguments()
        assert args.files == ['file1.csv']
        assert args.report == 'report.csv'

def test_parse_arguments_no_files():
    with patch('sys.argv', ['studperf.py']):
        with pytest.raises(SystemExit):
            parse_arguments()

def test_parse_arguments_invalid_report_dir(tmp_path):
    invalid_report = str(tmp_path + '/nonexistent/report.csv')

    with patch('sys.argv', ['studperf.py', '-f', 'file1.csv', '-r', invalid_report]):
        with pytest.raises(SystemExit):
            parse_arguments()

def test_collect_files_valid_file(tmp_path):
    csv_path = tmp_path + "/test.csv"
    csv_path.touch()
    files = collect_files([str(csv_path)])
    assert files == [str(csv_path)]

def test_collect_files_invalid_path():
    with patch('builtins.print') as mocked_print:
        files = collect_files(['nonexistent'])
        assert files == []
        mocked_print.assert_called_with("Warning: Invalid path provided -  \"nonexistent\", skipping...")

def test_collect_files_non_csv(tmp_path):
    txt_path = tmp_path + "/test.txt"
    txt_path.touch()

    with patch('builtins.print') as mocked_print:
        files = collect_files([str(txt_path)])
        assert files == []
        mocked_print.assert_called_with(f"Report file \"{str(txt_path)}\" must have a .csv extension, skipping...")

def test_read_student_data_valid():
    csv_path = os.path.join(DATA_DIR, "valid.csv")
    students = read_student_data([csv_path])
    assert students == {'Alice': [5.0], 'Bob': [3.0]}

def test_read_student_data_invalid_format():
    csv_path = os.path.join(DATA_DIR, "invalid.csv")

    with patch('builtins.print') as mocked_print:
        students = read_student_data([csv_path])
        assert students == {}
        mocked_print.assert_called_with(f"Warning: Skipping {csv_path} - missing 'student_name' or 'grade' columns")

def test_read_student_data_invalid_grade():
    csv_path = os.path.join(DATA_DIR, "invalid_grade.csv")

    with patch('builtins.print') as mocked_print:
        students = read_student_data([csv_path])
        assert students == {}
        mocked_print.assert_called_with(f"Warning: Skipping invalid grade in {csv_path} for Alice")

def test_read_student_data_no_valid_files():
    with patch('builtins.print') as mocked_print, patch('sys.exit') as mocked_exit:
        read_student_data([])
        mocked_print.assert_called_with("Error: No CSV files found in provided paths")
        mocked_exit.assert_called_with(1)

def test_compute_results():
    students = {'Alice': [5.0, 4.0], 'Bob': [3.0, 3.0]}
    results = compute_results(students)
    assert results == [['Alice', 4.5], ['Bob', 3.0]]

def test_write_report(tmp_path):
    results = [['Alice', 4.5], ['Bob', 3.0]]
    report_path = tmp_path + "/report.csv"

    with patch('builtins.print'):
        write_report(results, str(report_path)) # type: ignore

    with open(report_path, 'r', encoding='utf8') as f:
        reader = csv.DictReader(f)
        assert list(reader) == [{'student_name': 'Alice', 'grade': '4.5'},
                                {'student_name': 'Bob', 'grade': '3.0'}]

def test_main(tmp_path):
    csv_path = os.path.join(DATA_DIR, "valid.csv")
    report_path = tmp_path + "/report.csv"

    with patch('sys.argv', ['studperf.py', '-f', csv_path, '-r', str(report_path)]), \
        patch('builtins.print'):
        from studperf import main
        main()

    with open(report_path, 'r', encoding='utf8') as f:
        reader = csv.DictReader(f)
        assert list(reader) == [{'student_name': 'Alice', 'grade': '5.0'},
                                {'student_name': 'Bob', 'grade': '3.0'}]