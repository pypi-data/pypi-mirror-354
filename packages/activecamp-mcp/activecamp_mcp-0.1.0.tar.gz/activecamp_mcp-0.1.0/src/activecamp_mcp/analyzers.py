"""Automation analysis engines."""

from datetime import datetime
from typing import Any

import httpx

from .exceptions import AnalysisError, APIError, AutomationNotFoundError
from .models import (
    AutomationAnalysis,
    BlockInfo,
    ContactChange,
    FlowEdge,
    FlowGraph,
    FlowNode,
    TriggerInfo,
    VisualData,
)


class AutomationFlowAnalyzer:
    """Analyzes individual automation workflows."""

    def __init__(self, client: httpx.AsyncClient, cache_manager):
        self.client = client
        self.cache = cache_manager

    async def analyze_automation(self, automation_id: str) -> AutomationAnalysis:
        """Complete analysis of a single automation."""
        # Check cache first
        cached_analysis = await self.cache.get_automation_analysis(automation_id)
        if cached_analysis:
            return cached_analysis

        try:
            # Get basic automation info
            automation_info = await self._get_automation_info(automation_id)

            # Get triggers
            triggers = await self._analyze_triggers(automation_id)

            # Get blocks and build flow
            blocks = await self._analyze_blocks(automation_id)
            flow_graph = await self._build_flow_graph(blocks)

            # Analyze contact changes
            contact_changes = await self._analyze_contact_changes(blocks)

            # Get visual data if available
            visual_data = await self._get_visual_data(automation_info)

            analysis = AutomationAnalysis(
                automation_id=automation_id,
                name=automation_info['name'],
                description=automation_info.get('description'),
                triggers=triggers,
                blocks=blocks,
                flow_graph=flow_graph,
                contact_changes=contact_changes,
                visual_data=visual_data,
                analysis_timestamp=datetime.now(),
                analysis_status="complete"
            )

            # Cache the result
            await self.cache.cache_automation_analysis(analysis)

            return analysis

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise AutomationNotFoundError(automation_id)
            else:
                raise APIError(f"API error: {e}", e.response.status_code)
        except Exception as e:
            raise AnalysisError(f"Failed to analyze automation {automation_id}: {e}", automation_id)

    async def _get_automation_info(self, automation_id: str) -> dict[str, Any]:
        """Get basic automation information."""
        response = await self.client.get(f"automations/{automation_id}")
        response.raise_for_status()
        return response.json()["automation"]

    async def _analyze_triggers(self, automation_id: str) -> list[TriggerInfo]:
        """Analyze automation triggers."""
        response = await self.client.get(f"automations/{automation_id}/triggers")
        response.raise_for_status()
        triggers_data = response.json()["automationTriggers"]

        triggers = []
        for trigger_data in triggers_data:
            trigger_info = await self._parse_trigger(trigger_data)
            triggers.append(trigger_info)

        return triggers

    async def _parse_trigger(self, trigger_data: dict) -> TriggerInfo:
        """Parse trigger data into structured format."""
        trigger_type = trigger_data["type"]
        related_id = trigger_data.get("relid")

        # Resolve related entity name
        related_name = await self._resolve_entity_name(trigger_type, related_id)

        return TriggerInfo(
            trigger_id=trigger_data["id"],
            trigger_type=trigger_type,
            related_id=related_id,
            related_name=related_name,
            conditions=trigger_data.get("params", {}),
            multi_entry=trigger_data.get("multientry", False)
        )

    async def _resolve_entity_name(self, entity_type: str, entity_id: str) -> str | None:
        """Resolve entity ID to human-readable name."""
        if not entity_id:
            return None

        try:
            if entity_type == "subscribe":
                response = await self.client.get(f"lists/{entity_id}")
                return response.json()["list"]["name"]
            elif entity_type == "tag_added":
                response = await self.client.get(f"tags/{entity_id}")
                return response.json()["tag"]["tag"]
            elif entity_type == "deal_stage":
                response = await self.client.get(f"dealStages/{entity_id}")
                return response.json()["dealStage"]["title"]
            else:
                return None
        except Exception:
            # If we can't resolve the name, return None
            return None

    async def _analyze_blocks(self, automation_id: str) -> list[BlockInfo]:
        """Analyze automation blocks."""
        response = await self.client.get(f"automations/{automation_id}/blocks")
        response.raise_for_status()
        blocks_data = response.json()["automationBlocks"]

        blocks = []
        for block_data in blocks_data:
            block_info = await self._parse_block(block_data)
            blocks.append(block_info)

        return sorted(blocks, key=lambda x: x.order)

    async def _parse_block(self, block_data: dict) -> BlockInfo:
        """Parse block data into structured format."""
        block_type = block_data["type"]
        params = block_data.get("params", {})

        # Generate human-readable description
        description = await self._generate_block_description(block_type, params)

        # Determine if this block affects contacts
        affects_contact = self._block_affects_contact(block_type)

        return BlockInfo(
            block_id=block_data["id"],
            block_type=block_type,
            order=block_data["ordernum"],
            description=description,
            parameters=params,
            affects_contact=affects_contact,
            automation_id=block_data["automation"],
            parent_id=block_data.get("parent")
        )

    async def _generate_block_description(self, block_type: str, params: dict) -> str:
        """Generate human-readable description for a block."""
        if block_type == "send":
            campaign_id = params.get("campaignid")
            if campaign_id:
                try:
                    response = await self.client.get(f"campaigns/{campaign_id}")
                    campaign_name = response.json()["campaign"]["subject"]
                    return f"Send email campaign: {campaign_name}"
                except Exception:
                    pass
            return "Send email campaign"

        elif block_type == "dealstage":
            stage_id = params.get("stage")
            if stage_id:
                try:
                    response = await self.client.get(f"dealStages/{stage_id}")
                    stage_name = response.json()["dealStage"]["title"]
                    return f"Move to deal stage: {stage_name}"
                except Exception:
                    pass
            return "Change deal stage"

        elif block_type == "if":
            segment_id = params.get("segmentid")
            if segment_id:
                try:
                    response = await self.client.get(f"segments/{segment_id}")
                    segment_name = response.json()["segment"]["name"]
                    return f"Check if contact matches: {segment_name}"
                except Exception:
                    pass
            return "Conditional check"

        elif block_type == "wait":
            wait_time = params.get("wait_time", "specified time")
            return f"Wait {wait_time}"

        elif block_type == "sub":
            list_id = params.get("listid")
            if list_id:
                try:
                    response = await self.client.get(f"lists/{list_id}")
                    list_name = response.json()["list"]["name"]
                    return f"Subscribe to list: {list_name}"
                except Exception:
                    pass
            return "Subscribe to list"

        elif block_type == "layer":
            title = params.get("title", "External integration")
            return f"External action: {title}"

        else:
            return f"{block_type.title()} action"

    def _block_affects_contact(self, block_type: str) -> bool:
        """Determine if a block type affects contact data."""
        affecting_types = {
            "send", "dealstage", "sub", "unsub", "tag", "untag",
            "field", "layer", "goal", "webhook"
        }
        return block_type in affecting_types

    async def _analyze_contact_changes(self, blocks: list[BlockInfo]) -> list[ContactChange]:
        """Analyze what changes blocks make to contacts."""
        changes = []

        for block in blocks:
            if not block.affects_contact:
                continue

            change_type = self._get_change_type(block.block_type)
            if not change_type:
                continue

            target_id, target_name = self._extract_target_info(block)
            description = self._generate_change_description(block, target_name)

            change = ContactChange(
                change_type=change_type,
                target_id=target_id,
                target_name=target_name or "Unknown",
                description=description,
                block_id=block.block_id
            )
            changes.append(change)

        return changes

    def _get_change_type(self, block_type: str) -> str | None:
        """Map block type to contact change type."""
        mapping = {
            "send": "send_email",
            "sub": "add_to_list",
            "unsub": "remove_from_list",
            "tag": "add_tag",
            "untag": "remove_tag",
            "dealstage": "change_deal_stage",
            "field": "update_field",
            "layer": "external_action"
        }
        return mapping.get(block_type)

    def _extract_target_info(self, block: BlockInfo) -> tuple[str, str | None]:
        """Extract target ID and name from block parameters."""
        params = block.parameters

        if block.block_type == "send":
            return params.get("campaignid", ""), None
        elif block.block_type in ["sub", "unsub"]:
            return params.get("listid", ""), None
        elif block.block_type in ["tag", "untag"]:
            return params.get("tagid", ""), None
        elif block.block_type == "dealstage":
            return params.get("stage", ""), None
        elif block.block_type == "field":
            return params.get("fieldid", ""), None
        else:
            return params.get("id", ""), None

    def _generate_change_description(self, block: BlockInfo, target_name: str | None) -> str:
        """Generate description for contact change."""
        if target_name:
            return f"{block.description} ({target_name})"
        else:
            return block.description

    async def _build_flow_graph(self, blocks: list[BlockInfo]) -> FlowGraph:
        """Build flow graph from blocks."""
        nodes = []
        edges = []

        # Create nodes
        for block in blocks:
            node_type = self._get_node_type(block.block_type)
            node = FlowNode(
                node_id=block.block_id,
                node_type=node_type,
                label=block.description,
                block_id=block.block_id,
                metadata={"order": block.order}
            )
            nodes.append(node)

        # Create edges (simple sequential flow for now)
        sorted_blocks = sorted(blocks, key=lambda x: x.order)
        for i in range(len(sorted_blocks) - 1):
            current_block = sorted_blocks[i]
            next_block = sorted_blocks[i + 1]

            edge = FlowEdge(
                source=current_block.block_id,
                target=next_block.block_id,
                label="Next"
            )
            edges.append(edge)

        return FlowGraph(nodes=nodes, edges=edges)

    def _get_node_type(self, block_type: str) -> str:
        """Map block type to flow node type."""
        if block_type == "start":
            return "start"
        elif block_type in ["if", "else"]:
            return "condition"
        elif block_type == "end":
            return "end"
        else:
            return "action"

    async def _get_visual_data(self, automation_info: dict) -> VisualData | None:
        """Get visual data for automation (screenshots, etc.)."""
        # For now, just return None - visual data extraction would be implemented later
        screenshot_url = automation_info.get("screenshot_url")
        if screenshot_url:
            return VisualData(screenshot_url=screenshot_url)
        return None

