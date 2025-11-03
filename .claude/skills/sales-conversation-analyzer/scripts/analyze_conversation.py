#!/usr/bin/env python3
"""
CLI tool to analyze sales conversations
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analyzer import SalesConversationAnalyzer


def main():
    parser = argparse.ArgumentParser(
        description="Analyze sales conversation transcripts"
    )
    parser.add_argument(
        "transcript",
        help="Path to transcript file or transcript text"
    )
    parser.add_argument(
        "--outcome",
        default="unknown",
        help="Conversation outcome (booked, closed, lost, etc.)"
    )
    parser.add_argument(
        "--industry",
        default="unknown",
        help="Industry of the prospect"
    )
    parser.add_argument(
        "--deal-value",
        type=float,
        help="Deal value"
    )
    parser.add_argument(
        "--output",
        help="Output file path (JSON)"
    )
    parser.add_argument(
        "--no-ai",
        action="store_true",
        help="Disable AI-powered deep analysis"
    )

    args = parser.parse_args()

    # Load transcript
    if os.path.exists(args.transcript):
        with open(args.transcript, 'r') as f:
            transcript = f.read()
        print(f"📄 Loaded transcript from: {args.transcript}")
    else:
        transcript = args.transcript
        print("📝 Using provided transcript text")

    # Initialize analyzer
    print("🧠 Initializing analyzer...")
    analyzer = SalesConversationAnalyzer(
        vector_db_path="./data/vector_db",
        frameworks=["SPIN", "Challenger", "Gap_Selling", "MEDDIC"]
    )

    # Analyze
    print("🔍 Analyzing conversation...")
    analysis = analyzer.analyze(
        transcript=transcript,
        metadata={
            "outcome": args.outcome,
            "industry": args.industry,
            "deal_value": args.deal_value
        },
        use_ai=not args.no_ai
    )

    # Print results
    print("\n" + "="*60)
    print("📊 ANALYSIS RESULTS")
    print("="*60)

    print(f"\n🎯 Effectiveness Score: {analysis.effectiveness_score:.2f} / 1.0")
    print(f"🔥 Confidence: {analysis.confidence_score:.2f}")
    print(f"📈 Outcome: {analysis.outcome_classification}")
    print(f"⭐ Training Value: {analysis.training_value}")

    print(f"\n🎓 DETECTED PATTERNS ({len(analysis.key_patterns)}):")
    for i, pattern in enumerate(analysis.key_patterns[:5], 1):
        print(f"  {i}. {pattern['technique']} (effectiveness: {pattern.get('effectiveness', 0):.2f})")
        print(f"     \"{pattern.get('text', '')[:80]}...\"")

    print(f"\n🎯 BUYER SIGNALS:")
    print(f"  Intent Score: {analysis.buyer_signals.get('intent_score', 0)}/100")
    print(f"  Pain Level: {analysis.buyer_signals.get('pain_level', 'unknown')}")
    print(f"  Authority: {analysis.buyer_signals.get('authority', 'unknown')}")
    print(f"  Budget: {analysis.buyer_signals.get('budget_qualification', 'unknown')}")
    print(f"  Timeline: {analysis.buyer_signals.get('timeline', 'unknown')}")
    if analysis.buyer_signals.get('objections'):
        print(f"  Objections: {', '.join(analysis.buyer_signals['objections'])}")

    print(f"\n📈 CONVERSATION FLOW:")
    print(f"  Structure Quality: {analysis.conversation_flow.get('structure_quality', 'unknown')}")
    print(f"  Phases Completed: {', '.join(analysis.conversation_flow.get('phases_completed', []))}")
    print(f"  Completion Rate: {analysis.conversation_flow.get('completion_rate', 0):.0%}")

    print(f"\n📊 GAP ANALYSIS:")
    print(f"  Current Level: {analysis.gap_analysis.get('current_level', 'unknown')}")
    print(f"  World-Class Comparison: {analysis.gap_analysis.get('world_class_comparison', 0):.2f}")
    print(f"  Gap Score: {analysis.gap_analysis.get('gap_score', 0):.2f}")

    if analysis.gap_analysis.get('improvement_areas'):
        print(f"\n🎯 TOP IMPROVEMENT AREAS:")
        for i, area in enumerate(analysis.gap_analysis['improvement_areas'][:3], 1):
            print(f"  {i}. {area.get('name', 'Unknown')}")
            print(f"     Current: {area.get('current_score', 0):.2f} | Target: {area.get('world_class_score', 0):.2f} | Gap: {area.get('gap', 0):.2f}")

    print(f"\n💡 RECOMMENDATIONS:")
    for i, rec in enumerate(analysis.recommendations[:5], 1):
        print(f"  {i}. {rec}")

    print(f"\n🏷️  TAGS: {', '.join(analysis.pattern_tags)}")

    # Save output if requested
    if args.output:
        output_data = {
            "conversation_id": analysis.conversation_id,
            "effectiveness_score": analysis.effectiveness_score,
            "confidence_score": analysis.confidence_score,
            "outcome_classification": analysis.outcome_classification,
            "training_value": analysis.training_value,
            "key_patterns": analysis.key_patterns,
            "buyer_signals": analysis.buyer_signals,
            "conversation_flow": analysis.conversation_flow,
            "gap_analysis": analysis.gap_analysis,
            "recommendations": analysis.recommendations,
            "pattern_tags": analysis.pattern_tags
        }

        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)

        print(f"\n💾 Results saved to: {args.output}")

    print("\n" + "="*60)
    print("✅ Analysis Complete!")
    print("="*60)


if __name__ == "__main__":
    main()
