"""Basic tests for MCP server functionality that don't require complex mocking."""

import pytest
from fastmcp import Client

from activecamp_mcp.server import mcp


@pytest.mark.asyncio
async def test_mcp_server_creation():
    """Test that the MCP server is properly created."""
    assert mcp is not None
    assert hasattr(mcp, 'name')
    # Check that it's a FastMCPOpenAPI instance
    assert type(mcp).__name__ == 'FastMCPOpenAPI'


@pytest.mark.asyncio
async def test_server_tools_available():
    """Test that tools are available from the OpenAPI spec."""
    async with Client(mcp) as client:
        # List available tools
        tools = await client.list_tools()

        # Should have tools generated from OpenAPI spec
        assert len(tools) > 0

        # Check that we have some expected tools (based on common ActiveCampaign endpoints)
        tool_names = [tool.name for tool in tools]

        # Should have account-related tools
        account_tools = [name for name in tool_names if 'account' in name.lower()]
        assert len(account_tools) > 0, f"Expected account tools, got: {tool_names}"


@pytest.mark.asyncio
async def test_server_resources_available():
    """Test that resources are available from the OpenAPI spec."""
    async with Client(mcp) as client:
        # List available resources
        resources = await client.list_resources()

        # Should have resources generated from OpenAPI spec
        assert len(resources) > 0

        # Check that we have some expected resources
        resource_uris = [resource.uri for resource in resources]

        # Should have some account or contact resources
        assert any('account' in str(uri).lower() or 'contact' in str(uri).lower()
                  for uri in resource_uris), f"Expected account/contact resources, got: {resource_uris}"


@pytest.mark.asyncio
async def test_excluded_routes_not_present():
    """Test that excluded routes are not present in the server."""
    async with Client(mcp) as client:
        tools = await client.list_tools()
        tool_names = [tool.name for tool in tools]

        # Should NOT have excluded endpoints as tools
        # Check that POST /api/3/contacts is excluded
        post_contact_tools = [name for name in tool_names
                             if 'post' in name.lower() and 'contact' in name.lower()
                             and not any(x in name.lower() for x in ['data', 'goal', 'log'])]

        # Should be empty or very limited since we excluded POST /contacts
        assert len(post_contact_tools) == 0, f"Found unexpected POST contact tools: {post_contact_tools}"


@pytest.mark.asyncio
async def test_route_exclusions_working():
    """Test that our route exclusions are actually working."""
    # Import the server components to verify exclusions
    from fastmcp.server.openapi import MCPType

    from activecamp_mcp.server import route_maps

    # Verify we have exclusion rules
    exclusion_rules = [rm for rm in route_maps if rm.mcp_type == MCPType.EXCLUDE]
    assert len(exclusion_rules) >= 3

    # Verify specific patterns are excluded
    patterns = [rm.pattern for rm in exclusion_rules]

    # Should exclude granular contact data
    assert any("contacts/.+/.+" in pattern for pattern in patterns)

    # Should exclude POST contacts
    post_exclusions = [rm for rm in exclusion_rules
                      if rm.methods and "POST" in rm.methods]
    assert len(post_exclusions) >= 1


def test_yaml_spec_loading():
    """Test that the YAML specification loads correctly."""
    import yaml

    with open("data/activev3.yml") as f:
        spec = yaml.safe_load(f)

    # Basic validation
    assert "openapi" in spec
    assert "paths" in spec
    assert "info" in spec

    # Should have some paths
    assert len(spec["paths"]) > 0

    # Should be OpenAPI 3.x
    assert spec["openapi"].startswith("3.")


def test_server_imports():
    """Test that all required imports work correctly."""
    from fastmcp.server.openapi import RouteMap

    from activecamp_mcp.server import client, mcp, route_maps

    assert mcp is not None
    assert client is not None
    assert route_maps is not None
    assert len(route_maps) > 0
    assert all(isinstance(rm, RouteMap) for rm in route_maps)


@pytest.mark.asyncio
async def test_tool_names_and_schemas():
    """Test that tools have proper names and schemas."""
    async with Client(mcp) as client:
        tools = await client.list_tools()

        assert len(tools) > 0

        for tool in tools:
            # Each tool should have a name
            assert hasattr(tool, 'name')
            assert tool.name is not None
            assert len(tool.name) > 0

            # Each tool should have an input schema
            assert hasattr(tool, 'inputSchema')
            assert tool.inputSchema is not None

            # Schema should be a dict with type
            assert isinstance(tool.inputSchema, dict)
            assert 'type' in tool.inputSchema


@pytest.mark.asyncio
async def test_resource_uris_and_names():
    """Test that resources have proper URIs and names."""
    async with Client(mcp) as client:
        resources = await client.list_resources()

        assert len(resources) > 0

        for resource in resources:
            # Each resource should have a URI
            assert hasattr(resource, 'uri')
            assert resource.uri is not None
            assert len(str(resource.uri)) > 0

            # Each resource should have a name
            assert hasattr(resource, 'name')
            assert resource.name is not None
            assert len(resource.name) > 0
