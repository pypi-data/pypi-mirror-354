# 🚨 Automation Spam Hunter

This tool helps you find the ActiveCampaign automations responsible for sending spam messages like the "Automation Workz" messages you've been receiving.

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
./setup_and_run.sh
```

### Option 2: Manual Setup
```bash
# 1. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install requirements
pip install -r requirements_search.txt

# 3. Configure your ActiveCampaign credentials
cp .env.example .env
# Edit .env with your API details

# 4. Run the spam hunter
python search_spam_automations.py
```

## 🔑 Configuration

Create a `.env` file with your ActiveCampaign credentials:

```env
ACTIVECAMPAIGN_API_URL=https://your-account.api-us1.com
ACTIVECAMPAIGN_API_KEY=your-api-key-here
```

### Finding Your API Credentials:
1. Log into your ActiveCampaign account
2. Go to **Settings** → **Developer**
3. Copy your **API URL** and **API Key**

## 🔍 What It Searches For

Based on your spam screenshot, the tool searches for:

- ✅ **"Automation Workz"** - Main spam identifier
- ✅ **"Admissions Sampler"** - Workshop content
- ✅ **Zoom links** - Meeting URLs (zoom.us domain)
- ✅ **"82113727363"** - Specific meeting ID
- ✅ **"$25-$40"** - Earnings claims
- ✅ **"(313) 774-1106"** - Phone number
- ✅ **"Reply STOP to opt out"** - Compliance text

## 📊 Understanding Results

### Suspicion Levels:
- 🔴 **HIGH** - Found in 3+ searches (very likely the spam source)
- 🟡 **MEDIUM** - Found in 2 searches (strong candidate)
- 🟢 **LOW** - Found in 1 search (possible relation)

### Example Output:
```
🎯 CANDIDATE #1 - SUSPICION LEVEL: 🔴 HIGH
   Automation ID: 12345
   Name: Workshop Promotion Campaign
   Description: Promotes Automation Workz admissions workshop
   Match Count: 5 content matches
   Found in 4 searches: Primary Spam Content, Workshop/Admissions Content, Zoom Meeting Links, Earnings Claims
   
   📋 Matching Blocks (3):
      1. SEND - Send workshop invitation email
         Subject: Automation Workz - Attend Workshop
         Message: earn $25-$40 per hour. Attend Admissions Sampler at 12 noon or 7 pm...
```

## 🎯 Next Steps

1. **Identify the culprit** - Look for HIGH suspicion level automations
2. **Analyze in detail** - Use the automation ID to get full workflow analysis
3. **Take action** - Disable, modify, or delete the problematic automation

### Detailed Analysis:
```python
# Edit search_spam_automations.py and uncomment the last line:
asyncio.run(analyze_specific_automation("12345"))  # Replace with actual ID
```

## 🛠️ Troubleshooting

### "No automations found"
- Check your API credentials in `.env`
- Verify your ActiveCampaign account has automations
- The spam might be from a different system or account

### "API Error"
- Confirm your API URL format: `https://account.api-us1.com`
- Verify your API key is correct
- Check your ActiveCampaign account permissions

### "Connection Error"
- Check your internet connection
- Verify ActiveCampaign service status
- Try running the script again

## 🔧 Advanced Usage

### Custom Searches:
Edit `search_spam_automations.py` to add your own search patterns:

```python
{
    "name": "Custom Search",
    "tool": "search_automations_by_content",
    "params": {"search_fragment": "your custom text", "case_sensitive": False, "limit": 10}
}
```

### Regex Searches:
```python
{
    "name": "Phone Number Pattern",
    "tool": "search_automations_by_regex", 
    "params": {"pattern": r"\(\d{3}\)\s\d{3}-\d{4}", "limit": 10}
}
```

## 📞 Support

If you need help:
1. Check the troubleshooting section above
2. Verify your ActiveCampaign API access
3. Review the search results for clues about the automation structure

## 🎯 Success!

Once you find the spam automation:
1. **Document it** - Save the automation ID and details
2. **Disable it** - Turn off the automation in ActiveCampaign
3. **Clean up** - Remove affected contacts from lists if needed
4. **Monitor** - Watch for any remaining spam messages

Happy hunting! 🕵️‍♂️

