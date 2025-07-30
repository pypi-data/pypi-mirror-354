"""Test specific functionality for listing contacts and getting automations."""

import pytest
from fastmcp import Client

from activecamp_mcp.server import mcp


@pytest.mark.asyncio
async def test_can_list_contacts():
    """Test that the server provides the ability to list contacts."""
    async with Client(mcp) as client:
        resources = await client.list_resources()

        # Check that we have the Get_Contacts resource
        resource_uris = [str(resource.uri) for resource in resources]
        assert "resource://Get_Contacts" in resource_uris, f"Get_Contacts resource not found in: {resource_uris}"

        # Get the specific resource
        contacts_resource = next(res for res in resources if str(res.uri) == "resource://Get_Contacts")

        # Verify it has the expected properties
        assert contacts_resource.name == "Get_Contacts"
        assert hasattr(contacts_resource, 'uri')
        assert str(contacts_resource.uri) == "resource://Get_Contacts"


@pytest.mark.asyncio
async def test_can_get_automations():
    """Test that the server provides the ability to get automations."""
    async with Client(mcp) as client:
        resources = await client.list_resources()

        # Check that we have the List_Contact_Automations resource
        resource_uris = [str(resource.uri) for resource in resources]
        assert "resource://List_Contact_Automations" in resource_uris, f"List_Contact_Automations resource not found in: {resource_uris}"

        # Get the specific resource
        automations_resource = next(res for res in resources if str(res.uri) == "resource://List_Contact_Automations")

        # Verify it has the expected properties
        assert automations_resource.name == "List_Contact_Automations"
        assert hasattr(automations_resource, 'uri')
        assert str(automations_resource.uri) == "resource://List_Contact_Automations"


@pytest.mark.asyncio
async def test_contact_management_tools_available():
    """Test that contact management tools are available."""
    async with Client(mcp) as client:
        tools = await client.list_tools()

        tool_names = [tool.name for tool in tools]

        # Should have contact creation/update tool
        assert "Create_or_Update_Contact" in tool_names, f"Create_or_Update_Contact tool not found in: {tool_names}"

        # Should have contact deletion tool
        assert "Delete_Contact" in tool_names, f"Delete_Contact tool not found in: {tool_names}"

        # Should have bulk import tool
        assert "Bulk_import_contacts" in tool_names, f"Bulk_import_contacts tool not found in: {tool_names}"


@pytest.mark.asyncio
async def test_automation_management_tools_available():
    """Test that automation management tools are available."""
    async with Client(mcp) as client:
        tools = await client.list_tools()

        tool_names = [tool.name for tool in tools]

        # Should have automation tools
        assert "Add_Contact_to_Automation" in tool_names, f"Add_Contact_to_Automation tool not found in: {tool_names}"
        assert "Get_Contact_Automation" in tool_names, f"Get_Contact_Automation tool not found in: {tool_names}"
        assert "Delete_Contact_Automation" in tool_names, f"Delete_Contact_Automation tool not found in: {tool_names}"


@pytest.mark.asyncio
async def test_contact_tools_have_proper_schemas():
    """Test that contact-related tools have proper input schemas."""
    async with Client(mcp) as client:
        tools = await client.list_tools()

        # Find contact-related tools
        contact_tools = [tool for tool in tools if 'contact' in tool.name.lower()]

        assert len(contact_tools) > 0, "No contact tools found"

        for tool in contact_tools:
            # Each tool should have a valid input schema
            assert hasattr(tool, 'inputSchema'), f"Tool {tool.name} missing inputSchema"
            assert isinstance(tool.inputSchema, dict), f"Tool {tool.name} inputSchema is not a dict"
            assert 'type' in tool.inputSchema, f"Tool {tool.name} inputSchema missing type"

            # Should have description
            assert hasattr(tool, 'description'), f"Tool {tool.name} missing description"
            assert tool.description is not None, f"Tool {tool.name} has null description"


@pytest.mark.asyncio
async def test_automation_tools_have_proper_schemas():
    """Test that automation-related tools have proper input schemas."""
    async with Client(mcp) as client:
        tools = await client.list_tools()

        # Find automation-related tools
        automation_tools = [tool for tool in tools if 'automation' in tool.name.lower()]

        assert len(automation_tools) > 0, "No automation tools found"

        for tool in automation_tools:
            # Each tool should have a valid input schema
            assert hasattr(tool, 'inputSchema'), f"Tool {tool.name} missing inputSchema"
            assert isinstance(tool.inputSchema, dict), f"Tool {tool.name} inputSchema is not a dict"
            assert 'type' in tool.inputSchema, f"Tool {tool.name} inputSchema missing type"

            # Should have description
            assert hasattr(tool, 'description'), f"Tool {tool.name} missing description"
            assert tool.description is not None, f"Tool {tool.name} has null description"


def test_contacts_and_automations_not_excluded():
    """Test that contacts and automations functionality is not excluded by route maps."""
    from fastmcp.server.openapi import MCPType

    from activecamp_mcp.server import route_maps

    # Get exclusion patterns
    exclusions = [rm for rm in route_maps if rm.mcp_type == MCPType.EXCLUDE]
    exclusion_patterns = [rm.pattern for rm in exclusions]

    # Verify that general contact listing is not excluded
    # (We only exclude granular contact data and POST contacts)
    for pattern in exclusion_patterns:
        # Should not exclude GET /contacts (listing)
        assert not (pattern == r"^/api/3/contacts$" and any(rm.methods == ["GET"] for rm in exclusions if rm.pattern == pattern)), \
            "GET /contacts should not be excluded"

    # Verify automation endpoints are not excluded
    automation_patterns = [pattern for pattern in exclusion_patterns if 'automation' in pattern.lower()]
    assert len(automation_patterns) == 0, f"Automation endpoints should not be excluded, but found: {automation_patterns}"


@pytest.mark.asyncio
async def test_resource_functionality_summary():
    """Test and summarize the available contact and automation functionality."""
    async with Client(mcp) as client:
        tools = await client.list_tools()
        resources = await client.list_resources()

        # Count contact and automation capabilities
        contact_tools = [tool for tool in tools if 'contact' in tool.name.lower()]
        automation_tools = [tool for tool in tools if 'automation' in tool.name.lower()]
        contact_resources = [res for res in resources if 'contact' in str(res.uri).lower()]
        automation_resources = [res for res in resources if 'automation' in str(res.uri).lower()]

        # Verify we have sufficient capabilities
        assert len(contact_tools) >= 5, f"Expected at least 5 contact tools, got {len(contact_tools)}"
        assert len(automation_tools) >= 3, f"Expected at least 3 automation tools, got {len(automation_tools)}"
        assert len(contact_resources) >= 1, f"Expected at least 1 contact resource, got {len(contact_resources)}"
        assert len(automation_resources) >= 1, f"Expected at least 1 automation resource, got {len(automation_resources)}"

        # Verify specific capabilities exist
        tool_names = [tool.name for tool in tools]
        resource_uris = [str(res.uri) for res in resources]

        # Can list contacts
        assert "resource://Get_Contacts" in resource_uris, "Cannot list contacts"

        # Can manage contacts
        assert "Create_or_Update_Contact" in tool_names, "Cannot create/update contacts"
        assert "Delete_Contact" in tool_names, "Cannot delete contacts"

        # Can list automations
        assert "resource://List_Contact_Automations" in resource_uris, "Cannot list automations"

        # Can manage contact automations
        assert "Add_Contact_to_Automation" in tool_names, "Cannot add contacts to automations"
        assert "Get_Contact_Automation" in tool_names, "Cannot get contact automation details"
        assert "Delete_Contact_Automation" in tool_names, "Cannot remove contacts from automations"

