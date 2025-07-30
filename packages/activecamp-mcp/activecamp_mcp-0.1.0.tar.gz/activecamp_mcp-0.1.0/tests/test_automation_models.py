"""Tests for automation analysis data models."""

from datetime import datetime

import pytest

from activecamp_mcp.models import (
    AutomationAnalysis,
    BlockInfo,
    ContactChange,
    FlowEdge,
    FlowGraph,
    FlowNode,
    TriggerInfo,
)


class TestTriggerInfo:
    """Test TriggerInfo data model."""

    def test_trigger_info_creation(self):
        """Test basic TriggerInfo creation."""
        trigger = TriggerInfo(
            trigger_id="1",
            trigger_type="subscribe",
            related_id="20",
            related_name="Newsletter List",
            conditions={"listid": "20"},
            multi_entry=False
        )

        assert trigger.trigger_id == "1"
        assert trigger.trigger_type == "subscribe"
        assert trigger.related_id == "20"
        assert trigger.related_name == "Newsletter List"
        assert trigger.conditions == {"listid": "20"}
        assert trigger.multi_entry is False

    def test_trigger_info_with_optional_fields(self):
        """Test TriggerInfo with optional fields."""
        trigger = TriggerInfo(
            trigger_id="2",
            trigger_type="tag_added",
            related_id="5",
            related_name="VIP Tag"
        )

        assert trigger.conditions == {}
        assert trigger.multi_entry is False

    def test_trigger_info_validation(self):
        """Test TriggerInfo validation."""
        with pytest.raises(ValueError):
            TriggerInfo(
                trigger_id="",  # Empty ID should fail
                trigger_type="subscribe"
            )


class TestBlockInfo:
    """Test BlockInfo data model."""

    def test_block_info_creation(self):
        """Test basic BlockInfo creation."""
        block = BlockInfo(
            block_id="1",
            block_type="send",
            order=1,
            description="Send welcome email",
            parameters={"campaignid": "123"},
            affects_contact=True,
            automation_id="13"
        )

        assert block.block_id == "1"
        assert block.block_type == "send"
        assert block.order == 1
        assert block.description == "Send welcome email"
        assert block.parameters == {"campaignid": "123"}
        assert block.affects_contact is True
        assert block.automation_id == "13"
        assert block.parent_id is None

    def test_block_info_with_parent(self):
        """Test BlockInfo with parent relationship."""
        block = BlockInfo(
            block_id="2",
            block_type="if",
            order=2,
            description="Check if VIP",
            parameters={"segmentid": "5"},
            affects_contact=False,
            automation_id="13",
            parent_id="1"
        )

        assert block.parent_id == "1"

    def test_block_info_validation(self):
        """Test BlockInfo validation."""
        with pytest.raises(ValueError):
            BlockInfo(
                block_id="1",
                block_type="",  # Empty type should fail
                order=1,
                description="Test block",
                parameters={},
                affects_contact=False,
                automation_id="13"
            )


class TestContactChange:
    """Test ContactChange data model."""
    def test_contact_change_creation(self):
        """Test basic ContactChange creation."""
        change = ContactChange(
            change_type="add_tag",
            target_id="5",
            target_name="VIP Customer",
            description="Add VIP tag to contact",
            block_id="3"
        )

        assert change.change_type == "add_tag"
        assert change.target_id == "5"
        assert change.target_name == "VIP Customer"
        assert change.description == "Add VIP tag to contact"
        assert change.block_id == "3"

    def test_contact_change_types(self):
        """Test different contact change types."""
        valid_types = [
            "add_tag", "remove_tag", "add_to_list", "remove_from_list",
            "change_deal_stage", "send_email", "update_field"
        ]

        for change_type in valid_types:
            change = ContactChange(
                change_type=change_type,
                target_id="1",
                target_name="Test Target",
                description=f"Test {change_type}",
                block_id="1"
            )
            assert change.change_type == change_type


class TestFlowGraph:
    """Test FlowGraph data model."""

    def test_flow_graph_creation(self):
        """Test basic FlowGraph creation."""
        nodes = [
            FlowNode(node_id="1", node_type="start", label="Start"),
            FlowNode(node_id="2", node_type="action", label="Send Email")
        ]
        edges = [
            FlowEdge(source="1", target="2", label="Next")
        ]

        graph = FlowGraph(nodes=nodes, edges=edges)

        assert len(graph.nodes) == 2
        assert len(graph.edges) == 1
        assert graph.nodes[0].node_id == "1"
        assert graph.edges[0].source == "1"

    def test_empty_flow_graph(self):
        """Test empty FlowGraph creation."""
        graph = FlowGraph(nodes=[], edges=[])

        assert len(graph.nodes) == 0
        assert len(graph.edges) == 0


class TestAutomationAnalysis:
    """Test AutomationAnalysis data model."""

    def test_automation_analysis_creation(self):
        """Test basic AutomationAnalysis creation."""
        triggers = [
            TriggerInfo(
                trigger_id="1",
                trigger_type="subscribe",
                related_id="20",
                related_name="Newsletter List"
            )
        ]

        blocks = [
            BlockInfo(
                block_id="1",
                block_type="start",
                order=1,
                description="Start automation",
                parameters={},
                affects_contact=False,
                automation_id="13"
            )
        ]

        contact_changes = [
            ContactChange(
                change_type="add_tag",
                target_id="5",
                target_name="Subscriber",
                description="Add subscriber tag",
                block_id="2"
            )
        ]

        flow_graph = FlowGraph(
            nodes=[FlowNode(node_id="1", node_type="start", label="Start")],
            edges=[]
        )

        analysis = AutomationAnalysis(
            automation_id="13",
            name="Welcome Sequence",
            description="Welcome new subscribers",
            triggers=triggers,
            blocks=blocks,
            flow_graph=flow_graph,
            contact_changes=contact_changes,
            analysis_timestamp=datetime.utcnow()
        )

        assert analysis.automation_id == "13"
        assert analysis.name == "Welcome Sequence"
        assert analysis.description == "Welcome new subscribers"
        assert len(analysis.triggers) == 1
        assert len(analysis.blocks) == 1
        assert len(analysis.contact_changes) == 1
        assert analysis.visual_data is None
        assert analysis.analysis_status == "complete"

    def test_automation_analysis_with_optional_fields(self):
        """Test AutomationAnalysis with optional fields."""
        analysis = AutomationAnalysis(
            automation_id="14",
            name="Simple Automation",
            triggers=[],
            blocks=[],
            flow_graph=FlowGraph(nodes=[], edges=[]),
            contact_changes=[],
            analysis_timestamp=datetime.utcnow(),
            analysis_status="partial",
            error_message="Some blocks could not be analyzed"
        )

        assert analysis.description is None
        assert analysis.visual_data is None
        assert analysis.analysis_status == "partial"
        assert analysis.error_message == "Some blocks could not be analyzed"

    def test_automation_analysis_validation(self):
        """Test AutomationAnalysis validation."""
        with pytest.raises(ValueError):
            AutomationAnalysis(
                automation_id="",  # Empty ID should fail
                name="Test Automation",
                triggers=[],
                blocks=[],
                flow_graph=FlowGraph(nodes=[], edges=[]),
                contact_changes=[],
                analysis_timestamp=datetime.utcnow()
            )

    def test_automation_analysis_serialization(self):
        """Test AutomationAnalysis can be serialized to dict."""
        analysis = AutomationAnalysis(
            automation_id="13",
            name="Test Automation",
            triggers=[],
            blocks=[],
            flow_graph=FlowGraph(nodes=[], edges=[]),
            contact_changes=[],
            analysis_timestamp=datetime.utcnow()
        )

        data = analysis.model_dump()

        assert isinstance(data, dict)
        assert data["automation_id"] == "13"
        assert data["name"] == "Test Automation"
        assert "analysis_timestamp" in data
