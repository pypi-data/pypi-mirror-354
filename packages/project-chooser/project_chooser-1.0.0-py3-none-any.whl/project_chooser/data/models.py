"""
Data models for the project chooser system.

This module defines Pydantic models for project data structure validation
and type safety throughout the application.
"""

from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class Project(BaseModel):
    """
    Model representing an individual academic project.

    Attributes
    ----------
    project_id : str
        Unique identifier for the project.
    title : str
        Descriptive title of the project.
    supervisor : str
        Name of the project supervisor.
    student_capacity : int
        Number of students that can be assigned to this project.
    related_modules : List[str]
        List of academic modules related to this project.
    co_requisite : str
        Required co-requisite module, or "None" if not applicable.
    applicable_degrees : List[str]
        List of degree programmes for which this project is suitable.
    abstract : Optional[str]
        Detailed description of the project (optional).
    general_topics : List[str]
        List of general research topics covered by the project.
    mathematical_focus : List[str]
        List of specific mathematical focus areas.
    programming_languages : List[str]
        List of programming languages used in the project.
    research_methodology : List[str]
        List of research methodologies employed.
    bibliography : Optional[List[str]]
        List of relevant bibliographic references (optional).
    """

    project_id: str = Field(alias="id", description="Unique project identifier")
    title: str = Field(description="Project title")
    supervisor: str = Field(description="Project supervisor name")
    student_capacity: int = Field(
        ge=1, description="Number of students this project can accommodate"
    )
    related_modules: List[str] = Field(
        description="Academic modules related to this project"
    )
    co_requisite: str = Field(
        description="Required co-requisite module or 'None'"
    )
    applicable_degrees: List[str] = Field(
        description="Degree programmes suitable for this project"
    )
    abstract: Optional[str] = Field(
        default=None, description="Detailed project description"
    )
    general_topics: List[str] = Field(
        description="General research topics covered"
    )
    mathematical_focus: List[str] = Field(
        description="Specific mathematical focus areas"
    )
    programming_languages: List[str] = Field(
        description="Programming languages used"
    )
    research_methodology: List[str] = Field(
        description="Research methodologies employed"
    )
    bibliography: Optional[List[str]] = Field(
        default=None, description="Relevant bibliographic references"
    )

    @field_validator("student_capacity")
    @classmethod
    def validate_student_capacity(cls, capacity_value: int) -> int:
        """Ensure student capacity is positive."""
        if capacity_value < 1:
            raise ValueError("Student capacity must be at least 1")
        return capacity_value

    @field_validator("programming_languages", mode="before")
    @classmethod
    def filter_none_languages(cls, languages: List[str]) -> List[str]:
        """Remove 'None' entries from programming languages."""
        return [lang for lang in languages if lang.lower() != "none"]

    class Config:
        """Pydantic configuration."""
        populate_by_name = True
        validate_assignment = True


class ProjectData(BaseModel):
    """
    Model representing the root structure of project data.

    Attributes
    ----------
    projects : List[Project]
        List of all available projects.
    """

    projects: List[Project] = Field(description="List of available projects")

    @field_validator("projects")
    @classmethod
    def validate_projects_not_empty(cls, projects_list: List[Project]) -> List[Project]:
        """Ensure projects list is not empty."""
        if not projects_list:
            raise ValueError("Projects list cannot be empty")
        return projects_list


class UserPreferences(BaseModel):
    """
    Model representing user preferences for project recommendation.

    Attributes
    ----------
    degree : Optional[str]
        User's degree programme.
    current_modules : List[str]
        Modules the user is currently taking.
    avoid_supervisors : List[str]
        Supervisors the user wishes to avoid.
    preferred_supervisors : List[str]  # Added field
        Supervisors the user prefers.
    preferred_topics : List[str]
        Topics the user is interested in.
    preferred_methods : List[str]
        Research methodologies the user prefers.
    mathematical_focus : List[str]
        Mathematical areas the user wants to focus on.
    programming_languages : List[str]
        Programming languages the user knows.
    results_count : int
        Number of recommendations to return.
    results_filename : str
        Filename for saving results.
    """

    degree: Optional[str] = Field(default=None, description="User's degree programme")
    current_modules: List[str] = Field(
        default_factory=list, description="Currently enrolled modules"
    )
    avoid_supervisors: List[str] = Field(
        default_factory=list, description="Supervisors to avoid"
    )
    preferred_supervisors: List[str] = Field(  # Added field
        default_factory=list, description="Preferred supervisors"
    )
    preferred_topics: List[str] = Field(
        default_factory=list, description="Preferred research topics"
    )
    preferred_methods: List[str] = Field(
        default_factory=list, description="Preferred research methodologies"
    )
    mathematical_focus: List[str] = Field(
        default_factory=list, description="Preferred mathematical focus areas"
    )
    programming_languages: List[str] = Field(
        default_factory=list, description="Known programming languages"
    )
    results_count: int = Field(default=5, ge=0, description="Number of results to return")
    results_filename: str = Field(
        default="project_recommendations.md", description="Output filename"
    )


class RecommendationResult(BaseModel):
    """
    Model representing a single project recommendation result.

    Attributes
    ----------
    project : Project
        The recommended project.
    score : float
        Calculated match score.
    base_score : float
        Score before niche bonuses.
    niche_bonus : float
        Additional score from niche discovery.
    match_reasons : List[str]
        Reasons why this project matches user preferences.
    niche_insights : List[str]
        Insights into niche or interdisciplinary aspects.
    percentage_match : float
        Match score as percentage of maximum possible score.
    """

    project: Project = Field(description="The recommended project")
    score: float = Field(description="Total calculated match score")
    base_score: float = Field(description="Base score before niche bonuses")
    niche_bonus: float = Field(description="Additional score from niche discovery")
    match_reasons: List[str] = Field(description="Reasons for the match")
    niche_insights: List[str] = Field(default_factory=list, description="Niche discovery insights")
    percentage_match: float = Field(
        ge=0.0, le=100.0, description="Match percentage"
    )

    @field_validator("score", "base_score", "niche_bonus")
    @classmethod
    def validate_scores(cls, score_value: float) -> float:
        """Ensure scores are finite numbers."""
        if not isinstance(score_value, (int, float)) or not (
            -float("inf") < score_value < float("inf")
        ):
            raise ValueError("Score must be a finite number")
        return float(score_value)
