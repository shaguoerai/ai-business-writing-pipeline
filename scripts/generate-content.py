#!/usr/bin/env python3
"""
AI Content Generation Script
Part of the AI-Powered Business Writing Pipeline
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ContentGenerator:
    def __init__(self, api_key=None):
        """Initialize the content generator"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self.templates = self.load_templates()
    
    def load_templates(self):
        """Load prompt templates from prompts/ directory"""
        templates = {}
        prompts_dir = Path("prompts")
        
        if prompts_dir.exists():
            for file in prompts_dir.glob("*.md"):
                with open(file, 'r') as f:
                    content = f.read()
                    template_name = file.stem.replace("-", "_")
                    templates[template_name] = content
        
        # Fallback templates if prompts directory doesn't exist
        if not templates:
            templates = {
                "email_generator": """Write a professional email to {recipient} about {topic}.

Key points to include:
{key_points}

Tone: {tone}
Length: {length}
Desired outcome: {desired_outcome}

Format the email with:
- Appropriate greeting
- Clear subject line
- Professional body
- Call to action
- Professional closing""",
                
                "proposal_generator": """Create a professional business proposal for {client} regarding {project}.

Include these sections:
1. Executive Summary (3-4 sentences highlighting key benefits)
2. Understanding of Client Needs (based on {pain_points})
3. Proposed Solution (how we'll address each pain point)
4. Timeline and Deliverables (clear milestones)
5. Investment and ROI (cost vs. value delivered)
6. Next Steps (simple call to action)

Tone: Professional, confident, client-focused
Length: 2-3 pages maximum
Budget: {budget}
Deadline: {deadline}""",
                
                "report_generator": """Create a {period} report for {project_name} covering:

Progress this period:
- {progress_points}

Key accomplishments:
- {accomplishments}

Challenges faced and solutions:
- {challenges}

Next period priorities:
- {next_priorities}

Any support needed:
- {support_needed}

Format: Clear, scannable, action-oriented
Audience: {audience}
Tone: Professional, transparent"""
            }
        
        return templates
    
    def generate_email(self, recipient, topic, key_points, tone="professional", 
                      length="medium", desired_outcome="schedule a meeting"):
        """Generate a professional email"""
        prompt = self.templates["email_generator"].format(
            recipient=recipient,
            topic=topic,
            key_points=key_points,
            tone=tone,
            length=length,
            desired_outcome=desired_outcome
        )
        
        return self.call_ai(prompt, max_tokens=500)
    
    def generate_proposal(self, client, project, pain_points, budget, deadline):
        """Generate a client proposal"""
        prompt = self.templates["proposal_generator"].format(
            client=client,
            project=project,
            pain_points=pain_points,
            budget=budget,
            deadline=deadline
        )
        
        return self.call_ai(prompt, max_tokens=1500)
    
    def generate_report(self, project_name, period, progress_points, 
                       accomplishments, challenges, next_priorities, 
                       support_needed, audience="team"):
        """Generate a progress report"""
        prompt = self.templates["report_generator"].format(
            project_name=project_name,
            period=period,
            progress_points=progress_points,
            accomplishments=accomplishments,
            challenges=challenges,
            next_priorities=next_priorities,
            support_needed=support_needed,
            audience=audience
        )
        
        return self.call_ai(prompt, max_tokens=800)
    
    def call_ai(self, prompt, max_tokens=1000, model="gpt-4o-mini"):
        """Call the AI API"""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a professional business writing assistant. Create clear, concise, and effective business documents."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error calling AI API: {e}")
            return f"# AI Generation Failed\n\nError: {e}\n\nPrompt was:\n\n{prompt}"
    
    def save_output(self, content, output_type, metadata=None):
        """Save generated content to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        filename = f"{output_type}_{timestamp}.md"
        filepath = output_dir / filename
        
        # Add metadata header
        if metadata:
            metadata_str = "\n".join([f"{k}: {v}" for k, v in metadata.items()])
            content = f"---\n{metadata_str}\n---\n\n{content}"
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"✅ Content saved to: {filepath}")
        return filepath

def main():
    parser = argparse.ArgumentParser(description="Generate business content using AI")
    parser.add_argument("--type", required=True, choices=["email", "proposal", "report"],
                       help="Type of content to generate")
    
    # Email arguments
    parser.add_argument("--recipient", help="Email recipient")
    parser.add_argument("--topic", help="Email topic")
    parser.add_argument("--key-points", help="Key points to include (comma-separated)")
    
    # Proposal arguments
    parser.add_argument("--client", help="Client name")
    parser.add_argument("--project", help="Project description")
    parser.add_argument("--pain-points", help="Client pain points (comma-separated)")
    parser.add_argument("--budget", help="Project budget")
    parser.add_argument("--deadline", help="Project deadline")
    
    # Report arguments
    parser.add_argument("--project-name", help="Project name for report")
    parser.add_argument("--period", default="weekly", help="Report period (weekly, monthly)")
    parser.add_argument("--progress", help="Progress points (comma-separated)")
    parser.add_argument("--accomplishments", help="Accomplishments (comma-separated)")
    parser.add_argument("--challenges", help="Challenges faced (comma-separated)")
    parser.add_argument("--next-priorities", help="Next priorities (comma-separated)")
    parser.add_argument("--support-needed", help="Support needed (comma-separated)")
    
    # General arguments
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--api-key", help="OpenAI API key (overrides env var)")
    
    args = parser.parse_args()
    
    try:
        # Initialize generator
        generator = ContentGenerator(api_key=args.api_key)
        
        # Generate content based on type
        if args.type == "email":
            if not all([args.recipient, args.topic, args.key_points]):
                print("❌ Error: --recipient, --topic, and --key-points are required for email generation")
                sys.exit(1)
            
            key_points_list = [kp.strip() for kp in args.key_points.split(",")]
            key_points_formatted = "\n".join([f"- {kp}" for kp in key_points_list])
            
            content = generator.generate_email(
                recipient=args.recipient,
                topic=args.topic,
                key_points=key_points_formatted
            )
            
            metadata = {
                "type": "email",
                "recipient": args.recipient,
                "topic": args.topic,
                "generated_at": datetime.now().isoformat()
            }
        
        elif args.type == "proposal":
            if not all([args.client, args.project, args.pain_points, args.budget, args.deadline]):
                print("❌ Error: --client, --project, --pain-points, --budget, and --deadline are required for proposal generation")
                sys.exit(1)
            
            pain_points_list = [pp.strip() for pp in args.pain_points.split(",")]
            pain_points_formatted = "\n".join([f"- {pp}" for pp in pain_points_list])
            
            content = generator.generate_proposal(
                client=args.client,
                project=args.project,
                pain_points=pain_points_formatted,
                budget=args.budget,
                deadline=args.deadline
            )
            
            metadata = {
                "type": "proposal",
                "client": args.client,
                "project": args.project,
                "budget": args.budget,
                "deadline": args.deadline,
                "generated_at": datetime.now().isoformat()
            }
        
        elif args.type == "report":
            if not all([args.project_name, args.progress, args.accomplishments]):
                print("❌ Error: --project-name, --progress, and --accomplishments are required for report generation")
                sys.exit(1)
            
            progress_list = [p.strip() for p in args.progress.split(",")]
            accomplishments_list = [a.strip() for a in args.accomplishments.split(",")]
            challenges_list = [c.strip() for c in (args.challenges or "").split(",") if c.strip()]
            next_priorities_list = [np.strip() for np in (args.next_priorities or "").split(",") if np.strip()]
            support_needed_list = [sn.strip() for sn in (args.support_needed or "").split(",") if sn.strip()]
            
            progress_formatted = "\n".join([f"- {p}" for p in progress_list])
            accomplishments_formatted = "\n".join([f"- {a}" for a in accomplishments_list])
            challenges_formatted = "\n".join([f"- {c}" for c in challenges_list]) if challenges_list else "None reported"
            next_priorities_formatted = "\n".join([f"- {np}" for np in next_priorities_list]) if next_priorities_list else "To be determined"
            support_needed_formatted = "\n".join([f"- {sn}" for sn in support_needed_list]) if support_needed_list else "None needed"
            
            content = generator.generate_report(
                project_name=args.project_name,
                period=args.period,
                progress_points=progress_formatted,
                accomplishments=accomplishments_formatted,
                challenges=challenges_formatted,
                next_priorities=next_priorities_formatted,
                support_needed=support_needed_formatted
            )
            
            metadata = {
                "type": "report",
                "project_name": args.project_name,
                "period": args.period,
                "generated_at": datetime.now().isoformat()
            }
        
        else:
            print(f"❌ Error: Unknown content type: {args.type}")
            sys.exit(1)
        
        # Save output
        if args.output:
            output_path = Path(args.output)
            with open(output_path, 'w') as f:
                if metadata:
                    metadata_str = "\n".join([f"{k}: {v}" for k, v in metadata.items()])
                    f.write(f"---\n{metadata_str}\n---\n\n{content}")
                else:
                    f.write(content)
            print(f"✅ Content saved to: {output_path}")
        else:
            filepath = generator.save_output(content, args.type, metadata)
            print(f"\n📄 Generated content saved to: {filepath}")
        
        # Print success message
        print(f"\n🎉 Successfully generated {args.type}!")
        print(f"📝 Content preview:\n")
        print(content[:500] + "..." if len(content) > 500 else content)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()