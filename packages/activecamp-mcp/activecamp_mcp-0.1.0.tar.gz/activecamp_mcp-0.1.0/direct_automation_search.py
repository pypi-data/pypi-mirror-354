#!/usr/bin/env python3
"""
Direct automation search - Get raw automation data to find spam content
"""

import asyncio

import httpx

from src.activecamp_mcp.settings import settings

# Create an authenticated httpx.AsyncClient instance
client = httpx.AsyncClient(
    base_url=settings.ac_api_url,
    headers={
        "Api-Token": settings.ac_api_token,
        "Content-Type": "application/json"
    },
    timeout=30.0
)


async def search_automations_directly():
    """Search automations directly via API."""

    print("🔍 Direct Automation Search")
    print("=" * 50)

    try:
        # Get all automations
        print("📥 Fetching all automations...")
        response = await client.get("automations")
        response.raise_for_status()
        data = response.json()

        automations = data.get("automations", [])
        print(f"✅ Found {len(automations)} total automations")

        # Search for spam content in automation names and descriptions
        spam_candidates = []

        for automation in automations:
            automation_id = automation["id"]
            name = automation.get("name", "") or ""
            description = automation.get("description", "") or ""

            # Check for spam keywords
            spam_keywords = [
                "automation workz", "admissions sampler", "workshop",
                "zoom", "82113727363", "$25", "$40", "313", "774-1106"
            ]

            matches = []
            for keyword in spam_keywords:
                if keyword.lower() in name.lower() or keyword.lower() in description.lower():
                    matches.append(keyword)

            if matches:
                spam_candidates.append({
                    "id": automation_id,
                    "name": name,
                    "description": description,
                    "matches": matches
                })

        print(f"\n🎯 Found {len(spam_candidates)} candidate automations:")

        for i, candidate in enumerate(spam_candidates, 1):
            print(f"\n📋 CANDIDATE #{i}")
            print(f"   ID: {candidate['id']}")
            print(f"   Name: {candidate['name']}")
            print(f"   Description: {candidate['description'][:200]}...")
            print(f"   Keyword Matches: {', '.join(candidate['matches'])}")

            # Get automation details
            try:
                print(f"\n   🔍 Getting detailed blocks for automation {candidate['id']}...")
                blocks_response = await client.get(f"automations/{candidate['id']}/blocks")
                blocks_response.raise_for_status()
                blocks_data = blocks_response.json()

                blocks = blocks_data.get("blocks", [])
                print(f"   📦 Found {len(blocks)} blocks")

                # Search blocks for spam content
                spam_blocks = []
                for block in blocks:
                    block_type = block.get("type", "")
                    params = block.get("params", {})

                    # Check if this is a send block with content
                    if block_type == "send":
                        # Get campaign details if available
                        campaign_id = params.get("campaignid")
                        if campaign_id:
                            try:
                                campaign_response = await client.get(f"campaigns/{campaign_id}")
                                campaign_response.raise_for_status()
                                campaign_data = campaign_response.json()

                                campaign = campaign_data.get("campaign", {})
                                subject = campaign.get("subject", "")

                                # Check for spam content in subject
                                for keyword in spam_keywords:
                                    if keyword.lower() in subject.lower():
                                        spam_blocks.append({
                                            "block_id": block.get("id"),
                                            "block_type": block_type,
                                            "campaign_id": campaign_id,
                                            "subject": subject,
                                            "match": keyword
                                        })
                                        break

                            except Exception as e:
                                print(f"      ⚠️ Could not get campaign {campaign_id}: {e}")

                if spam_blocks:
                    print(f"   🚨 Found {len(spam_blocks)} blocks with spam content:")
                    for block in spam_blocks:
                        print(f"      • Block {block['block_id']} ({block['block_type']})")
                        print(f"        Subject: {block['subject']}")
                        print(f"        Match: {block['match']}")
                else:
                    print("   ✅ No spam content found in block details")

            except Exception as e:
                print(f"   ❌ Error getting blocks: {e}")

        if not spam_candidates:
            print("\n❌ No automations found with spam keywords in name/description")
            print("   The spam content might be in:")
            print("   • Email campaign content (not automation name/description)")
            print("   • Dynamic content or personalization")
            print("   • External system integration")

            # Show first few automations for reference
            print("\n📋 First 5 automations for reference:")
            for i, automation in enumerate(automations[:5], 1):
                print(f"   {i}. ID: {automation['id']} - {automation.get('name', 'No name')}")

    except Exception as e:
        print(f"❌ Search failed: {e}")

    finally:
        await client.aclose()


if __name__ == "__main__":
    asyncio.run(search_automations_directly())
