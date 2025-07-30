#!/bin/bash

# Automation Spam Hunter Setup Script
# This script sets up and runs the spam automation search

echo "🚨 AUTOMATION SPAM HUNTER SETUP 🚨"
echo "=================================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Install requirements
echo "📥 Installing requirements..."
pip install -r requirements_search.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Creating .env file template..."
    cat > .env << EOF
# ActiveCampaign API Configuration
ACTIVECAMPAIGN_API_URL=https://your-account.api-us1.com
ACTIVECAMPAIGN_API_KEY=your-api-key-here

# Optional: Set to 'development' for more verbose logging
ENVIRONMENT=production
EOF
    echo "📝 Please edit .env file with your ActiveCampaign credentials:"
    echo "   1. Replace 'your-account' with your ActiveCampaign account name"
    echo "   2. Replace 'your-api-key-here' with your actual API key"
    echo "   3. Save the file and run this script again"
    echo ""
    echo "🔑 To find your API key:"
    echo "   1. Log into ActiveCampaign"
    echo "   2. Go to Settings > Developer"
    echo "   3. Copy your API URL and Key"
    exit 1
fi

# Check if .env has been configured
if grep -q "your-api-key-here" .env; then
    echo "❌ Please configure your .env file with real ActiveCampaign credentials"
    echo "   Edit .env and replace the placeholder values"
    exit 1
fi

echo "✅ Setup complete!"
echo ""
echo "🔍 Running spam automation search..."
echo "=================================="

# Run the spam search
python search_spam_automations.py

echo ""
echo "🎯 Search complete! Check the results above."
echo ""
echo "💡 To analyze a specific automation in detail, edit search_spam_automations.py"
echo "   and uncomment the last line with the automation ID you want to investigate."

