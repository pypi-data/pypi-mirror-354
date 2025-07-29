"""
Data loading utilities for the project chooser system.

This module provides robust data loading capabilities with validation
and error handling.
"""

import json
from pathlib import Path
from typing import List, Union

from pydantic import ValidationError

from .models import Project, ProjectData
from .validator import ProjectDataValidator

class ProjectLoadError(Exception):
    """Exception raised when project data cannot be loaded."""
    pass

class ProjectLoader:
    """
    Handles loading and validation of project data from various sources.

    This class provides a robust interface for loading project data
    with comprehensive validation and error handling.
    """

    def __init__(self, validator: ProjectDataValidator = None) -> None:
        """
        Initialise the project loader.

        Parameters
        ----------
        validator : ProjectDataValidator, optional
            Custom validator instance. If None, uses default validator.
        """
        self.validator = validator or ProjectDataValidator()

    def load_from_json(self, file_path: Union[str, Path]) -> List[Project]:
        """
        Load projects from a JSON file.

        Parameters
        ----------
        file_path : Union[str, Path]
            Path to the JSON file containing project data.

        Returns
        -------
        List[Project]
            List of validated Project objects.

        Raises
        ------
        ProjectLoadError
            If the file cannot be loaded or validated.
        FileNotFoundError
            If the specified file does not exist.
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Project file not found: {file_path}")

        if not file_path.is_file():
            raise ProjectLoadError(f"Path is not a file: {file_path}")

        try:
            with open(file_path, encoding="utf-8") as file_handle:
                raw_data = json.load(file_handle)
        except json.JSONDecodeError as json_error:
            raise ProjectLoadError(
                f"Invalid JSON format in {file_path}: {json_error}"
            ) from json_error
        except IOError as io_error:
            raise ProjectLoadError(
                f"Could not read file {file_path}: {io_error}"
            ) from io_error

        return self._validate_and_parse(raw_data, file_path)

    def load_from_dict(self, data: dict) -> List[Project]:
        """
        Load projects from a dictionary.

        Parameters
        ----------
        data : dict
            Dictionary containing project data.

        Returns
        -------
        List[Project]
            List of validated Project objects.

        Raises
        ------
        ProjectLoadError
            If the data cannot be validated.
        """
        return self._validate_and_parse(data, "dictionary")

    def _validate_and_parse(
        self,
        raw_data: dict,
        source: Union[str, Path]
    ) -> List[Project]:
        """
        Validate and parse raw data into Project objects.

        Parameters
        ----------
        raw_data : dict
            Raw data dictionary to validate.
        source : Union[str, Path]
            Source identifier for error messages.

        Returns
        -------
        List[Project]
            List of validated Project objects.

        Raises
        ------
        ProjectLoadError
            If validation fails.
        """
        try:
            # Validate structure
            project_data = ProjectData(**raw_data)
        except ValidationError as validation_error:
            raise ProjectLoadError(
                f"Data validation failed for {source}: {validation_error}"
            ) from validation_error        # Additional custom validation
        validation_errors = self.validator.validate_projects(project_data.projects)
        if validation_errors:
            # Filter out distribution warnings for now
            critical_errors = [
                error for error in validation_errors
                if not error.startswith("Uneven distribution") and
                   not error.startswith("Very uneven distribution")
            ]
            if critical_errors:
                error_messages = "\n".join(critical_errors)
                raise ProjectLoadError(
                    f"Project validation failed for {source}:\n{error_messages}"
                )

        return project_data.projects

    def get_available_values(self, projects: List[Project]) -> dict:
        """
        Extract all available values for different project attributes.

        This is useful for building user interface choices and validation.

        Parameters
        ----------
        projects : List[Project]
            List of projects to analyse.

        Returns
        -------
        dict
            Dictionary containing sets of available values for each attribute.
        """
        available_values = {
            "degrees": set(),
            "supervisors": set(),
            "topics": set(),
            "methodologies": set(),
            "mathematical_focus": set(),
            "programming_languages": set(),
            "co_requisites": set(),
        }

        for project in projects:
            available_values["degrees"].update(project.applicable_degrees)
            available_values["supervisors"].add(project.supervisor)
            available_values["topics"].update(project.general_topics)
            available_values["methodologies"].update(project.research_methodology)
            available_values["mathematical_focus"].update(project.mathematical_focus)
            available_values["programming_languages"].update(
                project.programming_languages
            )
            if project.co_requisite.lower() != "none":
                available_values["co_requisites"].add(project.co_requisite)

        # Convert sets to sorted lists for consistent ordering
        return {
            key: sorted(list(values))
            for key, values in available_values.items()
        }

    def get_project_statistics(self, projects: List[Project]) -> dict:
        """
        Calculate basic statistics about the loaded projects.

        Parameters
        ----------
        projects : List[Project]
            List of projects to analyse.

        Returns
        -------
        dict
            Dictionary containing project statistics.
        """
        if not projects:
            return {"total_projects": 0}

        total_capacity = sum(project.student_capacity for project in projects)
        supervisors = set(project.supervisor for project in projects)
        degrees = set(
            degree
            for project in projects
            for degree in project.applicable_degrees
        )
        topics = set(
            topic
            for project in projects
            for topic in project.general_topics
        )

        return {
            "total_projects": len(projects),
            "total_capacity": total_capacity,
            "unique_supervisors": len(supervisors),
            "unique_degrees": len(degrees),
            "unique_topics": len(topics),
            "average_capacity": total_capacity / len(projects),
            "projects_with_prerequisites": len([
                p for p in projects if p.co_requisite.lower() != "none"
            ]),
        }
