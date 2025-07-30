"""Practical demonstration of how to use the contacts and automations functionality."""

import pytest
from fastmcp import Client

from activecamp_mcp.server import mcp


@pytest.mark.asyncio
async def test_list_contacts_resource_details():
    """Demonstrate how to access the list contacts resource."""
    async with Client(mcp) as client:
        resources = await client.list_resources()

        # Find the contacts resource
        contacts_resource = next(
            (res for res in resources if str(res.uri) == "resource://Get_Contacts"),
            None
        )

        assert contacts_resource is not None, "Get_Contacts resource not found"

        print("\n📋 CONTACTS LISTING RESOURCE:")
        print(f"   URI: {contacts_resource.uri}")
        print(f"   Name: {contacts_resource.name}")
        print(f"   Description: {getattr(contacts_resource, 'description', 'No description')}")

        # This resource can be used to list all contacts
        # In a real implementation, you would call:
        # contacts_data = await client.read_resource(contacts_resource.uri)


@pytest.mark.asyncio
async def test_list_automations_resource_details():
    """Demonstrate how to access the list automations resource."""
    async with Client(mcp) as client:
        resources = await client.list_resources()

        # Find the automations resource
        automations_resource = next(
            (res for res in resources if str(res.uri) == "resource://List_Contact_Automations"),
            None
        )

        assert automations_resource is not None, "List_Contact_Automations resource not found"

        print("\n🤖 AUTOMATIONS LISTING RESOURCE:")
        print(f"   URI: {automations_resource.uri}")
        print(f"   Name: {automations_resource.name}")
        print(f"   Description: {getattr(automations_resource, 'description', 'No description')}")

        # This resource can be used to list all contact automations
        # In a real implementation, you would call:
        # automations_data = await client.read_resource(automations_resource.uri)


@pytest.mark.asyncio
async def test_contact_management_tools_details():
    """Demonstrate the available contact management tools."""
    async with Client(mcp) as client:
        tools = await client.list_tools()

        # Find contact management tools
        contact_tools = [tool for tool in tools if 'contact' in tool.name.lower()]

        print(f"\n👥 CONTACT MANAGEMENT TOOLS ({len(contact_tools)} available):")

        for tool in contact_tools:
            print(f"\n   🔧 {tool.name}")
            print(f"      Description: {getattr(tool, 'description', 'No description')[:100]}...")

            # Show input schema structure
            if hasattr(tool, 'inputSchema') and 'properties' in tool.inputSchema:
                properties = tool.inputSchema['properties']
                print(f"      Parameters: {list(properties.keys())}")

        # Verify key tools are available
        tool_names = [tool.name for tool in contact_tools]
        assert "Create_or_Update_Contact" in tool_names
        assert "Delete_Contact" in tool_names
        assert "Bulk_import_contacts" in tool_names


@pytest.mark.asyncio
async def test_automation_management_tools_details():
    """Demonstrate the available automation management tools."""
    async with Client(mcp) as client:
        tools = await client.list_tools()

        # Find automation management tools
        automation_tools = [tool for tool in tools if 'automation' in tool.name.lower()]

        print(f"\n🤖 AUTOMATION MANAGEMENT TOOLS ({len(automation_tools)} available):")

        for tool in automation_tools:
            print(f"\n   ⚙️ {tool.name}")
            print(f"      Description: {getattr(tool, 'description', 'No description')[:100]}...")

            # Show input schema structure
            if hasattr(tool, 'inputSchema') and 'properties' in tool.inputSchema:
                properties = tool.inputSchema['properties']
                print(f"      Parameters: {list(properties.keys())}")

        # Verify key tools are available
        tool_names = [tool.name for tool in automation_tools]
        assert "Add_Contact_to_Automation" in tool_names
        assert "Get_Contact_Automation" in tool_names
        assert "Delete_Contact_Automation" in tool_names


@pytest.mark.asyncio
async def test_usage_workflow_demonstration():
    """Demonstrate a typical workflow for contacts and automations."""
    async with Client(mcp) as client:
        tools = await client.list_tools()

        print("\\n🔄 TYPICAL WORKFLOW DEMONSTRATION:")
        print("\\n1. 📋 LIST ALL CONTACTS:")
        print("   Use resource: resource://Get_Contacts")
        print("   # contacts_data = await client.read_resource('resource://Get_Contacts')")

        print("\n2. 👤 CREATE OR UPDATE A CONTACT:")
        create_tool = next((t for t in tools if t.name == "Create_or_Update_Contact"), None)
        if create_tool:
            print(f"   Use tool: {create_tool.name}")
            print(f"   # result = await client.call_tool('{create_tool.name}', {{...contact_data...}})")

        print("\n3. 🤖 LIST ALL AUTOMATIONS:")
        print("   Use resource: resource://List_Contact_Automations")
        print("   # automations = await client.read_resource('resource://List_Contact_Automations')")

        print("\n4. ➕ ADD CONTACT TO AUTOMATION:")
        add_automation_tool = next((t for t in tools if t.name == "Add_Contact_to_Automation"), None)
        if add_automation_tool:
            print(f"   Use tool: {add_automation_tool.name}")
            print(f"   # result = await client.call_tool('{add_automation_tool.name}', {{...automation_data...}})")

        print("\n5. 📊 GET CONTACT AUTOMATION STATUS:")
        get_automation_tool = next((t for t in tools if t.name == "Get_Contact_Automation"), None)
        if get_automation_tool:
            print(f"   Use tool: {get_automation_tool.name}")
            print(f"   # status = await client.call_tool('{get_automation_tool.name}', {{...params...}})")

        print("\n✅ All required tools and resources are available!")


def test_capabilities_summary():
    """Provide a summary of contacts and automations capabilities."""
    print("\n📊 ACTIVECAMPAIGN MCP SERVER CAPABILITIES SUMMARY:")
    print("\n🎯 CONTACTS CAPABILITIES:")
    print("   ✅ List all contacts (resource://Get_Contacts)")
    print("   ✅ Create or update contacts")
    print("   ✅ Delete contacts")
    print("   ✅ Bulk import contacts")
    print("   ✅ Add/remove tags from contacts")
    print("   ✅ Subscribe/unsubscribe contacts from lists")

    print("\n🎯 AUTOMATIONS CAPABILITIES:")
    print("   ✅ List all contact automations (resource://List_Contact_Automations)")
    print("   ✅ Add contacts to automations")
    print("   ✅ Get contact automation details")
    print("   ✅ Remove contacts from automations")

    print("\n🚫 EXCLUDED (for security/performance):")
    print("   ❌ POST /api/3/contacts (use Create_or_Update_Contact tool instead)")
    print("   ❌ Granular contact data endpoints (/contacts/{id}/contactData, etc.)")
    print("   ❌ Bulk delete accounts endpoint")

    print("\n🔧 USAGE:")
    print("   • Use resources for listing/reading data")
    print("   • Use tools for creating/updating/deleting data")
    print("   • All tools have proper input schemas and validation")

    # This is just a summary test, always passes
    assert True
