#!/usr/bin/env python3
"""
SMS and Integration Search - Find SMS campaigns and external integrations
"""

import asyncio
import json

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


async def search_sms_and_integrations():
    """Search for SMS campaigns and external integrations."""

    print("📱 SMS & INTEGRATION SEARCH")
    print("=" * 50)

    spam_keywords = [
        "automation workz", "automation-workz", "automationworkz", "aw",
        "admissions sampler", "workshop", "zoom.us", "82113727363",
        "$25-$40", "313", "774-1106", "reply stop", "clicksend"
    ]

    try:
        # Get all automations
        print("📥 Fetching all automations...")
        response = await client.get("automations")
        response.raise_for_status()
        data = response.json()

        automations = data.get("automations", [])
        print(f"✅ Found {len(automations)} total automations")

        sms_findings = []

        # Focus on suspicious automations
        suspicious_automations = [
            {"id": 58, "name": "Attended AW Sampler"},
            {"id": 41, "name": "Composite - Admissions - Application w/ ClickSend"},
            {"id": 13, "name": "Composite - Visions - Schedule Vision Boarding SMS"}
        ]

        print(f"\n🎯 Focusing on {len(suspicious_automations)} suspicious automations...")

        for auto_info in suspicious_automations:
            automation_id = auto_info["id"]
            automation_name = auto_info["name"]

            print(f"\n🔍 DEEP DIVE: Automation {automation_id} - {automation_name}")
            print("-" * 60)

            try:
                # Get automation details
                auto_response = await client.get(f"automations/{automation_id}")
                auto_response.raise_for_status()
                auto_data = auto_response.json()

                automation = auto_data.get("automation", {})
                print(f"📋 Description: {automation.get('description', 'No description')}")

                # Get automation blocks
                blocks_response = await client.get(f"automations/{automation_id}/blocks")
                blocks_response.raise_for_status()
                blocks_data = blocks_response.json()

                blocks = blocks_data.get("blocks", [])
                print(f"📦 Found {len(blocks)} blocks")

                for block in blocks:
                    block_type = block.get("type", "")
                    block_id = block.get("id", "")
                    params = block.get("params", {})

                    print(f"\n   🔧 Block {block_id} - Type: {block_type}")

                    # Check for external integrations
                    if block_type in ["webhook", "integration", "api", "external"]:
                        print("      🚨 EXTERNAL INTEGRATION FOUND!")
                        print(f"         Type: {block_type}")
                        print(f"         Params: {json.dumps(params, indent=8)}")

                        sms_findings.append({
                            "automation_id": automation_id,
                            "automation_name": automation_name,
                            "block_id": block_id,
                            "block_type": block_type,
                            "params": params,
                            "finding_type": "external_integration"
                        })

                    # Check for SMS-related parameters
                    param_text = json.dumps(params).lower()
                    sms_indicators = ["sms", "text", "phone", "clicksend", "twilio", "message"]

                    for indicator in sms_indicators:
                        if indicator in param_text:
                            print(f"      📱 SMS INDICATOR FOUND: {indicator}")
                            print(f"         Block Type: {block_type}")
                            print(f"         Relevant Params: {json.dumps(params, indent=8)}")

                            sms_findings.append({
                                "automation_id": automation_id,
                                "automation_name": automation_name,
                                "block_id": block_id,
                                "block_type": block_type,
                                "sms_indicator": indicator,
                                "params": params,
                                "finding_type": "sms_indicator"
                            })
                            break

                    # Check for spam keywords in parameters
                    spam_matches = []
                    for keyword in spam_keywords:
                        if keyword in param_text:
                            spam_matches.append(keyword)

                    if spam_matches:
                        print(f"      🚨 SPAM KEYWORDS FOUND: {', '.join(spam_matches)}")
                        print(f"         Block Type: {block_type}")
                        print(f"         Params: {json.dumps(params, indent=8)}")

                        sms_findings.append({
                            "automation_id": automation_id,
                            "automation_name": automation_name,
                            "block_id": block_id,
                            "block_type": block_type,
                            "spam_matches": spam_matches,
                            "params": params,
                            "finding_type": "spam_content"
                        })

                # Get automation triggers for more context
                triggers_response = await client.get(f"automations/{automation_id}/triggers")
                triggers_response.raise_for_status()
                triggers_data = triggers_response.json()

                triggers = triggers_data.get("triggers", [])
                print(f"🎯 Triggers ({len(triggers)}):")
                for trigger in triggers:
                    trigger_type = trigger.get("type", "")
                    params = trigger.get("params", {})
                    print(f"   • {trigger_type}: {json.dumps(params, indent=6)}")

            except Exception as e:
                print(f"   ❌ Error analyzing automation {automation_id}: {e}")

        # Also search for SMS campaigns directly
        print("\n📱 Searching for SMS campaigns...")
        try:
            # Try to get SMS campaigns (endpoint might vary)
            sms_response = await client.get("sms")
            if sms_response.status_code == 200:
                sms_data = sms_response.json()
                sms_campaigns = sms_data.get("sms", [])
                print(f"✅ Found {len(sms_campaigns)} SMS campaigns")

                for sms in sms_campaigns:
                    sms_content = str(sms).lower()
                    spam_matches = []
                    for keyword in spam_keywords:
                        if keyword in sms_content:
                            spam_matches.append(keyword)

                    if spam_matches:
                        print("🚨 SPAM SMS FOUND!")
                        print(f"   Matches: {', '.join(spam_matches)}")
                        print(f"   Content: {json.dumps(sms, indent=4)}")
            else:
                print("⚠️ SMS endpoint not available or no SMS campaigns")
        except Exception as e:
            print(f"⚠️ Could not search SMS campaigns: {e}")

        # Summary
        print("\n🎯 SMS & INTEGRATION SEARCH COMPLETE")
        print("=" * 60)

        if sms_findings:
            print(f"🚨 FOUND {len(sms_findings)} SUSPICIOUS ITEMS!")

            for finding in sms_findings:
                print(f"\n📋 Automation {finding['automation_id']}: {finding['automation_name']}")
                print(f"   Finding Type: {finding['finding_type']}")
                print(f"   Block: {finding['block_id']} ({finding['block_type']})")

                if finding['finding_type'] == "spam_content":
                    print(f"   Spam Matches: {', '.join(finding['spam_matches'])}")
                elif finding['finding_type'] == "sms_indicator":
                    print(f"   SMS Indicator: {finding['sms_indicator']}")

                print(f"   Params: {json.dumps(finding['params'], indent=6)}")
        else:
            print("❌ No SMS campaigns or external integrations found with spam content")
            print("   The spam might be coming from:")
            print("   • A different ActiveCampaign account")
            print("   • Manual SMS sending")
            print("   • Third-party service not integrated with ActiveCampaign")

    except Exception as e:
        print(f"❌ SMS search failed: {e}")

    finally:
        await client.aclose()


if __name__ == "__main__":
    asyncio.run(search_sms_and_integrations())

