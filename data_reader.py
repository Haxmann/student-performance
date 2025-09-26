"""Module for reading CSV sheets from files."""

from typing import Dict, List, Any
import os
import csv

class DataReader:
    """Class for reading and processing data from CSV files."""

    def collect_files(self, paths: List[str]) -> List[str]:
        ...
    
    def read_data(self, files: List[str], required_fields: List[str] = []) -> List[Dict[str, Any]]:
        ...
