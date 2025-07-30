"""Automation content search functionality."""

import re
from typing import Any

from .analyzers import AutomationFlowAnalyzer
from .exceptions import AnalysisError, APIError
from .models import BlockInfo, ContentSearchResult


class AutomationContentSearcher:
    """Searches automation content for specific text fragments."""

    def __init__(self, client, analyzer: AutomationFlowAnalyzer):
        """Initialize the content searcher.

        Args:
            client: HTTP client for API calls
            analyzer: AutomationFlowAnalyzer instance for analyzing automations
        """
        self.client = client
        self.analyzer = analyzer

    async def search_by_content_fragment(
        self,
        search_fragment: str,
        case_sensitive: bool = False,
        limit: int | None = None
    ) -> list[ContentSearchResult]:
        """Search automations for content fragments.

        Args:
            search_fragment: Text fragment to search for
            case_sensitive: Whether search should be case sensitive
            limit: Maximum number of results to return

        Returns:
            List of ContentSearchResult objects containing matching automations

        Raises:
            APIError: If API calls fail
            AnalysisError: If automation analysis fails
        """
        if not search_fragment or not search_fragment.strip():
            raise ValueError("search_fragment cannot be empty")

        try:
            # Get all automations
            automations = await self._get_all_automations()

            results = []
            processed_count = 0

            for automation in automations:
                automation_id = automation["id"]
                automation_name = automation.get("name", f"Automation {automation_id}")

                try:
                    # Analyze the automation to get its blocks
                    analysis = await self.analyzer.analyze_automation(automation_id)

                    # Search for content in the automation blocks
                    matching_blocks = self._search_blocks_for_content(
                        analysis.blocks,
                        search_fragment,
                        case_sensitive
                    )

                    if matching_blocks:
                        result = ContentSearchResult(
                            automation_id=automation_id,
                            automation_name=automation_name,
                            automation_description=analysis.description,
                            matching_blocks=matching_blocks,
                            match_count=len(matching_blocks),
                            search_fragment=search_fragment
                        )
                        results.append(result)

                        # Check limit
                        if limit and len(results) >= limit:
                            break

                except Exception as e:
                    # Log the error but continue with other automations
                    print(f"Warning: Failed to analyze automation {automation_id}: {e}")
                    continue

                processed_count += 1

            # Sort results by match count (most matches first)
            results.sort(key=lambda x: x.match_count, reverse=True)

            return results

        except Exception as e:
            raise AnalysisError(f"Failed to search automations for content: {e}")

    async def search_by_regex_pattern(
        self,
        pattern: str,
        limit: int | None = None
    ) -> list[ContentSearchResult]:
        """Search automations using regex patterns.

        Args:
            pattern: Regex pattern to search for
            limit: Maximum number of results to return

        Returns:
            List of ContentSearchResult objects containing matching automations
        """
        try:
            compiled_pattern = re.compile(pattern, re.IGNORECASE)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}")

        try:
            # Get all automations
            automations = await self._get_all_automations()

            results = []

            for automation in automations:
                automation_id = automation["id"]
                automation_name = automation.get("name", f"Automation {automation_id}")

                try:
                    # Analyze the automation to get its blocks
                    analysis = await self.analyzer.analyze_automation(automation_id)

                    # Search for pattern in the automation blocks
                    matching_blocks = self._search_blocks_for_regex(
                        analysis.blocks,
                        compiled_pattern
                    )

                    if matching_blocks:
                        result = ContentSearchResult(
                            automation_id=automation_id,
                            automation_name=automation_name,
                            automation_description=analysis.description,
                            matching_blocks=matching_blocks,
                            match_count=len(matching_blocks),
                            search_fragment=pattern
                        )
                        results.append(result)

                        # Check limit
                        if limit and len(results) >= limit:
                            break

                except Exception as e:
                    # Log the error but continue with other automations
                    print(f"Warning: Failed to analyze automation {automation_id}: {e}")
                    continue

            # Sort results by match count (most matches first)
            results.sort(key=lambda x: x.match_count, reverse=True)

            return results

        except Exception as e:
            raise AnalysisError(f"Failed to search automations with regex: {e}")

    async def find_automations_with_urls(
        self,
        domain_filter: str | None = None,
        limit: int | None = None
    ) -> list[ContentSearchResult]:
        """Find automations containing URLs.

        Args:
            domain_filter: Optional domain to filter URLs by (e.g., "zoom.us")
            limit: Maximum number of results to return

        Returns:
            List of ContentSearchResult objects containing automations with URLs
        """
        # URL regex pattern
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'

        if domain_filter:
            # More specific pattern for domain filtering
            url_pattern = rf'https?://[^\s<>"{{}}|\\^`\[\]]*{re.escape(domain_filter)}[^\s<>"{{}}|\\^`\[\]]*'

        return await self.search_by_regex_pattern(url_pattern, limit)

    async def _get_all_automations(self) -> list[dict[str, Any]]:
        """Get list of all automations from the API.

        Returns:
            List of automation dictionaries
        """
        try:
            response = await self.client.get("automations")
            response.raise_for_status()
            data = response.json()
            return data.get("automations", [])
        except Exception as e:
            raise APIError(f"Failed to fetch automations: {e}")

    def _search_blocks_for_content(
        self,
        blocks: list[BlockInfo],
        search_fragment: str,
        case_sensitive: bool = False
    ) -> list[BlockInfo]:
        """Search blocks for content fragments.

        Args:
            blocks: List of BlockInfo objects to search
            search_fragment: Text fragment to search for
            case_sensitive: Whether search should be case sensitive

        Returns:
            List of BlockInfo objects containing the search fragment
        """
        matching_blocks = []

        search_text = search_fragment if case_sensitive else search_fragment.lower()

        for block in blocks:
            # Search in block description
            block_description = block.description if case_sensitive else block.description.lower()
            if search_text in block_description:
                matching_blocks.append(block)
                continue

            # Search in block parameters
            if self._search_dict_for_content(block.parameters, search_text, case_sensitive):
                matching_blocks.append(block)

        return matching_blocks

    def _search_blocks_for_regex(
        self,
        blocks: list[BlockInfo],
        pattern: re.Pattern
    ) -> list[BlockInfo]:
        """Search blocks using regex pattern.

        Args:
            blocks: List of BlockInfo objects to search
            pattern: Compiled regex pattern

        Returns:
            List of BlockInfo objects matching the pattern
        """
        matching_blocks = []

        for block in blocks:
            # Search in block description
            if pattern.search(block.description):
                matching_blocks.append(block)
                continue

            # Search in block parameters
            if self._search_dict_for_regex(block.parameters, pattern):
                matching_blocks.append(block)

        return matching_blocks

    def _search_dict_for_content(
        self,
        data: dict[str, Any],
        search_text: str,
        case_sensitive: bool = False
    ) -> bool:
        """Recursively search dictionary for content.

        Args:
            data: Dictionary to search
            search_text: Text to search for
            case_sensitive: Whether search should be case sensitive

        Returns:
            True if content found, False otherwise
        """
        for _key, value in data.items():
            if isinstance(value, str):
                text_to_search = value if case_sensitive else value.lower()
                if search_text in text_to_search:
                    return True
            elif isinstance(value, dict):
                if self._search_dict_for_content(value, search_text, case_sensitive):
                    return True
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        text_to_search = item if case_sensitive else item.lower()
                        if search_text in text_to_search:
                            return True
                    elif isinstance(item, dict):
                        if self._search_dict_for_content(item, search_text, case_sensitive):
                            return True

        return False

    def _search_dict_for_regex(self, data: dict[str, Any], pattern: re.Pattern) -> bool:
        """Recursively search dictionary using regex pattern.

        Args:
            data: Dictionary to search
            pattern: Compiled regex pattern

        Returns:
            True if pattern matches, False otherwise
        """
        for _key, value in data.items():
            if isinstance(value, str):
                if pattern.search(value):
                    return True
            elif isinstance(value, dict):
                if self._search_dict_for_regex(value, pattern):
                    return True
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        if pattern.search(item):
                            return True
                    elif isinstance(item, dict):
                        if self._search_dict_for_regex(item, pattern):
                            return True

        return False
