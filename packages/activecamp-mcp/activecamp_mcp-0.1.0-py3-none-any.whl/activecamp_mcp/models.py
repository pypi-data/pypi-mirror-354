"""Data models for automation analysis."""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


class TriggerInfo(BaseModel):
    """Information about an automation trigger."""

    trigger_id: str = Field(..., min_length=1, description="Unique trigger identifier")
    trigger_type: str = Field(..., min_length=1, description="Type of trigger (subscribe, tag_added, etc.)")
    related_id: str | None = Field(None, description="ID of related entity (list, tag, etc.)")
    related_name: str | None = Field(None, description="Human-readable name of related entity")
    conditions: dict[str, Any] = Field(default_factory=dict, description="Trigger conditions and parameters")
    multi_entry: bool = Field(default=False, description="Whether contact can enter multiple times")

    @field_validator('trigger_id')
    @classmethod
    def validate_trigger_id(cls, v):
        if not v or not v.strip():
            raise ValueError("trigger_id cannot be empty")
        return v

    @field_validator('trigger_type')
    @classmethod
    def validate_trigger_type(cls, v):
        if not v or not v.strip():
            raise ValueError("trigger_type cannot be empty")
        return v


class BlockInfo(BaseModel):
    """Information about an automation block/step."""

    block_id: str = Field(..., min_length=1, description="Unique block identifier")
    block_type: str = Field(..., min_length=1, description="Type of block (send, if, wait, etc.)")
    order: int = Field(..., ge=0, description="Order/position in automation flow")
    description: str = Field(..., description="Human-readable description of block action")
    parameters: dict[str, Any] = Field(default_factory=dict, description="Block parameters and configuration")
    affects_contact: bool = Field(..., description="Whether this block affects contact data")
    automation_id: str = Field(..., min_length=1, description="ID of parent automation")
    parent_id: str | None = Field(None, description="ID of parent block (for nested blocks)")

    @field_validator('block_id')
    @classmethod
    def validate_block_id(cls, v):
        if not v or not v.strip():
            raise ValueError("block_id cannot be empty")
        return v

    @field_validator('block_type')
    @classmethod
    def validate_block_type(cls, v):
        if not v or not v.strip():
            raise ValueError("block_type cannot be empty")
        return v

    @field_validator('automation_id')
    @classmethod
    def validate_automation_id(cls, v):
        if not v or not v.strip():
            raise ValueError("automation_id cannot be empty")
        return v


class ContactChange(BaseModel):
    """Information about a change made to a contact."""

    change_type: Literal[
        "add_tag", "remove_tag", "add_to_list", "remove_from_list",
        "change_deal_stage", "send_email", "update_field", "external_action"
    ] = Field(..., description="Type of change made to contact")
    target_id: str = Field(..., description="ID of target entity (tag, list, field, etc.)")
    target_name: str = Field(..., description="Human-readable name of target entity")
    description: str = Field(..., description="Human-readable description of the change")
    block_id: str = Field(..., description="ID of block that makes this change")


class FlowNode(BaseModel):
    """A node in the automation flow graph."""

    node_id: str = Field(..., description="Unique node identifier")
    node_type: Literal["start", "action", "condition", "end"] = Field(..., description="Type of flow node")
    label: str = Field(..., description="Display label for the node")
    block_id: str | None = Field(None, description="Associated block ID if applicable")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional node metadata")


class FlowEdge(BaseModel):
    """An edge in the automation flow graph."""

    source: str = Field(..., description="Source node ID")
    target: str = Field(..., description="Target node ID")
    label: str | None = Field(None, description="Edge label (e.g., 'Yes', 'No', 'Next')")
    condition: str | None = Field(None, description="Condition for this edge to be taken")


class FlowGraph(BaseModel):
    """Graph representation of automation flow."""

    nodes: list[FlowNode] = Field(default_factory=list, description="Flow nodes")
    edges: list[FlowEdge] = Field(default_factory=list, description="Flow edges")


class VisualData(BaseModel):
    """Visual data for automation (screenshots, etc.)."""

    screenshot_url: str | None = Field(None, description="URL to automation screenshot")
    image_data: bytes | None = Field(None, description="Raw image data")
    visual_elements: list[dict[str, Any]] = Field(default_factory=list, description="Extracted visual elements")


class AutomationAnalysis(BaseModel):
    """Complete analysis of an automation workflow."""

    automation_id: str = Field(..., min_length=1, description="Unique automation identifier")
    name: str = Field(..., min_length=1, description="Automation name")
    description: str | None = Field(None, description="Automation description")
    triggers: list[TriggerInfo] = Field(default_factory=list, description="Automation triggers")
    blocks: list[BlockInfo] = Field(default_factory=list, description="Automation blocks/steps")
    flow_graph: FlowGraph = Field(..., description="Flow graph representation")
    contact_changes: list[ContactChange] = Field(default_factory=list, description="Changes made to contacts")
    visual_data: VisualData | None = Field(None, description="Visual automation data")
    analysis_timestamp: datetime = Field(..., description="When this analysis was performed")
    analysis_status: Literal["complete", "partial", "error"] = Field(default="complete", description="Analysis status")
    error_message: str | None = Field(None, description="Error message if analysis failed")

    @field_validator('automation_id')
    @classmethod
    def validate_automation_id(cls, v):
        if not v or not v.strip():
            raise ValueError("automation_id cannot be empty")
        return v

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("name cannot be empty")
        return v

    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            bytes: lambda v: v.hex() if v else None
        }


class AutomationEcosystem(BaseModel):
    """Complete automation ecosystem analysis."""

    automations: list[AutomationAnalysis] = Field(default_factory=list, description="All automation analyses")
    total_automations: int = Field(default=0, description="Total number of automations")
    last_updated: datetime = Field(..., description="When ecosystem was last analyzed")
    analysis_summary: dict[str, Any] = Field(default_factory=dict, description="Summary statistics")

    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ContentSearchResult(BaseModel):
    """Result of searching automations by content fragments."""

    automation_id: str = Field(..., min_length=1, description="ID of automation containing the content")
    automation_name: str = Field(..., min_length=1, description="Name of the automation")
    automation_description: str | None = Field(None, description="Description of the automation")
    matching_blocks: list[BlockInfo] = Field(default_factory=list, description="Blocks containing the search content")
    match_count: int = Field(default=0, ge=0, description="Number of content matches found")
    search_fragment: str = Field(..., min_length=1, description="The content fragment that was searched for")

    @field_validator('automation_id')
    @classmethod
    def validate_automation_id(cls, v):
        if not v or not v.strip():
            raise ValueError("automation_id cannot be empty")
        return v

    @field_validator('search_fragment')
    @classmethod
    def validate_search_fragment(cls, v):
        if not v or not v.strip():
            raise ValueError("search_fragment cannot be empty")
        return v


