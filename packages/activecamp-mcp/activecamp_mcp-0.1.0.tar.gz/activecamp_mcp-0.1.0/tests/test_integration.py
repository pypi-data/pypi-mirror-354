"""Integration tests for the ActiveCampaign MCP server."""

import pytest
from fastmcp import Client

from activecamp_mcp.server import mcp


@pytest.mark.asyncio
async def test_server_integration():
    """Test basic server integration without making real API calls."""
    async with Client(mcp) as client:
        # Test that we can connect and get basic info
        tools = await client.list_tools()
        resources = await client.list_resources()

        # Verify we have the expected number of tools and resources
        assert len(tools) == 19, f"Expected 19 tools, got {len(tools)}"
        assert len(resources) == 9, f"Expected 9 resources, got {len(resources)}"

        # Verify some specific tools exist
        tool_names = [tool.name for tool in tools]
        assert "Update_account" in tool_names
        assert "Create_account" in tool_names

        # Verify some specific resources exist
        resource_uris = [str(resource.uri) for resource in resources]
        assert "resource://List_accounts" in resource_uris

        # Verify excluded routes are not present
        # Should not have POST contacts tool
        post_contact_tools = [name for name in tool_names
                             if 'post' in name.lower() and 'contact' in name.lower()]
        assert len(post_contact_tools) == 0, f"Found unexpected POST contact tools: {post_contact_tools}"


@pytest.mark.asyncio
async def test_tool_schema_validation():
    """Test that tool schemas are properly formed."""
    async with Client(mcp) as client:
        tools = await client.list_tools()

        for tool in tools:
            # Each tool should have a valid schema
            schema = tool.inputSchema
            assert isinstance(schema, dict)
            assert 'type' in schema
            assert schema['type'] == 'object'

            # If it has properties, they should be properly defined
            if 'properties' in schema:
                assert isinstance(schema['properties'], dict)
                for _prop_name, prop_def in schema['properties'].items():
                    assert isinstance(prop_def, dict)
                    # Each property should have a type, $ref, or anyOf (for Optional types)
                    assert 'type' in prop_def or '$ref' in prop_def or 'anyOf' in prop_def, \
                        f"Property {_prop_name} in tool {tool.name} missing type, $ref, or anyOf: {prop_def}"


@pytest.mark.asyncio
async def test_resource_schema_validation():
    """Test that resource schemas are properly formed."""
    async with Client(mcp) as client:
        resources = await client.list_resources()

        for resource in resources:
            # Each resource should have a valid URI
            assert resource.uri is not None
            assert str(resource.uri).startswith('resource://')

            # Each resource should have a name
            assert resource.name is not None
            assert len(resource.name) > 0

            # Each resource should have a description
            assert hasattr(resource, 'description')


def test_route_exclusions_comprehensive():
    """Comprehensive test of route exclusions."""
    from fastmcp.server.openapi import MCPType

    from activecamp_mcp.server import route_maps

    # Get all exclusion rules
    exclusions = [rm for rm in route_maps if rm.mcp_type == MCPType.EXCLUDE]

    # Should have exactly 3 exclusions as defined
    assert len(exclusions) == 3

    # Test each exclusion rule
    patterns_and_methods = [(rm.pattern, rm.methods) for rm in exclusions]

    # Should exclude granular contact data
    granular_contact_exclusion = [
        (pattern, methods) for pattern, methods in patterns_and_methods
        if "contacts/.+/.+" in pattern
    ]
    assert len(granular_contact_exclusion) == 1

    # Should exclude POST contacts
    post_contact_exclusion = [
        (pattern, methods) for pattern, methods in patterns_and_methods
        if "contacts$" in pattern and methods and "POST" in methods
    ]
    assert len(post_contact_exclusion) == 1

    # Should exclude bulk delete accounts
    bulk_delete_exclusion = [
        (pattern, methods) for pattern, methods in patterns_and_methods
        if "accounts/bulk_delete" in pattern
    ]
    assert len(bulk_delete_exclusion) == 1
