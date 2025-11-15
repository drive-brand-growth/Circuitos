#!/usr/bin/env python3
"""
Comprehensive UI/UX Testing for MetroFlex Events AI Agent
Tests various user scenarios and evaluates response quality
"""

import os
import json
import sys
from datetime import datetime
from typing import List, Dict

# Assuming the agent can be imported after fixing the syntax error
# For now, we'll create a direct API testing approach

import requests
import time

class MetroFlexAgentTester:
    def __init__(self, base_url: str = "http://localhost:5001"):
        self.base_url = base_url
        self.session_id = "test-session-comprehensive"
        self.test_results = []

    def send_message(self, message: str) -> Dict:
        """Send a message to the AI agent and get response"""
        try:
            response = requests.post(
                f"{self.base_url}/webhook/chat",
                json={"message": message, "session_id": self.session_id},
                timeout=30
            )
            return {
                "success": True,
                "status_code": response.status_code,
                "data": response.json() if response.status_code == 200 else {},
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "status_code": 0,
                "data": {},
                "error": str(e)
            }

    def check_health(self) -> bool:
        """Check if the agent is running"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False

    def score_response(self, query: str, response_data: Dict, expected_keywords: List[str] = None) -> Dict:
        """Score the quality of the response"""
        score = 0
        max_score = 10
        feedback = []

        if not response_data.get("success"):
            return {
                "score": 0,
                "max_score": max_score,
                "feedback": ["Failed to get response from agent"],
                "response_text": ""
            }

        response_text = response_data.get("data", {}).get("response", "")

        # Criterion 1: Response exists and is not empty (2 points)
        if response_text and len(response_text) > 20:
            score += 2
            feedback.append("✓ Response is substantive")
        else:
            feedback.append("✗ Response is too short or empty")

        # Criterion 2: Response is relevant (contains expected keywords) (2 points)
        if expected_keywords:
            found_keywords = sum(1 for kw in expected_keywords if kw.lower() in response_text.lower())
            if found_keywords >= len(expected_keywords) * 0.5:  # At least 50% of keywords
                score += 2
                feedback.append(f"✓ Contains relevant keywords ({found_keywords}/{len(expected_keywords)})")
            else:
                feedback.append(f"✗ Missing key information ({found_keywords}/{len(expected_keywords)} keywords)")
        else:
            score += 1  # Partial credit if no keywords specified

        # Criterion 3: Appropriate length (1-2 points)
        word_count = len(response_text.split())
        if 30 <= word_count <= 200:
            score += 2
            feedback.append(f"✓ Good length ({word_count} words)")
        elif word_count < 30:
            score += 1
            feedback.append(f"~ Response could be more detailed ({word_count} words)")
        else:
            score += 1
            feedback.append(f"~ Response is lengthy ({word_count} words)")

        # Criterion 4: Professional tone (2 points)
        professional_indicators = ["metroflex", "npc", "competition", "register", "event"]
        tone_score = sum(1 for word in professional_indicators if word in response_text.lower())
        if tone_score >= 2:
            score += 2
            feedback.append("✓ Professional and on-brand tone")
        else:
            score += 1
            feedback.append("~ Could be more professional/on-brand")

        # Criterion 5: Actionable information (2 points)
        actionable_indicators = ["http", "register", "contact", "email", "call", "visit", "muscleware"]
        action_score = sum(1 for word in actionable_indicators if word.lower() in response_text.lower())
        if action_score >= 1:
            score += 2
            feedback.append("✓ Provides actionable next steps")
        else:
            feedback.append("✗ Lacks clear call-to-action")

        return {
            "score": score,
            "max_score": max_score,
            "percentage": (score / max_score) * 100,
            "feedback": feedback,
            "response_text": response_text,
            "word_count": word_count
        }

    def run_comprehensive_tests(self):
        """Run all test scenarios"""
        print("="*80)
        print("METROFLEX EVENTS AI AGENT - COMPREHENSIVE UI/UX TEST")
        print("="*80)
        print()

        # Check if agent is running
        print("Checking agent health...")
        if not self.check_health():
            print("❌ ERROR: Agent is not running at", self.base_url)
            print("Please start the agent first.")
            return

        print("✅ Agent is running")
        print()
        print("="*80)
        print("RUNNING TEST SCENARIOS")
        print("="*80)
        print()

        # Define test cases
        test_cases = [
            {
                "category": "Event Information",
                "query": "When is the Ronnie Coleman Classic?",
                "expected_keywords": ["May", "2026", "Ronnie Coleman", "Fort Worth"],
                "description": "Basic event date query"
            },
            {
                "category": "Event Information",
                "query": "Tell me about the Texas Legends Championship",
                "expected_keywords": ["Texas Legends", "March", "MetroFlex", "Arlington"],
                "description": "Event details query"
            },
            {
                "category": "Registration Process",
                "query": "How do I register for an NPC competition?",
                "expected_keywords": ["MuscleWare", "register", "NPC", "membership"],
                "description": "Registration process inquiry"
            },
            {
                "category": "Registration Process",
                "query": "What do I need to bring on competition day?",
                "expected_keywords": ["NPC card", "tanning", "suit", "posing"],
                "description": "Competition day requirements"
            },
            {
                "category": "Divisions - Women",
                "query": "What divisions are available for women?",
                "expected_keywords": ["Bikini", "Figure", "Women's Physique", "Wellness", "Bodybuilding"],
                "description": "Women's division inquiry"
            },
            {
                "category": "Divisions - Men",
                "query": "What's the difference between Men's Physique and Classic Physique?",
                "expected_keywords": ["board shorts", "posing trunks", "Classic", "Physique"],
                "description": "Division comparison query"
            },
            {
                "category": "MuscleWare Platform",
                "query": "What is MuscleWare?",
                "expected_keywords": ["registration", "platform", "NPC", "online"],
                "description": "Platform information query"
            },
            {
                "category": "Weight Classes",
                "query": "What are the weight classes for Men's Bodybuilding?",
                "expected_keywords": ["weight", "class", "Bantamweight", "Heavyweight", "lbs"],
                "description": "Specific weight class inquiry"
            },
            {
                "category": "Music Requirements",
                "query": "How do I upload my posing music?",
                "expected_keywords": ["music", "upload", "format", "60 seconds"],
                "description": "Music upload process"
            },
            {
                "category": "NPC Membership",
                "query": "Do I need an NPC membership to compete?",
                "expected_keywords": ["NPC", "card", "membership", "required", "purchase"],
                "description": "Membership requirement inquiry"
            },
            {
                "category": "Pricing",
                "query": "How much does it cost to register?",
                "expected_keywords": ["fee", "cost", "price", "registration"],
                "description": "Pricing information query"
            },
            {
                "category": "First-Time Competitor",
                "query": "I've never competed before. What should I know?",
                "expected_keywords": ["first", "beginner", "division", "preparation"],
                "description": "First-timer guidance"
            }
        ]

        # Run each test
        for i, test in enumerate(test_cases, 1):
            print(f"\n[TEST {i}/{len(test_cases)}] {test['category']}")
            print(f"Query: \"{test['query']}\"")
            print(f"Description: {test['description']}")
            print("-" * 80)

            # Send query
            response_data = self.send_message(test['query'])

            # Score response
            scoring = self.score_response(
                test['query'],
                response_data,
                test.get('expected_keywords')
            )

            # Store result
            self.test_results.append({
                "test_number": i,
                "category": test['category'],
                "query": test['query'],
                "description": test['description'],
                "response": scoring['response_text'],
                "score": scoring['score'],
                "max_score": scoring['max_score'],
                "percentage": scoring['percentage'],
                "feedback": scoring['feedback'],
                "word_count": scoring.get('word_count', 0)
            })

            # Print result
            print(f"\n📊 SCORE: {scoring['score']}/{scoring['max_score']} ({scoring['percentage']:.0f}%)")
            print("\n✏️ Feedback:")
            for feedback_item in scoring['feedback']:
                print(f"   {feedback_item}")

            print(f"\n💬 Response ({scoring.get('word_count', 0)} words):")
            print(f"{scoring['response_text'][:300]}{'...' if len(scoring['response_text']) > 300 else ''}")

            # Small delay between tests
            time.sleep(0.5)

        # Generate summary report
        self.generate_summary_report()

    def generate_summary_report(self):
        """Generate final test summary"""
        print("\n")
        print("="*80)
        print("COMPREHENSIVE TEST REPORT - SUMMARY")
        print("="*80)
        print()

        if not self.test_results:
            print("No test results to report.")
            return

        # Calculate overall statistics
        total_score = sum(r['score'] for r in self.test_results)
        max_possible = sum(r['max_score'] for r in self.test_results)
        overall_percentage = (total_score / max_possible) * 100

        # Category breakdown
        categories = {}
        for result in self.test_results:
            cat = result['category']
            if cat not in categories:
                categories[cat] = {'scores': [], 'max_scores': []}
            categories[cat]['scores'].append(result['score'])
            categories[cat]['max_scores'].append(result['max_score'])

        print(f"📈 OVERALL PERFORMANCE")
        print(f"   Total Score: {total_score}/{max_possible} ({overall_percentage:.1f}%)")
        print(f"   Tests Run: {len(self.test_results)}")
        print()

        # Performance rating
        if overall_percentage >= 90:
            rating = "EXCELLENT ⭐⭐⭐⭐⭐"
            assessment = "The agent performs at a world-class level."
        elif overall_percentage >= 80:
            rating = "VERY GOOD ⭐⭐⭐⭐"
            assessment = "The agent performs well with minor improvements needed."
        elif overall_percentage >= 70:
            rating = "GOOD ⭐⭐⭐"
            assessment = "The agent is functional but has room for improvement."
        elif overall_percentage >= 60:
            rating = "FAIR ⭐⭐"
            assessment = "The agent needs significant improvements."
        else:
            rating = "NEEDS WORK ⭐"
            assessment = "The agent requires major enhancements."

        print(f"🏆 PERFORMANCE RATING: {rating}")
        print(f"   {assessment}")
        print()

        # Category breakdown
        print("📊 PERFORMANCE BY CATEGORY")
        print()
        for cat, data in sorted(categories.items()):
            cat_score = sum(data['scores'])
            cat_max = sum(data['max_scores'])
            cat_pct = (cat_score / cat_max) * 100
            print(f"   {cat}: {cat_score}/{cat_max} ({cat_pct:.0f}%)")
        print()

        # Strengths
        print("💪 STRENGTHS IDENTIFIED")
        high_scoring = [r for r in self.test_results if r['percentage'] >= 80]
        if high_scoring:
            for result in high_scoring[:3]:  # Top 3
                print(f"   • {result['category']}: {result['description']} ({result['percentage']:.0f}%)")
        else:
            print("   • No clear strengths identified (all scores below 80%)")
        print()

        # Weaknesses
        print("⚠️ WEAKNESSES IDENTIFIED")
        low_scoring = sorted([r for r in self.test_results if r['percentage'] < 70], key=lambda x: x['percentage'])
        if low_scoring:
            for result in low_scoring[:3]:  # Bottom 3
                print(f"   • {result['category']}: {result['description']} ({result['percentage']:.0f}%)")
                print(f"     Issue: {', '.join([f for f in result['feedback'] if f.startswith('✗')])}")
        else:
            print("   • No major weaknesses identified (all scores above 70%)")
        print()

        # Recommendations
        print("🎯 RECOMMENDATIONS FOR IMPROVEMENT")
        recommendations = []

        # Analyze common issues
        missing_keywords = sum(1 for r in self.test_results if any('Missing key information' in f for f in r['feedback']))
        short_responses = sum(1 for r in self.test_results if any('too short' in f for f in r['feedback']))
        missing_cta = sum(1 for r in self.test_results if any('Lacks clear call-to-action' in f for f in r['feedback']))

        if missing_keywords > len(self.test_results) * 0.3:
            recommendations.append("Improve knowledge base coverage for specific topics")
        if short_responses > len(self.test_results) * 0.3:
            recommendations.append("Increase response detail and completeness")
        if missing_cta > len(self.test_results) * 0.3:
            recommendations.append("Add clear calls-to-action in responses (registration links, contact info)")

        if overall_percentage < 80:
            recommendations.append("Review and expand RAG retrieval parameters")
            recommendations.append("Enhance system prompt for better context awareness")

        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}. {rec}")
        else:
            print("   • Agent is performing well. Continue monitoring and minor optimizations.")

        print()
        print("="*80)
        print(f"Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)

        # Save detailed report to file
        self.save_detailed_report()

    def save_detailed_report(self):
        """Save detailed test results to JSON file"""
        report_data = {
            "test_date": datetime.now().isoformat(),
            "agent_url": self.base_url,
            "session_id": self.session_id,
            "total_tests": len(self.test_results),
            "overall_score": sum(r['score'] for r in self.test_results),
            "max_possible_score": sum(r['max_score'] for r in self.test_results),
            "overall_percentage": (sum(r['score'] for r in self.test_results) / sum(r['max_score'] for r in self.test_results)) * 100,
            "test_results": self.test_results
        }

        filename = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(report_data, f, indent=2)

        print(f"\n📄 Detailed report saved to: {filename}")

if __name__ == "__main__":
    # You can override the base URL if needed
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5001"

    tester = MetroFlexAgentTester(base_url)
    tester.run_comprehensive_tests()
