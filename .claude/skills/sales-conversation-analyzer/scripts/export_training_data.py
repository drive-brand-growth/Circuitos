#!/usr/bin/env python3
"""
Export training data from vector database
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.vector_store import VectorStore


def main():
    parser = argparse.ArgumentParser(
        description="Export training data for AI agent fine-tuning"
    )
    parser.add_argument(
        "--output",
        default="training_data.jsonl",
        help="Output file path (JSONL format)"
    )
    parser.add_argument(
        "--min-effectiveness",
        type=float,
        default=0.8,
        help="Minimum effectiveness score (0-1)"
    )
    parser.add_argument(
        "--outcomes",
        nargs="+",
        default=["booked", "closed", "demo_scheduled"],
        help="Outcomes to include"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=1000,
        help="Maximum number of examples"
    )
    parser.add_argument(
        "--format",
        choices=["jsonl", "csv", "json"],
        default="jsonl",
        help="Output format"
    )

    args = parser.parse_args()

    # Initialize vector store
    print("📚 Loading vector database...")
    vector_store = VectorStore("./data/vector_db")

    # Get statistics
    stats = vector_store.get_statistics()
    print(f"📊 Total conversations in database: {stats.get('total_conversations', 0)}")

    # Export training data
    print(f"\n🔍 Exporting training data...")
    print(f"   Min Effectiveness: {args.min_effectiveness}")
    print(f"   Outcomes: {', '.join(args.outcomes)}")
    print(f"   Limit: {args.limit}")

    training_data = vector_store.export_training_data(
        min_effectiveness=args.min_effectiveness,
        outcomes=args.outcomes,
        limit=args.limit
    )

    print(f"\n✅ Exported {len(training_data)} training examples")

    # Save based on format
    if args.format == "jsonl":
        with open(args.output, 'w') as f:
            for example in training_data:
                f.write(json.dumps(example) + "\n")
        print(f"💾 Saved as JSONL: {args.output}")

    elif args.format == "json":
        with open(args.output, 'w') as f:
            json.dump(training_data, f, indent=2)
        print(f"💾 Saved as JSON: {args.output}")

    elif args.format == "csv":
        import csv
        with open(args.output, 'w', newline='') as f:
            if training_data:
                writer = csv.DictWriter(f, fieldnames=training_data[0].keys())
                writer.writeheader()
                writer.writerows(training_data)
        print(f"💾 Saved as CSV: {args.output}")

    # Print sample
    if training_data:
        print(f"\n📝 Sample Training Example:")
        sample = training_data[0]
        print(json.dumps(sample, indent=2)[:500] + "...")

    print(f"\n✨ Ready for fine-tuning!")
    print(f"   Use this data to train AI agents on world-class sales patterns")


if __name__ == "__main__":
    main()
