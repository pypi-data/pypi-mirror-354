"""Tests for automation flow analyzer."""

from datetime import datetime
from unittest.mock import AsyncMock, Mock

import httpx
import pytest

from activecamp_mcp.analyzers import AutomationFlowAnalyzer
from activecamp_mcp.exceptions import APIError, AutomationNotFoundError
from activecamp_mcp.models import AutomationAnalysis, BlockInfo, FlowGraph, TriggerInfo


class TestAutomationFlowAnalyzer:
    """Test AutomationFlowAnalyzer class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock HTTP client."""
        return AsyncMock(spec=httpx.AsyncClient)

    @pytest.fixture
    def mock_cache(self):
        """Create a mock cache manager."""
        cache = Mock()
        cache.get_automation_analysis = AsyncMock(return_value=None)
        cache.cache_automation_analysis = AsyncMock()
        return cache

    @pytest.fixture
    def analyzer(self, mock_client, mock_cache):
        """Create an AutomationFlowAnalyzer instance."""
        return AutomationFlowAnalyzer(mock_client, mock_cache)

    @pytest.mark.asyncio
    async def test_analyze_automation_basic(self, analyzer, mock_client):
        """Test basic automation analysis."""
        # Mock API responses
        automation_response = Mock()
        automation_response.json.return_value = {
            "automation": {
                "id": "13",
                "name": "Welcome Sequence",
                "description": "Welcome new subscribers"
            }
        }

        triggers_response = Mock()
        triggers_response.json.return_value = {
            "automationTriggers": [
                {
                    "id": "1",
                    "type": "subscribe",
                    "relid": "20",
                    "params": {"listid": "20"},
                    "multientry": False
                }
            ]
        }

        blocks_response = Mock()
        blocks_response.json.return_value = {
            "automationBlocks": [
                {
                    "id": "1",
                    "type": "start",
                    "ordernum": 1,
                    "params": {},
                    "automation": "13"
                },
                {
                    "id": "2",
                    "type": "send",
                    "ordernum": 2,
                    "params": {"campaignid": "123"},
                    "automation": "13"
                }
            ]
        }

        # Mock entity name resolution
        list_response = Mock()
        list_response.json.return_value = {
            "list": {"name": "Newsletter List"}
        }

        campaign_response = Mock()
        campaign_response.json.return_value = {
            "campaign": {"subject": "Welcome Email"}
        }

        mock_client.get.side_effect = [
            automation_response,
            triggers_response,
            list_response,  # For trigger entity resolution - happens during trigger parsing!
            blocks_response,
            campaign_response  # For block description generation - happens during block parsing!
        ]

        result = await analyzer.analyze_automation("13")

        assert isinstance(result, AutomationAnalysis)
        assert result.automation_id == "13"
        assert result.name == "Welcome Sequence"
        assert result.description == "Welcome new subscribers"
        assert len(result.triggers) == 1
        assert len(result.blocks) == 2
        assert result.analysis_status == "complete"

        # Check trigger details
        trigger = result.triggers[0]
        assert trigger.trigger_id == "1"
        assert trigger.trigger_type == "subscribe"
        assert trigger.related_id == "20"
        assert trigger.related_name == "Newsletter List"

        # Check block details
        start_block = result.blocks[0]
        assert start_block.block_id == "1"
        assert start_block.block_type == "start"
        assert start_block.order == 1

        send_block = result.blocks[1]
        assert send_block.block_id == "2"
        assert send_block.block_type == "send"
        assert send_block.order == 2
        assert send_block.affects_contact is True

    @pytest.mark.asyncio
    async def test_analyze_automation_not_found(self, analyzer, mock_client):
        """Test automation not found error."""
        mock_client.get.side_effect = httpx.HTTPStatusError(
            "Not found",
            request=Mock(),
            response=Mock(status_code=404)
        )

        with pytest.raises(AutomationNotFoundError):
            await analyzer.analyze_automation("999")

    @pytest.mark.asyncio
    async def test_analyze_automation_api_error(self, analyzer, mock_client):
        """Test API error handling."""
        mock_client.get.side_effect = httpx.HTTPStatusError(
            "Server error",
            request=Mock(),
            response=Mock(status_code=500)
        )

        with pytest.raises(APIError):
            await analyzer.analyze_automation("13")

    @pytest.mark.asyncio
    async def test_analyze_automation_with_cache_hit(self, analyzer, mock_cache):
        """Test automation analysis with cache hit."""
        cached_analysis = AutomationAnalysis(
            automation_id="13",
            name="Cached Automation",
            triggers=[],
            blocks=[],
            flow_graph=FlowGraph(nodes=[], edges=[]),
            contact_changes=[],
            analysis_timestamp=datetime.now()
        )

        mock_cache.get_automation_analysis.return_value = cached_analysis

        result = await analyzer.analyze_automation("13")

        assert result == cached_analysis
        mock_cache.get_automation_analysis.assert_called_once_with("13")

    @pytest.mark.asyncio
    async def test_parse_trigger_subscribe_type(self, analyzer, mock_client):
        """Test parsing subscribe trigger type."""
        trigger_data = {
            "id": "1",
            "type": "subscribe",
            "relid": "20",
            "params": {"listid": "20"},
            "multientry": False
        }

        list_response = Mock()
        list_response.json.return_value = {
            "list": {"name": "Newsletter List"}
        }
        mock_client.get.return_value = list_response

        result = await analyzer._parse_trigger(trigger_data)

        assert isinstance(result, TriggerInfo)
        assert result.trigger_id == "1"
        assert result.trigger_type == "subscribe"
        assert result.related_id == "20"
        assert result.related_name == "Newsletter List"
        assert result.multi_entry is False

    @pytest.mark.asyncio
    async def test_parse_block_send_type(self, analyzer, mock_client):
        """Test parsing send block type."""
        block_data = {
            "id": "2",
            "type": "send",
            "ordernum": 2,
            "params": {"campaignid": "123"},
            "automation": "13"
        }

        campaign_response = Mock()
        campaign_response.json.return_value = {
            "campaign": {"subject": "Welcome Email"}
        }
        mock_client.get.return_value = campaign_response

        result = await analyzer._parse_block(block_data)

        assert isinstance(result, BlockInfo)
        assert result.block_id == "2"
        assert result.block_type == "send"
        assert result.order == 2
        assert result.affects_contact is True
        assert "Welcome Email" in result.description

    @pytest.mark.asyncio
    async def test_generate_block_description_send(self, analyzer, mock_client):
        """Test generating description for send block."""
        params = {"campaignid": "123"}

        campaign_response = Mock()
        campaign_response.json.return_value = {
            "campaign": {"subject": "Welcome Email"}
        }
        mock_client.get.return_value = campaign_response

        result = await analyzer._generate_block_description("send", params)

        assert result == "Send email campaign: Welcome Email"

    @pytest.mark.asyncio
    async def test_generate_block_description_wait(self, analyzer):
        """Test generating description for wait block."""
        params = {"wait_time": "1 day"}

        result = await analyzer._generate_block_description("wait", params)

        assert result == "Wait 1 day"

    @pytest.mark.asyncio
    async def test_generate_block_description_unknown(self, analyzer):
        """Test generating description for unknown block type."""
        params = {}

        result = await analyzer._generate_block_description("unknown_type", params)

        assert result == "Unknown_Type action"

    @pytest.mark.asyncio
    async def test_analyze_contact_changes(self, analyzer):
        """Test analyzing contact changes from blocks."""
        blocks = [
            BlockInfo(
                block_id="1",
                block_type="start",
                order=1,
                description="Start automation",
                parameters={},
                affects_contact=False,
                automation_id="13"
            ),
            BlockInfo(
                block_id="2",
                block_type="send",
                order=2,
                description="Send welcome email",
                parameters={"campaignid": "123"},
                affects_contact=True,
                automation_id="13"
            ),
            BlockInfo(
                block_id="3",
                block_type="sub",
                order=3,
                description="Subscribe to VIP list",
                parameters={"listid": "25"},
                affects_contact=True,
                automation_id="13"
            )
        ]

        result = await analyzer._analyze_contact_changes(blocks)

        assert len(result) == 2  # Only blocks that affect contacts

        # Check send email change
        send_change = next(c for c in result if c.change_type == "send_email")
        assert send_change.target_id == "123"
        assert send_change.block_id == "2"

        # Check list subscription change
        list_change = next(c for c in result if c.change_type == "add_to_list")
        assert list_change.target_id == "25"
        assert list_change.block_id == "3"

    @pytest.mark.asyncio
    async def test_build_flow_graph(self, analyzer):
        """Test building flow graph from blocks."""
        blocks = [
            BlockInfo(
                block_id="1",
                block_type="start",
                order=1,
                description="Start automation",
                parameters={},
                affects_contact=False,
                automation_id="13"
            ),
            BlockInfo(
                block_id="2",
                block_type="send",
                order=2,
                description="Send welcome email",
                parameters={},
                affects_contact=True,
                automation_id="13"
            ),
            BlockInfo(
                block_id="3",
                block_type="if",
                order=3,
                description="Check if VIP",
                parameters={},
                affects_contact=False,
                automation_id="13"
            )
        ]

        result = await analyzer._build_flow_graph(blocks)

        assert isinstance(result, FlowGraph)
        assert len(result.nodes) == 3
        assert len(result.edges) == 2  # Sequential connections

        # Check nodes
        start_node = next(n for n in result.nodes if n.node_type == "start")
        assert start_node.block_id == "1"

        action_node = next(n for n in result.nodes if n.node_type == "action")
        assert action_node.block_id == "2"

        condition_node = next(n for n in result.nodes if n.node_type == "condition")
        assert condition_node.block_id == "3"

        # Check edges
        first_edge = result.edges[0]
        assert first_edge.source == "1"
        assert first_edge.target == "2"

        second_edge = result.edges[1]
        assert second_edge.source == "2"
        assert second_edge.target == "3"
