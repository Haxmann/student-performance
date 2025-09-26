"""Module for generating performance reports based on data from CSV's."""

from typing import Dict, List, Any
from abc import ABC, abstractmethod
from tabulate import tabulate

class BaseReport(ABC):
    """Base abstract class for report generators."""

    @abstractmethod
    def generate(self, data: List[Dict[str, Any]]) -> str:
        """Generate the report from raw data."""
        pass

class StudentPerformanceReport(BaseReport):
    """Report for student performance."""

    def generate(self, data: List[Dict[str, Any]]) -> str:
        """Generate student performance report."""

        students: Dict[str, List[float]] = {}

        for row in data:
            if 'student_name' not in row or 'grade' not in row:
                print(f'Warning: Skipping row with missing student_name or grade: {row}')
                continue

            student = row['student_name']

            try:
                grade = float(row['grade'])

            except ValueError:
                print(f'Warning: Skipping invalid grade for {student}: {row["grade"]}')
                continue

            if student not in students:
                students[student] = [grade]

            else:
                students[student].append(grade)

        if not students:
            return "No valid student data found."

        results = [
            (student, round(sum(grades) / len(grades), 1))
            for student, grades in students.items()
        ]

        sorted_results = sorted(results, key=lambda x: x[1], reverse=True)

        return tabulate(
            sorted_results,
            headers=["student_name", "grade"],
            tablefmt="grid",
            showindex=range(1, len(sorted_results) + 1),
        )

class TeacherPerformanceReport(BaseReport):
    """Report for teacher performance."""

    def generate(self, data: List[Dict[str, Any]]) -> str:
        """Generate teacher performance report."""
        ...

class SubjectPerformanceReport(BaseReport):
    """Report for subject performance."""

    def generate(self, data: List[Dict[str, Any]]) -> str:
        """Generate subject performance report."""
        ...