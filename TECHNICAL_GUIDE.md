# Technical Guide: Building an AI Business Writing Pipeline 🛠️

> Complete implementation guide with production-ready code examples. Learn how to build, customize, and scale your own AI writing automation system.

[![GitHub stars](https://img.shields.io/github/stars/shaguoerai/ai-business-writing-pipeline?style=social)](https://github.com/shaguoerai/ai-business-writing-pipeline)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Table of Contents
- [🏗️ Architecture](#️-architecture)
- [💻 Core Implementation](#-core-implementation)
- [⚙️ Advanced Configuration](#️-advanced-configuration)
- [🔧 Troubleshooting](#-troubleshooting)
- [📈 Performance Optimization](#-performance-optimization)
- [🚀 Deployment Guide](#-deployment-guide)
- [🔍 Testing & Validation](#-testing--validation)
- [🤝 Contributing](#-contributing)

## 🎯 What You'll Learn

This guide provides a complete walkthrough for building a production-ready AI business writing automation system. You'll learn:

1. **System Architecture**: How to design scalable AI writing pipelines
2. **Core Implementation**: Production-ready code with best practices
3. **Advanced Configuration**: Multi-model support and optimization
4. **Troubleshooting**: Common issues and solutions
5. **Performance Tuning**: Optimizing for speed and cost
6. **Deployment Strategies**: From local development to production

All code examples are available in this repository and can be directly used or customized for your needs.

## 🏗️ Architecture

### System Components
1. **Content Generation Engine** (Python + OpenAI API)
2. **Prompt Management System** (Template-based)
3. **Automation Scheduler** (GitHub Actions)
4. **Output Processing** (Markdown/PDF/Email)
5. **Monitoring & Analytics** (Logging + Metrics)

### Data Flow
```
User Input → Prompt Template → OpenAI API → Content Validation → Output Generation
```

## 💻 Core Implementation

### 1. Python Environment Setup

**requirements.txt:**
```txt
openai>=1.0.0
python-dotenv>=1.0.0
markdown>=3.5.0
pandas>=2.0.0
jinja2>=3.0.0
python-dateutil>=2.8.2
```

**Environment Configuration (.env):**
```bash
OPENAI_API_KEY=your_key_here
MODEL=gpt-4o-mini
TEMPERATURE=0.7
MAX_TOKENS=2000
LOG_LEVEL=INFO
```

### 2. Main Content Generator

**File: `scripts/generate-content.py`**
```python
import os
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

class BusinessWritingGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("MODEL", "gpt-4o-mini")
        
    def generate_proposal(self, client, project, pain_points, budget, deadline):
        """Generate client proposal"""
        prompt = self.load_prompt("proposal").format(
            client=client,
            project=project,
            pain_points=pain_points,
            budget=budget,
            deadline=deadline
        )
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Professional business writer"},
                {"role": "user", "content": prompt}
            ]
        )
        
        return self.save_output("proposal", response.choices[0].message.content)
```

### 3. Prompt Templates

**File: `prompts/proposal-generator.md`**
```markdown
# Client Proposal for {client}

## Project: {project}

### Client Challenges:
{pain_points}

### Proposed Solution:
We will address these challenges through:

1. **Strategic Analysis** - Deep dive into current processes
2. **Custom Implementation** - Tailored automation workflows
3. **Ongoing Support** - Continuous optimization

### Investment:
- Budget: {budget}
- Timeline: {deadline}

### Expected Outcomes:
- 85-95% time savings on writing tasks
- Consistent, professional communication
- Scalable processes for growth
```

### 4. GitHub Actions Automation

**File: `.github/workflows/ai-writing.yml`**
```yaml
name: AI Writing Automation
on:
  schedule:
    - cron: '0 9 * * 1'  # Weekly on Monday
    - cron: '0 8 * * 1-5' # Daily on weekdays

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install -r requirements.txt
      - run: python scripts/generate-content.py --type proposal
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

## 🚀 Advanced Features

### A. Template Variables System
```python
class TemplateEngine:
    variables = {
        "current_date": lambda: datetime.now().strftime("%Y-%m-%d"),
        "company_name": "Your Business",
        "contact_email": "hello@company.com"
    }
    
    def render(self, template, custom_vars={}):
        for key, value in {**self.variables, **custom_vars}.items():
            if callable(value):
                value = value()
            template = template.replace(f"{{{key}}}", str(value))
        return template
```

### B. Content Validation
```python
class ContentValidator:
    REQUIRED_SECTIONS = {
        "proposal": ["Executive Summary", "Problem Statement", "Solution", "Budget", "Timeline"],
        "email": ["Subject", "Greeting", "Body", "Call to Action", "Signature"],
        "report": ["Overview", "Metrics", "Analysis", "Recommendations"]
    }
    
    def validate(self, content_type, content):
        required = self.REQUIRED_SECTIONS.get(content_type, [])
        found = [section for section in required if section.lower() in content.lower()]
        return {
            "score": len(found) / len(required) * 100,
            "missing": [s for s in required if s.lower() not in content.lower()]
        }
```

### C. Batch Processing
```python
def batch_generate(clients_data, content_type="proposal"):
    """Generate content for multiple clients"""
    results = []
    generator = BusinessWritingGenerator()
    
    for client_data in clients_data:
        try:
            if content_type == "proposal":
                output = generator.generate_proposal(**client_data)
            elif content_type == "email":
                output = generator.generate_email(**client_data)
            
            results.append({
                "client": client_data.get("client"),
                "status": "success",
                "output": output
            })
        except Exception as e:
            results.append({
                "client": client_data.get("client"),
                "status": "error",
                "error": str(e)
            })
    
    return results
```

## 📊 Performance Optimization

### 1. Caching Prompts
```python
from functools import lru_cache

class PromptManager:
    @lru_cache(maxsize=32)
    def get_prompt(self, prompt_name):
        """Cache frequently used prompts"""
        with open(f"prompts/{prompt_name}.md", "r") as f:
            return f.read()
```

### 2. Async Processing
```python
import asyncio
from openai import AsyncOpenAI

async def generate_async(prompts):
    """Generate multiple contents concurrently"""
    client = AsyncOpenAI()
    tasks = []
    
    for prompt in prompts:
        task = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        tasks.append(task)
    
    return await asyncio.gather(*tasks)
```

### 3. Rate Limiting
```python
import time
from collections import deque

class RateLimiter:
    def __init__(self, calls_per_minute=60):
        self.calls = deque()
        self.limit = calls_per_minute
    
    def wait_if_needed(self):
        now = time.time()
        
        # Remove calls older than 1 minute
        while self.calls and now - self.calls[0] > 60:
            self.calls.popleft()
        
        if len(self.calls) >= self.limit:
            sleep_time = 60 - (now - self.calls[0])
            time.sleep(sleep_time)
        
        self.calls.append(now)
```

## 🔧 Deployment Options

### Option 1: Serverless (AWS Lambda)
```python
# lambda_function.py
import json
from generate_content import BusinessWritingGenerator

def lambda_handler(event, context):
    generator = BusinessWritingGenerator()
    
    # Parse event data
    content_type = event.get("content_type", "proposal")
    data = event.get("data", {})
    
    # Generate content
    if content_type == "proposal":
        result = generator.generate_proposal(**data)
    elif content_type == "email":
        result = generator.generate_email(**data)
    
    return {
        "statusCode": 200,
        "body": json.dumps({"output": result})
    }
```

### Option 2: Docker Container
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "scripts/generate-content.py"]
```

### Option 3: Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-writing
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: generator
        image: ai-writing:latest
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: openai-secret
              key: api-key
```

## 📈 Monitoring & Analytics

### 1. Logging Setup
```python
import logging
import structlog

def setup_logging():
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ]
    )
    
    return structlog.get_logger()
```

### 2. Performance Metrics
```python
from dataclasses import dataclass
from datetime import datetime
import statistics

@dataclass
class PerformanceMetrics:
    generation_time: float
    token_usage: int
    content_length: int
    validation_score: float
    
class MetricsCollector:
    def __init__(self):
        self.metrics = []
    
    def add_metric(self, metric):
        self.metrics.append(metric)
    
    def get_summary(self):
        return {
            "total_generations": len(self.metrics),
            "avg_generation_time": statistics.mean([m.generation_time for m in self.metrics]),
            "avg_token_usage": statistics.mean([m.token_usage for m in self.metrics]),
            "avg_validation_score": statistics.mean([m.validation_score for m in self.metrics])
        }
```

### 3. Error Tracking
```python
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

def setup_error_tracking():
    sentry_sdk.init(
        dsn="your_sentry_dsn",
        integrations=[LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)]
    )
```

## 🧪 Testing

### Unit Tests
```python
import pytest
from generate_content import BusinessWritingGenerator

def test_proposal_generation():
    generator = BusinessWritingGenerator()
    
    # Mock OpenAI response
    with patch('openai.OpenAI') as mock_openai:
        mock_openai.return_value.chat.completions.create.return_value = Mock(
            choices=[Mock(message=Mock(content="Test proposal"))]
        )
        
        result = generator.generate_proposal(
            client="Test Client",
            project="Test Project",
            pain_points="Test pain points",
            budget="$1000",
            deadline="2026-12-31"
        )
        
        assert "Test proposal" in result
```

### Integration Tests
```python
def test_github_actions_workflow():
    """Test that GitHub Actions workflow generates content"""
    # Simulate workflow run
    result = run_workflow("ai-writing.yml")
    
    assert result["success"] == True
    assert "output" in result
    assert os.path.exists("output/proposal_*.md")
```

### Load Testing
```python
def test_concurrent_generations():
    """Test system under load"""
    import concurrent.futures
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for i in range(10):
            futures.append(executor.submit(generate_proposal, f"Client{i}"))
        
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    
    assert len(results) == 10
    assert all(r["status"] == "success" for r in results)
```

## 🔒 Security Best Practices

### 1. API Key Management
```python
from cryptography.fernet import Fernet

class SecureConfig:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
    
    def encrypt_key(self, api_key):
        return self.cipher.encrypt(api_key.encode())
    
    def decrypt_key(self, encrypted_key):
        return self.cipher.decrypt(encrypted_key).decode()
```

### 2. Input Validation
```python
import re

def sanitize_input(text):
    """Sanitize user input to prevent injection"""
    # Remove potentially dangerous characters
    text = re.sub(r'[<>"\'&]', '', text)
    
    # Limit length
    if len(text) > 10000:
        raise ValueError("Input too long")
    
    return text
```

### 3. Audit Logging
```python
class AuditLogger:
    def log_generation(self, user, content_type, metadata):
        """Log all content generation for audit trail"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user,
            "content_type": content_type,
            "metadata": metadata,
            "ip_address": request.remote_addr if hasattr(request, 'remote_addr') else None
        }
        
        # Write to secure log
        with open("/var/log/ai_writing_audit.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
```

## ⚙️ Advanced Configuration

### Multi-Model Support

The pipeline supports multiple AI models. Configure your preferred model in `config.yaml`:

```yaml
# config.yaml
ai:
  # OpenAI GPT models (recommended for most use cases)
  openai:
    model: "gpt-4"  # or "gpt-3.5-turbo"
    temperature: 0.7
    max_tokens: 2000
    
  # Claude models (excellent for long-form content)
  anthropic:
    model: "claude-3-opus-20240229"  # or "claude-3-sonnet-20240229"
    max_tokens: 4000
    
  # Local models (for privacy-sensitive applications)
  local:
    model_path: "./models/llama-2-7b"
    device: "cuda"  # or "cpu"
    
  # Model selection strategy
  default_provider: "openai"
  fallback_provider: "anthropic"
```

### Performance Optimization

#### Caching Strategy
Implement response caching to reduce API calls and improve performance:

```python
# caching.py
import hashlib
import json
from datetime import datetime, timedelta

class ContentCache:
    def __init__(self, cache_dir=".cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def get_cache_key(self, prompt, model, temperature):
        """Generate unique cache key for prompt and parameters"""
        content = f"{prompt}|{model}|{temperature}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, key, max_age_hours=24):
        """Get cached response if available and not expired"""
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                cached = json.load(f)
                
            # Check if cache is still valid
            cache_time = datetime.fromisoformat(cached['timestamp'])
            if datetime.now() - cache_time < timedelta(hours=max_age_hours):
                return cached['response']
        
        return None
    
    def set(self, key, response):
        """Cache response with timestamp"""
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'response': response
        }
        
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f)
```

#### Batch Processing
For processing multiple items efficiently:

```python
# batch_processor.py
from concurrent.futures import ThreadPoolExecutor, as_completed

class BatchProcessor:
    def __init__(self, max_workers=5):
        self.max_workers = max_workers
    
    def process_batch(self, items, process_func):
        """Process items in parallel"""
        results = {}
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_item = {
                executor.submit(process_func, item): item 
                for item in items
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_item):
                item = future_to_item[future]
                try:
                    results[item['id']] = future.result()
                except Exception as e:
                    results[item['id']] = {'error': str(e)}
        
        return results

# Usage example
processor = BatchProcessor(max_workers=3)
email_templates = [
    {'id': 1, 'type': 'welcome', 'client': 'Client A'},
    {'id': 2, 'type': 'follow-up', 'client': 'Client B'},
    {'id': 3, 'type': 'thank-you', 'client': 'Client C'},
]

results = processor.process_batch(email_templates, generate_email)
```

### Security Configuration

#### API Key Management
Never hardcode API keys. Use environment variables or secret management:

```python
# security.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SecureConfig:
    @staticmethod
    def get_api_key(provider):
        """Safely retrieve API key from environment"""
        env_var = f"{provider.upper()}_API_KEY"
        api_key = os.getenv(env_var)
        
        if not api_key:
            raise ValueError(f"{env_var} not found in environment variables")
        
        # Validate key format (basic check)
        if provider == 'openai' and not api_key.startswith('sk-'):
            raise ValueError("Invalid OpenAI API key format")
            
        return api_key
    
    @staticmethod
    def mask_key(key):
        """Mask API key for logging"""
        if len(key) > 8:
            return f"{key[:4]}...{key[-4:]}"
        return "****"
```

#### Content Filtering
Implement content safety checks:

```python
# content_safety.py
class ContentSafetyFilter:
    def __init__(self):
        self.banned_patterns = [
            r'\b(hack|exploit|attack)\b',
            r'\b(illegal|unlawful)\b',
            # Add more patterns as needed
        ]
    
    def check_content(self, content):
        """Check content for safety violations"""
        import re
        
        violations = []
        for pattern in self.banned_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                violations.append(pattern)
        
        return {
            'safe': len(violations) == 0,
            'violations': violations,
            'content': content if len(violations) == 0 else '[FILTERED]'
        }
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue 1: API Authentication Failed
**Symptoms**: `401 Unauthorized` or `Invalid API key` errors
**Solutions**:
1. Verify API key is correctly set in environment variables:
   ```bash
   echo $OPENAI_API_KEY  # Should show your key (masked)
   ```
2. Check key permissions and quota
3. Regenerate key if compromised

#### Issue 2: Rate Limiting
**Symptoms**: `429 Too Many Requests` errors
**Solutions**:
1. Implement exponential backoff:
   ```python
   import time
   
   def make_request_with_backoff(func, max_retries=5):
       for attempt in range(max_retries):
           try:
               return func()
           except RateLimitError:
               wait_time = 2 ** attempt  # Exponential backoff
               time.sleep(wait_time)
       raise Exception("Max retries exceeded")
   ```
2. Reduce request frequency
3. Upgrade API tier if needed

#### Issue 3: Content Quality Issues
**Symptoms**: Generic or low-quality output
**Solutions**:
1. Improve prompt specificity
2. Adjust temperature (lower for consistency, higher for creativity)
3. Add examples to prompts
4. Implement output validation

#### Issue 4: Performance Problems
**Symptoms**: Slow response times
**Solutions**:
1. Enable response caching
2. Use batch processing for multiple items
3. Optimize prompt length
4. Consider model downgrade (GPT-4 → GPT-3.5)

### Debugging Guide

1. **Enable Detailed Logging**:
   ```python
   import logging
   
   logging.basicConfig(
       level=logging.DEBUG,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   )
   ```

2. **Test Individual Components**:
   ```bash
   # Test API connectivity
   python -c "import openai; print(openai.Model.list())"
   
   # Test prompt generation
   python scripts/test_prompt.py
   
   # Test content generation
   python scripts/test_generation.py --simple
   ```

3. **Monitor Resource Usage**:
   ```bash
   # CPU/Memory usage
   top -b -n 1 | grep python
   
   # API usage
   openai api usage --date 2026-04-06
   ```

## 📈 Performance Optimization

### Benchmarking

Create performance benchmarks to track improvements:

```python
# benchmarks.py
import time
from datetime import datetime

class PerformanceBenchmark:
    def __init__(self):
        self.metrics = {}
    
    def start_timer(self, operation):
        self.metrics[operation] = {
            'start': time.time(),
            'end': None,
            'duration': None
        }
    
    def end_timer(self, operation):
        if operation in self.metrics:
            self.metrics[operation]['end'] = time.time()
            self.metrics[operation]['duration'] = \
                self.metrics[operation]['end'] - self.metrics[operation]['start']
    
    def get_report(self):
        report = {
            'timestamp': datetime.now().isoformat(),
            'metrics': {}
        }
        
        for operation, data in self.metrics.items():
            if data['duration'] is not None:
                report['metrics'][operation] = {
                    'duration_seconds': round(data['duration'], 3),
                    'start_time': data['start'],
                    'end_time': data['end']
                }
        
        return report

# Usage
benchmark = PerformanceBenchmark()
benchmark.start_timer('email_generation')
# ... generate email ...
benchmark.end_timer('email_generation')
print(benchmark.get_report())
```

### Cost Optimization

Track and optimize API costs:

```python
# cost_tracker.py
class CostTracker:
    def __init__(self):
        self.usage = {
            'openai': {'tokens': 0, 'cost': 0.0},
            'anthropic': {'tokens': 0, 'cost': 0.0}
        }
        
        # Pricing as of 2026-04 (check current rates)
        self.pricing = {
            'openai': {
                'gpt-4': {'input': 0.03, 'output': 0.06},  # per 1K tokens
                'gpt-3.5-turbo': {'input': 0.001, 'output': 0.002}
            },
            'anthropic': {
                'claude-3-opus': {'input': 0.015, 'output': 0.075},
                'claude-3-sonnet': {'input': 0.003, 'output': 0.015}
            }
        }
    
    def track_usage(self, provider, model, input_tokens, output_tokens):
        """Track token usage and calculate cost"""
        if provider in self.usage and model in self.pricing.get(provider, {}):
            input_cost = (input_tokens / 1000) * self.pricing[provider][model]['input']
            output_cost = (output_tokens / 1000) * self.pricing[provider][model]['output']
            total_cost = input_cost + output_cost
            
            self.usage[provider]['tokens'] += input_tokens + output_tokens
            self.usage[provider]['cost'] += total_cost
            
            return total_cost
        return 0.0
    
    def get_report(self):
        """Generate cost usage report"""
        total_cost = sum(provider['cost'] for provider in self.usage.values())
        
        return {
            'total_cost': round(total_cost, 4),
            'providers': self.usage,
            'timestamp': datetime.now().isoformat()
        }
```

### Optimization Recommendations

1. **For Speed**:
   - Use GPT-3.5 instead of GPT-4 (3-5x faster)
   - Implement response caching
   - Use batch processing
   - Optimize prompt length

2. **For Cost**:
   - Use GPT-3.5 for non-critical content
   - Implement token usage limits
   - Cache frequent responses
   - Use local models for development

3. **For Quality**:
   - Use GPT-4 for important documents
   - Implement multi-step refinement
   - Add human review for critical content
   - Use specialized prompts for each content type

## 🚀 Production Readiness Checklist

### Before Deployment
- [ ] API keys stored in environment variables/secrets
- [ ] Rate limiting implemented
- [ ] Error handling and logging configured
- [ ] Content validation in place
- [ ] Backup and recovery procedures documented

### Monitoring
- [ ] Application logs centralized
- [ ] Performance metrics collected
- [ ] Alerting configured for errors
- [ ] Usage analytics implemented

### Maintenance
- [ ] Regular dependency updates scheduled
- [ ] Prompt template versioning implemented
- [ ] Backup of generated content
- [ ] Regular security audits

## 📚 Additional Resources

### Learning Materials
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [GitHub Actions Guide](https://docs.github.com/en/actions)
- [Python Best Practices](https://docs.python-guide.org/)

### Community
- [GitHub Discussions](https://github.com/shaguoerai/ai-business-writing-pipeline/discussions)
- [Discord Community](https://discord.gg/your-invite-link)
- [Stack Overflow Tag](https://stackoverflow.com/questions/tagged/ai-automation)

### Support
- [Issue Tracker](https://github.com/shaguoerai/ai-business-writing-pipeline/issues)
- [Email Support](mailto:support@shaguoer.gumroad.com)
- [Premium Documentation](https://shaguoer.gumroad.com/l/oxjut)

---

## 🎯 Getting Started

### Quick Start
```bash
# 1. Clone the repository
git clone https://github.com/shaguoerai/ai-business-writing-pipeline.git

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment
echo "OPENAI_API_KEY=your_key_here" > .env

# 4. Generate your first proposal
python scripts/generate-content.py \
  --type proposal \
  --client "Test Client" \
  --project "Website Redesign" \
  --budget "$15,000" \
  --deadline "2026-06-30"
```

### Next Steps
1. **Customize prompts** in the `prompts/` directory
2. **Configure automation** in `.github/workflows/ai-writing.yml`
3. **Set up monitoring** with your preferred tools
4. **Scale deployment** based on your needs

---

**Need Help?**
- Join our [GitHub Discussions](https://github.com/shaguoerai/ai-business-writing-pipeline/discussions)
- Check the [FAQ](FAQ.md)
- Purchase the [Premium Package](https://shaguoer.gumroad.com/l/oxjut) for video tutorials and priority support

**Contribute**
- Star the repository ⭐
- Report bugs 🐛
- Suggest features 💡
- Submit pull requests 🔧

---

*Last updated: 2026-04-04*  
*Maintained by: [Nova](https://github.com/shaguoerai)*