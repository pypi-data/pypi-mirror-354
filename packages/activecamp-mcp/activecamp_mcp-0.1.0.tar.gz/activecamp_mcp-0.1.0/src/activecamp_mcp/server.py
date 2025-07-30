import httpx
import yaml
from fastmcp import FastMCP
from fastmcp.server.openapi import MCPType, RouteMap

from activecamp_mcp.analyzers import AutomationFlowAnalyzer
from activecamp_mcp.cache import CacheManager
from activecamp_mcp.content_search import AutomationContentSearcher
from activecamp_mcp.settings import settings

# Create an authenticated httpx.AsyncClient instance
client = httpx.AsyncClient(
    base_url=settings.ac_api_url,
    headers={
        "Api-Token": settings.ac_api_token,
        "Content-Type": "application/json"
    },
    timeout=30.0
)

# Define the list of RouteMap objects for exclusions.
route_maps = [
    # Exclude granular contact data: pattern=r"^/api/3/contacts/.+/.+"
    RouteMap(
        pattern=r"^/api/3/contacts/.+/.+",
        mcp_type=MCPType.EXCLUDE
    ),
    # Exclude simple contact creation: pattern=r"^/api/3/contacts$", methods=["POST"]
    RouteMap(
        pattern=r"^/api/3/contacts$",
        methods=["POST"],
        mcp_type=MCPType.EXCLUDE
    ),
    # Exclude bulk delete accounts endpoint
    RouteMap(
        pattern=r"^/api/3/accounts/bulk_delete/.+",
        mcp_type=MCPType.EXCLUDE
    ),
]

# Load and parse the YAML from activev3.yml
with open("data/activev3.yml") as f:
    spec = yaml.safe_load(f)

# Call FastMCP.from_openapi and assign the result to mcp
mcp = FastMCP.from_openapi(
    openapi_spec=spec,
    client=client,
    route_maps=route_maps
)

# Initialize automation analysis components
cache_manager = CacheManager()
automation_analyzer = AutomationFlowAnalyzer(client, cache_manager)
content_searcher = AutomationContentSearcher(client, automation_analyzer)


@mcp.tool()
async def search_automations_by_content(
    search_fragment: str,
    case_sensitive: bool = False,
    limit: int | None = 10
) -> list[dict]:
    """Search automations for specific content fragments.

    This tool helps you find automations that contain specific text in their messages,
    subjects, or other content. Perfect for tracking down the source of spam messages
    or finding automations with specific content.

    Args:
        search_fragment: Text fragment to search for (e.g., "Automation Workz", "workshop")
        case_sensitive: Whether the search should be case sensitive (default: False)
        limit: Maximum number of results to return (default: 10)

    Returns:
        List of automation search results with matching content
    """
    try:
        results = await content_searcher.search_by_content_fragment(
            search_fragment=search_fragment,
            case_sensitive=case_sensitive,
            limit=limit
        )

        # Convert to dict format for MCP response
        return [
            {
                "automation_id": result.automation_id,
                "automation_name": result.automation_name,
                "automation_description": result.automation_description,
                "match_count": result.match_count,
                "search_fragment": result.search_fragment,
                "matching_blocks": [
                    {
                        "block_id": block.block_id,
                        "block_type": block.block_type,
                        "description": block.description,
                        "parameters": block.parameters,
                        "order": block.order
                    }
                    for block in result.matching_blocks
                ]
            }
            for result in results
        ]
    except Exception as e:
        return [{"error": f"Search failed: {str(e)}"}]


@mcp.tool()
async def search_automations_by_regex(
    pattern: str,
    limit: int | None = 10
) -> list[dict]:
    """Search automations using regex patterns.

    Advanced search tool that allows you to use regular expressions to find
    automations with specific patterns in their content.

    Args:
        pattern: Regular expression pattern to search for
        limit: Maximum number of results to return (default: 10)

    Returns:
        List of automation search results matching the regex pattern
    """
    try:
        results = await content_searcher.search_by_regex_pattern(
            pattern=pattern,
            limit=limit
        )

        # Convert to dict format for MCP response
        return [
            {
                "automation_id": result.automation_id,
                "automation_name": result.automation_name,
                "automation_description": result.automation_description,
                "match_count": result.match_count,
                "search_pattern": result.search_fragment,
                "matching_blocks": [
                    {
                        "block_id": block.block_id,
                        "block_type": block.block_type,
                        "description": block.description,
                        "parameters": block.parameters,
                        "order": block.order
                    }
                    for block in result.matching_blocks
                ]
            }
            for result in results
        ]
    except Exception as e:
        return [{"error": f"Regex search failed: {str(e)}"}]


@mcp.tool()
async def find_automations_with_urls(
    domain_filter: str | None = None,
    limit: int | None = 10
) -> list[dict]:
    """Find automations containing URLs.

    Useful for finding automations that include links, especially helpful for
    tracking down automations with specific domains (like zoom.us links).

    Args:
        domain_filter: Optional domain to filter by (e.g., "zoom.us", "example.com")
        limit: Maximum number of results to return (default: 10)

    Returns:
        List of automations containing URLs, optionally filtered by domain
    """
    try:
        results = await content_searcher.find_automations_with_urls(
            domain_filter=domain_filter,
            limit=limit
        )

        # Convert to dict format for MCP response
        return [
            {
                "automation_id": result.automation_id,
                "automation_name": result.automation_name,
                "automation_description": result.automation_description,
                "match_count": result.match_count,
                "domain_filter": domain_filter,
                "matching_blocks": [
                    {
                        "block_id": block.block_id,
                        "block_type": block.block_type,
                        "description": block.description,
                        "parameters": block.parameters,
                        "order": block.order
                    }
                    for block in result.matching_blocks
                ]
            }
            for result in results
        ]
    except Exception as e:
        return [{"error": f"URL search failed: {str(e)}"}]


@mcp.tool()
async def analyze_automation_workflow(automation_id: str) -> dict:
    """Analyze a specific automation workflow in detail.

    Get comprehensive analysis of an automation including triggers, blocks,
    flow graph, and visual data.

    Args:
        automation_id: ID of the automation to analyze

    Returns:
        Complete automation analysis including structure and content
    """
    try:
        analysis = await automation_analyzer.analyze_automation(automation_id)

        return {
            "automation_id": analysis.automation_id,
            "name": analysis.name,
            "description": analysis.description,
            "triggers": [
                {
                    "trigger_id": trigger.trigger_id,
                    "trigger_type": trigger.trigger_type,
                    "related_id": trigger.related_id,
                    "related_name": trigger.related_name,
                    "conditions": trigger.conditions,
                    "multi_entry": trigger.multi_entry
                }
                for trigger in analysis.triggers
            ],
            "blocks": [
                {
                    "block_id": block.block_id,
                    "block_type": block.block_type,
                    "order": block.order,
                    "description": block.description,
                    "parameters": block.parameters,
                    "affects_contact": block.affects_contact,
                    "parent_id": block.parent_id
                }
                for block in analysis.blocks
            ],
            "flow_graph": {
                "nodes": [
                    {
                        "node_id": node.node_id,
                        "node_type": node.node_type,
                        "label": node.label,
                        "metadata": node.metadata
                    }
                    for node in analysis.flow_graph.nodes
                ] if analysis.flow_graph else [],
                "edges": [
                    {
                        "source": edge.source,
                        "target": edge.target,
                        "label": edge.label,
                        "condition": edge.condition
                    }
                    for edge in analysis.flow_graph.edges
                ] if analysis.flow_graph else []
            },
            "visual_data": {
                "screenshot_url": analysis.visual_data.screenshot_url,
                "visual_elements": analysis.visual_data.visual_elements
            } if analysis.visual_data else None,
            "analysis_timestamp": analysis.analysis_timestamp.isoformat() if analysis.analysis_timestamp else None
        }
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

def main():
    mcp.run(
        host=settings.host,
        port=settings.port,
        transport="sse",
    )


if __name__ == "__main__":
    main()
