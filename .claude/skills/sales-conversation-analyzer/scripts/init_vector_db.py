#!/usr/bin/env python3
"""
Initialize Vector Database for Sales Conversation Analyzer
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.vector_store import VectorStore


def main():
    """Initialize the vector database"""
    print("🚀 Initializing Sales Conversation Analyzer Vector Database...")

    # Create vector store
    db_path = "./data/vector_db"
    print(f"📁 Creating database at: {db_path}")

    vector_store = VectorStore(db_path)

    # Get statistics
    stats = vector_store.get_statistics()

    print("\n✅ Vector Database Initialized Successfully!")
    print(f"📊 Database Type: {stats.get('database_type', 'unknown')}")
    print(f"📚 Total Conversations: {stats.get('total_conversations', 0)}")

    if stats.get('database_type') == 'chromadb':
        print("\n✨ ChromaDB is active - full vector search available!")
    else:
        print("\n⚠️  Using JSON fallback - consider installing ChromaDB:")
        print("   pip install chromadb")

    print("\n📖 Next Steps:")
    print("   1. Load world-class patterns: python scripts/load_world_class_patterns.py")
    print("   2. Analyze conversations: python scripts/analyze_conversation.py")
    print("   3. Export training data: python scripts/export_training_data.py")

    print("\n✨ Ready to analyze sales conversations!")


if __name__ == "__main__":
    main()
