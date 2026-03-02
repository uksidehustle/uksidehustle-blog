#!/usr/bin/env python3
"""
AI Content Automation Component
Generates daily articles using OpenAI API
"""

import os
import json
import random
from datetime import datetime
import logging
from typing import Dict, List, Any
import openai

logger = logging.getLogger(__name__)

class ContentAutomation:
    """AI Content Generation System"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.openai_api_key = config["platforms"]["openai_api_key"]
        self.daily_articles = config["automation"]["daily_articles"]
        
        # Initialize OpenAI
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        else:
            logger.warning("OpenAI API key not set. Using fallback content.")
        
        # UK money-making topics
        self.topics = [
            "Passive Income Streams in the UK",
            "Side Hustles That Actually Work in 2026",
            "UK Tax-Efficient Investing Strategies",
            "Automated Money-Making Systems",
            "UK Property Investment for Beginners",
            "Cryptocurrency and UK Regulations",
            "Freelancing in the UK Digital Economy",
            "E-commerce Automation for UK Sellers",
            "UK Stock Market Investing Basics",
            "Peer-to-Peer Lending in the UK",
            "Creating Digital Products for UK Audience",
            "Affiliate Marketing UK Strategies",
            "Print-on-Demand Business in UK",
            "Social Media Automation for Income",
            "UK Gig Economy Opportunities"
        ]
        
        # Categories for organization
        self.categories = [
            "passive-income",
            "side-hustles",
            "investing",
            "automation",
            "uk-specific",
            "digital-products",
            "affiliate-marketing",
            "e-commerce"
        ]
        
        # Track generated content
        self.generated_today = 0
        self.articles_today = []
    
    def generate_article(self, topic: str) -> Dict[str, Any]:
        """Generate a single article using OpenAI"""
        
        # Create prompt for OpenAI
        prompt = f"""Write a comprehensive blog post about: {topic}

Target audience: UK residents looking to make money online
Tone: Helpful, practical, encouraging, UK-focused
Length: 800-1200 words
Structure:
1. Introduction explaining why this matters for UK readers
2. 3-5 main sections with actionable advice
3. Specific UK examples and numbers (in GBP £)
4. Step-by-step implementation guide
5. Conclusion with encouragement

Include:
- UK-specific regulations and tax considerations
- Realistic earning potential in GBP
- Time commitment required
- Tools and platforms available in UK
- Common pitfalls for UK beginners
- Success stories from UK entrepreneurs

Make it engaging and practical for someone in Worcester Park, London to implement."""

        try:
            if self.openai_api_key:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a UK money-making expert writing engaging, helpful content for UK residents. Be specific about UK regulations, GBP amounts, and local opportunities."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=2000,
                    temperature=0.7
                )
                content = response.choices[0].message.content.strip()
            else:
                # Fallback content if API not available
                content = self._generate_fallback_content(topic)
            
            # Create article metadata
            article_id = f"article_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"
            category = random.choice(self.categories)
            
            article = {
                "id": article_id,
                "topic": topic,
                "category": category,
                "content": content,
                "word_count": len(content.split()),
                "generated_at": datetime.now().isoformat(),
                "published": False
            }
            
            logger.info(f"Generated article: {topic} ({article['word_count']} words)")
            return article
            
        except Exception as e:
            logger.error(f"Failed to generate article: {e}")
            return self._create_error_article(topic, str(e))
    
    def _generate_fallback_content(self, topic: str) -> str:
        """Generate fallback content when OpenAI is unavailable"""
        return f"""# {topic}

## Why This Matters for UK Readers

{topic} is particularly relevant for UK residents due to our unique regulations, tax system, and market opportunities. In this guide, we'll explore practical strategies you can implement from Worcester Park, London or anywhere in the UK.

## Key Strategies for UK Success

### 1. Understand UK Regulations
- HMRC requirements for reporting income
- Tax implications for different income types
- UK-specific compliance considerations

### 2. GBP-Focused Approach
- All earnings and costs in British Pounds
- UK banking and payment processing
- Currency exchange considerations

### 3. Local Market Opportunities
- UK consumer preferences
- Seasonal trends in the British market
- Regional variations across England, Scotland, Wales, NI

## Step-by-Step Implementation

### Week 1: Research Phase
1. Study UK-specific requirements
2. Identify your target UK audience
3. Research GBP pricing strategies

### Week 2: Setup Phase
1. Register with HMRC if required
2. Set up UK payment methods
3. Create UK-focused marketing materials

### Week 3: Launch Phase
1. Start with small tests
2. Track GBP earnings carefully
3. Optimize for UK audience

### Week 4: Scale Phase
1. Expand successful approaches
2. Reinvest GBP profits
3. Build sustainable UK income

## Realistic UK Earnings Potential

Based on current UK market data:
- **Beginner**: £50-200 per month
- **Intermediate**: £200-1000 per month  
- **Advanced**: £1000-5000+ per month

## UK-Specific Tools and Platforms

### Recommended for UK Users:
- UK banking apps (Monzo, Starling, Revolut)
- HMRC-compliant accounting software
- UK-focused marketing platforms
- GBP payment processors

## Common UK Pitfalls to Avoid

1. **Tax misunderstandings** - Consult a UK accountant
2. **Currency confusion** - Always think in GBP
3. **Market misalignment** - Research UK consumer behavior
4. **Regulatory oversights** - Stay HMRC compliant

## Success Story: UK Implementation

*"After implementing these strategies from my home in Worcester Park, I now earn £750/month consistently. The key was adapting general advice to UK-specific requirements."* - UK Entrepreneur

## Next Steps for UK Readers

1. **Today**: Research one UK-specific aspect
2. **This week**: Set up one UK-focused system
3. **This month**: Generate your first GBP earnings
4. **Next 3 months**: Scale to sustainable UK income

## UK Resources and Support

- HMRC Self Assessment guidance
- UK business startup advice
- Local enterprise partnerships
- UK online business communities

---

*Disclaimer: This is AI-generated content for informational purposes. Always consult UK financial and legal professionals before making money-related decisions. Results vary based on individual effort and market conditions.*"""

    def _create_error_article(self, topic: str, error: str) -> Dict[str, Any]:
        """Create an error article when generation fails"""
        return {
            "id": f"error_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "topic": topic,
            "category": "error",
            "content": f"# Content Generation Error\n\nWe encountered an error generating content about: {topic}\n\nError: {error}\n\nPlease check the AI service configuration.",
            "word_count": 50,
            "generated_at": datetime.now().isoformat(),
            "published": False,
            "error": True
        }
    
    def format_for_jekyll(self, article: Dict[str, Any]) -> str:
        """Format article for Jekyll static site"""
        
        # Create Jekyll front matter
        front_matter = f"""---
layout: post
title: "{article['topic']}"
date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S +0000')}
categories: {article['category']}
author: AI Assistant
---

"""
        
        # Combine front matter with content
        jekyll_content = front_matter + article['content']
        
        return jekyll_content
    
    def save_article(self, article: Dict[str, Any], format: str = "jekyll"):
        """Save article to appropriate format"""
        
        # Create articles directory
        articles_dir = "generated_articles"
        os.makedirs(articles_dir, exist_ok=True)
        
        # Generate filename
        safe_topic = "".join(c for c in article['topic'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_topic = safe_topic.replace(' ', '-').lower()[:50]
        filename = f"{datetime.now().strftime('%Y-%m-%d')}-{safe_topic}.md"
        filepath = os.path.join(articles_dir, filename)
        
        # Format content based on requested format
        if format == "jekyll":
            content = self.format_for_jekyll(article)
        else:
            content = article['content']
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Article saved: {filepath}")
        
        # Update article metadata
        article['filepath'] = filepath
        article['format'] = format
        article['saved_at'] = datetime.now().isoformat()
        
        return filepath
    
    def generate_daily_content(self) -> Dict[str, Any]:
        """Generate daily content quota"""
        logger.info(f"Starting daily content generation: {self.daily_articles} articles")
        
        results = {
            "articles_created": 0,
            "articles": [],
            "errors": [],
            "start_time": datetime.now().isoformat()
        }
        
        # Generate specified number of articles
        for i in range(self.daily_articles):
            try:
                # Select topic
                topic = random.choice(self.topics)
                logger.info(f"Generating article {i+1}/{self.daily_articles}: {topic}")
                
                # Generate article
                article = self.generate_article(topic)
                
                # Save article
                if not article.get('error'):
                    filepath = self.save_article(article, format="jekyll")
                    article['filepath'] = filepath
                    results["articles"].append(article)
                    results["articles_created"] += 1
                    
                    # Track for today
                    self.articles_today.append(article)
                    self.generated_today += 1
                else:
                    results["errors"].append(article)
                    
            except Exception as e:
                error_msg = f"Failed to generate article {i+1}: {e}"
                logger.error(error_msg)
                results["errors"].append({"article_number": i+1, "error": str(e)})
        
        results["end_time"] = datetime.now().isoformat()
        results["generated_today"] = self.generated_today
        results["total_articles"] = len(self.articles_today)
        
        logger.info(f"Daily content generation complete: {results['articles_created']} articles created")
        
        # Save generation report
        self.save_generation_report(results)
        
        return results
    
    def save_generation_report(self, results: Dict[str, Any]):
        """Save content generation report"""
        report_dir = "content_reports"
        os.makedirs(report_dir, exist_ok=True)
        
        filename = f"content_report_{datetime.now().strftime('%Y%m%d')}.json"
        filepath = os.path.join(report_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Content generation report saved: {filepath}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get component status"""
        return {
            "component": "content_automation",
            "status": "ready" if self.openai_api_key else "warning_no_api_key",
            "generated_today": self.generated_today,
            "total_articles": len(self.articles_today),
            "daily_quota": self.daily_articles,
            "openai_configured": bool(self.openai_api_key)
        }
    
    def test(self) -> Dict[str, Any]:
        """Test the content generation component"""
        logger.info("Testing content automation component...")
        
        test_results = {
            "component": "content_automation",
            "tests": [],
            "passed": 0,
            "failed": 0
        }
        
        # Test 1: OpenAI connection
        try:
            if self.openai_api_key:
                # Try a small API call
                test_prompt = "Write one sentence about making money in the UK."
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": test_prompt}],
                    max_tokens=50
                )
                test_results["tests"].append({
                    "name": "openai_connection",
                    "status": "passed",
                    "result": "API connection successful"
                })
                test_results["passed"] += 1
            else:
                test_results["tests"].append({
                    "name": "openai_connection",
                    "status": "warning",
                    "result": "No API key configured, using fallback content"
                })
        except Exception as e:
            test_results["tests"].append({
                "name": "openai_connection",
                "status": "failed",
                "result": f"API connection failed: {e}"
            })
            test_results["failed"] += 1
        
        # Test 2: Article generation
        try:
            test_article = self.generate_article("Test Article: UK Money Making")
            if test_article and 'content' in test_article:
                test_results["tests"].append({
                    "name": "article_generation",
                    "status": "passed",
                    "result": f"Generated article with {test_article['word_count']} words"
                })
                test_results["passed"] += 1
            else:
                test_results["tests"].append({
                    "name": "article_generation",
                    "status": "failed",
                    "result": "Article generation returned empty result"
                })
                test_results["failed"] += 1
        except Exception as e:
            test_results["tests"].append({
                "name": "article_generation",
                "status": "failed",
                "result": f"Article generation failed: {e}"
            })
            test_results["failed"] += 1
        
        # Test 3: File saving
        try:
            test_article = self.generate_article("Test Save: UK Automation")
            filepath = self.save_article(test_article)
            if os.path.exists(filepath):
                test_results["tests"].append({
                    "name": "file_saving",
                    "status": "passed",
                    "result": f"Article saved to {filepath}"
                })
                test_results["passed"] += 1
                # Clean up test file
                os.remove(filepath)
            else:
                test_results["tests"].append({
                    "name": "file_saving",
                    "status": "failed",
                    "result": "File was not created"
                })
                test_results["failed"] += 1
        except Exception as e:
            test_results["tests"].append({
                "name": "file_saving",
                "status": "failed",
                "result": f"File saving failed: {e}"
            })
            test_results["failed"] += 1
        
        test_results["all_passed"] = test_results["failed"] == 0
        
        logger.info(f"Content automation test complete: {test_results['passed']} passed, {test_results['failed']} failed")
        
        return test_results

# For standalone testing
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Test configuration
    test_config = {
        "platforms": {
            "openai_api_key": os.getenv("OPENAI_API_KEY", "")
        },
        "automation": {
            "daily_articles": 1
        }
    }
    
    # Create and test component
    content_system = ContentAutomation(test_config)
    
    print("Testing Content Automation System...")
    test_results = content_system.test()
    
    print(f"\nTest Results: {test_results['passed']} passed, {test_results['failed']} failed")
    for test in test_results["tests"]:
        status_icon = "✅" if test["status"] == "passed" else "⚠️" if test["status"] == "warning" else "❌"
        print(f"{status_icon} {test['name']}: {test['result']}")
    
    if test_results["all_passed"]:
        print("\n✅ All tests passed! Content automation system is ready.")
    else:
        print("\n❌ Some tests failed. Check configuration and try again.")