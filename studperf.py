"""Main module"""
import argparse

from .data_reader import DataReader
from .reports import BaseReport, StudentPerformanceReport, TeacherPerformanceReport, SubjectPerformanceReport

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        prog="studperf",
        description="Student Performance Report Tool",
    )

    parser.add_argument(
        "-f",
        "--files",
        action="extend",
        nargs="+",
        type=str,
        required=True,
        help="""File(s) containing grade data.
Examples:
%(prog)s --files file1.csv --files /folder/file2.csv file3.csv
""",
    )

    parser.add_argument(
        "-r",
        "--report",
        type=str,
        required=True,
        help="Type of report to generate (e.g., student-performance, teacher-performance (WIP), subject-performance(WIP))",
    )

    return parser.parse_args()

def get_report_generator(report_type: str) -> BaseReport:
    """Factory to get the appropriate report generator."""

    reports = {
        "student-performance": StudentPerformanceReport(),
        "teacher-performance": TeacherPerformanceReport(),
        "subject-performance": SubjectPerformanceReport(),
    }

    if report_type not in reports:
        raise ValueError(f"Unknown report type: {report_type}")

    return reports[report_type]


def main() -> None:
    """Main function to run the report tool."""

    args = parse_arguments()
    reader = DataReader()
    files = reader.collect_files(args.files)
    required_fields = []

    if args.report == "student-performance":
        required_fields = ["student_name", "grade"]

    elif args.report == "teacher-performance":
        required_fields = ["teacher_name", "grade"]

    elif args.report == "subject-performance":
        required_fields = ["subject", "grade"]

    data = reader.read_data(files, required_fields)
    generator = get_report_generator(args.report)
    report = generator.generate(data)
    print(report)

if __name__ == "__main__":
    main()
