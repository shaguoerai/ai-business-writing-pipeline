# Getting Started with AI Business Writing Pipeline

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.11+** (check with `python --version`)
- **Git** (for version control)
- **OpenAI API key** (or Claude API key)
- **GitHub account** (for template usage)

### Step 1: Use the Template
1. Visit the [GitHub repository](https://github.com/shaguoerai/ai-business-writing-pipeline)
2. Click **"Use this template"** → **"Create a new repository"**
3. Name your repository (e.g., `my-business-writing-automation`)
4. Click **"Create repository"**

### Step 2: Clone Your Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### Step 3: Set Up Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "OPENAI_API_KEY=your_key_here" > .env
```

### Step 4: Generate Your First Content
```bash
# Generate a professional email
python scripts/generate-content.py \
  --type email \
  --recipient "client@company.com" \
  --topic "Project Update" \
  --key-points "On track for deadline,Need feedback on designs,Budget within 5%"

# Generate a client proposal
python scripts/generate-content.py \
  --type proposal \
  --client "Tech Startup Inc" \
  --project "Website Redesign" \
  --pain-points "Slow loading times,Poor mobile experience,Outdated design" \
  --budget "$15,000" \
  --deadline "2026-05-15"
```

### Step 5: Set Up Automation (Optional)
1. Go to your repository **Settings** → **Secrets and variables** → **Actions**
2. Add your `OPENAI_API_KEY` as a repository secret
3. The GitHub Actions workflow will run automatically on schedule

## 📁 Project Structure

```
ai-business-writing-pipeline/
├── README.md              # Main documentation
├── GETTING_STARTED.md     # This guide
├── scripts/
│   └── generate-content.py # Core content generation script
├── prompts/               # Prompt templates
│   ├── email-generator.md
│   └── proposal-generator.md
├── examples/              # Real-world examples
│   └── client-proposal.md
├── workflow-example.yml   # GitHub Actions template
├── requirements.txt       # Python dependencies
└── .gitignore            # Git ignore file
```

## 🔧 Configuration Options

### Environment Variables
```bash
# .env file
OPENAI_API_KEY=sk-...              # Required for OpenAI
ANTHROPIC_API_KEY=sk-ant-...       # Optional for Claude
MODEL=gpt-4o-mini                  # Default model
TEMPERATURE=0.7                    # Creativity level (0-1)
MAX_TOKENS=1000                    # Response length limit
```

### Customizing Prompts
Edit files in the `prompts/` directory:
```markdown
# prompts/email-generator.md
Write a professional email to {recipient} about {topic}.

Key points to include:
{key_points}

Tone: {tone}
Length: {length}
Desired outcome: {desired_outcome}
```

### GitHub Actions Schedule
Edit `.github/workflows/ai-writing.yml`:
```yaml
on:
  schedule:
    # Run every Monday at 9 AM UTC
    - cron: '0 9 * * 1'
    
    # Run every weekday at 8 AM UTC
    - cron: '0 8 * * 1-5'
```

## 🎯 Use Cases

### For Freelancers
```bash
# Daily client updates
python scripts/generate-content.py \
  --type email \
  --recipient "client@company.com" \
  --topic "Daily Progress" \
  --key-points "Completed feature X,Started work on Y,Questions about Z"

# Weekly invoices
python scripts/generate-content.py \
  --type report \
  --project-name "Client Project" \
  --period "weekly" \
  --progress "Completed 3 features,Fixed 5 bugs" \
  --accomplishments "Delivered ahead of schedule,Client satisfaction 95%"
```

### For Startups
```bash
# Investor updates
python scripts/generate-content.py \
  --type email \
  --recipient "investors@fund.com" \
  --topic "Q2 Progress Report" \
  --key-points "Revenue growth 25%,User base doubled,New hires completed"

# Team announcements
python scripts/generate-content.py \
  --type email \
  --recipient "team@startup.com" \
  --topic "New Feature Launch" \
  --key-points "Feature X now live,User feedback positive,Next steps outlined"
```

### For Agencies
```bash
# Client proposals (batch)
for client in "ClientA" "ClientB" "ClientC"; do
  python scripts/generate-content.py \
    --type proposal \
    --client "$client" \
    --project "Marketing Campaign" \
    --pain-points "Low engagement,Poor conversion,High CAC" \
    --budget "$10,000" \
    --deadline "2026-06-30"
done
```

## 🔍 Troubleshooting

### Common Issues

#### 1. API Key Not Found
```
Error: OPENAI_API_KEY not found in environment variables
```
**Solution:** Make sure your `.env` file exists and contains `OPENAI_API_KEY=your_key_here`

#### 2. Module Not Found
```
ModuleNotFoundError: No module named 'openai'
```
**Solution:** Run `pip install -r requirements.txt`

#### 3. GitHub Actions Not Running
**Solution:** Check repository secrets and workflow permissions

#### 4. Output Files Not Created
**Solution:** Check `output/` directory permissions

### Debug Mode
Enable debug logging:
```bash
export DEBUG=true
python scripts/generate-content.py --type email ...
```

## 📚 Advanced Topics

### Custom Model Integration
Edit `scripts/generate-content.py`:
```python
# Change from OpenAI to Claude
from anthropic import Anthropic
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
```

### Adding New Content Types
1. Create new prompt template in `prompts/`
2. Add new function in `scripts/generate-content.py`
3. Update command-line arguments

### Team Collaboration
1. Fork the template for your team
2. Set up branch protection rules
3. Use pull requests for prompt changes
4. Review generated content before sending

## 🤝 Support

### Community Help
- **GitHub Discussions**: [Ask questions](https://github.com/shaguoerai/ai-business-writing-pipeline/discussions)
- **Issue Tracker**: [Report bugs](https://github.com/shaguoerai/ai-business-writing-pipeline/issues)

### Premium Support
Get personalized help with:
- Custom workflow setup
- Team training
- Advanced configuration
- Priority bug fixes

[Get Premium Support](https://shaguoer.gumroad.com/l/ai-writing-automation)

## 📈 Next Steps

1. **Customize prompts** for your specific needs
2. **Set up automation** with GitHub Actions
3. **Integrate with your tools** (Slack, Email, CRM)
4. **Share feedback** to help improve the template

## 🎉 Congratulations!
You're now ready to automate 80% of your business writing tasks. Start small, iterate based on results, and scale as you gain confidence.

**Pro tip:** Keep a log of time saved each week to track your ROI!