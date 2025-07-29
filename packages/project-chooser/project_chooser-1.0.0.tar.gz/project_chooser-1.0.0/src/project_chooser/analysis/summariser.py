"""
Project summariser and analysis functionality.

This module provides comprehensive analysis capabilities for project data,
including statistical analysis, summary generation, and report creation
in multiple output formats.
"""

from typing import List, Dict, Any, Counter as CounterType, Optional
from collections import Counter
from pathlib import Path

from ..data.models import Project, ProjectData
from ..data.loader import ProjectLoader
from ..utils.display import StatisticsFormatter
from ..utils.io import ResultsWriter, FileHandler


class ProjectSummariser:
    """
    Analyses and summarises project data with comprehensive statistical reporting.

    This class provides methods to analyse project collections, generate
    statistics about various project attributes, and create detailed
    summary reports in both console and file formats.

    Attributes
    ----------
    formatter : StatisticsFormatter
        Formatter for displaying statistical results.
    writer : ResultsWriter
        Writer for saving analysis results to files.
    """

    def __init__(self, use_colour_output: bool = True, output_directory: str = "results") -> None:
        """
        Initialise the project summariser.

        Parameters
        ----------
        use_colour_output : bool, optional
            Whether to use coloured console output (default is True).
        output_directory : str, optional
            Directory for saving output files (default is "results").
        """
        self.formatter = StatisticsFormatter(use_colour=use_colour_output)
        self.writer = ResultsWriter(output_directory=output_directory)

    def analyse_projects_from_file(
        self,
        filepath: str,
        output_filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyse projects from a JSON file and optionally save results.

        Parameters
        ----------
        filepath : str
            Path to JSON file containing project data.
        output_filename : Optional[str], optional
            Filename for saving markdown report (default is None for console only).

        Returns
        -------
        Dict[str, Any]
            Dictionary containing analysis results and statistics.

        Raises
        ------
        FileNotFoundError
            If the specified JSON file cannot be found.
        ValueError
            If the JSON file contains invalid project data.
        """
        # Load project data
        loader = ProjectLoader()
        projects = loader.load_from_json(filepath)
        project_data = ProjectData(projects=projects)

        # Perform analysis
        analysis_results = self.analyse_projects(project_data.projects)

        # Display results
        if output_filename:
            # Save to markdown file
            output_path = self.writer.output_directory / output_filename
            with output_path.open('w', encoding='utf-8') as file:
                file.write(f"# Project Analysis Report: {Path(filepath).name}\n")
                self._display_analysis_results(analysis_results, output_file=file)

            self.formatter.console.print(f"[green]✓[/green] Analysis report saved to {output_path}")
        else:
            # Display to console only
            self._display_analysis_results(analysis_results)

        return analysis_results

    def analyse_projects(self, projects: List[Project]) -> Dict[str, Any]:
        """
        Analyse a collection of projects and generate comprehensive statistics.

        Parameters
        ----------
        projects : List[Project]
            List of project objects to analyse.

        Returns
        -------
        Dict[str, Any]
            Dictionary containing analysis results with the following structure:
            - 'total_projects': Total number of projects
            - 'total_capacity': Total student capacity
            - 'counters': Dictionary of Counter objects for different attributes
            - 'statistics': Additional calculated statistics
        """
        if not projects:
            return {
                'total_projects': 0,
                'total_capacity': 0,
                'counters': {},
                'statistics': {}
            }

        # Initialise counters for different project attributes
        counters = {
            'related_modules': Counter(),
            'programming_languages': Counter(),
            'general_topics': Counter(),
            'mathematical_focus': Counter(),
            'research_methodology': Counter(),
            'applicable_degrees': Counter(),
            'supervisors': Counter()
        }

        total_capacity = 0

        # Process each project
        for project in projects:
            self._process_single_project(project, counters)
            total_capacity += project.student_capacity

        # Calculate capacity distribution
        capacity_distribution = Counter(
            project.student_capacity for project in projects
        )

        # Calculate additional statistics
        statistics = self._calculate_additional_statistics(projects, counters)

        return {
            'total_projects': len(projects),
            'total_capacity': total_capacity,
            'counters': counters,
            'capacity_distribution': capacity_distribution,
            'statistics': statistics
        }

    def _process_single_project(
        self,
        project: Project,
        counters: Dict[str, CounterType[str]]
    ) -> None:
        """
        Process a single project and update counter statistics.

        Parameters
        ----------
        project : Project
            Project object to process.
        counters : Dict[str, Counter[str]]
            Dictionary of counters to update.
        """
        # Update related modules counter
        counters['related_modules'].update(project.related_modules)

        # Update programming languages counter (exclude "none" entries)
        programming_languages = [
            lang for lang in project.programming_languages
            if lang.lower() not in ['none', 'n/a', '']
        ]
        counters['programming_languages'].update(programming_languages)

        # Update other attribute counters
        counters['general_topics'].update(project.general_topics)
        counters['mathematical_focus'].update(project.mathematical_focus)
        counters['research_methodology'].update(project.research_methodology)
        counters['applicable_degrees'].update(project.applicable_degrees)

        # Update supervisor counter
        counters['supervisors'][project.supervisor] += 1

    def _calculate_additional_statistics(
        self,
        projects: List[Project],
        counters: Dict[str, CounterType[str]]
    ) -> Dict[str, Any]:
        """
        Calculate additional statistical measures.

        Parameters
        ----------
        projects : List[Project]
            List of projects to analyse.
        counters : Dict[str, Counter[str]]
            Dictionary of attribute counters.

        Returns
        -------
        Dict[str, Any]
            Dictionary of additional statistics.
        """
        statistics = {}

        # Average capacity per project
        if projects:
            total_capacity = sum(project.student_capacity for project in projects)
            statistics['average_capacity_per_project'] = total_capacity / len(projects)
        else:
            statistics['average_capacity_per_project'] = 0.0

        # Most common attributes
        statistics['most_common'] = {}
        for attr_name, counter in counters.items():
            if counter:
                most_common_item, count = counter.most_common(1)[0]
                statistics['most_common'][attr_name] = {
                    'item': most_common_item,
                    'count': count,
                    'percentage': (count / len(projects)) * 100 if projects else 0
                }

        # Diversity metrics (number of unique values)
        statistics['diversity'] = {}
        for attr_name, counter in counters.items():
            statistics['diversity'][attr_name] = len(counter)

        # Projects per supervisor statistics
        if counters['supervisors']:
            supervisor_counts = list(counters['supervisors'].values())
            statistics['supervisor_stats'] = {
                'min_projects': min(supervisor_counts),
                'max_projects': max(supervisor_counts),
                'average_projects': sum(supervisor_counts) / len(supervisor_counts)
            }

        return statistics

    def _display_analysis_results(
        self,
        analysis_results: Dict[str, Any],
        output_file: Optional[Any] = None
    ) -> None:
        """
        Display comprehensive analysis results.

        Parameters
        ----------
        analysis_results : Dict[str, Any]
            Analysis results from analyse_projects method.
        output_file : Optional[Any], optional
            File handle for output (default is None for console only).
        """
        # Display summary statistics
        self.formatter.format_summary_statistics(
            analysis_results['total_projects'],
            analysis_results['total_capacity'],
            output_file
        )

        # Display counter statistics for each attribute
        counters = analysis_results['counters']

        # Related modules (top 10)
        self.formatter.format_counter_statistics(
            "Related Modules (Top 10)",
            counters['related_modules'],
            output_file,
            max_items=10
        )

        # Programming languages
        self.formatter.format_counter_statistics(
            "Programming Languages",
            counters['programming_languages'],
            output_file
        )

        # General topics (top 15)
        self.formatter.format_counter_statistics(
            "General Topics (Top 15)",
            counters['general_topics'],
            output_file,
            max_items=15
        )

        # Mathematical focus areas
        self.formatter.format_counter_statistics(
            "Mathematical Focus Areas",
            counters['mathematical_focus'],
            output_file
        )

        # Research methodologies
        self.formatter.format_counter_statistics(
            "Research Methodologies",
            counters['research_methodology'],
            output_file
        )

        # Applicable degrees
        self.formatter.format_counter_statistics(
            "Applicable Degrees",
            counters['applicable_degrees'],
            output_file
        )

        # Supervisor statistics
        self.formatter.format_supervisor_statistics(
            counters['supervisors'],
            output_file
        )

        # Capacity distribution
        self.formatter.format_capacity_distribution(
            analysis_results['capacity_distribution'],
            output_file
        )

    def generate_summary_report(
        self,
        projects: List[Project],
        report_title: str = "Project Analysis Report",
        filename: Optional[str] = None
    ) -> Path:
        """
        Generate a comprehensive summary report and save to file.

        Parameters
        ----------
        projects : List[Project]
            List of projects to analyse.
        report_title : str, optional
            Title for the report (default is "Project Analysis Report").
        filename : Optional[str], optional
            Output filename (default generates timestamped filename).

        Returns
        -------
        Path
            Path to the generated report file.
        """
        analysis_results = self.analyse_projects(projects)

        # Prepare data for the writer
        report_data = {
            'title': report_title,
            'total_projects': analysis_results['total_projects'],
            'total_capacity': analysis_results['total_capacity'],
            'counters': {
                'Related Modules (Top 10)': dict(
                    analysis_results['counters']['related_modules'].most_common(10)
                ),
                'Programming Languages': dict(
                    analysis_results['counters']['programming_languages']
                ),
                'General Topics (Top 15)': dict(
                    analysis_results['counters']['general_topics'].most_common(15)
                ),
                'Mathematical Focus Areas': dict(
                    analysis_results['counters']['mathematical_focus']
                ),
                'Research Methodologies': dict(
                    analysis_results['counters']['research_methodology']
                ),
                'Applicable Degrees': dict(
                    analysis_results['counters']['applicable_degrees']
                ),
                'Supervisor Project Counts': dict(
                    analysis_results['counters']['supervisors']
                ),
                'Capacity Distribution': dict(
                    analysis_results['capacity_distribution']
                )
            }
        }

        return self.writer.write_analysis_markdown(report_data, filename)

    def export_statistics_json(
        self,
        projects: List[Project],
        filename: Optional[str] = None
    ) -> Path:
        """
        Export analysis statistics to a JSON file.

        Parameters
        ----------
        projects : List[Project]
            List of projects to analyse.
        filename : Optional[str], optional
            Output filename (default generates timestamped filename).

        Returns
        -------
        Path
            Path to the exported JSON file.
        """
        analysis_results = self.analyse_projects(projects)

        # Convert Counter objects to regular dicts for JSON serialisation
        json_data = {
            'summary': {
                'total_projects': analysis_results['total_projects'],
                'total_capacity': analysis_results['total_capacity'],
                'statistics': analysis_results['statistics']
            },
            'counters': {
                name: dict(counter)
                for name, counter in analysis_results['counters'].items()
            },
            'capacity_distribution': dict(analysis_results['capacity_distribution'])
        }

        if filename is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"project_statistics_{timestamp}.json"

        filepath = self.writer.output_directory / filename
        FileHandler.write_json_file(filepath, json_data)

        return filepath
