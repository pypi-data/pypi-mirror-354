"""
Input/output utilities for the Project Chooser system.

This module provides classes and functions for handling file operations,
data loading, and results writing in various formats.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional, List, Union
from datetime import datetime

from ..data.models import RecommendationResult


class FileHandler:
    """
    Handles general file operations for the project chooser system.

    This class provides methods for safe file reading, writing, and
    path validation with proper error handling.
    """

    @staticmethod
    def read_json_file(filepath: Union[str, Path]) -> Dict[str, Any]:
        """
        Read and parse a JSON file safely.

        Parameters
        ----------
        filepath : Union[str, Path]
            Path to the JSON file to read.

        Returns
        -------
        Dict[str, Any]
            Parsed JSON data as a dictionary.

        Raises
        ------
        FileNotFoundError
            If the specified file does not exist.
        json.JSONDecodeError
            If the file contains invalid JSON.
        IOError
            If there are permission or other I/O issues.
        """
        filepath = Path(filepath)

        if not filepath.exists():
            raise FileNotFoundError(f"JSON file not found: {filepath}")

        if not filepath.is_file():
            raise IOError(f"Path is not a file: {filepath}")

        try:
            with filepath.open('r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError as error:
            raise json.JSONDecodeError(
                f"Invalid JSON format in {filepath}: {error.msg}",
                error.doc,
                error.pos
            ) from error
        except IOError as error:
            raise IOError(f"Error reading file {filepath}: {error}") from error

    @staticmethod
    def write_text_file(
        filepath: Union[str, Path],
        content: str,
        encoding: str = 'utf-8'
    ) -> None:
        """
        Write text content to a file safely.

        Parameters
        ----------
        filepath : Union[str, Path]
            Path where to write the file.
        content : str
            Text content to write.
        encoding : str, optional
            Text encoding to use (default is 'utf-8').

        Raises
        ------
        IOError
            If there are permission or other I/O issues.
        """
        filepath = Path(filepath)

        # Create parent directories if they don't exist
        filepath.parent.mkdir(parents=True, exist_ok=True)

        try:
            with filepath.open('w', encoding=encoding) as file:
                file.write(content)
        except IOError as error:
            raise IOError(f"Error writing file {filepath}: {error}") from error

    @staticmethod
    def write_json_file(
        filepath: Union[str, Path],
        data: Dict[str, Any],
        indent: int = 2
    ) -> None:
        """
        Write data to a JSON file safely.

        Parameters
        ----------
        filepath : Union[str, Path]
            Path where to write the JSON file.
        data : Dict[str, Any]
            Data to serialise as JSON.
        indent : int, optional
            JSON indentation level (default is 2).

        Raises
        ------
        IOError
            If there are permission or other I/O issues.
        TypeError
            If the data cannot be serialised to JSON.
        """
        filepath = Path(filepath)

        # Create parent directories if they don't exist
        filepath.parent.mkdir(parents=True, exist_ok=True)

        try:
            with filepath.open('w', encoding='utf-8') as file:
                json.dump(data, file, indent=indent, ensure_ascii=False)
        except (IOError, TypeError) as error:
            raise type(error)(f"Error writing JSON file {filepath}: {error}") from error

    @staticmethod
    def ensure_directory_exists(dirpath: Union[str, Path]) -> Path:
        """
        Ensure a directory exists, creating it if necessary.

        Parameters
        ----------
        dirpath : Union[str, Path]
            Path to the directory.

        Returns
        -------
        Path
            Path object for the directory.

        Raises
        ------
        IOError
            If the directory cannot be created.
        """
        dirpath = Path(dirpath)

        try:
            dirpath.mkdir(parents=True, exist_ok=True)
            return dirpath
        except IOError as error:
            raise IOError(f"Cannot create directory {dirpath}: {error}") from error


class ResultsWriter:
    """
    Handles writing of recommendation results to various output formats.

    This class provides methods to save recommendation results, analysis
    reports, and other output data in different formats (Markdown, JSON, etc.).

    Attributes
    ----------
    output_directory : Path
        Directory where output files will be saved.
    """

    def __init__(self, output_directory: Union[str, Path] = "results") -> None:
        """
        Initialise the results writer.

        Parameters
        ----------
        output_directory : Union[str, Path], optional
            Directory for output files (default is "results").
        """
        self.output_directory = Path(output_directory)
        FileHandler.ensure_directory_exists(self.output_directory)

    def write_recommendations_markdown(
        self,
        recommendations: List[RecommendationResult],
        filename: Optional[str] = None,
        max_results: Optional[int] = None
    ) -> Path:
        """
        Write recommendation results to a Markdown file.

        Parameters
        ----------
        recommendations : List[RecommendationResult]
            List of recommendation results to write.
        filename : Optional[str], optional
            Output filename. If None, generates timestamped filename.
        max_results : Optional[int], optional
            Maximum number of results to write (default is all).

        Returns
        -------
        Path
            Path to the written file.
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recommendations_{timestamp}.md"

        filepath = self.output_directory / filename

        if max_results is not None:
            recommendations = recommendations[:max_results]

        # Generate markdown content
        lines = [
            f"# Top {len(recommendations)} Project Recommendations\n",
            "*Enhanced with niche discovery to help you find hidden gems!*\n",
            f"*Generated on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}*\n\n"
        ]

        for index, result in enumerate(recommendations, 1):
            project = result.project
            lines.extend([
                f"## {index}. {project.title} ({project.supervisor})\n",
                f"- **Match score:** {result.score:.1f}",
                f"- **Match reasons:** {', '.join(result.match_reasons)}"
            ])

            if result.niche_insights:  # type: ignore
                lines.append(
                    f"- **✨ Niche insights:** {'; '.join(result.niche_insights)}"  # type: ignore
                )
            else:
                lines.append("- **✨ Niche insights:** No niche insights found.")

            lines.extend([
                f"- **Co-requisite:** {project.co_requisite}",
                f"- **Focus:** {', '.join(project.mathematical_focus)}",
                f"- **Methods:** {', '.join(project.research_methodology)}",
                f"- **Tech:** {', '.join(project.programming_languages)}",
                f"- **Applicable degrees:** {', '.join(project.applicable_degrees)}",
                f"- **Student capacity:** {project.student_capacity}\n"
            ])

        # Add niche discovery explanation
        lines.extend([
            "---\n",
            "## About Niche Discovery\n",
            "This system uses advanced algorithms to help you discover projects "
            "you might not have considered:\n",
            "- **Cluster analysis** - Groups similar projects to find alternatives",
            "- **Diversity scoring** - Identifies unique combinations of topics",
            "- **Semantic matching** - Finds projects with related but different keywords",
            "- **Supervisor expertise** - Considers supervisor's research breadth\n",
            "Look for the ✨ niche insights in each recommendation!\n"
        ])

        content = '\n'.join(lines)
        FileHandler.write_text_file(filepath, content)

        return filepath

    def write_recommendations_json(
        self,
        recommendations: List[RecommendationResult],
        filename: Optional[str] = None,
        max_results: Optional[int] = None
    ) -> Path:
        """
        Write recommendation results to a JSON file.

        Parameters
        ----------
        recommendations : List[RecommendationResult]
            List of recommendation results to write.
        filename : Optional[str], optional
            Output filename. If None, generates timestamped filename.
        max_results : Optional[int], optional
            Maximum number of results to write (default is all).

        Returns
        -------
        Path
            Path to the written file.
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recommendations_{timestamp}.json"

        filepath = self.output_directory / filename

        if max_results is not None:
            recommendations = recommendations[:max_results]

        # Convert to JSON-serialisable format
        data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_recommendations": len(recommendations)
            },
            "recommendations": [
                {
                    "rank": index,
                    "score": result.score,
                    "match_reasons": result.match_reasons,
                    "niche_insights": result.niche_insights,  # type: ignore
                    "project": {
                        "id": result.project.project_id,
                        "title": result.project.title,
                        "supervisor": result.project.supervisor,
                        "student_capacity": result.project.student_capacity,
                        "co_requisite": result.project.co_requisite,
                        "related_modules": result.project.related_modules,
                        "programming_languages": result.project.programming_languages,
                        "general_topics": result.project.general_topics,
                        "mathematical_focus": result.project.mathematical_focus,
                        "research_methodology": result.project.research_methodology,
                        "applicable_degrees": result.project.applicable_degrees
                    }
                }
                for index, result in enumerate(recommendations, 1)
            ]
        }

        FileHandler.write_json_file(filepath, data)

        return filepath

    def write_analysis_markdown(
        self,
        analysis_data: Dict[str, Any],
        filename: Optional[str] = None
    ) -> Path:
        """
        Write project analysis results to a Markdown file.

        Parameters
        ----------
        analysis_data : Dict[str, Any]
            Analysis data including counters and statistics.
        filename : Optional[str], optional
            Output filename. If None, generates timestamped filename.

        Returns
        -------
        Path
            Path to the written file.
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"analysis_{timestamp}.md"

        filepath = self.output_directory / filename

        lines = [
            "# Project Analysis Report\n",
            f"*Generated on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}*\n",
            "## Summary Statistics\n",
            f"Total Projects: {analysis_data.get('total_projects', 0)}",
            f"Total Student Capacity: {analysis_data.get('total_capacity', 0)}\n"
        ]

        # Add counter statistics
        for section_name, counter_data in analysis_data.get('counters', {}).items():
            lines.append(f"### {section_name}\n")

            if not counter_data:
                lines.append("*No data available for this category.*\n")
                continue

            total = sum(counter_data.values())
            for item, count in counter_data.most_common():
                percentage = (count / total) if total > 0 else 0.0
                lines.append(f"- {item}: {count} ({percentage:.1%})")

            lines.append("")

        content = '\n'.join(lines)
        FileHandler.write_text_file(filepath, content)

        return filepath

    def write_preferences_json(
        self,
        preferences: Dict[str, Any],
        filename: Optional[str] = None
    ) -> Path:
        """
        Write user preferences to a JSON file.

        Parameters
        ----------
        preferences : Dict[str, Any]
            User preferences data.
        filename : Optional[str], optional
            Output filename. If None, uses default name.

        Returns
        -------
        Path
            Path to the written file.
        """
        if filename is None:
            filename = "user_preferences.json"

        filepath = self.output_directory / filename

        data = {
            "metadata": {
                "saved_at": datetime.now().isoformat(),
                "version": "1.0"
            },
            "preferences": preferences
        }

        FileHandler.write_json_file(filepath, data)

        return filepath
