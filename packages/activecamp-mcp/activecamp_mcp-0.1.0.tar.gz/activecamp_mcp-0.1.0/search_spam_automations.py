#!/usr/bin/env python3
"""
Automation Spam Hunter - Find the automations responsible for spam messages

This script uses the MCP tools to search your ActiveCampaign automations
for the specific content patterns from your spam messages.
"""

import asyncio

from fastmcp import Client

from src.activecamp_mcp.server import mcp


async def search_for_spam_automations():
    """Search for automations responsible for the spam messages."""

    print("🔍 Starting Automation Spam Hunt...")
    print("=" * 60)

    async with Client(mcp) as client:
        # Get available tools to confirm everything is working
        tools = await client.list_tools()
        search_tools = [tool.name for tool in tools if 'search' in tool.name.lower()]
        print(f"✅ Connected to MCP server with {len(search_tools)} search tools available")
        print(f"   Available search tools: {', '.join(search_tools)}")
        print()

        # Define our search queries based on the spam screenshot
        searches = [
            {
                "name": "Primary Spam Content",
                "tool": "search_automations_by_content",
                "params": {"search_fragment": "Automation Workz", "case_sensitive": False, "limit": 10}
            },
            {
                "name": "Workshop/Admissions Content",
                "tool": "search_automations_by_content",
                "params": {"search_fragment": "Admissions Sampler", "case_sensitive": False, "limit": 10}
            },
            {
                "name": "Zoom Meeting Links",
                "tool": "find_automations_with_urls",
                "params": {"domain_filter": "zoom.us", "limit": 10}
            },
            {
                "name": "Specific Meeting ID",
                "tool": "search_automations_by_content",
                "params": {"search_fragment": "82113727363", "case_sensitive": False, "limit": 10}
            },
            {
                "name": "Earnings Claims",
                "tool": "search_automations_by_content",
                "params": {"search_fragment": "$25-$40", "case_sensitive": False, "limit": 10}
            },
            {
                "name": "Phone Number",
                "tool": "search_automations_by_content",
                "params": {"search_fragment": "(313) 774-1106", "case_sensitive": False, "limit": 10}
            },
            {
                "name": "Opt-out Text",
                "tool": "search_automations_by_content",
                "params": {"search_fragment": "Reply STOP to opt out", "case_sensitive": False, "limit": 10}
            }
        ]

        all_candidates = {}

        # Run each search
        for search in searches:
            print(f"🔎 Searching for: {search['name']}")
            print(f"   Query: {search['params']}")

            try:
                # Call the MCP tool
                result = await client.call_tool(search["tool"], search["params"])

                if result and isinstance(result, list) and len(result) > 0:
                    # Check if we got an error
                    if len(result) == 1 and "error" in result[0]:
                        print(f"   ❌ Error: {result[0]['error']}")
                    else:
                        print(f"   ✅ Found {len(result)} candidate automation(s)")

                        # Store candidates
                        for candidate in result:
                            automation_id = candidate.get("automation_id")
                            if automation_id:
                                if automation_id not in all_candidates:
                                    all_candidates[automation_id] = {
                                        "automation": candidate,
                                        "found_in_searches": []
                                    }
                                all_candidates[automation_id]["found_in_searches"].append(search["name"])
                else:
                    print("   ⚪ No matches found")

            except Exception as e:
                print(f"   ❌ Search failed: {str(e)}")

            print()

        # Analyze and rank candidates
        print("📊 CANDIDATE ANALYSIS")
        print("=" * 60)

        if not all_candidates:
            print("❌ No automations found matching the spam content patterns.")
            print("   This could mean:")
            print("   • The automation is using different text than what's visible")
            print("   • The content is dynamically generated")
            print("   • The automation is in a different ActiveCampaign account")
            print("   • The messages are sent via a different system")
            return

        # Sort candidates by number of search matches (most suspicious first)
        sorted_candidates = sorted(
            all_candidates.items(),
            key=lambda x: len(x[1]["found_in_searches"]),
            reverse=True
        )

        print(f"Found {len(sorted_candidates)} candidate automation(s):")
        print()

        for i, (automation_id, data) in enumerate(sorted_candidates, 1):
            automation = data["automation"]
            searches_found = data["found_in_searches"]

            print(f"🎯 CANDIDATE #{i} - SUSPICION LEVEL: {'🔴 HIGH' if len(searches_found) >= 3 else '🟡 MEDIUM' if len(searches_found) >= 2 else '🟢 LOW'}")
            print(f"   Automation ID: {automation_id}")
            print(f"   Name: {automation.get('automation_name', 'Unknown')}")
            print(f"   Description: {automation.get('automation_description', 'No description')}")
            print(f"   Match Count: {automation.get('match_count', 0)} content matches")
            print(f"   Found in {len(searches_found)} searches: {', '.join(searches_found)}")

            # Show matching blocks
            matching_blocks = automation.get("matching_blocks", [])
            if matching_blocks:
                print(f"   📋 Matching Blocks ({len(matching_blocks)}):")
                for j, block in enumerate(matching_blocks[:3], 1):  # Show first 3 blocks
                    print(f"      {j}. {block.get('block_type', 'unknown').upper()} - {block.get('description', 'No description')}")

                    # Show key parameters
                    params = block.get('parameters', {})
                    if 'subject' in params:
                        print(f"         Subject: {params['subject'][:100]}...")
                    if 'message' in params:
                        print(f"         Message: {params['message'][:150]}...")

                if len(matching_blocks) > 3:
                    print(f"      ... and {len(matching_blocks) - 3} more blocks")

            print()

        # Provide next steps
        print("🎯 NEXT STEPS")
        print("=" * 60)

        if sorted_candidates:
            top_candidate = sorted_candidates[0]
            automation_id = top_candidate[0]
            searches_found = len(top_candidate[1]["found_in_searches"])

            if searches_found >= 3:
                print(f"🔴 HIGH CONFIDENCE: Automation {automation_id} is very likely the spam source!")
                print(f"   • Found in {searches_found} different searches")
                print("   • Contains multiple spam content patterns")
                print("   • Recommend immediate investigation and disabling")
            elif searches_found >= 2:
                print(f"🟡 MEDIUM CONFIDENCE: Automation {automation_id} is a strong candidate")
                print(f"   • Found in {searches_found} searches")
                print("   • Recommend detailed analysis")
            else:
                print(f"🟢 LOW CONFIDENCE: Automation {automation_id} has some matches")
                print(f"   • Only found in {searches_found} search")
                print("   • May be related but not the primary source")

            print()
            print("To get detailed analysis of the top candidate, run:")
            print(f"   analyze_automation_workflow('{automation_id}')")

        print()
        print("✅ Spam hunt complete!")


async def analyze_specific_automation(automation_id: str):
    """Get detailed analysis of a specific automation."""

    print(f"🔬 Analyzing Automation {automation_id} in detail...")
    print("=" * 60)

    async with Client(mcp) as client:
        try:
            result = await client.call_tool("analyze_automation_workflow", {"automation_id": automation_id})

            if result and "error" not in result:
                print(f"📋 Automation Name: {result.get('name', 'Unknown')}")
                print(f"📝 Description: {result.get('description', 'No description')}")
                print()

                # Show triggers
                triggers = result.get('triggers', [])
                if triggers:
                    print(f"🎯 Triggers ({len(triggers)}):")
                    for trigger in triggers:
                        print(f"   • {trigger.get('trigger_type', 'unknown')}: {trigger.get('description', 'No description')}")
                    print()

                # Show blocks
                blocks = result.get('blocks', [])
                if blocks:
                    print(f"🧩 Automation Blocks ({len(blocks)}):")
                    for i, block in enumerate(blocks, 1):
                        print(f"   {i}. {block.get('block_type', 'unknown').upper()} - {block.get('description', 'No description')}")

                        # Show parameters for send blocks
                        if block.get('block_type') == 'send':
                            params = block.get('parameters', {})
                            if 'subject' in params:
                                print(f"      📧 Subject: {params['subject']}")
                            if 'message' in params:
                                message = params['message'][:300] + "..." if len(params['message']) > 300 else params['message']
                                print(f"      💬 Message: {message}")
                        print()

                # Show contact changes
                contact_changes = result.get('contact_changes', [])
                if contact_changes:
                    print(f"👥 Contact Changes ({len(contact_changes)}):")
                    for change in contact_changes:
                        print(f"   • {change.get('change_type', 'unknown')}: {change.get('description', 'No description')}")
                    print()

            else:
                print(f"❌ Failed to analyze automation: {result.get('error', 'Unknown error')}")

        except Exception as e:
            print(f"❌ Analysis failed: {str(e)}")


if __name__ == "__main__":
    print("🚨 AUTOMATION SPAM HUNTER 🚨")
    print("Finding the automation responsible for your spam messages...")
    print()

    # Run the spam search
    asyncio.run(search_for_spam_automations())

    # Optionally analyze a specific automation
    # Uncomment and replace with actual automation ID:
    # asyncio.run(analyze_specific_automation("12345"))

