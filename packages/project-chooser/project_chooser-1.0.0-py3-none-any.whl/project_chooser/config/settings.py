"""
Configuration settings and constants for the project chooser system.

This module centralises all configuration parameters, making the system
highly configurable and maintainable.
"""

from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class ScoringWeights:
    """
    Configuration for scoring weights used in project matching.

    Attributes
    ----------
    degree : float
        Weight for degree programme match.
    co_requisite : float
        Weight for co-requisite module match.
    co_requisite_penalty : float
        Penalty for missing co-requisite.
    topic : float
        Weight for topic matches.
    methodology : float
        Weight for research methodology matches.
    focus : float
        Weight for mathematical focus matches.
    programming : float
        Weight for programming language matches.
    supervisor : float
        Weight for supervisor preference.
    supervisor_penalty : float
        Penalty for avoided supervisors.
    """

    degree: float = 15.0
    co_requisite: float = 10.0
    co_requisite_penalty: float = -20.0  # Penalty if co-req specified and not met
    topic: float = 5.0
    methodology: float = 5.0
    focus: float = 5.0
    programming: float = 5.0
    supervisor: float = 10.0
    supervisor_penalty: float = -50.0  # Penalty for avoiding a supervisor
    niche_topic_bonus: float = 15.0
    niche_skill_bonus: float = 10.0
    # New caps for max_score calculation
    max_score_topic_cap: int = 3  # Max number of topic matches to count in max_score
    max_score_method_cap: int = 2  # Max number of method matches to count in max_score
    max_score_focus_cap: int = 2  # Max number of focus matches to count in max_score
    max_score_programming_cap: int = 2  # Max number of programming matches to count in max_score


@dataclass
class NicheDiscoveryConfig:
    """
    Configuration for niche discovery features.

    Attributes
    ----------
    min_niche_threshold : int
        Maximum frequency for a topic to be considered "niche".
    cross_domain_bonus_per_additional_domain : float
        Bonus factor applied for each additional academic domain a project spans beyond the first.
    topic_exploration_count : int
        Number of additional topics to explore.
    serendipity_factor : float
        Weight for unexpected/serendipitous matches.
    max_niche_recommendations : int
        Maximum number of niche topics to include in recommendations.
    """

    min_niche_threshold: int = 3
    topic_exploration_count: int = 8
    cross_domain_bonus_per_additional_domain: float = 0.5  # Renamed and default set
    serendipity_factor: float = 0.3  # Retained for _calculate_serendipity_bonus logic
    max_niche_recommendations: int = 3


@dataclass
class DisplayConfig:
    """
    Configuration for display and output formatting.

    Attributes
    ----------
    default_results_count : int
        Default number of recommendations to show.
    default_results_filename : str
        Default filename for saving results.
    max_topics_display : int
        Maximum number of topics to show in selection.
    show_debug_info : bool
        Whether to show debugging information.
    use_colour_output : bool
        Whether to use coloured terminal output.
    """

    default_results_count: int = 5
    default_results_filename: str = "project_recommendations.md"
    max_topics_display: int = 15
    show_debug_info: bool = False
    use_colour_output: bool = True


@dataclass
class InteractionConfig:
    """
    Configuration for user interaction and questioning.

    Attributes
    ----------
    max_questions : int
        Maximum number of questions to ask user.
    min_projects_threshold : int
        Stop asking questions when this many projects remain.
    initial_questions : List[str]
        Questions to always ask first.
    enable_bayesian_questioning : bool
        Whether to use Bayesian question selection.
    bayesian_info_gain_threshold : float
        Minimum information gain to ask a Bayesian-selected question.
    """

    max_questions: int = 7
    min_projects_threshold: int = 5
    initial_questions: List[str] = None  # type: ignore
    enable_bayesian_questioning: bool = True
    bayesian_info_gain_threshold: float = 0.25  # Default to a more conservative 0.25

    def __post_init__(self) -> None:
        """Set default initial questions if none provided."""
        if self.initial_questions is None:
            self.initial_questions = ["degree"]


# Semantic groupings for topic clustering
SEMANTIC_GROUPS: Dict[str, List[str]] = {
    "pure_algebra": [
        "Group Theory",
        "Abstract Algebra",
        "Algebraic Topology"
    ],
    "number_theory": [
        "Number Theory",
        "Algebraic Number Theory",
        "Cryptography"
    ],
    "analysis": [
        "Complex Analysis",
        "Mathematical Analysis",
        "Differential Geometry"
    ],
    "applied_analysis": [
        "Calculus",
        "Partial Differential Equations",
        "Functional Analysis"
    ],
    "optimisation": [
        "Optimization",
        "Operations Research",
        "Linear Programming"
    ],
    "statistics": [
        "Statistics",
        "Probability Theory",
        "Bayesian Analysis"
    ],
    "finance": [
        "Financial Mathematics",
        "Actuarial Science",
        "Risk Management"
    ],
    "biology": [
        "Mathematical Biology",
        "Theoretical Biology",
        "Epidemiology"
    ],
    "machine_learning": [
        "Machine Learning",
        "Pattern Recognition",
        "Neural Networks"
    ],
    "computer_vision": [
        "Computer Vision",
        "Image Processing",
        "Signal Processing"
    ],
    "data_science": [
        "Data Science",
        "Data Mining",
        "Statistical Learning"
    ],
    "dynamics": [
        "Chaos Theory",
        "Predator-Prey Dynamics",
        "Dynamical Systems"
    ],
    "computation": [
        "Monte Carlo Methods",
        "Numerical Methods",
        "Scientific Computing"
    ],
    "education": [
        "Mathematics Education",
        "History of Mathematics"
    ],
    "philosophy": [
        "Philosophy of Mathematics",
        "Logic"
    ],
    "modelling": [
        "Agent-Based Modeling",
        "Mathematical Modeling"
    ],
    "environment": [
        "Environmental Science",
        "Climate Modeling"
    ],
    "logic_cs": [
        "Logic/Theoretical Computer Science",
        "Proof Construction"
    ]
}

# Cross-domain semantic groups for interdisciplinary detection
CROSS_DOMAIN_GROUPS: Dict[str, List[str]] = {
    "algebra": [
        "Group Theory",
        "Abstract Algebra",
        "Number Theory"
    ],
    "analysis": [
        "Complex Analysis",
        "Mathematical Analysis",
        "Calculus"
    ],
    "applied": [
        "Machine Learning",
        "Data Science",
        "Financial Mathematics"
    ],
    "dynamics": [
        "Chaos Theory",
        "Dynamical Systems"
    ],
    "other": []  # Will contain everything else
}

# Available question types for interactive system
QUESTION_TYPES: List[str] = [
    "degree",
    "current_modules",
    "avoid_supervisors",
    "preferred_topics",
    "preferred_methods",
    "math_focus",
    "programming"
]

# Degree categories for validation and analysis
DEGREE_CATEGORIES: Dict[str, List[str]] = {
    "mathematics": [
        "mathematics",
        "mathematics with philosophy",
        "mathematics and theoretical physics",
        "mathematics and computer science",
        "mathematics with computer science",
        "mathematics with chemistry",
        "mathematics with theoretical physics"
    ],
    "physics": [
        "physics",
        "physics with philosophy",
        "mathematics and theoretical physics"
    ]
}


class Settings:
    """
    Main settings class that aggregates all configuration options.

    This class provides a centralised interface to all configuration
    parameters and can be easily extended or modified.
    """

    def __init__(self) -> None:
        """Initialise settings with default values."""
        self.scoring = ScoringWeights()
        self.niche_discovery = NicheDiscoveryConfig()
        self.display = DisplayConfig()
        self.interaction = InteractionConfig()
        self.semantic_groups = SEMANTIC_GROUPS
        self.cross_domain_groups = CROSS_DOMAIN_GROUPS
        self.question_types = QUESTION_TYPES
        self.degree_categories = DEGREE_CATEGORIES

    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary format."""
        return {
            "scoring": {
                "degree": self.scoring.degree,
                "co_requisite": self.scoring.co_requisite,
                "co_requisite_penalty": self.scoring.co_requisite_penalty,
                "topic": self.scoring.topic,
                "methodology": self.scoring.methodology,
                "focus": self.scoring.focus,
                "programming": self.scoring.programming,
                "supervisor": self.scoring.supervisor,
                "supervisor_penalty": self.scoring.supervisor_penalty,
            },
            "niche_discovery": {
                "min_niche_threshold": self.niche_discovery.min_niche_threshold,
                "topic_exploration_count": self.niche_discovery.topic_exploration_count,
                "cross_domain_bonus_per_additional_domain": (
                    self.niche_discovery.cross_domain_bonus_per_additional_domain
                ),
                "serendipity_factor": self.niche_discovery.serendipity_factor,
                "max_niche_recommendations": self.niche_discovery.max_niche_recommendations,
            },
            "display": {
                "default_results_count": self.display.default_results_count,
                "default_results_filename": self.display.default_results_filename,
                "max_topics_display": self.display.max_topics_display,
                "show_debug_info": self.display.show_debug_info,
                "use_colour_output": self.display.use_colour_output,
            },
            "interaction": {
                "max_questions": self.interaction.max_questions,
                "min_projects_threshold": self.interaction.min_projects_threshold,
                "initial_questions": self.interaction.initial_questions,
                "enable_bayesian_questioning": self.interaction.enable_bayesian_questioning,
                "bayesian_info_gain_threshold": self.interaction.bayesian_info_gain_threshold,
            }
        }

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "Settings":
        """Create settings from dictionary configuration."""
        settings = cls()

        if "scoring" in config_dict:
            scoring_config = config_dict["scoring"]
            settings.scoring = ScoringWeights(**scoring_config)

        if "niche_discovery" in config_dict:
            niche_config = config_dict["niche_discovery"]
            settings.niche_discovery = NicheDiscoveryConfig(**niche_config)

        if "display" in config_dict:
            display_config = config_dict["display"]
            settings.display = DisplayConfig(**display_config)

        if "interaction" in config_dict:
            interaction_config = config_dict["interaction"]
            settings.interaction = InteractionConfig(**interaction_config)

        return settings


# Global default settings instance
DEFAULT_CONFIG = Settings()
