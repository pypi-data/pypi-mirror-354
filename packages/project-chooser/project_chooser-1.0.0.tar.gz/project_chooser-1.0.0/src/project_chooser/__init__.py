"""
Project Chooser - AI-powered academic project recommendation system.

This package provides intelligent project recommendation capabilities with
advanced niche discovery features to help students find suitable academic
projects based on their interests and preferences.
"""

__version__ = "1.0.0"
__author__ = "Project Chooser Team"

from .core.recommender import ProjectRecommender
from .data.models import Project, ProjectData, UserPreferences, RecommendationResult
from .data.loader import ProjectLoader
from .analysis.summariser import ProjectSummariser
from .utils.display import RecommendationDisplayer, StatisticsFormatter

__all__ = [
    "ProjectRecommender",
    "Project",
    "ProjectData",
    "UserPreferences",
    "RecommendationResult",
    "ProjectLoader",
    "ProjectSummariser",
    "RecommendationDisplayer",
    "StatisticsFormatter",
]
