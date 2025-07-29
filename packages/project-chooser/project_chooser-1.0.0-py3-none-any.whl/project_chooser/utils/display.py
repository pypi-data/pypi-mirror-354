"""
Display and formatting utilities for the Project Chooser system.

This module provides classes and functions for formatting and displaying
project recommendations, statistics, and other output in both console
and file formats.
"""

from typing import List, TextIO, Optional, Counter as CounterType
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..data.models import RecommendationResult


class RecommendationDisplayer:
    """
    Handles the display of project recommendations in console and markdown formats.

    This class provides methods to display project recommendations with enhanced
    formatting, including niche discovery information, match scores, and detailed
    project information.

    Attributes
    ----------
    console : Console
        Rich console instance for enhanced terminal output.
    use_colour : bool
        Whether to use coloured output in terminal display.
    """

    def __init__(self, use_colour: bool = True) -> None:
        """
        Initialise the recommendation displayer.

        Parameters
        ----------
        use_colour : bool, optional
            Whether to use coloured terminal output (default is True).
        """
        self.console = Console(color_system="auto" if use_colour else None)
        self.use_colour = use_colour

    def display_recommendations(
        self,
        recommendations: List[RecommendationResult],
        results_count: int,
        max_score: float,
        output_file: Optional[str] = None
    ) -> None:
        """
        Display project recommendations in console and optionally save to file.

        Parameters
        ----------
        recommendations : List[RecommendationResult]
            List of recommendation results to display.
        results_count : int
            Number of top results to show.
        max_score : float
            Maximum possible recommendation score.
        output_file : Optional[str], optional
            File path to save markdown output (default is None).
        """
        if results_count == 0:
            results_count = len(recommendations)

        # Console display
        self._display_console_header(results_count, output_file)

        # Markdown content for file output
        markdown_lines = self._generate_markdown_header(results_count)

        for index, result in enumerate(recommendations[:results_count], 1):
            self._display_single_recommendation_console(index, result, max_score)
            markdown_lines.extend(
                self._generate_single_recommendation_markdown(index, result, max_score)
            )

        # Add niche discovery explanation
        self._display_niche_discovery_info()
        markdown_lines.extend(self._generate_niche_discovery_markdown())

        # Save to file if requested
        if output_file:
            self._save_markdown_file(output_file, markdown_lines)

    def _display_console_header(self, results_count: int, output_file: Optional[str]) -> None:
        """Display header information in console."""
        title = f"🏆 Top {results_count} Project Recommendations"
        if output_file:
            title += f" (also written to {output_file})"

        subtitle = "✨ Enhanced with niche discovery to help you find hidden gems!"

        self.console.print(Panel(
            f"[bold green]{title}[/bold green]\n{subtitle}",
            title="[bold blue]Project Chooser Results[/bold blue]",
            border_style="blue"
        ))

    def _display_single_recommendation_console(
        self,
        index: int,
        result: RecommendationResult,
        max_score: float
    ) -> None:
        """Display a single recommendation in console format."""
        project = result.project

        # Main project title
        title = f"{index}. {project.title} ({project.supervisor})"
        self.console.print(f"\n[bold cyan]{title}[/bold cyan]")

        # Create a table for project details
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Label", style="dim")
        table.add_column("Value")

        table.add_row("📈 Match score:", f"{result.score:.1f} / {max_score:.1f}")
        table.add_row("🎯 Match reasons:", ", ".join(result.match_reasons))

        if result.niche_insights:  # type: ignore
            table.add_row("✨ Niche insights:", "; ".join(result.niche_insights))  # type: ignore

        table.add_row("📚 Co-requisite:", project.co_requisite)
        table.add_row("🔍 Focus:", ", ".join(project.mathematical_focus))
        table.add_row("🛠 Methods:", ", ".join(project.research_methodology))
        table.add_row("💻 Tech:", ", ".join(project.programming_languages))

        self.console.print(table)

    def _display_niche_discovery_info(self) -> None:
        """Display information about niche discovery system."""
        info_text = """
[bold yellow]About Niche Discovery[/bold yellow]

This system uses advanced algorithms to help you discover projects you might not have considered:

• [green]Cluster analysis[/green] - Groups similar projects to find alternatives
• [green]Diversity scoring[/green] - Identifies unique combinations of topics
• [green]Semantic matching[/green] - Finds projects with related but different keywords
• [green]Supervisor expertise[/green] - Considers supervisor's research breadth

Look for the ✨ niche insights in each recommendation!
        """
        self.console.print(Panel(info_text.strip(), border_style="yellow"))

    def _generate_markdown_header(self, results_count: int) -> List[str]:
        """Generate markdown header content."""
        return [
            f"# Top {results_count} Project Recommendations\n",
            "*Enhanced with niche discovery to help you find hidden gems!*\n\n"
        ]

    def _generate_single_recommendation_markdown(
        self,
        index: int,
        result: RecommendationResult,
        max_score: float
    ) -> List[str]:
        """Generate markdown content for a single recommendation."""
        project = result.project
        lines = [
            f"## {index}. {project.title} ({project.supervisor})\n",
            f"- **Match score:** {result.score:.1f} / {max_score:.1f}",
            f"- **Match reasons:** {', '.join(result.match_reasons)}"
        ]

        if result.niche_insights:  # type: ignore
            insights = '; '.join(result.niche_insights)  # type: ignore
            lines.append(f"- **✨ Niche insights:** {insights}")

        lines.extend([
            f"- **Co-requisite:** {project.co_requisite}",
            f"- **Focus:** {', '.join(project.mathematical_focus)}",
            f"- **Methods:** {', '.join(project.research_methodology)}",
            f"- **Tech:** {', '.join(project.programming_languages)}\n"
        ])

        return lines

    def _generate_niche_discovery_markdown(self) -> List[str]:
        """Generate markdown content for niche discovery explanation."""
        return [
            "---\n",
            "## About Niche Discovery\n",
            "This system uses advanced algorithms to help you discover projects "
            "you might not have considered:\n",
            "- **Cluster analysis** - Groups similar projects to find alternatives",
            "- **Diversity scoring** - Identifies unique combinations of topics",
            "- **Semantic matching** - Finds projects with related but different keywords",
            "- **Supervisor expertise** - Considers supervisor's research breadth\n",
            "Look for the ✨ niche insights in each recommendation!\n"
        ]

    def _save_markdown_file(self, filepath: str, content: List[str]) -> None:
        """Save markdown content to file."""
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.writelines(line + '\n' if not line.endswith('\n') else line
                                for line in content)
            self.console.print(f"[green]✓[/green] Results saved to {filepath}")
        except IOError as error:
            self.console.print(f"[red]✗[/red] Error saving to {filepath}: {error}")


class StatisticsFormatter:
    """
    Handles formatting and display of statistical analysis results.

    This class provides methods to format counter statistics, create tables,
    and generate both console and markdown output for project analysis results.

    Attributes
    ----------
    console : Console
        Rich console instance for enhanced terminal output.
    use_colour : bool
        Whether to use coloured output in terminal display.
    """

    def __init__(self, use_colour: bool = True) -> None:
        """
        Initialise the statistics formatter.

        Parameters
        ----------
        use_colour : bool, optional
            Whether to use coloured terminal output (default is True).
        """
        self.console = Console(color_system="auto" if use_colour else None)
        self.use_colour = use_colour

    def format_counter_statistics(
        self,
        title: str,
        counter: CounterType[str],
        output_file: Optional[TextIO] = None,
        max_items: Optional[int] = None
    ) -> None:
        """
        Format and display counter statistics to console and/or file.

        Parameters
        ----------
        title : str
            Header title for the statistics section.
        counter : Counter[str]
            Counter object with items to display.
        output_file : Optional[TextIO], optional
            File handle for markdown output (default is None).
        max_items : Optional[int], optional
            Maximum number of items to show (default is None for all).
        """

        def _write_output(text: str) -> None:
            """Write to both console and file if provided."""
            if output_file:
                output_file.write(text + "\n")
            else:
                self.console.print(text)

        # Section header
        if output_file:
            _write_output(f"\n### {title}")
        else:
            self.console.print(f"\n[bold blue]{title}[/bold blue]")

        if not counter:
            no_data_msg = "*No data available for this category.*"
            _write_output(no_data_msg)
            _write_output("")
            return

        total_items = sum(counter.values())
        items = counter.most_common(max_items)

        if output_file:
            # Markdown format
            for item, count in items:
                percentage = (count / total_items) if total_items > 0 else 0.0
                _write_output(f"- {item}: {count} ({percentage:.1%})")
        else:
            # Console table format
            table = Table(show_header=False, box=None)
            table.add_column("Item", style="cyan", width=45)
            table.add_column("Count", justify="right", style="green", width=6)
            table.add_column("Percentage", justify="right", style="yellow", width=8)

            for item, count in items:
                percentage = (count / total_items) if total_items > 0 else 0.0
                table.add_row(item, str(count), f"({percentage:.1%})")

            self.console.print(table)

        _write_output("")

    def format_summary_statistics(
        self,
        total_projects: int,
        total_capacity: int,
        output_file: Optional[TextIO] = None
    ) -> None:
        """
        Format and display summary statistics.

        Parameters
        ----------
        total_projects : int
            Total number of projects.
        total_capacity : int
            Total student capacity across all projects.
        output_file : Optional[TextIO], optional
            File handle for markdown output (default is None).
        """

        def _write_output(text: str) -> None:
            """Write to both console and file if provided."""
            if output_file:
                output_file.write(text + "\n")
            else:
                self.console.print(text)

        if output_file:
            _write_output("\n## Summary Statistics")
            _write_output(f"Total Projects: {total_projects}")
            _write_output(f"Total Student Capacity: {total_capacity}\n")
        else:
            self.console.print("\n[bold blue]Summary Statistics[/bold blue]")

            stats_table = Table(show_header=False, box=None)
            stats_table.add_column("Metric", style="cyan")
            stats_table.add_column("Value", style="green", justify="right")

            stats_table.add_row("Total Projects", str(total_projects))
            stats_table.add_row("Total Student Capacity", str(total_capacity))

            self.console.print(stats_table)
            self.console.print()

    def format_capacity_distribution(
        self,
        capacity_counts: CounterType[int],
        output_file: Optional[TextIO] = None
    ) -> None:
        """
        Format and display capacity distribution statistics.

        Parameters
        ----------
        capacity_counts : Counter[int]
            Counter of student capacity values.
        output_file : Optional[TextIO], optional
            File handle for markdown output (default is None).
        """

        def _write_output(text: str) -> None:
            """Write to both console and file if provided."""
            if output_file:
                output_file.write(text + "\n")
            else:
                self.console.print(text)

        if output_file:
            _write_output("## Capacity Distribution")
        else:
            self.console.print("\n[bold blue]Capacity Distribution[/bold blue]")

        if capacity_counts:
            if output_file:
                for capacity, count in capacity_counts.most_common():
                    _write_output(f"- Projects with {capacity} student capacity: {count}")
            else:
                table = Table(show_header=False, box=None)
                table.add_column("Capacity", style="cyan")
                table.add_column("Project Count", style="green", justify="right")

                for capacity, count in capacity_counts.most_common():
                    table.add_row(f"{capacity} student(s)", str(count))

                self.console.print(table)
        else:
            _write_output("*No capacity data available.*")

        _write_output("")

    def format_supervisor_statistics(
        self,
        supervisor_counts: CounterType[str],
        output_file: Optional[TextIO] = None
    ) -> None:
        """
        Format and display supervisor project counts.

        Parameters
        ----------
        supervisor_counts : Counter[str]
            Counter of projects per supervisor.
        output_file : Optional[TextIO], optional
            File handle for markdown output (default is None).
        """

        def _write_output(text: str) -> None:
            """Write to both console and file if provided."""
            if output_file:
                output_file.write(text + "\n")
            else:
                self.console.print(text)

        if output_file:
            _write_output("## Supervisor Project Counts")
        else:
            self.console.print("\n[bold blue]Supervisor Project Counts[/bold blue]")

        if supervisor_counts:
            if output_file:
                for supervisor, count in supervisor_counts.most_common():
                    _write_output(f"- {supervisor}: {count} projects")
            else:
                table = Table(show_header=False, box=None)
                table.add_column("Supervisor", style="cyan", width=40)
                table.add_column("Projects", style="green", justify="right")

                for supervisor, count in supervisor_counts.most_common():
                    table.add_row(supervisor, str(count))

                self.console.print(table)
        else:
            _write_output("*No supervisor data available.*")

        _write_output("")
