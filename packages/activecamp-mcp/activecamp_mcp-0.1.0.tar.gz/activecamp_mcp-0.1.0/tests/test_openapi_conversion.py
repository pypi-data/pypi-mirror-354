"""Test OpenAPI to MCP conversion with route exclusions."""

import yaml
from fastmcp.server.openapi import MCPType

from activecamp_mcp.server import client, mcp, route_maps


def test_route_maps_defined():
    """Test that route maps for exclusions are properly defined."""

    # Should have at least 3 exclusion rules
    assert len(route_maps) >= 3

    # All should be exclusion type
    for route_map in route_maps:
        assert route_map.mcp_type == MCPType.EXCLUDE

    # Check specific patterns exist
    patterns = [rm.pattern for rm in route_maps if rm.pattern]

    # Should exclude granular contact data
    assert any(r"contacts/.+/.+" in pattern for pattern in patterns)

    # Should exclude simple contact creation (POST /contacts)
    post_contact_exclusions = [
        rm for rm in route_maps
        if rm.pattern and "contacts$" in rm.pattern and "POST" in (rm.methods or [])
    ]
    assert len(post_contact_exclusions) >= 1


def test_yaml_loading():
    """Test that activev3.yml can be loaded and parsed."""

    with open("data/activev3.yml") as f:
        spec = yaml.safe_load(f)

    # Basic OpenAPI structure validation
    assert "openapi" in spec
    assert "info" in spec
    assert "paths" in spec
    assert spec["openapi"].startswith("3.")


def test_mcp_creation():
    """Test that FastMCP server was created successfully."""
    # Verify the mcp object exists and is properly configured
    assert mcp is not None

    # Verify it has the expected attributes of a FastMCP instance
    assert hasattr(mcp, 'run')
    assert hasattr(mcp, 'get_tools')
    assert hasattr(mcp, 'get_resources')


def test_mcp_variable_exists():
    """Test that the mcp variable is properly assigned."""

    # Should be a FastMCP instance
    assert mcp is not None

    # Should have tools and resources methods (from OpenAPI spec)
    assert hasattr(mcp, 'get_tools')
    assert hasattr(mcp, 'get_resources')

    # Should have a name
    assert hasattr(mcp, 'name')
    assert mcp.name == "OpenAPI FastMCP"


def test_client_configuration():
    """Test that the httpx client is properly configured."""

    # Should have base_url set
    assert client.base_url is not None

    # Should have API token in headers
    assert "Api-Token" in client.headers

