"""
Niche discovery algorithms for finding hidden gems in project recommendations.

This module implements advanced algorithms to surface interesting but
uncommon projects that users might otherwise miss.
"""

import logging
from typing import List, Tuple, Optional, Set, Dict
from collections import Counter

from ..data.models import Project, UserPreferences, ProjectData
from ..config.settings import Settings


class NicheDiscoveryEngine:
    """
    Engine for discovering and scoring niche aspects of projects.
    """

    def __init__(self, settings: Settings):
        """
        Initialise NicheDiscoveryEngine with configuration.
        """
        self.settings = settings
        if not logging.getLogger().hasHandlers():
            log_level = logging.DEBUG if self.settings.display.show_debug_info else logging.INFO
            logging.basicConfig(
                level=log_level,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )

    def _get_attribute_frequencies(self, project_data: ProjectData) -> Dict[str, Counter]:
        """Helper to calculate frequencies of various attributes across all projects."""
        topic_counts: Counter = Counter()
        language_counts: Counter = Counter()
        method_counts: Counter = Counter()  # For research_methodology
        focus_counts: Counter = Counter()   # For mathematical_focus

        for p_item in project_data.projects:
            if p_item.general_topics:
                topic_counts.update(p_item.general_topics)
            if p_item.programming_languages:
                language_counts.update(p_item.programming_languages)
            if p_item.research_methodology:  # Corrected attribute name
                method_counts.update(p_item.research_methodology)
            if p_item.mathematical_focus:    # Corrected attribute name
                focus_counts.update(p_item.mathematical_focus)

        return {
            "topics": topic_counts,
            "languages": language_counts,
            "methods": method_counts,
            "focus_areas": focus_counts,
        }

    def _get_project_domains(self, project: Project) -> Set[str]:
        """Determine which academic domains a project belongs to."""
        domains = set()
        if not project.general_topics:  # Handle case where project has no topics
            return domains

        project_topics_set = set(project.general_topics)

        # Correctly access cross_domain_groups from the main Settings object
        cross_domain_groups = self.settings.cross_domain_groups or {}

        for domain, domain_topics_list in cross_domain_groups.items():
            if domain == "other":  # Assuming "other" is a fallback, not for bonus
                continue
            if domain_topics_list and project_topics_set.intersection(set(domain_topics_list)):
                domains.add(domain)

        return domains

    def _calculate_cross_domain_bonus(
        self, project: Project, detailed_output: bool = False
    ) -> Tuple[float, Optional[str]]:
        """Calculates bonus for projects spanning multiple domains."""
        domains = self._get_project_domains(project)
        bonus = 0.0
        debug_msg: Optional[str] = None
        num_domains = len(domains)

        if num_domains > 1:
            bonus = (
                (num_domains - 1) *
                self.settings.niche_discovery.cross_domain_bonus_per_additional_domain
            )
            if detailed_output:
                domain_list_str = ", ".join(sorted(list(domains)))
                debug_msg = (
                    f"Cross-Domain Bonus: +{bonus:.2f} for {num_domains} domains "
                    f"({domain_list_str})."
                )
                logging.debug(f"  P_ID {project.project_id}: {debug_msg}")
        elif detailed_output:
            if num_domains == 1:
                domain_list_str = ", ".join(sorted(list(domains)))
                debug_msg = (
                    f"Cross-Domain: Project in 1 domain ({domain_list_str}), no bonus."
                )
            else:
                debug_msg = "Cross-Domain: Project in 0 defined domains, no bonus."
            if debug_msg:
                logging.debug(f"  P_ID {project.project_id}: {debug_msg}")
        return bonus, debug_msg

    def _calculate_serendipity_bonus(
        self,
        project: Project,
        preferences: UserPreferences,
        project_data: ProjectData,
        detailed_output: bool = False
    ) -> Tuple[float, Optional[str]]:
        """
        Placeholder for calculating serendipity bonus.
        Actual logic for 0.3, 0.2, 0.2 components needs to be defined based on available data.
        """
        bonus = 0.0
        debug_msg_parts: List[str] = []

        # Placeholder logic - this needs to be defined based on actual serendipity factors.
        # For now, it contributes nothing.

        if detailed_output:
            no_factors_msg = (
                "Serendipity: No specific serendipity factors applied (placeholder logic)."
            )
            debug_msg_parts.append(no_factors_msg)
            # Optional: log if you want to see this message per project when no factors apply
            # logging.debug(f"  P_ID {project.project_id}: {no_factors_msg}")

        final_debug_msg = " | ".join(debug_msg_parts) if debug_msg_parts else None
        return bonus, final_debug_msg

    def calculate_niche_bonus(
        self,
        project: Project,
        preferences: UserPreferences,
        project_data: ProjectData,
        detailed_output: bool = False,
    ) -> Tuple[float, Optional[str]]:
        """
        Calculates a niche bonus score for a project using detailed logic.
        """
        total_bonus_score = 0.0
        debug_messages: List[str] = []
        weights = self.settings.scoring
        niche_config = self.settings.niche_discovery

        logging.debug(f"NicheDiscovery: Calculating niche bonus for P_ID: {project.project_id}")

        attribute_frequencies = self._get_attribute_frequencies(project_data)
        topic_frequencies = attribute_frequencies["topics"]
        language_frequencies = attribute_frequencies["languages"]
        # method_frequencies = attribute_frequencies["methods"] # If needed for niche methods
        # focus_frequencies = attribute_frequencies["focus_areas"] # If needed for niche focus

        # Niche Topic Bonus
        if preferences.preferred_topics and project.general_topics:
            common_topics = set(preferences.preferred_topics).intersection(
                project.general_topics
            )
            project_niche_topic_bonus = 0.0
            niche_topics_found = []
            for topic in common_topics:
                if topic_frequencies.get(topic, 0) <= niche_config.min_niche_threshold:
                    project_niche_topic_bonus += weights.niche_topic_bonus
                    niche_topics_found.append(topic)

            if project_niche_topic_bonus > 0:
                total_bonus_score += project_niche_topic_bonus
                # Corrected f-string for joining topics
                topics_str = ", ".join(sorted(niche_topics_found))
                msg = (
                    f"Niche Topic Bonus: +{project_niche_topic_bonus:.2f} "
                    f"(for niche topics: {topics_str}; "
                    f"threshold<={niche_config.min_niche_threshold})."
                )
                if detailed_output:
                    debug_messages.append(msg)
                logging.debug(f"  P_ID {project.project_id}: {msg}")

        # Niche Skill Bonus (Programming Languages)
        if preferences.programming_languages and project.programming_languages:
            common_langs = set(preferences.programming_languages).intersection(
                project.programming_languages
            )
            project_niche_skill_bonus = 0.0
            niche_langs_found = []
            for lang in common_langs:
                if language_frequencies.get(lang, 0) <= niche_config.min_niche_threshold:
                    project_niche_skill_bonus += weights.niche_skill_bonus
                    niche_langs_found.append(lang)

            if project_niche_skill_bonus > 0:
                total_bonus_score += project_niche_skill_bonus
                # Corrected f-string for joining languages
                langs_str = ", ".join(sorted(niche_langs_found))
                msg = (
                    f"Niche Skill Bonus: +{project_niche_skill_bonus:.2f} "
                    f"(for niche languages: {langs_str}; "
                    f"threshold<={niche_config.min_niche_threshold})."
                )
                if detailed_output:
                    debug_messages.append(msg)
                logging.debug(f"  P_ID {project.project_id}: {msg}")

        # Cross-Domain Bonus
        cross_domain_bonus, cd_debug_msg = self._calculate_cross_domain_bonus(
            project, detailed_output=detailed_output  # Ensure detailed_output is passed
        )
        if cross_domain_bonus > 0:
            total_bonus_score += cross_domain_bonus
        if detailed_output and cd_debug_msg:
            debug_messages.append(cd_debug_msg)

        # Serendipity Bonus
        serendipity_bonus, s_debug_msg = self._calculate_serendipity_bonus(
            project,
            preferences,
            project_data,
            detailed_output=detailed_output  # Ensure detailed_output is passed
        )
        if serendipity_bonus > 0:
            total_bonus_score += serendipity_bonus
        if detailed_output and s_debug_msg:
            debug_messages.append(s_debug_msg)

        if not debug_messages and detailed_output:
            no_bonus_msg = "No niche bonuses applied."
            debug_messages.append(no_bonus_msg)
            logging.debug(f"  P_ID {project.project_id}: {no_bonus_msg}")

        # Filter out None or empty strings before joining
        final_debug_msg = " | ".join(filter(None, debug_messages)) if detailed_output else None

        logging.debug(f"  P_ID {project.project_id}: Total Niche Bonus = {total_bonus_score:.2f}")
        return total_bonus_score, final_debug_msg

    def identify_interdisciplinary_projects(
        self,
        projects: List[Project]
    ) -> List[Tuple[Project, List[str]]]:
        """
        Identify projects that span multiple academic domains.

        Parameters
        ----------
        projects : List[Project]
            List of projects to analyse.

        Returns
        -------
        List[Tuple[Project, List[str]]]
            List of (project, domains) tuples for interdisciplinary projects.
        """
        interdisciplinary_projects = []

        for project in projects:
            # This call should now use the single, corrected _get_project_domains
            domains = self._get_project_domains(project)

            if len(domains) > 1:
                # Ensure domains is a list of strings for appending, not a set
                interdisciplinary_projects.append((project, sorted(list(domains))))

        # Sort by number of domains (most interdisciplinary first)
        interdisciplinary_projects.sort(key=lambda item: len(item[1]), reverse=True)

        return interdisciplinary_projects

    def find_hidden_connections(
        self,
        user_interests: List[str],
        projects: List[Project]
    ) -> Dict[str, List[Project]]:
        """
        Find projects that connect user interests in unexpected ways.

        Parameters
        ----------
        user_interests : List[str]
            Topics the user has expressed interest in.
        projects : List[Project]
            Available projects to search through.

        Returns
        -------
        Dict[str, List[Project]]
            Dictionary mapping connection types to relevant projects.
        """
        connections = {
            "bridge_projects": [],  # Projects connecting disparate interests
            "deepening_projects": [],  # Projects that go deeper into interests
            "adjacent_projects": [],  # Projects in related but different areas
        }

        if not user_interests:
            return connections

        user_interest_set = set(user_interests)

        for project in projects:
            project_topics = set(project.general_topics)

            # Bridge projects: connect multiple user interests
            matching_interests = user_interest_set & project_topics
            if len(matching_interests) >= 2:
                connections["bridge_projects"].append(project)

            # Deepening projects: focus intensively on one interest
            elif (len(matching_interests) == 1 and
                  self._is_specialisation_project(project, list(matching_interests)[0])):
                connections["deepening_projects"].append(project)

            # Adjacent projects: related to interests but in different domain
            elif self._is_adjacent_to_interests(project, user_interests):
                connections["adjacent_projects"].append(project)

        return connections

    def calculate_novelty_score(self, project: Project, all_projects: List[Project]) -> float:
        """
        Calculate how novel/unique a project is compared to others.

        Parameters
        ----------
        project : Project
            Project to evaluate for novelty.
        all_projects : List[Project]
            All available projects for comparison.

        Returns
        -------
        float
            Novelty score (higher = more novel/unique).
        """
        if not all_projects:
            return 0.0

        project_topics = set(project.general_topics)
        project_methods = set(project.research_methodology)
        project_focus = set(project.mathematical_focus)

        # Calculate average similarity to other projects
        similarities = []

        for other_project in all_projects:
            if other_project.project_id == project.project_id:
                continue

            other_topics = set(other_project.general_topics)
            other_methods = set(other_project.research_methodology)
            other_focus = set(other_project.mathematical_focus)

            # Jaccard similarity for each dimension
            topic_similarity = self._jaccard_similarity(project_topics, other_topics)
            method_similarity = self._jaccard_similarity(project_methods, other_methods)
            focus_similarity = self._jaccard_similarity(project_focus, other_focus)

            # Combined similarity
            overall_similarity = (topic_similarity + method_similarity + focus_similarity) / 3
            similarities.append(overall_similarity)

        # Novelty is inverse of average similarity
        if similarities:
            average_similarity = sum(similarities) / len(similarities)
            return 1.0 - average_similarity
        else:
            return 1.0  # Completely novel if no other projects

    def generate_niche_insights(
        self,
        project: Project,
        preferences: UserPreferences,
        niche_topics: Set[str]
    ) -> List[str]:
        """
        Generate human-readable insights about why a project is interesting
        from a niche perspective.

        Parameters
        ----------
        project : Project
            Project to analyse.
        preferences : UserPreferences
            User's preferences.
        niche_topics : Set[str]
            Set of niche topics.

        Returns
        -------
        List[str]
            List of insight strings explaining the niche appeal.
        """
        insights = []

        # Niche topic insights
        user_topics = set(preferences.preferred_topics)
        project_topics = set(project.general_topics)

        niche_matches = user_topics & project_topics & niche_topics
        if niche_matches:
            insights.append(f"Niche topics: {', '.join(sorted(niche_matches))}")

        # Interdisciplinary insights
        domains = self._get_project_domains(project)
        if len(domains) > 1:
            insights.append(f"Interdisciplinary: {', '.join(sorted(domains))}")

        # Unique combination insights
        topic_combo_rarity = self._assess_topic_combination_rarity(project)
        if topic_combo_rarity > 0.8:  # Very rare combination
            insights.append("Unique topic combination")

        # Methodology insights
        if project.research_methodology:
            unique_methods = [
                method for method in project.research_methodology
                if method not in ["Theoretical Analysis", "Literature Review"]  # Common methods
            ]
            if unique_methods:
                insights.append(f"Novel methods: {', '.join(unique_methods)}")

        return insights

    def _is_specialisation_project(self, project: Project, interest: str) -> bool:
        """Check if project represents deep specialisation in a topic."""
        # Simple heuristic: project focuses heavily on the interest
        project_topics = project.general_topics

        # If the interest appears multiple times or project has few other topics
        interest_related = [topic for topic in project_topics if interest.lower() in topic.lower()]

        return len(interest_related) > 1 or len(project_topics) <= 2

    def _is_adjacent_to_interests(self, project: Project, user_interests: List[str]) -> bool:
        """Check if project is in areas adjacent to user interests."""
        # This is a simplified implementation
        # In practice, you'd want a more sophisticated semantic similarity measure

        project_topics = set(project.general_topics)
        user_topics = set(user_interests)

        # No direct overlap but some shared domain
        if project_topics & user_topics:
            return False

        # Check if they share any semantic group
        user_domains = set()
        project_domains = set()

        cross_domain_groups = {}
        if hasattr(self.settings, 'cross_domain_groups') and \
           self.settings.cross_domain_groups is not None:
            cross_domain_groups = self.settings.cross_domain_groups
        else:
            logging.warning(
                "_is_adjacent_to_interests: settings.cross_domain_groups not configured."
            )
            # If no domain groups are configured, adjacency based on them cannot be determined.
            # For now, if groups are missing, it won't find shared domains.

        for domain, domain_topics in cross_domain_groups.items():
            domain_topic_set = set(domain_topics)
            if user_topics & domain_topic_set:
                user_domains.add(domain)
            if project_topics & domain_topic_set:
                project_domains.add(domain)

        # Adjacent if they share at least one domain
        return bool(user_domains & project_domains)

    def _jaccard_similarity(self, set1: Set[str], set2: Set[str]) -> float:
        """Calculate Jaccard similarity between two sets."""
        if not set1 and not set2:
            return 1.0

        intersection = len(set1 & set2)
        union = len(set1 | set2)

        return intersection / union if union > 0 else 0.0

    def _assess_topic_combination_rarity(self, project: Project) -> float:
        """Assess how rare the combination of topics in this project is."""
        # Simplified implementation - would need historical data for full analysis

        num_topics = len(project.general_topics)

        # More topics = potentially rarer combination
        if num_topics >= 4:
            return 0.9
        elif num_topics >= 3:
            return 0.6
        elif num_topics >= 2:
            return 0.3
        else:
            return 0.1

    def _is_unusual_supervisor_topic_combo(
        self,
        supervisor: str,
        topics: Set[str]
    ) -> bool:
        """Check if supervisor/topic combination is unusual."""
        # This would require historical data about supervisors and their typical topics
        # For now, return False as a placeholder
        return False


def identify_research_gaps(projects: List[Project]) -> Dict[str, List[str]]:
    """
    Identify potential research gaps by analysing topic combinations.

    Parameters
    ----------
    projects : List[Project]
        List of projects to analyse.

    Returns
    -------
    Dict[str, List[str]]
        Dictionary mapping gap types to specific gaps identified.
    """
    gaps = {
        "underrepresented_combinations": [],
        "missing_methodologies": [],
        "programming_gaps": [],
    }

    # Analyse topic combinations
    all_topics = set(topic for project in projects for topic in project.general_topics)
    topic_pairs = set()

    for project in projects:
        project_topics = project.general_topics
        for i, topic1 in enumerate(project_topics):
            for j, topic2 in enumerate(project_topics):
                if i < j:  # Avoid duplicates
                    topic_pairs.add((min(topic1, topic2), max(topic1, topic2)))

    # Find underrepresented combinations
    all_possible_pairs = {
        (min(t1, t2), max(t1, t2))
        for t1 in all_topics
        for t2 in all_topics
        if t1 != t2
    }

    missing_combinations = all_possible_pairs - topic_pairs
    # Only report interesting missing combinations (this would need more sophisticated filtering)
    gaps["underrepresented_combinations"] = [
        f"{pair[0]} + {pair[1]}"
        for pair in list(missing_combinations)[:5]  # Limit output
    ]

    return gaps
