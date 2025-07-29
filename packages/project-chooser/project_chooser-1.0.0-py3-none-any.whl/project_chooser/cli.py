"""
Command-line interface for the Project Chooser system.

This module provides a comprehensive CLI interface using Typer for interacting
with the project recommendation and analysis system.
"""

import typer
from typing import Optional
from rich.console import Console
from rich.panel import Panel

from .data.loader import ProjectLoader
from .data.validator import ProjectDataValidator
from .core.recommender import ProjectRecommender  # type: ignore
from .analysis.summariser import ProjectSummariser
from .config.settings import Settings
from .data.models import UserPreferences, ProjectData  # Import ProjectData

# Create the main Typer app
app = typer.Typer(
    name="project-chooser",
    help="🎯 AI-powered academic project recommendation system with niche discovery",
    rich_markup_mode="rich"
)

# Create a console for rich output
console = Console()


@app.command()
def recommend(
    data_file: str = typer.Argument(
        "projects.json",
        help="Path to the JSON file containing project data"
    ),
    output_file: Optional[str] = typer.Option(
        None,
        "--output", "-o",
        help="Output file for recommendations (default: auto-generated)"
    ),
    max_results: int = typer.Option(
        5,
        "--max-results", "-n",
        help="Maximum number of recommendations to show",
        min=1
    ),
    interactive: bool = typer.Option(
        True,
        "--interactive/--no-interactive", "-i/-I",
        help="Use interactive questioning mode"
    ),
    use_niche_discovery: bool = typer.Option(
        True,
        "--niche/--no-niche",
        help="Enable niche discovery features"
    ),
    colour: bool = typer.Option(
        True,
        "--colour/--no-colour", "-c/-C",
        help="Use coloured output"
    )
) -> None:
    """
    🎯 Get personalised project recommendations based on your preferences.

    This command runs the interactive recommendation system that asks you
    questions about your interests and provides tailored project suggestions
    with niche discovery insights.
    """
    try:
        # Load and validate project data
        console.print("[blue]Loading project data...[/blue]")
        loader = ProjectLoader()
        projects_list = loader.load_from_json(data_file)  # Renamed for clarity

        # Wrap projects in ProjectData container
        project_data_container = ProjectData(projects=projects_list)

        # Validate data
        validator = ProjectDataValidator()
        # Validate the list of projects from the container
        validation_errors = validator.validate_projects(project_data_container.projects)

        if validation_errors:
            console.print("[red]❌ Data validation failed:[/red]")
            for error in validation_errors:
                console.print(f"  • {error}")
            raise typer.Exit(1)

        # Configure the system
        settings = Settings()

        # Apply CLI overrides for settings used as defaults
        settings.display.default_results_count = max_results
        settings.display.use_colour_output = colour

        # Create recommender
        recommender = ProjectRecommender(settings=settings)

        final_output_filename: Optional[str]
        final_max_results: int  # 0 means all

        user_prefs_for_recommender: UserPreferences
        if interactive:
            # Pass the ProjectData container to get_interactive_preferences
            user_prefs_for_recommender = (
                recommender.get_interactive_preferences(project_data_container)
            )
            # Interactive prompts override CLI options for filename and count
            final_output_filename = user_prefs_for_recommender.results_filename
            final_max_results = user_prefs_for_recommender.results_count
        else:
            # Non-interactive: use CLI options or defaults
            user_prefs_for_recommender = UserPreferences()
            final_output_filename = output_file  # From --output CLI option
            final_max_results = max_results    # From --max-results CLI option

        console.print("\\\\n[green]🚀 Starting recommendation process...[/green]")
        # Pass the ProjectData container to recommend_projects
        recommendations = recommender.recommend_projects(
            project_data=project_data_container,
            preferences=user_prefs_for_recommender
        )

        if not recommendations:
            console.print(
                "[yellow]No recommendations generated. "
                "Please check your preferences.[/yellow]"
            )
            raise typer.Exit(0)

        num_actually_written: int
        writer_max_results_arg: Optional[int]

        if final_max_results == 0:
            num_actually_written = len(recommendations)
            writer_max_results_arg = None  # Writer interprets None as all
        else:
            num_actually_written = min(len(recommendations), final_max_results)
            writer_max_results_arg = num_actually_written

        from .utils.io import ResultsWriter
        writer = ResultsWriter()
        actual_path_obj = writer.write_recommendations_markdown(
            recommendations,
            filename=final_output_filename,
            max_results=writer_max_results_arg
        )
        actual_output_path_str = str(actual_path_obj)

        if num_actually_written > 0:
            console.print(
                f"\\\\n[green]✅ Top {num_actually_written} project recommendations saved![/green]"
            )

        console.print(f"[blue]📁 Results saved to: {actual_output_path_str}[/blue]")

    except FileNotFoundError as error:
        console.print(f"[red]File not found: {error}[/red]")
        raise typer.Exit(1)
    except Exception as error:
        console.print(f"[red]An error occurred: {error}[/red]")
        raise typer.Exit(1)


@app.command()
def analyse(
    data_file: str = typer.Argument(
        "projects.json",
        help="Path to the JSON file containing project data"
    ),
    output_file: Optional[str] = typer.Option(
        None,
        "--output", "-o",
        help="Output file for analysis report (default: console only)"
    ),
    export_json: bool = typer.Option(
        False,
        "--json",
        help="Also export statistics as JSON"
    ),
    colour: bool = typer.Option(
        True,
        "--colour/--no-colour", "-c/-C",
        help="Use coloured output"
    )
) -> None:
    """
    📊 Analyse project data and generate comprehensive statistics.

    This command analyses the project dataset and provides detailed statistics
    about supervisors, topics, methodologies, and other project attributes.
    """
    try:
        summariser = ProjectSummariser(use_colour_output=colour)
        results = summariser.analyse_projects_from_file(data_file, output_filename=output_file)
        if export_json:
            summariser.export_statistics_json(results['projects'], filename=None)
    except FileNotFoundError as error:
        console.print(f"[red]File not found: {error}[/red]")
        raise typer.Exit(1)
    except Exception as error:
        console.print(f"[red]An error occurred: {error}[/red]")
        raise typer.Exit(1)


@app.command()
def validate(
    data_file: str = typer.Argument(
        "projects.json",
        help="Path to the JSON file to validate"
    ),
    strict: bool = typer.Option(
        False,
        "--strict",
        help="Treat warnings as errors"
    )
) -> None:
    """
    ✅ Validate project data file for correctness and completeness.

    This command validates the structure and content of a project data file,
    checking for required fields, data types, and consistency issues.
    """
    try:
        loader = ProjectLoader()
        projects = loader.load_from_json(data_file)
        validator = ProjectDataValidator()
        errors = validator.validate_projects(projects)
        if errors:
            console.print("[red]Validation errors found:[/red]")
            for error in errors:
                console.print(f"  • {error}")
            if strict:
                raise typer.Exit(1)
        else:
            console.print("[green]No validation errors found.[/green]")
    except FileNotFoundError as error:
        console.print(f"[red]File not found: {error}[/red]")
        raise typer.Exit(1)
    except Exception as error:
        console.print(f"[red]An error occurred: {error}[/red]")
        raise typer.Exit(1)


@app.command()
def config(
    show: bool = typer.Option(
        False,
        "--show",
        help="Show current configuration"
    ),
    export: Optional[str] = typer.Option(
        None,
        "--export",
        help="Export configuration to file"
    )
) -> None:
    """
    ⚙️  Manage system configuration settings.

    This command allows you to view and export the current system
    configuration, including scoring weights, niche discovery settings,
    and display options.
    """
    if show or export:
        settings = Settings()
        config_dict = settings.to_dict()
        if show:
            console.print(config_dict)
        if export:
            import json
            with open(export, "w", encoding="utf-8") as f:
                json.dump(config_dict, f, indent=2)
            console.print(f"[green]Configuration exported to {export}[/green]")
    else:
        console.print("[yellow]No action specified. Use --show or --export.[/yellow]")


@app.command()
def version() -> None:
    """
    📋 Show version information.
    """
    console.print(Panel(
        "[bold blue]Project Chooser[/bold blue]\n"
        "Version: 1.0.0\n"
        "AI-powered academic project recommendation system\n"
        "with enhanced niche discovery capabilities.",
        title="[bold green]Version Info[/bold green]",
        border_style="blue"
    ))


if __name__ == "__main__":
    app()
