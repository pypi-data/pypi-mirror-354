#!/usr/bin/env python3
"""
Quick Spam Search - Find automations with specific content patterns
"""

import asyncio

from fastmcp import Client

from src.activecamp_mcp.server import mcp


async def quick_search():
    """Quick search for spam automations."""

    print("🔍 Quick Spam Search - Finding 'Automation Workz' content...")
    print("=" * 60)

    async with Client(mcp) as client:
        # Search for the main spam identifier
        print("🎯 Searching for 'Automation Workz'...")
        try:
            result = await client.call_tool(
                "search_automations_by_content",
                {
                    "search_fragment": "Automation Workz",
                    "case_sensitive": False,
                    "limit": 5
                }
            )

            if result and isinstance(result, list) and len(result) > 0:
                if "error" in result[0]:
                    print(f"❌ Error: {result[0]['error']}")
                else:
                    print(f"✅ Found {len(result)} automation(s) with 'Automation Workz'")

                    for i, automation in enumerate(result, 1):
                        print(f"\n🎯 CANDIDATE #{i}")
                        print(f"   ID: {automation.get('automation_id')}")
                        print(f"   Name: {automation.get('automation_name')}")
                        print(f"   Matches: {automation.get('match_count', 0)}")

                        blocks = automation.get('matching_blocks', [])
                        if blocks:
                            print(f"   📋 Matching Blocks ({len(blocks)}):")
                            for j, block in enumerate(blocks[:2], 1):  # Show first 2 blocks
                                print(f"      {j}. {block.get('block_type', 'unknown').upper()}")
                                print(f"         Description: {block.get('description', 'No description')}")

                                params = block.get('parameters', {})
                                if 'subject' in params:
                                    print(f"         Subject: {params['subject'][:100]}...")
                                if 'message' in params:
                                    print(f"         Message: {params['message'][:200]}...")
            else:
                print("⚪ No automations found with 'Automation Workz'")

        except Exception as e:
            print(f"❌ Search failed: {str(e)}")

        print("\n" + "=" * 60)

        # Also try searching for workshop content
        print("🎯 Searching for 'Admissions Sampler'...")
        try:
            result2 = await client.call_tool(
                "search_automations_by_content",
                {
                    "search_fragment": "Admissions Sampler",
                    "case_sensitive": False,
                    "limit": 5
                }
            )

            if result2 and isinstance(result2, list) and len(result2) > 0:
                if "error" in result2[0]:
                    print(f"❌ Error: {result2[0]['error']}")
                else:
                    print(f"✅ Found {len(result2)} automation(s) with 'Admissions Sampler'")

                    for i, automation in enumerate(result2, 1):
                        print(f"\n🎯 WORKSHOP CANDIDATE #{i}")
                        print(f"   ID: {automation.get('automation_id')}")
                        print(f"   Name: {automation.get('automation_name')}")
                        print(f"   Matches: {automation.get('match_count', 0)}")
            else:
                print("⚪ No automations found with 'Admissions Sampler'")

        except Exception as e:
            print(f"❌ Workshop search failed: {str(e)}")

        print("\n🎯 Search complete!")


if __name__ == "__main__":
    asyncio.run(quick_search())

