"""Enhanced blog generation module for Tia N. List project.

This module creates high-quality, intelligence-rich blog posts with
threat categorization, IOCs, TTPs, and actionable insights.
"""

import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from src import database, persona
from src.threat_classifier import classify_article, get_threat_classifier


def generate_intelligence_summary() -> Dict[str, Any]:
    """Generate a comprehensive threat intelligence summary.

    Returns:
        Dictionary containing intelligence analysis and categorized threats.
    """
    print("Generating enhanced threat intelligence summary...")

    # Get top articles
    articles = database.get_top_articles(15)
    if not articles:
        print("No articles found for intelligence summary")
        return {}

    classifier = get_threat_classifier()

    # Categorize articles
    categorized_articles = {}
    threat_summary = {}
    total_articles = len(articles)

    for article in articles:
        title = article['title']
        content = article.get('raw_content', '')

        # Classify threat
        category, confidence = classify_article(title, content)

        # Add to category
        if category not in categorized_articles:
            categorized_articles[category] = []

        categorized_articles[category].append({
            **article,
            'threat_category': category,
            'confidence': confidence
        })

        # Track threat summary
        if category not in threat_summary:
            threat_summary[category] = {
                'count': 0,
                'avg_score': 0,
                'total_score': 0,
                'highest_score': 0,
                'top_article': None
            }

        threat_summary[category]['count'] += 1
        score = article.get('score', 0)
        threat_summary[category]['total_score'] += score

        if score > threat_summary[category]['highest_score']:
            threat_summary[category]['highest_score'] = score
            threat_summary[category]['top_article'] = article

    # Calculate averages
    for category in threat_summary:
        count = threat_summary[category]['count']
        if count > 0:
            threat_summary[category]['avg_score'] = threat_summary[category]['total_score'] / count

    return {
        'categorized_articles': categorized_articles,
        'threat_summary': threat_summary,
        'total_articles': total_articles,
        'generated_at': datetime.datetime.now()
    }


def extract_ttps_from_content(content: str) -> List[str]:
    """Extract Tactics, Techniques, and Procedures from content.

    Args:
        content: Article content to analyze.

    Returns:
        List of identified TTPs.
    """
    ttp_patterns = [
        'spear phishing',
        'credential harvesting',
        'privilege escalation',
        'lateral movement',
        'data exfiltration',
        'command and control',
        'persistence mechanism',
        'defense evasion',
        'reconnaissance',
        'weaponization',
        'delivery',
        'exploitation',
        'installation',
        'objectives',
        'supply chain compromise',
        'watering hole',
        'malicious document',
        'macro execution',
        'script injection',
        'api abuse',
        'brute force',
        'dictionary attack'
    ]

    found_ttps = []
    content_lower = content.lower()

    for ttp in ttp_patterns:
        if ttp in content_lower:
            found_ttps.append(ttp.title())

    return list(set(found_ttps))  # Remove duplicates


def generate_enhanced_daily_summary() -> bool:
    """Generate an enhanced daily summary blog post with rich intelligence.

    Returns:
        True if successful, False otherwise.
    """
    try:
        # Generate intelligence summary
        intel = generate_intelligence_summary()
        if not intel:
            print("No intelligence data available")
            return False

        categorized_articles = intel['categorized_articles']
        threat_summary = intel['threat_summary']
        total_articles = intel['total_articles']

        # Get joke
        joke = persona.fetch_joke_of_the_day()

        # Create enhanced blog content
        now = datetime.datetime.now()
        blog_content = f"""---
title: "Threat Intelligence Daily Briefing - {now.strftime('%Y-%m-%d')}"
date: {now.strftime('%Y-%m-%d')}
tags: [threat-intelligence, cybersecurity, daily-briefing, ttps]
author: "Tia N. List"
summary: "Comprehensive daily briefing with categorized threats, IOCs, and actionable intelligence from {total_articles} analyzed sources."
---

# 🕵️‍♀️ Threat Intelligence Daily Briefing

**Date:** {now.strftime('%B %d, %Y')}
**Sources Analyzed:** {total_articles} articles
**Threat Categories:** {len(categorized_articles)} identified

Good morning, cyber defenders! Your AI-powered threat intelligence analyst has processed {total_articles} sources to bring you today's critical security landscape analysis.

---

## 🚨 Critical Threats (Priority Alert)

"""

        # Add critical threats (high-scoring articles)
        critical_articles = []
        for category, articles in categorized_articles.items():
            for article in articles:
                if article.get('score', 0) >= 80:
                    critical_articles.append((category, article))

        critical_articles.sort(key=lambda x: x[1].get('score', 0), reverse=True)

        for i, (category, article) in enumerate(critical_articles[:5], 1):
            classifier = get_threat_classifier()
            emoji = classifier.get_category_emoji(category)

            # Extract TTPs
            ttps = extract_ttps_from_content(article.get('raw_content', ''))
            ttp_text = f"**TTPs:** {', '.join(ttps[:3])}" if ttps else ""

            # Extract IOCs
            iocs = database.get_iocs_by_article_id(article['id'])
            ioc_text = ""
            if iocs:
                ioc_text = "**Key IOCs:** " + ", ".join([f"{ioc['type']}: {ioc['value']}" for ioc in iocs[:3]])

            # Generate actionable insight
            content_length = len(article.get('raw_content', ''))
            insight = generate_actionable_insight(category, article['title'], content_length)

            blog_content += f"""### {i}. {article['title']}

**Threat Type:** {emoji} {category.value.replace('_', ' ').title()} | **Relevance:** 🟢 ({article.get('score', 0)}/100)

**Summary:** {article.get('summary', 'No summary available')[:300]}...

{ttp_text}

{ioc_text}

**🎯 Tia's Analysis:** {insight}

**Source:** [{article.get('source_name', 'Unknown')}]({article['url']})

---

"""

        # Add threat category breakdown
        blog_content += """
## 📊 Threat Landscape Analysis

**Current Threat Distribution:**

"""

        for category, data in sorted(threat_summary.items(), key=lambda x: x[1]['count'], reverse=True):
            if data['count'] > 0:
                classifier = get_threat_classifier()
                emoji = classifier.get_category_emoji(category)
                description = classifier.get_category_description(category)

                blog_content += f"""**{emoji} {category.value.replace('_', ' ').title()}** ({data['count']} incidents)
- {description}
- Average Severity: {data['avg_score']:.0f}/100

"""

        # Add executive summary
        blog_content += """
## 📋 Executive Summary

**Key Takeaways for Leadership:**

"""

        if critical_articles:
            blog_content += f"""• **{len(critical_articles)} high-priority threats** identified requiring immediate attention
• **Primary attack vectors:** """

            # Identify top threat patterns
            top_categories = sorted(threat_summary.items(), key=lambda x: x[1]['avg_score'], reverse=True)[:3]
            category_names = [cat.value.replace('_', ' ').title() for cat, _ in top_categories]
            blog_content += f"{', '.join(category_names)}\n"

            # Recommend actions
            blog_content += f"""• **Recommended immediate actions:** Enhanced monitoring, user education, and security controls review
• **Resource allocation:** Focus on {"incident response" if any(c.value == "ransomware" for c in top_categories) else "preventive measures"}

"""

        # Add actionable recommendations
        blog_content += """
## 🛡️ Defensive Recommendations

**Based on today's threat landscape:**

"""

        recommendations = generate_defensive_recommendations(categorized_articles)
        for rec in recommendations[:5]:
            blog_content += f"• {rec}\n"

        # Add joke section
        if joke:
            blog_content += f"""
## 🎭 Today's Cybersecurity Wisdom

While staying vigilant against threats, remember to maintain perspective:

_{joke}_

Sometimes the best defense is a good sense of humor... and updated antivirus.

---

"""

        # Add methodology
        blog_content += f"""
## 📈 Intelligence Methodology

This briefing analyzes {total_articles} threat intelligence sources using:

• **AI-powered classification** and relevance scoring
• **Automated IOC/TTP extraction** from full article content
• **Threat categorization** with confidence scoring
• **Cross-source correlation** and pattern analysis

**Data Quality:** {len([a for articles in categorized_articles.values() for a in articles if a.get('content_source') == 'scraped'])} articles enhanced with full content extraction

---

*Generated by Tia N. List - Your AI-powered Threat Intelligence Analyst*
*Last updated: {now.strftime('%Y-%m-%d %H:%M:%S')}*
"""

        # Ensure hugo/content/posts directory exists
        posts_dir = Path("hugo/content/posts")
        posts_dir.mkdir(parents=True, exist_ok=True)

        # Create filename with date
        filename = f"{now.strftime('%Y-%m-%d')}-threat-intelligence-briefing.md"
        filepath = posts_dir / filename

        # Write blog post
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(blog_content)

        print(f"✅ Enhanced intelligence briefing generated: {filename}")
        print(f"📁 Content length: {len(blog_content)} characters")
        print(f"🎯 Threat categories analyzed: {len(categorized_articles)}")
        print(f"🚨 Critical threats identified: {len(critical_articles)}")

        return True

    except Exception as e:
        print(f"✗ Error generating enhanced briefing: {e}")
        return False


def generate_actionable_insight(category, title: str, content_length: int) -> str:
    """Generate actionable insight based on threat category and article.

    Args:
        category: Threat category.
        title: Article title.
        content_length: Length of article content.

    Returns:
        Actionable insight text.
    """
    insights = {
        'malware': "Update antivirus signatures and implement application whitelisting. Monitor network traffic for suspicious connections.",
        'phishing': "Conduct immediate user awareness training. Implement email filtering and multi-factor authentication enforcement.",
        'vulnerability': "Prioritize patching for affected systems. Implement compensating controls until patches can be applied.",
        'data_breach': "Review incident response plans. Notify affected parties and assess regulatory compliance requirements.",
        'ransomware': "Ensure critical data backups are isolated and tested. Review incident response and business continuity plans.",
        'supply_chain': "Audit third-party dependencies and implement software composition analysis. Review vendor security practices.",
        'apt': "Enhance monitoring and logging. Review access controls and implement threat hunting procedures.",
        'social_engineering': "Conduct security awareness training. Implement verification procedures for sensitive requests.",
        'network_security': "Review firewall rules and network segmentation. Implement intrusion detection and prevention systems.",
        'mobile_security': "Review mobile device management policies. Update mobile applications and operating systems.",
        'cloud_security': "Review cloud security configurations and access controls. Implement cloud security monitoring.",
        'iot_security': "Segment IoT networks and update device firmware. Implement network-based monitoring for IoT devices."
    }

    base_insight = insights.get(category.value, "Review security controls and monitor for related activity.")

    # Add content quality context
    if content_length > 3000:
        base_insight += " Detailed technical analysis available for deep-dive investigation."

    return base_insight


def generate_defensive_recommendations(categorized_articles: Dict) -> List[str]:
    """Generate defensive recommendations based on threat patterns.

    Args:
        categorized_articles: Articles categorized by threat type.

    Returns:
        List of defensive recommendations.
    """
    recommendations = []

    # Analyze threat patterns
    for category, articles in categorized_articles.items():
        if len(articles) >= 2:  # Multiple incidents of same type
            if category.value == 'phishing':
                recommendations.append("Implement advanced email filtering and regular user phishing simulations")
            elif category.value == 'malware':
                recommendations.append("Enhance endpoint detection and response (EDR) capabilities")
            elif category.value == 'vulnerability':
                recommendations.append("Accelerate patch management programs for critical systems")
            elif category.value == 'ransomware':
                recommendations.append("Strengthen backup and recovery procedures with regular testing")

    # General recommendations
    if not recommendations:
        recommendations = [
            "Maintain regular security awareness training for all personnel",
            "Keep systems and applications patched with latest security updates",
            "Monitor security logs and alerts for suspicious activities",
            "Regularly test incident response procedures and business continuity plans"
        ]

    return recommendations


if __name__ == "__main__":
    success = generate_enhanced_daily_summary()
    if not success:
        print("Failed to generate enhanced intelligence briefing")