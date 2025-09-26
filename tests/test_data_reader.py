"""Testing module for reader.py"""
import os
from unittest.mock import patch

from ..data_reader import DataReader

DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data")

def test_collect_files_valid_file(tmp_path):
    """Testing if input csv was correctly handled"""

    csv_path = os.path.join(tmp_path, "test.csv")

    with open(csv_path, 'a', encoding='utf8') as empty_file:
        empty_file.close()

    reader = DataReader()
    files = reader.collect_files([str(csv_path)])
    assert files == [str(csv_path)]

def test_collect_files_invalid_path():
    """Testing for invalid input csv's path(s)"""

    reader = DataReader()

    with patch('builtins.print') as mocked_print:
        files = reader.collect_files(['nonexistent'])
        assert not files
        mocked_print.assert_called_with('Warning: Invalid path - "nonexistent", skipping...')

def test_collect_files_non_csv(tmp_path):
    """Testing if non-csv file was supplied"""

    txt_path = os.path.join(tmp_path, "test.txt")

    with open(txt_path, 'a', encoding='utf8') as empty_file:
        empty_file.close()

    reader = DataReader()

    with patch('builtins.print') as mocked_print:
        files = reader.collect_files([str(txt_path)])
        assert not files
        mocked_print.assert_called_with(
            f'Report file "{txt_path}" must have a .csv extension, skipping...')

def test_read_data_valid():
    """Testing for handling of valid dataset"""

    csv_path = os.path.join(DATA_DIR, "valid1.csv")
    reader = DataReader()
    data = reader.read_data([csv_path], required_fields=["student_name", "grade"])

    assert len(data) == 4
    assert {'student_name': 'Alice'} in data[0] and {'grade': '5'} in data[0]
    assert {'student_name': 'Bob'} in data[1] and {'grade': '3'} in data[1]
    assert {'student_name': 'Alice'} in data[2] and {'grade': '4'} in data[2]
    assert {'student_name': 'Bob'} in data[3] and {'grade': '2'} in data[3]

def test_read_data_missing_required_fields():
    """Testing for handling of dataset with invalid header"""

    csv_path = os.path.join(DATA_DIR, "invalid_columns.csv")
    reader = DataReader()
    fields = ["student_name", "grade"]

    with patch('builtins.print') as mocked_print:
        data = reader.read_data([csv_path], required_fields=fields)
        assert not data
        mocked_print.assert_called_with(
            f'Warning: Skipping {csv_path} - missing required columns: {fields}')

def test_read_data_no_valid_files():
    """Testing for case where no valid csv was supplied"""

    reader = DataReader()

    with patch('builtins.print') as mocked_print:
        data = reader.read_data([])
        assert not data
        mocked_print.assert_called_with("Error: No CSV files found in provided paths")
