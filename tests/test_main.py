"""Testing module for studperf.py"""
import os
from unittest.mock import patch

import pytest

from ..studperf import parse_arguments, get_report_generator, main
from ..data_reader import DataReader
from ..reports import StudentPerformanceReport

DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data")

def test_parse_arguments_valid():
    """Testing the validity of supplied arguments."""

    with patch('sys.argv', ['studperf.py', '-f', 'file1.csv', '-r', 'student-performance']):
        args = parse_arguments()
        assert args.files == ['file1.csv']
        assert args.report == 'student-performance'

def test_parse_arguments_no_files():
    """Testing the case w/o input files"""

    with patch('sys.argv', ['studperf.py']):
        with pytest.raises(SystemExit):
            parse_arguments()

def test_parse_arguments_no_report():
    """Testing the case w/o report type"""

    with patch('sys.argv', ['studperf.py', '--files', 'file1.csv']):
        with pytest.raises(SystemExit):
            parse_arguments()

def test_get_report_generator_valid():
    """Test getting valid report generator"""

    generator = get_report_generator("student-performance")
    assert isinstance(generator, StudentPerformanceReport)

def test_get_report_generator_invalid():
    """Test getting invalid report generator"""

    with pytest.raises(ValueError):
        get_report_generator("invalid-report")

def test_parse_arguments_invalid_report_dir(tmp_path):
    """Testing the case for invalid report path"""

    invalid_report = os.path.join(tmp_path, 'nonexistent/report.csv')

    with patch('sys.argv', ['studperf.py', '-f', 'file1.csv', '-r', invalid_report]):
        with pytest.raises(SystemExit):
            parse_arguments()

def test_read_student_data_invalid_grade():
    """Testing dataset with invalid grade values"""

    csv_path = os.path.join(DATA_DIR, "invalid_grade.csv")
    reader = DataReader()

    with patch('builtins.print') as mocked_print:
        data = reader.read_data([csv_path])
        mocked_print.assert_called_with(f"Warning: Skipping invalid grade in {csv_path} for Eve")
        assert data == {'Frank': '4'}

def test_main_student_performance(capsys):
    """Testing the main function for student-performance report."""

    csv_path = os.path.join(DATA_DIR, "valid1.csv")

    with patch('sys.argv', ['studperf.py', '--files', csv_path, '--report', 'student-performance']):
        main()

    captured = capsys.readouterr()
    assert "Alice" in captured.out
    assert "4.5" in captured.out
    assert "Bob" in captured.out
    assert "2.5" in captured.out
