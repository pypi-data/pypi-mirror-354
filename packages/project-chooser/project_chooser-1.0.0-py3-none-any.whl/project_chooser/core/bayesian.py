"""
Bayesian inference utilities for the project chooser system.

This module provides statistical methods for intelligent question selection
and preference learning.
"""

import math
from typing import List, Dict, Any, Optional
from collections import Counter

from ..config.settings import Settings
from ..data.models import Project


def bayesian_update(prior_probability: float, likelihood: float) -> float:
    """
    Perform a simple Bayesian update for binary features.

    Parameters
    ----------
    prior_probability : float
        Prior probability estimate (between 0 and 1).
    likelihood : float
        Likelihood of evidence given hypothesis (between 0 and 1).

    Returns
    -------
    float
        Updated posterior probability.

    Notes
    -----
    This implements a simplified Bayesian update assuming a binary outcome
    and uniform prior for the alternative hypothesis.
    """
    if not (0 <= prior_probability <= 1):
        raise ValueError("Prior probability must be between 0 and 1")
    if not (0 <= likelihood <= 1):
        raise ValueError("Likelihood must be between 0 and 1")

    numerator = prior_probability * likelihood
    denominator = numerator + (1 - prior_probability) * (1 - likelihood)

    if denominator == 0:
        return prior_probability

    return numerator / denominator


def calculate_entropy(probabilities: List[float]) -> float:
    """
    Calculate the Shannon entropy of a probability distribution.

    Parameters
    ----------
    probabilities : List[float]
        List of probability values that should sum to 1.

    Returns
    -------
    float
        Shannon entropy in bits.

    Notes
    -----
    Entropy measures the uncertainty in a probability distribution.
    Higher entropy indicates more uncertainty/information content.
    """
    if not probabilities:
        return 0.0

    # Normalise probabilities to ensure they sum to 1
    total = sum(probabilities)
    if total == 0:
        return 0.0

    normalised_probs = [prob / total for prob in probabilities]

    entropy_value = 0.0
    for probability in normalised_probs:
        if probability > 0:
            entropy_value -= probability * math.log2(probability)

    return entropy_value


def information_gain(
    projects: List[Project],
    feature_key: str,
    current_filters: Optional[Dict[str, Any]] = None
) -> float:
    """
    Calculate the expected information gain from asking about a feature.

    Parameters
    ----------
    projects : List[Project]
        List of projects to consider.
    feature_key : str
        The feature/question to evaluate for information gain.
    current_filters : Optional[Dict[str, Any]]
        Current user preferences/filters applied.

    Returns
    -------
    float
        Expected information gain from asking this question.

    Notes
    -----
    Information gain measures how much uncertainty is reduced by knowing
    the answer to a particular question. Higher values indicate more
    informative questions.
    """
    if current_filters is None:
        current_filters = {}

    # Filter projects based on current preferences
    filtered_projects = _apply_filters(projects, current_filters)

    if not filtered_projects:
        return 0.0

    # Get possible values for this feature
    possible_values = _get_feature_values(filtered_projects, feature_key)

    if not possible_values:
        return 0.0

    # Calculate entropy for each possible answer
    total_projects = len(filtered_projects)
    weighted_entropy = 0.0

    for value in possible_values:
        # Projects that would match this value
        matching_projects = _filter_by_feature_value(
            filtered_projects, feature_key, value
        )

        if not matching_projects:
            continue

        # Weight by proportion of projects
        weight = len(matching_projects) / total_projects

        # Calculate entropy of remaining projects after this answer
        # For simplicity, we'll use the number of remaining projects as a proxy
        if len(matching_projects) == 0:
            entropy_after = 0.0
        else:
            # Simplified entropy based on remaining project distribution
            entropy_after = math.log2(len(matching_projects))

        weighted_entropy += weight * entropy_after

    # Current entropy (before asking the question)
    current_entropy = math.log2(len(filtered_projects)) if filtered_projects else 0.0

    # Information gain is reduction in entropy
    return max(0.0, current_entropy - weighted_entropy)


def select_most_informative_question(
    projects: List[Project],
    candidate_questions: List[str],
    current_filters: Optional[Dict[str, Any]] = None,
    settings: Optional[Settings] = None  # Use Settings type hint
) -> Optional[str]:
    """
    Select the question that provides the maximum expected information gain.

    Parameters
    ----------
    projects : List[Project]
        List of available projects.
    candidate_questions : List[str]
        List of question types to consider.
    current_filters : Optional[Dict[str, Any]]
        Current user preferences/filters.
    settings : Optional[Settings]
        Configuration settings.

    Returns
    -------
    Optional[str]
        The most informative question to ask, or None if no good questions remain.
    """
    if not candidate_questions:
        return None

    best_question = None
    max_information_gain = -1.0

    for question in candidate_questions:
        gain = information_gain(projects, question, current_filters)

        if gain > max_information_gain:
            max_information_gain = gain
            best_question = question

    # Only return a question if it provides meaningful information gain
    # Use a default threshold if settings are not provided or attribute is missing
    threshold = 0.1  # Default threshold
    if settings and hasattr(settings, 'interaction') and \
       hasattr(settings.interaction, 'bayesian_info_gain_threshold'):
        threshold = settings.interaction.bayesian_info_gain_threshold

    return best_question if max_information_gain > threshold else None


def _apply_filters(
    projects: List[Project],
    filters: Dict[str, Any]
) -> List[Project]:
    """Apply current user filters to project list."""
    filtered = projects.copy()

    for filter_key, filter_value in filters.items():
        if filter_key == "degree" and filter_value:
            filtered = [
                project for project in filtered
                if filter_value in project.applicable_degrees
            ]
        elif filter_key == "current_modules" and filter_value:
            filtered = [
                project for project in filtered
                if (project.co_requisite in filter_value or
                    project.co_requisite.lower() == "none")
            ]
        elif filter_key == "avoid_supervisors" and filter_value:
            filtered = [
                project for project in filtered
                if project.supervisor not in filter_value
            ]
        elif filter_key == "preferred_topics" and filter_value:
            filtered = [
                project for project in filtered
                if set(filter_value) & set(project.general_topics)
            ]
        elif filter_key == "preferred_methods" and filter_value:
            filtered = [
                project for project in filtered
                if set(filter_value) & set(project.research_methodology)
            ]
        elif filter_key == "math_focus" and filter_value:
            filtered = [
                project for project in filtered
                if set(filter_value) & set(project.mathematical_focus)
            ]
        elif filter_key == "programming" and filter_value:
            filtered = [
                project for project in filtered
                if set(filter_value) & set(project.programming_languages)
            ]

    return filtered


def _get_feature_values(projects: List[Project], feature_key: str) -> List[str]:
    """Extract all possible values for a given feature from projects."""
    values = set()

    for project in projects:
        if feature_key == "degree":
            values.update(project.applicable_degrees)
        elif feature_key == "current_modules":
            if project.co_requisite.lower() != "none":
                values.add(project.co_requisite)
        elif feature_key == "avoid_supervisors":
            values.add(project.supervisor)
        elif feature_key == "preferred_topics":
            values.update(project.general_topics)
        elif feature_key == "preferred_methods":
            values.update(project.research_methodology)
        elif feature_key == "math_focus":
            values.update(project.mathematical_focus)
        elif feature_key == "programming":
            values.update(
                lang for lang in project.programming_languages
                if lang.lower() != "none"
            )

    return list(values)


def _filter_by_feature_value(
    projects: List[Project],
    feature_key: str,
    value: str
) -> List[Project]:
    """Filter projects that match a specific feature value."""
    filtered = []

    for project in projects:
        matches = False

        if feature_key == "degree":
            matches = value in project.applicable_degrees
        elif feature_key == "current_modules":
            matches = value == project.co_requisite
        elif feature_key == "avoid_supervisors":
            matches = value != project.supervisor
        elif feature_key == "preferred_topics":
            matches = value in project.general_topics
        elif feature_key == "preferred_methods":
            matches = value in project.research_methodology
        elif feature_key == "math_focus":
            matches = value in project.mathematical_focus
        elif feature_key == "programming":
            matches = value in project.programming_languages

        if matches:
            filtered.append(project)

    return filtered


def estimate_user_preferences(
    user_answers: Dict[str, Any],
    projects: List[Project]
) -> Dict[str, float]:
    """
    Estimate user preferences based on their answers using Bayesian inference.

    Parameters
    ----------
    user_answers : Dict[str, Any]
        User's answers to questions.
    projects : List[Project]
        Available projects to learn from.

    Returns
    -------
    Dict[str, float]
        Estimated preference scores for different attributes.
    """
    preferences = {}

    # For each answered question, update our belief about user preferences
    for question_type, answer in user_answers.items():
        if question_type == "preferred_topics" and answer:
            # Learn about topic preferences
            topic_counter = Counter(
                topic for project in projects
                for topic in project.general_topics
            )

            for topic in answer:
                # Higher preference for chosen topics
                preferences[f"topic_{topic}"] = 0.8

                # Also increase preference for related topics (simplified)
                for related_topic, count in topic_counter.most_common(10):
                    if related_topic != topic and related_topic not in answer:
                        # Weak positive correlation for common topics
                        preferences[f"topic_{related_topic}"] = preferences.get(
                            f"topic_{related_topic}", 0.3
                        ) + 0.1

    return preferences
