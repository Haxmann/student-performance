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
        ...

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