"""
Data validation utilities for the project chooser system.

This module provides comprehensive validation for project data
beyond basic Pydantic validation.
"""

from typing import List
from collections import Counter

from .models import Project


class ProjectDataValidator:
    """
    Provides advanced validation for project data.

    This validator performs checks that go beyond basic type validation,
    ensuring data quality and consistency.
    """

    def __init__(self) -> None:
        """Initialise the validator."""
        self.min_title_length = 10
        self.max_title_length = 200
        self.min_supervisor_name_length = 2
        self.max_capacity_per_project = 50

    def validate_projects(self, projects: List[Project]) -> List[str]:
        """
        Validate a list of projects and return any validation errors.

        Parameters
        ----------
        projects : List[Project]
            List of projects to validate.

        Returns
        -------
        List[str]
            List of validation error messages. Empty if no errors.
        """
        errors = []

        # Check for duplicate IDs
        project_ids = [project.project_id for project in projects]
        duplicate_ids = [
            project_id
            for project_id, count in Counter(project_ids).items()
            if count > 1
        ]
        if duplicate_ids:
            errors.append(f"Duplicate project IDs found: {duplicate_ids}")

        # Validate individual projects
        for index, project in enumerate(projects):
            project_errors = self.validate_single_project(project)
            for error in project_errors:
                errors.append(f"Project {index + 1} ({project.project_id}): {error}")

        # Check for suspicious patterns
        pattern_errors = self._check_suspicious_patterns(projects)
        errors.extend(pattern_errors)

        return errors

    def validate_single_project(self, project: Project) -> List[str]:
        """
        Validate a single project and return any validation errors.

        Parameters
        ----------
        project : Project
            Project to validate.

        Returns
        -------
        List[str]
            List of validation error messages. Empty if no errors.
        """
        errors = []

        # Title validation
        if len(project.title) < self.min_title_length:
            errors.append(
                f"Title too short (minimum {self.min_title_length} characters)"
            )
        elif len(project.title) > self.max_title_length:
            errors.append(
                f"Title too long (maximum {self.max_title_length} characters)"
            )

        # Supervisor validation
        if len(project.supervisor) < self.min_supervisor_name_length:
            errors.append("Supervisor name too short")

        # Capacity validation
        if project.student_capacity > self.max_capacity_per_project:
            errors.append(
                f"Unusually high capacity ({project.student_capacity}), "
                f"maximum expected: {self.max_capacity_per_project}"
            )

        # Content validation
        if not project.general_topics:
            errors.append("No general topics specified")

        if not project.mathematical_focus:
            errors.append("No mathematical focus specified")

        if not project.research_methodology:
            errors.append("No research methodology specified")

        if not project.applicable_degrees:
            errors.append("No applicable degrees specified")

        # Check for empty or meaningless entries
        empty_topics = [
            topic
            for topic in project.general_topics
            if not topic.strip() or len(topic.strip()) < 3
        ]
        if empty_topics:
            errors.append(f"Empty or too short topics: {empty_topics}")

        return errors

    def _check_suspicious_patterns(self, projects: List[Project]) -> List[str]:
        """
        Check for suspicious patterns across all projects.

        Parameters
        ----------
        projects : List[Project]
            List of all projects to check.

        Returns
        -------
        List[str]
            List of warning messages about suspicious patterns.
        """
        warnings = []

        # Check supervisor workload distribution
        supervisor_counts = Counter(project.supervisor for project in projects)
        max_projects_per_supervisor = max(supervisor_counts.values())
        avg_projects_per_supervisor = sum(supervisor_counts.values()) / len(supervisor_counts)

        if max_projects_per_supervisor > 3 * avg_projects_per_supervisor:
            overloaded_supervisors = [
                supervisor
                for supervisor, count in supervisor_counts.items()
                if count > 2 * avg_projects_per_supervisor
            ]
            warnings.append(
                    f"Some supervisors have unusually many projects: {overloaded_supervisors}"
                )

        # Check for degree distribution by category
        from ..config.settings import Settings
        settings = Settings()
        degree_categories = settings.degree_categories
        category_counts = {cat: 0 for cat in degree_categories}
        degree_to_category = {}
        # Build a mapping from degree name (lowercase) to category
        for cat, names in degree_categories.items():
            for name in names:
                degree_to_category[name.lower()] = cat
        # Count projects by category
        for project in projects:
            found = set()
            for degree in project.applicable_degrees:
                cat = degree_to_category.get(degree.lower())
                if cat:
                    found.add(cat)
            for cat in found:
                category_counts[cat] += 1
        # Validate all degrees are covered by a category
        all_degrees = set(
            degree.lower() for project in projects for degree in project.applicable_degrees
        )
        uncovered = [d for d in all_degrees if d not in degree_to_category]
        if uncovered:
            warnings.append(
                f"Degree(s) not covered by DEGREE_CATEGORIES: {uncovered}"
            )
        min_count = min(category_counts.values()) if category_counts else 0
        max_count = max(category_counts.values()) if category_counts else 0
        if min_count > 0 and max_count > 10 * min_count:
            warnings.append(
                "Very uneven distribution of projects across degree categories: "
                f"{category_counts}"
            )

        # Check for topic diversity
        all_topics = [
            topic for project in projects for topic in project.general_topics
        ]
        topic_counts = Counter(all_topics)
        unique_topics = len(topic_counts)
        total_topic_instances = len(all_topics)

        if unique_topics < total_topic_instances / 10:  # Less than 10% unique
            warnings.append(
                "Low topic diversity - many projects share the same topics"
            )

        return warnings

    def suggest_improvements(self, projects: List[Project]) -> List[str]:
        """
        Suggest improvements for the project dataset.

        Parameters
        ----------
        projects : List[Project]
            List of projects to analyse.

        Returns
        -------
        List[str]
            List of improvement suggestions.
        """
        suggestions = []

        # Check missing abstracts
        missing_abstracts = [
            project.project_id
            for project in projects
            if not project.abstract or len(project.abstract.strip()) < 50
        ]
        if missing_abstracts:
            suggestions.append(
                f"Consider adding detailed abstracts to projects: {missing_abstracts}"
            )

        # Check programming language coverage
        programming_projects = [
            project for project in projects
            if any(lang.lower() != "none" for lang in project.programming_languages)
        ]
        programming_percentage = len(programming_projects) / len(projects) * 100

        if programming_percentage < 30:
            suggestions.append(
                "Consider adding more programming-focused projects "
                f"(currently {programming_percentage:.1f}%)"
            )        # Check interdisciplinary projects
        interdisciplinary_count = 0
        for project in projects:
            if len(set(project.mathematical_focus)) > 2:
                interdisciplinary_count += 1
        interdisciplinary_percentage = interdisciplinary_count / len(projects) * 100
        if interdisciplinary_percentage < 20:
            suggestions.append(
                "Consider adding more interdisciplinary projects "
                f"(currently {interdisciplinary_percentage:.1f}%)"
            )

        return suggestions
