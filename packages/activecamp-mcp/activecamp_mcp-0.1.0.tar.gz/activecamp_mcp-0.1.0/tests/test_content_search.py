"""Tests for automation content search functionality."""

from datetime import datetime
from unittest.mock import AsyncMock, Mock

import pytest

from activecamp_mcp.content_search import AutomationContentSearcher
from activecamp_mcp.models import (
    AutomationAnalysis,
    BlockInfo,
    ContentSearchResult,
    FlowGraph,
)


class TestAutomationContentSearcher:
    """Test AutomationContentSearcher class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock HTTP client."""
        return AsyncMock()

    @pytest.fixture
    def mock_analyzer(self):
        """Create a mock automation analyzer."""
        return AsyncMock()

    @pytest.fixture
    def searcher(self, mock_client, mock_analyzer):
        """Create an AutomationContentSearcher instance."""
        return AutomationContentSearcher(mock_client, mock_analyzer)

    @pytest.mark.asyncio
    async def test_search_by_content_fragment_basic(self, searcher, mock_client, mock_analyzer):
        """Test basic content fragment search."""
        # Mock automation list response
        automations_response = Mock()
        automations_response.json.return_value = {
            "automations": [
                {"id": "1", "name": "Welcome Email"},
                {"id": "2", "name": "Workshop Invitation"}
            ]
        }
        mock_client.get.return_value = automations_response

        # Mock automation analysis
        mock_analysis = AutomationAnalysis(
            automation_id="2",
            name="Workshop Invitation",
            description="Sends workshop invitations",
            flow_graph=FlowGraph(nodes=[], edges=[]),
            analysis_timestamp=datetime.now(),
            blocks=[
                BlockInfo(
                    block_id="block_1",
                    block_type="send",
                    order=1,
                    description="Send workshop invitation email",
                    parameters={
                        "subject": "Attend Automation Workz Admissions Workshop",
                        "message": "To join the workshop you need to enter through our zoom link https://us02web.zoom.us/j/82113727363"
                    },
                    affects_contact=False,
                    automation_id="2"
                )
            ]
        )

        # Mock analysis for automation 1 (no match)
        mock_analysis_1 = AutomationAnalysis(
            automation_id="1",
            name="Welcome Email",
            flow_graph=FlowGraph(nodes=[], edges=[]),
            analysis_timestamp=datetime.now(),
            blocks=[
                BlockInfo(
                    block_id="block_1",
                    block_type="send",
                    order=1,
                    description="Send welcome email",
                    parameters={"subject": "Welcome to our platform"},
                    affects_contact=False,
                    automation_id="1"
                )
            ]
        )

        # Mock analyzer to return different analyses based on ID
        def mock_analyze(automation_id):
            if automation_id == "2":
                return mock_analysis
            else:
                return mock_analysis_1

        mock_analyzer.analyze_automation.side_effect = mock_analyze

        # Search for content fragment
        results = await searcher.search_by_content_fragment("Automation Workz")

        # Verify results
        assert len(results) == 1
        result = results[0]
        assert isinstance(result, ContentSearchResult)
        assert result.automation_id == "2"
        assert result.automation_name == "Workshop Invitation"
        assert len(result.matching_blocks) == 1
        assert "Automation Workz" in result.matching_blocks[0].parameters["subject"]

    @pytest.mark.asyncio
    async def test_search_by_content_fragment_multiple_matches(self, searcher, mock_client, mock_analyzer):
        """Test content search with multiple matching automations."""
        # Mock automation list response
        automations_response = Mock()
        automations_response.json.return_value = {
            "automations": [
                {"id": "1", "name": "Welcome Email"},
                {"id": "2", "name": "Workshop Invitation"},
                {"id": "3", "name": "Follow-up Workshop"}
            ]
        }
        mock_client.get.return_value = automations_response

        # Mock automation analyses
        analysis_1 = AutomationAnalysis(
            automation_id="2",
            name="Workshop Invitation",
            flow_graph=FlowGraph(nodes=[], edges=[]),
            analysis_timestamp=datetime.now(),
            blocks=[
                BlockInfo(
                    block_id="block_1",
                    block_type="send",
                    order=1,
                    description="Send workshop invitation",
                    parameters={"subject": "Join our workshop today!"},
                    affects_contact=False,
                    automation_id="2"
                )
            ]
        )

        analysis_2 = AutomationAnalysis(
            automation_id="3",
            name="Follow-up Workshop",
            flow_graph=FlowGraph(nodes=[], edges=[]),
            analysis_timestamp=datetime.now(),
            blocks=[
                BlockInfo(
                    block_id="block_2",
                    block_type="send",
                    order=1,
                    description="Send workshop follow-up",
                    parameters={"message": "Don't miss our upcoming workshop session"},
                    affects_contact=False,
                    automation_id="3"
                )
            ]
        )

        # Mock analyzer to return different analyses based on ID
        def mock_analyze(automation_id):
            if automation_id == "2":
                return analysis_1
            elif automation_id == "3":
                return analysis_2
            else:
                return AutomationAnalysis(
                    automation_id=automation_id,
                    name="Other",
                    flow_graph=FlowGraph(nodes=[], edges=[]),
                    analysis_timestamp=datetime.now(),
                    blocks=[]
                )

        mock_analyzer.analyze_automation.side_effect = mock_analyze

        # Search for content fragment
        results = await searcher.search_by_content_fragment("workshop")

        # Verify results
        assert len(results) == 2
        automation_ids = [r.automation_id for r in results]
        assert "2" in automation_ids
        assert "3" in automation_ids

    @pytest.mark.asyncio
    async def test_search_by_content_fragment_no_matches(self, searcher, mock_client, mock_analyzer):
        """Test content search with no matches."""
        # Mock automation list response
        automations_response = Mock()
        automations_response.json.return_value = {
            "automations": [
                {"id": "1", "name": "Welcome Email"}
            ]
        }
        mock_client.get.return_value = automations_response

        # Mock automation analysis with no matching content
        mock_analysis = AutomationAnalysis(
            automation_id="1",
            name="Welcome Email",
            flow_graph=FlowGraph(nodes=[], edges=[]),
            analysis_timestamp=datetime.now(),
            blocks=[
                BlockInfo(
                    block_id="block_1",
                    block_type="send",
                    order=1,
                    description="Send welcome email",
                    parameters={"subject": "Welcome to our platform"},
                    affects_contact=False,
                    automation_id="1"
                )
            ]
        )
        mock_analyzer.analyze_automation.return_value = mock_analysis

        # Search for content fragment that doesn't exist
        results = await searcher.search_by_content_fragment("nonexistent content")

        # Verify no results
        assert len(results) == 0

    @pytest.mark.asyncio
    async def test_search_by_content_fragment_case_insensitive(self, searcher, mock_client, mock_analyzer):
        """Test that content search is case insensitive."""
        # Mock automation list response
        automations_response = Mock()
        automations_response.json.return_value = {
            "automations": [{"id": "1", "name": "Test Automation"}]
        }
        mock_client.get.return_value = automations_response

        # Mock automation analysis
        mock_analysis = AutomationAnalysis(
            automation_id="1",
            name="Test Automation",
            flow_graph=FlowGraph(nodes=[], edges=[]),
            analysis_timestamp=datetime.now(),
            blocks=[
                BlockInfo(
                    block_id="block_1",
                    block_type="send",
                    order=1,
                    description="Send email",
                    parameters={"subject": "AUTOMATION WORKZ Workshop"},
                    affects_contact=False,
                    automation_id="1"
                )
            ]
        )
        mock_analyzer.analyze_automation.return_value = mock_analysis

        # Search with different case
        results = await searcher.search_by_content_fragment("automation workz")

        # Verify match found despite case difference
        assert len(results) == 1
        assert results[0].automation_id == "1"

    @pytest.mark.asyncio
    async def test_search_by_url_fragment(self, searcher, mock_client, mock_analyzer):
        """Test searching for URL fragments in automation content."""
        # Mock automation list response
        automations_response = Mock()
        automations_response.json.return_value = {
            "automations": [{"id": "1", "name": "Zoom Workshop"}]
        }
        mock_client.get.return_value = automations_response

        # Mock automation analysis with URL
        mock_analysis = AutomationAnalysis(
            automation_id="1",
            name="Zoom Workshop",
            flow_graph=FlowGraph(nodes=[], edges=[]),
            analysis_timestamp=datetime.now(),
            blocks=[
                BlockInfo(
                    block_id="block_1",
                    block_type="send",
                    order=1,
                    description="Send zoom link",
                    parameters={
                        "message": "Join us at https://us02web.zoom.us/j/82113727363"
                    },
                    affects_contact=False,
                    automation_id="1"
                )
            ]
        )
        mock_analyzer.analyze_automation.return_value = mock_analysis

        # Search for URL fragment
        results = await searcher.search_by_content_fragment("us02web.zoom.us")

        # Verify URL match found
        assert len(results) == 1
        assert results[0].automation_id == "1"
        assert "us02web.zoom.us" in results[0].matching_blocks[0].parameters["message"]

    @pytest.mark.asyncio
    async def test_search_multiple_content_types(self, searcher, mock_client, mock_analyzer):
        """Test searching across different content types (subject, message, etc.)."""
        # Mock automation list response
        automations_response = Mock()
        automations_response.json.return_value = {
            "automations": [{"id": "1", "name": "Multi-content Automation"}]
        }
        mock_client.get.return_value = automations_response

        # Mock automation analysis with content in different fields
        mock_analysis = AutomationAnalysis(
            automation_id="1",
            name="Multi-content Automation",
            flow_graph=FlowGraph(nodes=[], edges=[]),
            analysis_timestamp=datetime.now(),
            blocks=[
                BlockInfo(
                    block_id="block_1",
                    block_type="send",
                    order=1,
                    description="Send email with workshop info",
                    parameters={
                        "subject": "Workshop Invitation",
                        "message": "Join our Automation Workz session",
                        "sms_text": "Text reminder for workshop"
                    },
                    affects_contact=False,
                    automation_id="1"
                )
            ]
        )
        mock_analyzer.analyze_automation.return_value = mock_analysis

        # Search for content that appears in message field
        results = await searcher.search_by_content_fragment("Automation Workz")

        # Verify match found in message field
        assert len(results) == 1
        assert results[0].automation_id == "1"
