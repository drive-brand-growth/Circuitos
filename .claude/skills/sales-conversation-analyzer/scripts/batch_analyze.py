#!/usr/bin/env python3
"""
Batch Analysis - Analyze multiple conversations from CSV or database
"""

import os
import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analyzer import SalesConversationAnalyzer
from src.data_ingestion import DataIngestion


def main():
    parser = argparse.ArgumentParser(
        description="Batch analyze conversations from CSV, database, or directory"
    )
    parser.add_argument(
        "source",
        help="Path to CSV file, directory, or database connection string"
    )
    parser.add_argument(
        "--type",
        choices=["csv", "directory", "database", "auto"],
        default="auto",
        help="Source type (auto-detect if not specified)"
    )
    parser.add_argument(
        "--db-type",
        choices=["sqlite", "postgres", "mysql"],
        help="Database type (if source is database)"
    )
    parser.add_argument(
        "--query",
        help="SQL query (if source is database)"
    )
    parser.add_argument(
        "--output",
        default="batch_analysis_results.json",
        help="Output file for results"
    )
    parser.add_argument(
        "--format",
        choices=["json", "csv", "jsonl"],
        default="json",
        help="Output format"
    )
    parser.add_argument(
        "--parallel",
        type=int,
        default=1,
        help="Number of parallel workers"
    )

    args = parser.parse_args()

    # Initialize components
    print("🧠 Initializing analyzer...")
    analyzer = SalesConversationAnalyzer(
        vector_db_path="./data/vector_db"
    )

    data_ingestion = DataIngestion()

    # Ingest conversations
    print(f"📥 Ingesting conversations from {args.source}...")
    conversations = []

    try:
        if args.type == "database" or (args.type == "auto" and args.db_type):
            if not args.query:
                print("Error: --query required for database ingestion")
                return

            conversations = data_ingestion.ingest_database(
                connection_string=args.source,
                query=args.query,
                db_type=args.db_type or "sqlite"
            )

        elif args.type == "directory" or (args.type == "auto" and os.path.isdir(args.source)):
            conversations = data_ingestion.ingest_directory(
                directory_path=args.source,
                recursive=True
            )

        else:  # CSV or file
            conversations = data_ingestion.ingest_file(args.source)

    except Exception as e:
        print(f"❌ Error ingesting data: {e}")
        return

    print(f"✅ Loaded {len(conversations)} conversations")

    # Analyze conversations
    print(f"\n🔍 Analyzing {len(conversations)} conversations...")
    results = []

    for i, conv in enumerate(conversations, 1):
        try:
            print(f"  [{i}/{len(conversations)}] Analyzing {conv.get('conversation_id', 'unknown')}...")

            # Validate conversation
            is_valid, errors = data_ingestion.validate_conversation(conv)
            if not is_valid:
                print(f"    ⚠️  Skipping - validation errors: {errors}")
                continue

            # Analyze
            analysis = analyzer.analyze(
                transcript=conv['transcript'],
                metadata={
                    'conversation_id': conv.get('conversation_id'),
                    'outcome': conv.get('outcome'),
                    'industry': conv.get('industry'),
                    'deal_value': conv.get('deal_value'),
                    'duration': conv.get('duration'),
                    'contact_id': conv.get('contact_id'),
                    'agent_id': conv.get('agent_id'),
                    'buyer_persona': conv.get('buyer_persona')
                },
                use_ai=False  # Disable AI for batch processing speed
            )

            # Extract key results
            result = {
                'conversation_id': analysis.conversation_id,
                'effectiveness_score': analysis.effectiveness_score,
                'outcome_classification': analysis.outcome_classification,
                'predicted_outcome': analysis.ml_prediction.get('predicted_outcome') if analysis.ml_prediction else None,
                'prediction_confidence': analysis.ml_prediction.get('confidence') if analysis.ml_prediction else None,
                'consistency_score': analysis.ml_prediction.get('consistency_score') if analysis.ml_prediction else None,
                'buyer_intent_score': analysis.buyer_signals.get('intent_score'),
                'pain_level': analysis.buyer_signals.get('pain_level'),
                'authority': analysis.buyer_signals.get('authority'),
                'budget': analysis.buyer_signals.get('budget_qualification'),
                'timeline': analysis.buyer_signals.get('timeline'),
                'patterns_detected': len(analysis.key_patterns),
                'frameworks_used': list(analysis.framework_alignment.get('frameworks_used', [])) if analysis.framework_alignment else [],
                'training_value': analysis.training_value,
                'consistent_signals_count': len(analysis.consistent_buying_signals) if analysis.consistent_buying_signals else 0,
                'loss_preventable': analysis.loss_analysis.get('preventable') if analysis.loss_analysis else None,
                'loss_root_causes': [c['cause'] for c in analysis.loss_analysis.get('root_causes', [])[:3]] if analysis.loss_analysis else None,
                'recommendations': analysis.recommendations[:3]
            }

            results.append(result)

            print(f"    ✓ Effectiveness: {analysis.effectiveness_score:.2f} | Intent: {analysis.buyer_signals.get('intent_score')}/100")

        except Exception as e:
            print(f"    ❌ Error analyzing: {e}")

    # Save results
    print(f"\n💾 Saving results to {args.output}...")

    if args.format == "json":
        import json
        with open(args.output, 'w') as f:
            json.dump({
                'total_conversations': len(conversations),
                'successfully_analyzed': len(results),
                'results': results,
                'summary': _generate_summary(results)
            }, f, indent=2)

    elif args.format == "csv":
        import csv
        if results:
            with open(args.output, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)

    elif args.format == "jsonl":
        with open(args.output, 'w') as f:
            import json
            for result in results:
                f.write(json.dumps(result) + '\n')

    print(f"✅ Saved {len(results)} results")

    # Print summary
    print("\n" + "="*60)
    print("📊 BATCH ANALYSIS SUMMARY")
    print("="*60)
    summary = _generate_summary(results)

    print(f"\n📈 Overall Metrics:")
    print(f"  Total Analyzed: {summary['total']}")
    print(f"  Average Effectiveness: {summary['avg_effectiveness']:.2f}")
    print(f"  Average Intent Score: {summary['avg_intent']:.0f}/100")
    print(f"  Average Consistency: {summary['avg_consistency']:.2f}")

    print(f"\n🎯 Outcomes:")
    for outcome, count in summary['outcomes'].items():
        print(f"  {outcome}: {count} ({count/summary['total']*100:.0f}%)")

    print(f"\n⚠️  Issues:")
    print(f"  Preventable Losses: {summary['preventable_losses']}")
    print(f"  Low Intent (<50): {summary['low_intent']}")
    print(f"  Poor Effectiveness (<0.6): {summary['poor_effectiveness']}")

    print(f"\n💎 High Value:")
    print(f"  High Training Value: {summary['high_training_value']}")
    print(f"  World-class (>0.85): {summary['world_class']}")

    print("\n" + "="*60)
    print("✨ Batch Analysis Complete!")
    print("="*60)


def _generate_summary(results):
    """Generate summary statistics"""
    if not results:
        return {}

    from collections import Counter

    total = len(results)

    return {
        'total': total,
        'avg_effectiveness': sum(r.get('effectiveness_score', 0) for r in results) / total,
        'avg_intent': sum(r.get('buyer_intent_score', 0) for r in results) / total,
        'avg_consistency': sum(r.get('consistency_score', 0) for r in results if r.get('consistency_score')) / max(sum(1 for r in results if r.get('consistency_score')), 1),
        'outcomes': dict(Counter(r.get('outcome_classification', 'unknown') for r in results)),
        'preventable_losses': sum(1 for r in results if r.get('loss_preventable') == True),
        'low_intent': sum(1 for r in results if r.get('buyer_intent_score', 100) < 50),
        'poor_effectiveness': sum(1 for r in results if r.get('effectiveness_score', 1) < 0.6),
        'high_training_value': sum(1 for r in results if r.get('training_value') == 'high'),
        'world_class': sum(1 for r in results if r.get('effectiveness_score', 0) >= 0.85)
    }


if __name__ == "__main__":
    main()
