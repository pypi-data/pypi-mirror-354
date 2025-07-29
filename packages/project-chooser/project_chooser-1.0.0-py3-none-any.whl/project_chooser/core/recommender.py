"""
Main project recommendation engine.

This module coordinates all aspects of the recommendation system,
from user interaction to scoring and result generation.
"""

import logging
from typing import List, Dict, Any, Tuple, Set, Optional

import questionary
from rich.console import Console

from ..config.settings import Settings
from ..data.models import (
    Project,
    ProjectData,
    UserPreferences,
    RecommendationResult,
)
from .bayesian import select_most_informative_question
from .niche_discovery import NicheDiscoveryEngine

# Initialize logger for this module
logger = logging.getLogger(__name__)


class ProjectRecommender:
    """Core class for handling project recommendations."""

    def __init__(self, settings: Settings):
        """
        Initialise the Recommender with configuration settings.
        """
        self.settings = settings
        self.niche_engine = NicheDiscoveryEngine(settings)
        # Configure logging if not already configured by a higher-level module
        if not logging.getLogger().hasHandlers():
            # Access display settings via self.settings.display
            log_level = logging.DEBUG if self.settings.display.show_debug_info else logging.INFO
            logging.basicConfig(
                level=log_level,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        logger.info("ProjectRecommender initialized.")

    def _get_unique_attributes(self, project_data: ProjectData, attribute_name: str) -> List[str]:
        """Helper to get unique, sorted, non-empty attribute values from all projects."""
        all_values: Set[str] = set()
        for project in project_data.projects:
            values = getattr(project, attribute_name, None)
            if values:
                if isinstance(values, list):
                    for value in values:
                        if value and value.strip().lower() != "none":
                            all_values.add(value.strip())
                elif isinstance(values, str):  # For single string attributes like supervisor
                    if values and values.strip().lower() != "none":
                        all_values.add(values.strip())
        return sorted(list(all_values))

    def get_interactive_preferences(self, project_data: ProjectData) -> UserPreferences:
        """
        Interactively gathers user preferences using questionary with intelligent filtering.
        """
        console = Console()
        prefs = UserPreferences()
        
        console.print(
            "\n[bold cyan]Please enter your preferences:[/bold cyan]"
        )

        # Step 1: Degree selection with immediate filtering
        all_degrees = self._get_unique_attributes(project_data, "applicable_degrees")
        if all_degrees:
            degree_choices = all_degrees + ["Other/Not listed"]
            degree_response = questionary.select(
                "Select your degree programme:",
                choices=degree_choices,
                default=all_degrees[0] if all_degrees else "Other/Not listed"
            ).ask()
            
            if degree_response == "Other/Not listed" or degree_response is None:
                console.print(
                    "[red]No projects are available for degrees not listed. "
                    "Exiting.[/red]"
                )
                raise SystemExit("No applicable projects found for the selected degree.")
            else:
                prefs.degree = degree_response
        else:
            console.print("[red]No degree information found in project data.[/red]")
            raise SystemExit("No degree information available.")

        # Filter projects immediately based on degree
        filtered_projects = [
            p for p in project_data.projects
            if prefs.degree in p.applicable_degrees
        ]
        
        if not filtered_projects:
            console.print(f"[red]No projects found for degree: {prefs.degree}[/red]")
            raise SystemExit("No applicable projects found for the selected degree.")
        
        console.print(
            f"[green]Found {len(filtered_projects)} projects for {prefs.degree}[/green]"
        )
        
        # Create filtered project data for subsequent choices
        filtered_project_data = ProjectData(projects=filtered_projects)

        # Step 2: Get choices from filtered projects only
        filtered_topics = self._get_unique_attributes(
            filtered_project_data, "general_topics"
        )
        if filtered_topics:
            preferred_topics_list = questionary.checkbox(
                "Select your preferred general topics:",
                choices=filtered_topics,
            ).ask()
            if preferred_topics_list is not None:
                prefs.preferred_topics = preferred_topics_list

        filtered_methods = self._get_unique_attributes(
            filtered_project_data, "research_methodology"
        )
        if filtered_methods:
            preferred_methods_list = questionary.checkbox(
                "Select your preferred research methodologies:",
                choices=filtered_methods,
            ).ask()
            if preferred_methods_list is not None:
                prefs.preferred_methods = preferred_methods_list

        filtered_focus_areas = self._get_unique_attributes(
            filtered_project_data, "mathematical_focus"
        )
        if filtered_focus_areas:
            preferred_focus_list = questionary.checkbox(
                "Select your preferred mathematical focus areas:",
                choices=filtered_focus_areas,
            ).ask()
            if preferred_focus_list is not None:
                prefs.mathematical_focus = preferred_focus_list

        filtered_languages = self._get_unique_attributes(
            filtered_project_data, "programming_languages"
        )
        if filtered_languages:
            preferred_languages_list = questionary.checkbox(
                "Select your preferred programming languages:",
                choices=filtered_languages,
            ).ask()
            if preferred_languages_list is not None:
                prefs.programming_languages = preferred_languages_list
        
        filtered_supervisors = self._get_unique_attributes(
            filtered_project_data, "supervisor"
        )
        if filtered_supervisors:
            preferred_supervisors_list = questionary.checkbox(
                "Select your preferred supervisors (if any):",
                choices=filtered_supervisors,
            ).ask()
            if preferred_supervisors_list is not None:
                prefs.preferred_supervisors = preferred_supervisors_list
            
            avoid_supervisors_list = questionary.checkbox(
                "Select supervisors to avoid (if any):",
                choices=filtered_supervisors,
            ).ask()
            if avoid_supervisors_list is not None:
                prefs.avoid_supervisors = avoid_supervisors_list

        filtered_modules = self._get_unique_attributes(
            filtered_project_data, "related_modules"
        )
        if filtered_modules:
            current_modules_list = questionary.checkbox(
                "Select your current modules taken:",
                choices=filtered_modules,
            ).ask()
            if current_modules_list is not None:
                prefs.current_modules = current_modules_list

        # Results configuration
        results_count_str = questionary.text(
            "How many recommendations would you like to see?",
            default=str(self.settings.display.default_results_count)
        ).ask()
        
        if results_count_str is not None:
            try:
                prefs.results_count = int(results_count_str)
            except ValueError:
                console.print(
                    f"[yellow]Invalid number, using default: "
                    f"{self.settings.display.default_results_count}[/yellow]"
                )
                prefs.results_count = self.settings.display.default_results_count
        else:
            prefs.results_count = self.settings.display.default_results_count

        default_filename = (
            self.settings.display.default_results_filename or
            "project_recommendations.md"
        )
        results_filename_response = questionary.text(
            "Enter filename for results:",
            default=default_filename
        ).ask()
        
        if results_filename_response is not None and results_filename_response.strip():
            prefs.results_filename = results_filename_response
        else:
            prefs.results_filename = default_filename
            
        console.print("[green]Preferences collected.[/green]\n")
        return prefs

    def recommend_projects(
        self, preferences: UserPreferences, project_data: ProjectData
    ) -> List[RecommendationResult]:
        """
        Recommends projects based on user preferences and project data.
        """
        logger.info("Starting project recommendation process.")
        logger.debug(f"Initial user preferences: {preferences}")

        asked_questions: Set[str] = set()
        # Access interaction settings via self.settings.interaction
        if self.settings.interaction.enable_bayesian_questioning:
            logger.info("Starting Bayesian questioning phase.")
            preferences = self._ask_bayesian_questions(
                preferences, project_data, asked_questions
            )
            logger.info("Bayesian questioning phase completed.")
            logger.debug(f"Preferences after Bayesian questioning: {preferences}")

        max_score = self._calculate_max_score(preferences, project_data)
        if max_score == 0:
            logger.warning(
                "Max score is 0. Normalization will result in 0% for all projects. "
                "This might indicate an issue with preference settings or scoring weights."
            )
        logger.info(f"Calculated max_score for normalization: {max_score}")

        results: List[RecommendationResult] = []
        for project in project_data.projects:
            logger.debug(f"Processing project: {project.project_id} - {project.title}")
            base_score, match_reasons = self._calculate_base_match_score(
                preferences, project
            )

            niche_bonus, niche_debug_info = self.niche_engine.calculate_niche_bonus(
                project, preferences, project_data, detailed_output=True
            )

            current_match_reasons = list(match_reasons)  # Create a mutable copy
            if niche_debug_info:
                niche_insight_message = f"Niche Engine Insights: {niche_debug_info}"
                current_match_reasons.append(niche_insight_message)
                logger.debug(
                    f"  Project {project.project_id}: Niche insights added - {niche_debug_info}"
                )

            total_score = base_score + niche_bonus
            log_message_score = (
                f"  Project {project.project_id}: Base={base_score}, "
                f"Niche={niche_bonus}, Total={total_score}"
            )
            logger.debug(log_message_score)
            
            percentage_match = (total_score / max_score) * 100 if max_score > 0 else 0.0
            percentage_match = max(0.0, min(percentage_match, 100.0))  # Ensure between 0-100%
            logger.debug(
                f"  Project {project.project_id}: Percentage Match = {percentage_match:.2f}%"
            )

            results.append(
                RecommendationResult(
                    project=project,
                    score=total_score,
                    base_score=base_score,
                    niche_bonus=niche_bonus,
                    match_reasons=current_match_reasons,
                    niche_insights=[niche_debug_info] if niche_debug_info else [],
                    percentage_match=percentage_match,
                )
            )

        results.sort(key=lambda r: r.score, reverse=True)
        # Access display settings via self.settings.display (results_count is on preferences)
        log_message_results = (
            f"Generated {len(results)} recommendations. "
            f"Returning top {preferences.results_count}."
        )
        logger.info(log_message_results)

        final_results = results[: preferences.results_count]
        for res in final_results:
            logger.debug(
                f"Final Rec: {res.project.project_id}, Score: {res.score}, "
                f"Pct: {res.percentage_match:.2f}%"
            )
        return final_results

    def _ask_bayesian_questions(
        self,
        preferences: UserPreferences,
        project_data: ProjectData,
        asked_questions: Set[str],
    ) -> UserPreferences:
        """
        Interactively refines user preferences using Bayesian questioning.
        """
        logger.info("Bayesian questioning phase started.")

        # Access interaction settings via self.settings.interaction
        for i in range(self.settings.interaction.max_questions):
            logger.debug(f"Bayesian question iteration {i+1}")

            potential_questions_map = self._get_potential_questions(
                project_data, preferences, asked_questions
            )
            if not potential_questions_map:
                logger.info("No more potential questions to generate.")
                break

            current_filters = self._convert_preferences_to_filters(preferences)
            candidate_question_keys = list(potential_questions_map.keys())

            question_key = select_most_informative_question(
                project_data.projects,  # Pass List[Project]
                candidate_question_keys,
                current_filters,
                self.settings,  # Pass the whole settings object
            )

            if not question_key:
                logger.info("No more informative questions to ask based on current info gain.")
                break

            options_for_question = potential_questions_map.get(question_key, [])

            # --- Actual user interaction placeholder ---
            logger.info(
                f"Placeholder: Would ask question about: {question_key}. "
                f"Options: {options_for_question[:3]}..."  # Log first few options
            )

            # Simulate an answer or user action (e.g., user picks first option or skips)
            # For now, we will assume the question was asked and just mark it.
            # In a real scenario, you'd get an 'answer' and call:
            # simulated_answer = options_for_question[0] if options_for_question else None
            # if simulated_answer:
            # preferences = self._update_preferences_with_answer(
            # preferences, question_key, simulated_answer, options_for_question
            # )

            asked_questions.add(question_key)
            # If a specific option was chosen, you might mark that too:
            # if simulated_answer:
            # asked_questions.add(f"{question_key}_{simulated_answer}")

            log_msg_asked = (
                f"Added {question_key} to asked_questions. "
                f"Current asked: {asked_questions}"
            )
            logger.debug(log_msg_asked)

            # Placeholder for checking min_projects_threshold or other exit conditions
            # if len(filtered_projects_after_answer) <=\
            # self.settings.interaction.min_projects_threshold:
            #     logger.info("Min projects threshold reached after question.")
            #     break

        logger.debug(f"Returning preferences from Bayesian questioning: {preferences}")
        return preferences

    def _convert_preferences_to_filters(self, preferences: UserPreferences) -> Dict[str, Any]:
        """Converts UserPreferences object to a dictionary suitable for filtering."""
        filters: Dict[str, Any] = {}
        if preferences.degree:
            filters["degree"] = preferences.degree
        if preferences.current_modules:
            filters["current_modules"] = preferences.current_modules
        if preferences.avoid_supervisors:
            filters["avoid_supervisors"] = preferences.avoid_supervisors
        if preferences.preferred_topics:
            filters["preferred_topics"] = preferences.preferred_topics
        if preferences.preferred_methods:
            filters["preferred_methods"] = preferences.preferred_methods
        if preferences.mathematical_focus:
            filters["math_focus"] = preferences.mathematical_focus
        if preferences.programming_languages:
            filters["programming"] = preferences.programming_languages

        logger.debug(f"Converted preferences to filters: {filters}")
        return filters

    def _get_potential_questions(
        self,
        project_data: ProjectData,
        preferences: UserPreferences,
        asked_questions: Set[str]
    ) -> Dict[str, Any]:
        """
        Generates a dictionary of potential questions based on project attributes
        not yet covered.
        """
        logger.debug(f"Generating potential questions. Already asked: {asked_questions}")
        potential_q: Dict[str, Any] = {}

        all_topics = set()
        for p in project_data.projects:
            all_topics.update(p.general_topics)
        unasked_topics = [
            t for t in all_topics if t not in preferences.preferred_topics and
            f"topic_{t}" not in asked_questions
        ]
        if "topic" not in asked_questions and unasked_topics:  # Check general 'topic' key
            potential_q["topic"] = list(set(unasked_topics))  # Use set for unique topics

        all_methods = set()
        for p in project_data.projects:
            all_methods.update(p.research_methodology)
        unasked_methods = [
            m for m in all_methods if m not in preferences.preferred_methods and
            f"method_{m}" not in asked_questions
        ]
        if "methodology" not in asked_questions and unasked_methods:
            potential_q["methodology"] = list(set(unasked_methods))

        all_focus = set()
        for p in project_data.projects:
            all_focus.update(p.mathematical_focus)
        unasked_focus = [
            f for f in all_focus if f not in preferences.mathematical_focus and
            f"focus_{f}" not in asked_questions
        ]
        if "focus" not in asked_questions and unasked_focus:
            potential_q["focus"] = list(set(unasked_focus))

        all_prog_langs = set()
        for p in project_data.projects:
            all_prog_langs.update(p.programming_languages)
        all_prog_langs = {
            lang for lang in all_prog_langs if lang and lang.lower() != "none"
        }
        unasked_langs = [
            lang for lang in all_prog_langs if lang not in preferences.programming_languages and
            f"programming_{lang}" not in asked_questions  # Changed l to lang
        ]
        if "programming" not in asked_questions and unasked_langs:
            potential_q["programming"] = list(set(unasked_langs))

        all_supervisors = set()
        for p in project_data.projects:
            if p.supervisor:  # Ensure supervisor is not None
                all_supervisors.add(p.supervisor)
        unasked_supervisors = [
            s for s in all_supervisors
            if s not in preferences.preferred_supervisors and
            s not in preferences.avoid_supervisors and
            f"supervisor_{s}" not in asked_questions
        ]
        if "supervisor" not in asked_questions and unasked_supervisors:
            potential_q["supervisor"] = list(set(unasked_supervisors))

        logger.debug(f"Generated potential questions: {potential_q}")
        return potential_q

    def _update_preferences_with_answer(
        self,
        preferences: UserPreferences,
        question_key: str,
        answer: Any,
        question_options: Optional[List[str]] = None  # Options presented
    ) -> UserPreferences:
        """Updates UserPreferences based on the answer to a question."""
        logger.debug(f"Updating preferences for question '{question_key}' with answer '{answer}'")

        if answer and isinstance(answer, str):  # Ensure answer is not None and is a string
            if question_key == "topic":
                if answer not in preferences.preferred_topics:
                    preferences.preferred_topics.append(answer)
                    logger.info(f"Added '{answer}' to preferred topics.")
            elif question_key == "methodology":
                if answer not in preferences.preferred_methods:
                    preferences.preferred_methods.append(answer)
                    logger.info(f"Added '{answer}' to preferred methods.")
            elif question_key == "focus":
                if answer not in preferences.mathematical_focus:
                    preferences.mathematical_focus.append(answer)
                    logger.info(f"Added '{answer}' to mathematical focus areas.")
            elif question_key == "programming":
                if answer not in preferences.programming_languages:
                    preferences.programming_languages.append(answer)
                    logger.info(f"Added '{answer}' to preferred programming languages.")
            elif question_key == "supervisor":
                if answer not in preferences.preferred_supervisors:
                    preferences.preferred_supervisors.append(answer)
                    logger.info(f"Added '{answer}' to preferred supervisors.")
            else:
                log_warn_prefs = (
                    f"No specific preference update logic for question key: {question_key}"
                )
                logger.warning(log_warn_prefs)

        logger.debug(f"Updated preferences: {preferences}")
        return preferences

    def _calculate_max_score(
        self, preferences: UserPreferences, project_data: ProjectData
    ) -> float:
        """
        Calculates the theoretical maximum possible score a project could achieve
        based on current preferences and scoring weights, including niche bonuses.
        """
        max_score = 0.0
        weights = self.settings.scoring
        niche_config = self.settings.niche_discovery

        logger.debug("--- Calculating Max Score ---")
        logger.debug(f"User Preferences for Max Score Calc: {preferences}")
        logger.debug(f"Scoring Weights: {weights}")
        logger.debug(f"Niche Config: {niche_config}")

        # Base Score Components
        if preferences.degree:
            max_score += weights.degree
            logger.debug(f"  + MaxScore (Degree: {preferences.degree}): +{weights.degree}")

        if preferences.current_modules:  # Assumes a project could match this co-requisite
            max_score += weights.co_requisite
            logger.debug(f"  + MaxScore (Potential Co-requisite Match): +{weights.co_requisite}")
        else:
            # If user has no modules, an ideal project for them would also have no co-req,
            # or if it does, it's a match. Penalty is in base score.
            logger.debug(
                "  - MaxScore (User has no modules, co-req match assumed or no co-req project)"
            )

        if preferences.preferred_topics:
            num_matches = min(len(preferences.preferred_topics), weights.max_score_topic_cap)
            contribution = num_matches * weights.topic
            max_score += contribution
            log_msg_topic = (
                f"  + MaxScore (Topics - {len(preferences.preferred_topics)} pref, "
                f"cap {weights.max_score_topic_cap}): +{contribution}"
            )
            logger.debug(log_msg_topic)

        if preferences.preferred_methods:
            num_matches = min(len(preferences.preferred_methods), weights.max_score_method_cap)
            contribution = num_matches * weights.methodology
            max_score += contribution
            log_msg_method = (
                f"  + MaxScore (Methods - {len(preferences.preferred_methods)} pref, "
                f"cap {weights.max_score_method_cap}): +{contribution}"
            )
            logger.debug(log_msg_method)

        if preferences.mathematical_focus:
            num_matches = min(len(preferences.mathematical_focus), weights.max_score_focus_cap)
            contribution = num_matches * weights.focus
            max_score += contribution
            log_msg_focus = (
                f"  + MaxScore (Focus - {len(preferences.mathematical_focus)} pref, "
                f"cap {weights.max_score_focus_cap}): +{contribution}"
            )
            logger.debug(log_msg_focus)

        if preferences.programming_languages:
            num_matches = min(
                len(preferences.programming_languages), weights.max_score_programming_cap
            )
            contribution = num_matches * weights.programming
            max_score += contribution
            log_msg_prog = (
                f"  + MaxScore (Prog - {len(preferences.programming_languages)} pref, "
                f"cap {weights.max_score_programming_cap}): +{contribution}"
            )
            logger.debug(log_msg_prog)

        if preferences.preferred_supervisors:  # Assumes one preferred supervisor match
            max_score += weights.supervisor
            logger.debug(f"  + MaxScore (Preferred Supervisor match): +{weights.supervisor}")

        # Niche Score Components
        if preferences.preferred_topics:
            max_score += weights.niche_topic_bonus
            logger.debug(f"  + MaxScore (Pot. Niche Topic): +{weights.niche_topic_bonus}")

        if preferences.programming_languages:
            max_score += weights.niche_skill_bonus
            logger.debug(f"  + MaxScore (Pot. Niche Skill): +{weights.niche_skill_bonus}")

        num_defined_domains = len(self.settings.cross_domain_groups)
        if num_defined_domains > 1:
            max_cross_domain_bonus = (
                (num_defined_domains - 1) *
                niche_config.cross_domain_bonus_per_additional_domain
            )
            max_score += max_cross_domain_bonus
            logger.debug(
                f"  + MaxScore (Pot. Max Cross-Domain for {num_defined_domains} domains): "
                f"+{max_cross_domain_bonus}"
            )
        else:
            logger.debug("  - MaxScore (No cross-domain bonus: <2 domains in settings)")

        logger.debug("  - MaxScore (Serendipity Bonus currently placeholder, adds 0)")
        logger.info(f"--- Total Calculated Max Score (incl. niche) = {max_score} ---")
        return max_score

    def _calculate_base_match_score(
        self, preferences: UserPreferences, project: Project
    ) -> Tuple[float, List[str]]:
        """Calculates the base match score for a project against user preferences."""
        score = 0.0
        match_reasons: List[str] = []
        weights = self.settings.scoring  # Direct access to ScoringWeights instance

        log_base_score_start = (
            f"--- Calculating Base Score for P_ID: {project.project_id} "
            f"('{project.title}') ---"
        )
        logger.debug(log_base_score_start)

        if preferences.degree:
            if preferences.degree in project.applicable_degrees:
                score += weights.degree
                reason = f"Degree: Matches '{preferences.degree}' (+{weights.degree})"
                match_reasons.append(reason)
                logger.debug(f"  {reason}")
            else:
                reason = (
                    f"Degree: Mismatch. User: '{preferences.degree}', "
                    f"Project: {project.applicable_degrees} (No score change)"
                )
                match_reasons.append(reason)
                logger.debug(f"  {reason}")
        else:
            logger.debug("  Degree: No user preference specified.")

        project_co_req = project.co_requisite
        user_has_modules = preferences.current_modules and len(preferences.current_modules) > 0

        if project_co_req and project_co_req.lower() != "none":
            log_co_req_check = (
                f"  Co-req: Project requires '{project_co_req}'. "
                f"User modules: {preferences.current_modules}"
            )
            logger.debug(log_co_req_check)
            if user_has_modules:
                if project_co_req in preferences.current_modules:
                    score += weights.co_requisite
                    reason = (
                        f"Co-req: MET. Project needs '{project_co_req}', "
                        f"user has it (+{weights.co_requisite})"
                    )
                    match_reasons.append(reason)
                    logger.debug(f"  {reason}")
                else:
                    score += weights.co_requisite_penalty
                    reason = (
                        f"Co-req: MISMATCH. Project needs '{project_co_req}', user has "
                        f"{preferences.current_modules} ({weights.co_requisite_penalty})"
                    )
                    match_reasons.append(reason)
                    logger.debug(f"  {reason}")
            else:
                score += weights.co_requisite_penalty  # Penalize if project has co-req
                reason = (
                    f"Co-req: UNMET (User has no modules listed). Project needs "
                    f"'{project_co_req}' ({weights.co_requisite_penalty})"
                )
                match_reasons.append(reason)
                logger.debug(f"  {reason}")
        else:
            logger.debug("  Co-req: Project has no co-requisite or it's 'None'.")

        if preferences.preferred_topics and project.general_topics:
            common_topics = set(preferences.preferred_topics).intersection(
                project.general_topics
            )
            if common_topics:
                val = len(common_topics) * weights.topic
                score += val
                reason = (
                    f"Topics: Matched {len(common_topics)}: "
                    f"{', '.join(sorted(list(common_topics)))} (+{val})"
                )
                match_reasons.append(reason)
                logger.debug(f"  {reason}")
            else:
                log_topic_overlap = (
                    f"  Topics: No overlap. User: {preferences.preferred_topics}, "
                    f"Project: {project.general_topics}"
                )
                logger.debug(log_topic_overlap)
        elif preferences.preferred_topics:
            logger.debug(
                f"  Topics: User has prefs ({preferences.preferred_topics}), but no project topics."
            )
        elif project.general_topics:
            logger.debug(
                f"  Topics: Project has topics ({project.general_topics}), but no user prefs."
            )
        else:
            logger.debug("  Topics: Neither user nor project has topic info.")

        if preferences.preferred_methods and project.research_methodology:
            common_methods = set(preferences.preferred_methods).intersection(
                project.research_methodology
            )
            if common_methods:
                val = len(common_methods) * weights.methodology
                score += val
                reason = (
                    f"Methods: Matched {len(common_methods)}: "
                    f"{', '.join(sorted(list(common_methods)))} (+{val})"
                )
                match_reasons.append(reason)
                logger.debug(f"  {reason}")
            else:
                log_method_overlap = (
                    f"  Methods: No overlap. User: {preferences.preferred_methods}, "
                    f"Project: {project.research_methodology}"
                )
                logger.debug(log_method_overlap)
        elif preferences.preferred_methods:
            logger.debug(
                f"  Methods: User has prefs ({preferences.preferred_methods}), "
                f"but no project methods."
            )
        elif project.research_methodology:
            logger.debug(
                f"  Methods: Project has methods ({project.research_methodology}), "
                f"but no user prefs."
            )
        else:
            logger.debug("  Methods: Neither user nor project has method info.")

        if preferences.mathematical_focus and project.mathematical_focus:
            common_focus = set(preferences.mathematical_focus).intersection(
                project.mathematical_focus
            )
            if common_focus:
                val = len(common_focus) * weights.focus
                score += val
                reason = (
                    f"Focus: Matched {len(common_focus)}: "
                    f"{', '.join(sorted(list(common_focus)))} (+{val})"
                )
                match_reasons.append(reason)
                logger.debug(f"  {reason}")
            else:
                log_focus_overlap = (
                    f"  Focus: No overlap. User: {preferences.mathematical_focus}, "
                    f"Project: {project.mathematical_focus}"
                )
                logger.debug(log_focus_overlap)
        elif preferences.mathematical_focus:
            logger.debug(
                f"  Focus: User has prefs ({preferences.mathematical_focus}), but no project focus."
            )
        elif project.mathematical_focus:
            logger.debug(
                f"  Focus: Project has focus ({project.mathematical_focus}), but no user prefs."
            )
        else:
            logger.debug("  Focus: Neither user nor project has focus area info.")

        valid_project_langs = {
            lang for lang in project.programming_languages
            if lang and lang.lower() != "none"
        } if project.programming_languages else set()

        if preferences.programming_languages and valid_project_langs:
            common_langs = set(preferences.programming_languages).intersection(
                valid_project_langs
            )
            if common_langs:
                val = len(common_langs) * weights.programming
                score += val
                reason = (
                    f"Programming: Matched {len(common_langs)}: "
                    f"{', '.join(sorted(list(common_langs)))} (+{val})"
                )
                match_reasons.append(reason)
                logger.debug(f"  {reason}")
            else:
                log_prog_overlap = (
                    f"  Programming: No overlap. User: {preferences.programming_languages}, "
                    f"Project valid: {valid_project_langs}"
                )
                logger.debug(log_prog_overlap)
        elif preferences.programming_languages:
            log_prog_user_no_proj = (
                f"  Programming: User has prefs ({preferences.programming_languages}), "
                f"but project has no valid languages ({project.programming_languages})."
            )
            logger.debug(log_prog_user_no_proj)
        elif valid_project_langs:
            logger.debug(
                f"  Programming: Project has valid ({valid_project_langs}), but no user prefs."
            )
        else:
            logger.debug(
                "  Programming: Neither user nor project has programming language info."
            )

        if project.supervisor:
            if project.supervisor in preferences.preferred_supervisors:
                score += weights.supervisor
                reason = (
                    f"Supervisor: Matches preferred \'{project.supervisor}\' "
                    f"(+{weights.supervisor})"
                )
                match_reasons.append(reason)
                logger.debug(f"  {reason}")
            elif project.supervisor in preferences.avoid_supervisors:  # Corrected indentation
                score += weights.supervisor_penalty
                reason = (
                    f"Supervisor: Matches avoided \'{project.supervisor}\' "
                    f"({weights.supervisor_penalty})"
                )
                match_reasons.append(reason)
                logger.debug(f"  {reason}")
            else:
                logger.debug(f"  Supervisor: \'{project.supervisor}\' is neutral.")
        else:
            logger.debug("  Supervisor: Project has no supervisor listed.")

        logger.debug(f"--- Base score for P_ID {project.project_id} calculated: {score} ---")
        if not match_reasons:
            match_reasons.append(
                "No specific positive or negative scoring factors in base calculation."
            )
            logger.debug("  No specific positive/negative base scoring factors.")

        return score, match_reasons
