from typing import List, Dict, Any

from reports import StudentPerformanceReport, TeacherPerformanceReport, SubjectPerformanceReport

def test_student_performance_report(capsys):
    """Test student performance report generation."""

    data: List[Dict[str, Any]] = [
        {'student_name': 'Alice', 'grade': '5'},
        {'student_name': 'Alice', 'grade': '4'},
        {'student_name': 'Bob', 'grade': '3'},
        {'student_name': 'Bob', 'grade': '3'},
    ]

    generator = StudentPerformanceReport()
    report = generator.generate(data)
    print(report)  # To capture output if needed, but since generate returns string

    assert "Alice" in report
    assert "4.5" in report
    assert "Bob" in report
    assert "3.0" in report

def test_teacher_performance_report(capsys):
    """Test teacher performance report generation."""

    data: List[Dict[str, Any]] = [
        {'teacher_name': 'Mr. Smith', 'grade': '5'},
        {'teacher_name': 'Mr. Smith', 'grade': '4'},
        {'teacher_name': 'Ms. Johnson', 'grade': '3'},
        {'teacher_name': 'Ms. Johnson', 'grade': '3'},
    ]

    generator = TeacherPerformanceReport()
    report = generator.generate(data)
    print(report)

    assert "Mr. Smith" in report
    assert "4.5" in report
    assert "Ms. Johnson" in report
    assert "3.0" in report

def test_subject_performance_report(capsys):
    """Test subject performance report generation."""

    data: List[Dict[str, Any]] = [
        {'subject': 'Math', 'grade': '5'},
        {'subject': 'Math', 'grade': '4'},
        {'subject': 'Science', 'grade': '3'},
        {'subject': 'Science', 'grade': '3'},
    ]

    generator = SubjectPerformanceReport()
    report = generator.generate(data)
    print(report)

    assert "Math" in report
    assert "4.5" in report
    assert "Science" in report
    assert "3.0" in report