"""
Topic clustering algorithms for enhanced topic discovery.

This module provides sophisticated topic clustering that ensures both
common and niche topics are represented in user choices.
"""

import random
import math
from typing import List, Set, Dict, Optional
from collections import Counter

from ..data.models import Project
from ..config.settings import Settings


class TopicClusterer:
    """
    Provides enhanced topic clustering with niche discovery capabilities.

    This class implements algorithms to select representative topics
    that balance popular choices with niche discovery opportunities.
    """

    def __init__(self, settings=None) -> None:
        """
        Initialise the topic clusterer.

        Parameters
        ----------
        settings : Settings, optional
            Configuration settings. Uses default if not provided.
        """
        self.settings = settings or Settings()
        self.semantic_groups = self.settings.semantic_groups

    def cluster_topics(
        self,
        projects: List[Project],
        user_interests: Optional[List[str]] = None,
        max_topics: Optional[int] = None
    ) -> List[str]:
        """
        Perform enhanced topic clustering with niche discovery.

        This method improves upon basic frequency-based selection by:
        1. Analysing topic co-occurrence patterns
        2. Including niche topics that might interest the user
        3. Ensuring cross-domain representation
        4. Considering user's existing interests for expansion

        Parameters
        ----------
        projects : List[Project]
            List of projects to extract topics from.
        user_interests : Optional[List[str]]
            Topics the user has already expressed interest in.
        max_topics : Optional[int]
            Maximum number of topics to return.

        Returns
        -------
        List[str]
            List of representative topics with enhanced niche discovery.
        """
        if max_topics is None:
            max_topics = self.settings.display.max_topics_display

        # Extract all topics from projects
        all_topics = [
            topic for project in projects
            for topic in project.general_topics
        ]

        if not all_topics:
            return []

        topic_counts = Counter(all_topics)
        unique_topics = list(topic_counts.keys())

        if len(unique_topics) <= max_topics:
            return unique_topics

        return self._select_representative_topics(
            topic_counts, user_interests, max_topics
        )

    def identify_niche_topics(self, projects: List[Project]) -> Set[str]:
        """
        Identify topics that appear in few projects (potential niche interests).

        Parameters
        ----------
        projects : List[Project]
            List of projects to analyse.

        Returns
        -------
        Set[str]
            Set of niche topic names.
        """
        threshold = self.settings.niche_discovery.min_niche_threshold

        topic_counts = Counter(
            topic for project in projects
            for topic in project.general_topics
        )

        return {
            topic for topic, count in topic_counts.items()
            if count <= threshold
        }

    def get_topic_diversity_score(self, topics: List[str]) -> float:
        """
        Calculate a diversity score for a list of topics.

        Parameters
        ----------
        topics : List[str]
            List of topics to evaluate.

        Returns
        -------
        float
            Diversity score (higher = more diverse).
        """
        if not topics:
            return 0.0

        # Count how many different semantic groups are represented
        groups_covered = set()

        for topic in topics:
            topic_group = self._get_topic_group(topic)
            if topic_group:
                groups_covered.add(topic_group)

        # Diversity is the ratio of groups covered to total possible groups
        max_possible_groups = len(self.semantic_groups)
        diversity_ratio = len(groups_covered) / max_possible_groups

        # Also consider the distribution within groups
        group_distribution = self._calculate_group_distribution(topics)
        distribution_score = self._calculate_distribution_evenness(group_distribution)

        # Combine both metrics
        return (diversity_ratio + distribution_score) / 2

    def expand_user_interests(
        self,
        user_topics: List[str],
        all_projects: List[Project],
        expansion_count: int = 3
    ) -> List[str]:
        """
        Expand user's stated interests with related topics they might like.

        Parameters
        ----------
        user_topics : List[str]
            Topics the user has already indicated interest in.
        all_projects : List[Project]
            All available projects to learn patterns from.
        expansion_count : int
            Number of additional topics to suggest.

        Returns
        -------
        List[str]
            List of potentially interesting related topics.
        """
        if not user_topics:
            return []

        # Find projects that contain user's interests
        relevant_projects = [
            project for project in all_projects
            if set(user_topics) & set(project.general_topics)
        ]

        # Count co-occurring topics
        co_occurrence_counts = Counter()
        for project in relevant_projects:
            for topic in project.general_topics:
                if topic not in user_topics:
                    co_occurrence_counts[topic] += 1

        # Select topics that frequently co-occur with user interests
        # but aren't too common overall (to maintain some niche appeal)
        all_topic_counts = Counter(
            topic for project in all_projects
            for topic in project.general_topics
        )

        candidates = []
        for topic, co_count in co_occurrence_counts.most_common():
            # Calculate a score that balances co-occurrence with rarity
            overall_frequency = all_topic_counts[topic]
            if overall_frequency > 0:
                score = co_count / overall_frequency
                candidates.append((topic, score))

        # Sort by score and return top candidates
        candidates.sort(key=lambda item: item[1], reverse=True)
        return [topic for topic, _ in candidates[:expansion_count]]

    def _select_representative_topics(
        self,
        topic_counts: Counter,
        user_interests: Optional[List[str]],
        max_topics: int
    ) -> List[str]:
        """Select representative topics using advanced algorithm."""
        selected_topics = set()

        # Identify niche topics for special consideration
        niche_threshold = self.settings.niche_discovery.min_niche_threshold
        niche_topics = {
            topic for topic, count in topic_counts.items()
            if count <= niche_threshold
        }

        # Frequency-based stratification
        sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
        total_topics = len(sorted_topics)

        high_frequency = sorted_topics[:total_topics // 3]
        medium_frequency = sorted_topics[total_topics // 3:2 * total_topics // 3]
        low_frequency = sorted_topics[2 * total_topics // 3:]

        # Always include top 3 most frequent for baseline coverage
        for topic, _ in high_frequency[:3]:
            selected_topics.add(topic)

        # If user has interests, expand with related topics
        if user_interests:
            # This would be called after we have some user input
            # For now, we'll prepare for future enhancement
            pass

        # Ensure diversity across semantic groups
        groups_covered = set()
        for group_name, group_topics in self.semantic_groups.items():
            if len(selected_topics) >= max_topics - 4:
                break

            available_in_group = [
                topic for topic in group_topics
                if topic in topic_counts
            ]

            if available_in_group and group_name not in groups_covered:
                # Prefer niche topics within the group if available
                niche_in_group = [
                    topic for topic in available_in_group
                    if topic in niche_topics
                ]

                if niche_in_group:
                    best_topic = max(niche_in_group, key=lambda t: topic_counts[t])
                else:
                    best_topic = max(available_in_group, key=lambda t: topic_counts[t])

                selected_topics.add(best_topic)
                groups_covered.add(group_name)

        # Add medium frequency topics for balance
        remaining_slots = max_topics - len(selected_topics) - 3
        for topic, _ in medium_frequency[:remaining_slots]:
            if topic not in selected_topics:
                selected_topics.add(topic)

        # Always include niche topics for discovery
        max_niche = self.settings.niche_discovery.max_niche_recommendations
        niche_candidates = [
            topic for topic, _ in low_frequency
            if topic not in selected_topics and topic in niche_topics
        ]

        if niche_candidates:
            num_niche = min(max_niche, len(niche_candidates), max_topics - len(selected_topics))
            selected_topics.update(random.sample(niche_candidates, num_niche))

        return list(selected_topics)

    def _get_topic_group(self, topic: str) -> Optional[str]:
        """Find which semantic group a topic belongs to."""
        for group_name, group_topics in self.semantic_groups.items():
            if topic in group_topics:
                return group_name
        return None

    def _calculate_group_distribution(self, topics: List[str]) -> Dict[str, int]:
        """Calculate how many topics belong to each semantic group."""
        distribution = {}

        for topic in topics:
            group = self._get_topic_group(topic)
            group_key = group if group else "other"
            distribution[group_key] = distribution.get(group_key, 0) + 1

        return distribution

    def _calculate_distribution_evenness(self, distribution: Dict[str, int]) -> float:
        """Calculate how evenly distributed topics are across groups."""
        if not distribution:
            return 0.0

        values = list(distribution.values())
        total = sum(values)

        if total == 0:
            return 0.0

        # Calculate Shannon evenness index
        num_groups = len(values)
        if num_groups <= 1:
            return 1.0

        # Calculate actual entropy
        actual_entropy = 0.0
        for count in values:
            if count > 0:
                proportion = count / total
                actual_entropy -= proportion * math.log2(proportion)

        # Maximum possible entropy (perfectly even distribution)
        max_entropy = (num_groups.bit_length() - 1) if num_groups > 1 else 0

        # Evenness is ratio of actual to maximum entropy
        return actual_entropy / max_entropy if max_entropy > 0 else 1.0


def create_topic_cooccurrence_matrix(projects: List[Project]) -> Dict[str, Dict[str, int]]:
    """
    Create a co-occurrence matrix for topics across projects.

    Parameters
    ----------
    projects : List[Project]
        List of projects to analyse.

    Returns
    -------
    Dict[str, Dict[str, int]]
        Nested dictionary representing topic co-occurrence counts.
    """
    # Get all unique topics
    all_topics = set(
        topic for project in projects
        for topic in project.general_topics
    )

    # Initialise matrix
    cooccurrence_matrix = {
        topic1: {topic2: 0 for topic2 in all_topics}
        for topic1 in all_topics
    }

    # Count co-occurrences
    for project in projects:
        project_topics = project.general_topics
        for i, topic1 in enumerate(project_topics):
            for j, topic2 in enumerate(project_topics):
                if i != j:  # Don't count self-cooccurrence
                    cooccurrence_matrix[topic1][topic2] += 1

    return cooccurrence_matrix


def find_topic_communities(
    cooccurrence_matrix: Dict[str, Dict[str, int]],
    min_community_size: int = 3
) -> List[List[str]]:
    """
    Find communities of topics that frequently appear together.

    Parameters
    ----------
    cooccurrence_matrix : Dict[str, Dict[str, int]]
        Topic co-occurrence matrix.
    min_community_size : int
        Minimum size for a topic community.

    Returns
    -------
    List[List[str]]
        List of topic communities (groups of related topics).
    """
    # Simplified community detection using thresholding
    topics = list(cooccurrence_matrix.keys())
    communities = []
    used_topics = set()

    for topic in topics:
        if topic in used_topics:
            continue

        # Find topics strongly connected to this one
        community = [topic]
        connections = cooccurrence_matrix[topic]

        # Sort by connection strength
        sorted_connections = sorted(
            connections.items(),
            key=lambda item: item[1],
            reverse=True
        )        # Add strongly connected topics
        for connected_topic, strength in sorted_connections:
            if (connected_topic not in used_topics and
                    connected_topic != topic and
                    strength > 1):  # Threshold for "strong" connection
                community.append(connected_topic)
                if len(community) >= min_community_size:
                    break

        # Only keep communities of sufficient size
        if len(community) >= min_community_size:
            communities.append(community)
            used_topics.update(community)

    return communities
