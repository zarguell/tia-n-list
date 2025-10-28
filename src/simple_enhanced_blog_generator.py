"""Simple enhanced blog generation module for Tia N. List project.

A simpler version for testing the enhanced blog generation features.
"""

import datetime
from pathlib import Path
from typing import List, Dict, Any
from src import database, persona
from src.threat_classifier import classify_article


def generate_simple_enhanced_summary() -> bool:
    """Generate a simple enhanced summary with threat categorization.

    Returns:
        True if successful, False otherwise.
    """
    try:
        print("Generating simple enhanced threat intelligence summary...")

        # Get top articles
        articles = database.get_top_articles(8)
        if not articles:
            print("No articles found for summary")
            return False

        # Categorize articles
        categorized = {}
        for article in articles:
            title = article['title']
            content = article.get('raw_content', '')

            # Classify threat
            category, confidence = classify_article(title, content)
            category_name = category.value.replace('_', ' ').title()

            if category_name not in categorized:
                categorized[category_name] = []

            categorized[category_name].append({
                'title': article['title'],
                'summary': article.get('summary', 'No summary available'),
                'score': article.get('score', 0),
                'url': article['url'],
                'source': article.get('source_name', 'Unknown'),
                'confidence': confidence,
                'category': category_name
            })

        # Get joke
        joke = persona.fetch_joke_of_the_day()

        # Create enhanced blog content
        now = datetime.datetime.now()
        blog_content = f"""---
title: "Enhanced Threat Intelligence Briefing - {now.strftime('%Y-%m-%d')}"
date: {now.strftime('%Y-%m-%d')}
tags: [threat-intelligence, cybersecurity, enhanced-briefing]
author: "Tia N. List"
summary: "Enhanced briefing with threat categorization and actionable intelligence."
---

# 🛡️ Enhanced Threat Intelligence Briefing

**Date:** {now.strftime('%B %d, %Y')}
**Sources Analyzed:** {len(articles)} articles
**Threat Categories:** {len(categorized)} identified

Good morning, cyber defenders! Your AI-powered threat intelligence analyst has processed today's security feeds to provide enhanced threat analysis with categorization and actionable insights.

---

## 🚨 Priority Threat Analysis

"""

        # Add top threats by score
        all_articles_sorted = sorted(articles, key=lambda x: x.get('score', 0), reverse=True)

        for i, article in enumerate(all_articles_sorted[:5], 1):
            # Classify this article
            category, confidence = classify_article(article['title'], article.get('raw_content', ''))
            category_name = category.value.replace('_', ' ').title()

            # Generate specific insight based on category
            insight = generate_category_insight(category_name, article['title'])

            blog_content += f"""### {i}. {article['title']}

**Category:** {category_name} | **Relevance:** 🟢 ({article.get('score', 0)}/100)

**Analysis:** {article.get('summary', 'No summary available')[:250]}...

**🎯 Tia's Enhanced Analysis:** {insight}

**Source:** [{article.get('source_name', 'Unknown')}]({article['url']})

---

"""

        # Add threat category breakdown
        blog_content += """
## 📊 Threat Category Breakdown

**Today's Threat Landscape:**

"""

        for category_name, category_articles in sorted(categorized.items(), key=lambda x: len(x[1]), reverse=True):
            avg_score = sum(a['score'] for a in category_articles) / len(category_articles)
            blog_content += f"""**{category_name}** ({len(category_articles)} incidents)
- Average Severity: {avg_score:.0f}/100
- Sample: {category_articles[0]['title'][:60]}...

"""

        # Add actionable recommendations
        blog_content += """
## 🛠️ Priority Actions

**Immediate Defensive Measures:**
"""

        # Generate recommendations based on top categories
        top_categories = sorted(categorized.items(), key=lambda x: len(x[1]), reverse=True)[:3]
        for category_name, articles in top_categories:
            action = get_category_action(category_name)
            blog_content += f"• **{category_name}:** {action}\n"

        # Add executive summary
        blog_content += f"""
## 📋 Executive Summary

**Key Intelligence Points:**
• **{len(all_articles_sorted)} relevant threats** identified from security feeds
• **Primary concern:** {top_categories[0][0] if top_categories else 'General security threats'} with {len(top_categories[0][1])} related incidents
• **Average threat severity:** {sum(a.get('score', 0) for a in articles) / len(articles):.0f}/100

**Strategic Recommendations:**
1. Enhanced monitoring for {', '.join([cat[0] for cat in top_categories[:2]])}
2. User awareness training focused on identified threat patterns
3. Review and update relevant security controls

"""

        # Add joke section
        if joke:
            blog_content += f"""
## 🎭 Cybersecurity Perspective

While we focus on serious threats, remember to maintain balance:

_{joke}_

A well-rested security team is an effective security team.

---

"""

        # Add methodology
        blog_content += f"""
## 🔍 Analysis Methodology

This enhanced briefing includes:

• **AI-powered threat categorization** with confidence scoring
• **Pattern recognition** across multiple sources
• **Actionable intelligence** tailored to threat types
• **Executive summary** for leadership awareness

**Data sources:** {len(articles)} processed articles
**Enhancement features:** Threat classification, confidence scoring, tailored recommendations

---

*Generated by Tia N. List - Enhanced AI-powered Threat Intelligence Analyst*
*Analysis completed: {now.strftime('%Y-%m-%d %H:%M:%S')}*
"""

        # Ensure hugo/content/posts directory exists
        posts_dir = Path("hugo/content/posts")
        posts_dir.mkdir(parents=True, exist_ok=True)

        # Create filename with date
        filename = f"{now.strftime('%Y-%m-%d')}-enhanced-threat-briefing.md"
        filepath = posts_dir / filename

        # Write blog post
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(blog_content)

        print(f"✅ Enhanced threat briefing generated: {filename}")
        print(f"📁 Content length: {len(blog_content)} characters")
        print(f"🎯 Categories analyzed: {len(categorized)}")
        print(f"📊 Articles processed: {len(articles)}")

        return True

    except Exception as e:
        print(f"✗ Error generating enhanced briefing: {e}")
        import traceback
        traceback.print_exc()
        return False


def generate_category_insight(category_name: str, title: str) -> str:
    """Generate specific insight based on threat category.

    Args:
        category_name: Name of the threat category.
        title: Article title.

    Returns:
        Category-specific insight.
    """
    insights = {
        'Data Breach': "Implement immediate incident response procedures. Review access logs and notify affected stakeholders. Consider regulatory notification requirements.",
        'Malware': "Update antivirus definitions and conduct system scans. Review network traffic for indicators of compromise and isolate affected systems.",
        'Phishing': "Enhance email filtering and conduct user awareness training. Implement multi-factor authentication and verify email sender authenticity.",
        'Vulnerability': "Prioritize patch management for affected systems. Implement compensating controls and monitor for exploitation attempts.",
        'Ransomware': "Verify backup integrity and isolation. Review incident response plans and consider business continuity procedures.",
        'Supply Chain': "Audit third-party dependencies and monitor supply chain communications. Review vendor security practices and access controls.",
        'Apt': "Enhance threat hunting and monitoring capabilities. Review access logs and consider threat intelligence sharing partnerships.",
        'Social Engineering': "Conduct security awareness training and implement verification procedures for sensitive requests. Review social media policies.",
        'Network Security': "Review firewall configurations and network segmentation. Implement intrusion detection and monitor network anomalies.",
        'Other': "Review security controls and monitor for related activity. Update relevant policies and procedures."
    }

    return insights.get(category_name, "Review security controls and implement enhanced monitoring for this threat type.")


def get_category_action(category_name: str) -> str:
    """Get immediate action for threat category.

    Args:
        category_name: Name of the threat category.

    Returns:
        Immediate action recommendation.
    """
    actions = {
        'Data Breach': "Activate incident response team and assess scope",
        'Malware': "Scan all endpoints and update signatures",
        'Phishing': "Block sender domains and user awareness alert",
        'Vulnerability': "Prioritize patching of critical systems",
        'Ransomware': "Verify backup isolation and recovery procedures",
        'Supply Chain': "Audit third-party access and dependencies",
        'Apt': "Enhance monitoring and threat hunting activities",
        'Social Engineering': "Send security awareness alert to all staff",
        'Network Security': "Review firewall rules and network logs",
        'Other': "Monitor for related activities and review controls"
    }

    return actions.get(category_name, "Review and update relevant security controls")


if __name__ == "__main__":
    success = generate_simple_enhanced_summary()
    if not success:
        print("Failed to generate simple enhanced briefing")