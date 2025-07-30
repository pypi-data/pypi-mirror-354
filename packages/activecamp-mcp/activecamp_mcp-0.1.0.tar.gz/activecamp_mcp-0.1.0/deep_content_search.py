#!/usr/bin/env python3
"""
Deep Content Search - Search actual email content within automations
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


async def deep_search_email_content():
    """Search deep into email content within automations."""

    print("🔍 DEEP CONTENT SEARCH - Examining Email Content")
    print("=" * 60)

    spam_keywords = [
        "automation workz", "automation-workz", "automationworkz",
        "admissions sampler", "workshop", "zoom.us", "82113727363",
        "$25-$40", "313", "774-1106", "reply stop to opt out"
    ]

    try:
        # Get all automations
        print("📥 Fetching all automations...")
        response = await client.get("automations")
        response.raise_for_status()
        data = response.json()

        automations = data.get("automations", [])
        print(f"✅ Found {len(automations)} total automations")

        spam_findings = []

        for i, automation in enumerate(automations, 1):
            automation_id = automation["id"]
            automation_name = automation.get("name", "") or ""

            print(f"\n🔍 [{i}/{len(automations)}] Analyzing automation {automation_id}: {automation_name[:50]}...")

            try:
                # Get automation blocks
                blocks_response = await client.get(f"automations/{automation_id}/blocks")
                blocks_response.raise_for_status()
                blocks_data = blocks_response.json()

                blocks = blocks_data.get("blocks", [])

                for block in blocks:
                    block_type = block.get("type", "")
                    block_id = block.get("id", "")
                    params = block.get("params", {})

                    # Focus on send blocks (email campaigns)
                    if block_type == "send":
                        campaign_id = params.get("campaignid")
                        if campaign_id:
                            try:
                                # Get campaign details
                                campaign_response = await client.get(f"campaigns/{campaign_id}")
                                campaign_response.raise_for_status()
                                campaign_data = campaign_response.json()

                                campaign = campaign_data.get("campaign", {})
                                subject = campaign.get("subject", "") or ""

                                # Check subject for spam content
                                subject_matches = []
                                for keyword in spam_keywords:
                                    if keyword.lower() in subject.lower():
                                        subject_matches.append(keyword)

                                if subject_matches:
                                    print("   🚨 FOUND SPAM IN SUBJECT!")
                                    print(f"      Campaign ID: {campaign_id}")
                                    print(f"      Subject: {subject}")
                                    print(f"      Matches: {', '.join(subject_matches)}")

                                    spam_findings.append({
                                        "automation_id": automation_id,
                                        "automation_name": automation_name,
                                        "block_id": block_id,
                                        "campaign_id": campaign_id,
                                        "subject": subject,
                                        "matches": subject_matches,
                                        "location": "subject"
                                    })

                                # Try to get email content/body
                                try:
                                    # Get campaign messages for content
                                    messages_response = await client.get(f"campaigns/{campaign_id}/messages")
                                    if messages_response.status_code == 200:
                                        messages_data = messages_response.json()
                                        messages = messages_data.get("messages", [])

                                        for message in messages:
                                            html_content = message.get("html", "") or ""
                                            text_content = message.get("text", "") or ""

                                            # Check HTML content
                                            html_matches = []
                                            for keyword in spam_keywords:
                                                if keyword.lower() in html_content.lower():
                                                    html_matches.append(keyword)

                                            # Check text content
                                            text_matches = []
                                            for keyword in spam_keywords:
                                                if keyword.lower() in text_content.lower():
                                                    text_matches.append(keyword)

                                            if html_matches or text_matches:
                                                print("   🚨 FOUND SPAM IN EMAIL BODY!")
                                                print(f"      Campaign ID: {campaign_id}")
                                                print(f"      HTML matches: {', '.join(html_matches) if html_matches else 'None'}")
                                                print(f"      Text matches: {', '.join(text_matches) if text_matches else 'None'}")

                                                # Show snippet of content
                                                if html_content:
                                                    print(f"      HTML snippet: {html_content[:200]}...")
                                                if text_content:
                                                    print(f"      Text snippet: {text_content[:200]}...")

                                                spam_findings.append({
                                                    "automation_id": automation_id,
                                                    "automation_name": automation_name,
                                                    "block_id": block_id,
                                                    "campaign_id": campaign_id,
                                                    "subject": subject,
                                                    "html_matches": html_matches,
                                                    "text_matches": text_matches,
                                                    "location": "email_body",
                                                    "html_snippet": html_content[:500] if html_content else "",
                                                    "text_snippet": text_content[:500] if text_content else ""
                                                })

                                except Exception:
                                    # Messages endpoint might not be available, continue
                                    pass

                            except Exception as e:
                                print(f"      ⚠️ Could not get campaign {campaign_id}: {e}")

                    # Also check other block types for spam content
                    elif block_type in ["condition", "wait", "goal"]:
                        # Check block parameters for any text content
                        param_text = str(params)
                        param_matches = []
                        for keyword in spam_keywords:
                            if keyword.lower() in param_text.lower():
                                param_matches.append(keyword)

                        if param_matches:
                            print("   🚨 FOUND SPAM IN BLOCK PARAMS!")
                            print(f"      Block Type: {block_type}")
                            print(f"      Block ID: {block_id}")
                            print(f"      Matches: {', '.join(param_matches)}")
                            print(f"      Params: {param_text[:300]}...")

                            spam_findings.append({
                                "automation_id": automation_id,
                                "automation_name": automation_name,
                                "block_id": block_id,
                                "block_type": block_type,
                                "matches": param_matches,
                                "location": "block_params",
                                "params": param_text[:1000]
                            })

            except Exception as e:
                print(f"   ❌ Error analyzing automation {automation_id}: {e}")

        # Summary
        print("\n🎯 DEEP SEARCH COMPLETE")
        print("=" * 60)

        if spam_findings:
            print(f"🚨 FOUND {len(spam_findings)} SPAM INSTANCES!")

            # Group by automation
            by_automation = {}
            for finding in spam_findings:
                auto_id = finding["automation_id"]
                if auto_id not in by_automation:
                    by_automation[auto_id] = []
                by_automation[auto_id].append(finding)

            for auto_id, findings in by_automation.items():
                auto_name = findings[0]["automation_name"]
                print(f"\n🎯 AUTOMATION {auto_id}: {auto_name}")
                print(f"   📊 {len(findings)} spam instances found")

                for finding in findings:
                    location = finding["location"]
                    if location == "subject":
                        print(f"   📧 Subject: {finding['subject']}")
                        print(f"      Matches: {', '.join(finding['matches'])}")
                    elif location == "email_body":
                        print(f"   📧 Email Body (Campaign {finding['campaign_id']})")
                        if finding.get("html_matches"):
                            print(f"      HTML matches: {', '.join(finding['html_matches'])}")
                        if finding.get("text_matches"):
                            print(f"      Text matches: {', '.join(finding['text_matches'])}")
                    elif location == "block_params":
                        print(f"   🔧 Block {finding['block_id']} ({finding['block_type']})")
                        print(f"      Matches: {', '.join(finding['matches'])}")
        else:
            print("❌ No spam content found in email campaigns or block parameters")
            print("   The spam might be coming from:")
            print("   • External webhook/integration")
            print("   • SMS campaigns (not email)")
            print("   • Different ActiveCampaign account")
            print("   • Dynamic content generation")

    except Exception as e:
        print(f"❌ Deep search failed: {e}")

    finally:
        await client.aclose()


if __name__ == "__main__":
    asyncio.run(deep_search_email_content())

