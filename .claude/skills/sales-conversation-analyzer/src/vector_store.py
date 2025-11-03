"""
Vector Store - Manages vector database for conversation patterns
"""

from typing import List, Dict, Any, Optional
import json
import os
from pathlib import Path


class VectorStore:
    """
    Manages vector database for storing and retrieving conversation patterns
    Uses ChromaDB for vector storage and semantic search
    """

    def __init__(self, db_path: str = "./data/vector_db"):
        """
        Initialize vector store

        Args:
            db_path: Path to the database directory
        """
        self.db_path = db_path
        self.collection_name = "sales_conversation_patterns"

        # Create directory if it doesn't exist
        Path(db_path).mkdir(parents=True, exist_ok=True)

        # Initialize ChromaDB (or fallback to JSON if ChromaDB not available)
        try:
            import chromadb
            self.use_chromadb = True
            self.client = chromadb.PersistentClient(path=db_path)
            self.collection = self._get_or_create_collection()
        except ImportError:
            print("ChromaDB not available. Using JSON fallback storage.")
            self.use_chromadb = False
            self.json_db_path = os.path.join(db_path, "conversations.json")
            self._init_json_db()

    def _get_or_create_collection(self):
        """Get or create ChromaDB collection"""
        try:
            return self.client.get_collection(name=self.collection_name)
        except:
            return self.client.create_collection(
                name=self.collection_name,
                metadata={
                    "description": "Sales conversation patterns for positive outcomes",
                    "embedding_function": "openai"
                }
            )

    def _init_json_db(self):
        """Initialize JSON database fallback"""
        if not os.path.exists(self.json_db_path):
            with open(self.json_db_path, 'w') as f:
                json.dump({"conversations": []}, f)

    def add_conversation(self, analysis) -> bool:
        """
        Add a conversation analysis to the vector database

        Args:
            analysis: ConversationAnalysis object

        Returns:
            True if successful, False otherwise
        """
        try:
            if self.use_chromadb:
                return self._add_to_chromadb(analysis)
            else:
                return self._add_to_json(analysis)
        except Exception as e:
            print(f"Error adding conversation to vector store: {e}")
            return False

    def _add_to_chromadb(self, analysis) -> bool:
        """Add to ChromaDB"""
        try:
            # Prepare document (text to store)
            document = self._prepare_document(analysis)

            # Prepare metadata
            metadata = {
                "conversation_id": analysis.conversation_id,
                "outcome": analysis.metadata.outcome or "unknown",
                "outcome_value": float(analysis.metadata.deal_value or 0),
                "industry": analysis.metadata.industry or "unknown",
                "buyer_persona": analysis.metadata.buyer_persona or "unknown",
                "pain_points": json.dumps(analysis.buyer_signals.get("pain_level", [])),
                "techniques_used": json.dumps([p.get("technique") for p in analysis.key_patterns]),
                "effectiveness_score": float(analysis.effectiveness_score),
                "duration_seconds": int(analysis.metadata.duration or 0),
                "agent_id": analysis.metadata.agent_id or "unknown",
                "timestamp": analysis.metadata.timestamp.isoformat()
            }

            # Add to collection
            self.collection.add(
                embeddings=[analysis.vector_embedding],
                documents=[document],
                metadatas=[metadata],
                ids=[analysis.conversation_id]
            )

            return True

        except Exception as e:
            print(f"Error adding to ChromaDB: {e}")
            return False

    def _add_to_json(self, analysis) -> bool:
        """Add to JSON fallback"""
        try:
            # Load existing data
            with open(self.json_db_path, 'r') as f:
                data = json.load(f)

            # Prepare conversation data
            conv_data = {
                "conversation_id": analysis.conversation_id,
                "outcome_classification": analysis.outcome_classification,
                "effectiveness_score": analysis.effectiveness_score,
                "key_patterns": analysis.key_patterns,
                "buyer_signals": analysis.buyer_signals,
                "pattern_tags": analysis.pattern_tags,
                "training_value": analysis.training_value,
                "metadata": {
                    "conversation_id": analysis.conversation_id,
                    "outcome": analysis.metadata.outcome,
                    "deal_value": analysis.metadata.deal_value,
                    "industry": analysis.metadata.industry,
                    "timestamp": analysis.metadata.timestamp.isoformat()
                },
                "vector_embedding": analysis.vector_embedding
            }

            # Add to conversations list
            data["conversations"].append(conv_data)

            # Save back to JSON
            with open(self.json_db_path, 'w') as f:
                json.dump(data, f, indent=2)

            return True

        except Exception as e:
            print(f"Error adding to JSON: {e}")
            return False

    def find_similar(
        self,
        embedding: List[float],
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find similar conversations

        Args:
            embedding: Query embedding vector
            filters: Metadata filters (e.g., {"outcome": "positive"})
            limit: Maximum number of results

        Returns:
            List of similar conversations
        """
        if self.use_chromadb:
            return self._query_chromadb(embedding, filters, limit)
        else:
            return self._query_json(embedding, filters, limit)

    def _query_chromadb(
        self,
        embedding: List[float],
        filters: Optional[Dict],
        limit: int
    ) -> List[Dict[str, Any]]:
        """Query ChromaDB"""
        try:
            # Build where clause
            where = None
            if filters:
                where = {}
                for key, value in filters.items():
                    if isinstance(value, list):
                        where[key] = {"$in": value}
                    else:
                        where[key] = value

            # Query collection
            results = self.collection.query(
                query_embeddings=[embedding],
                where=where,
                n_results=limit
            )

            # Format results
            formatted_results = []
            if results and results["ids"]:
                for i in range(len(results["ids"][0])):
                    formatted_results.append({
                        "conversation_id": results["ids"][0][i],
                        "document": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i],
                        "distance": results["distances"][0][i] if "distances" in results else None
                    })

            return formatted_results

        except Exception as e:
            print(f"Error querying ChromaDB: {e}")
            return []

    def _query_json(
        self,
        embedding: List[float],
        filters: Optional[Dict],
        limit: int
    ) -> List[Dict[str, Any]]:
        """Query JSON fallback using simple filtering"""
        try:
            # Load data
            with open(self.json_db_path, 'r') as f:
                data = json.load(f)

            conversations = data.get("conversations", [])

            # Apply filters
            if filters:
                filtered = []
                for conv in conversations:
                    match = True
                    for key, value in filters.items():
                        if key == "outcome":
                            if conv.get("metadata", {}).get("outcome") != value:
                                match = False
                                break
                        elif key == "effectiveness_score":
                            if isinstance(value, dict) and "$gte" in value:
                                if conv.get("effectiveness_score", 0) < value["$gte"]:
                                    match = False
                                    break
                    if match:
                        filtered.append(conv)
                conversations = filtered

            # Sort by effectiveness score (simple ranking since we don't have true vector similarity)
            conversations.sort(key=lambda x: x.get("effectiveness_score", 0), reverse=True)

            # Return top results
            return conversations[:limit]

        except Exception as e:
            print(f"Error querying JSON: {e}")
            return []

    def export_training_data(
        self,
        min_effectiveness: float = 0.8,
        outcomes: List[str] = None,
        limit: int = 1000
    ) -> List[Dict[str, Any]]:
        """
        Export training data for AI agent fine-tuning

        Args:
            min_effectiveness: Minimum effectiveness score
            outcomes: List of outcomes to include (e.g., ["booked", "closed"])
            limit: Maximum number of examples

        Returns:
            List of training examples
        """
        if outcomes is None:
            outcomes = ["booked", "closed", "demo_scheduled"]

        # Query for high-quality conversations
        if self.use_chromadb:
            # Query all conversations with filters
            try:
                results = self.collection.get(
                    where={
                        "effectiveness_score": {"$gte": min_effectiveness},
                        "outcome": {"$in": outcomes}
                    },
                    limit=limit
                )

                training_examples = []
                if results and results["ids"]:
                    for i in range(len(results["ids"])):
                        training_examples.append({
                            "instruction": "Respond to the prospect using world-class sales techniques",
                            "input": results["documents"][i],
                            "context": results["metadatas"][i],
                            "effectiveness_score": results["metadatas"][i].get("effectiveness_score")
                        })

                return training_examples

            except Exception as e:
                print(f"Error exporting from ChromaDB: {e}")
                return []

        else:
            # Export from JSON
            try:
                with open(self.json_db_path, 'r') as f:
                    data = json.load(f)

                conversations = data.get("conversations", [])

                # Filter
                filtered = [
                    conv for conv in conversations
                    if (conv.get("effectiveness_score", 0) >= min_effectiveness and
                        conv.get("metadata", {}).get("outcome") in outcomes)
                ]

                # Sort by effectiveness
                filtered.sort(key=lambda x: x.get("effectiveness_score", 0), reverse=True)

                # Convert to training format
                training_examples = []
                for conv in filtered[:limit]:
                    # Extract key patterns as training examples
                    for pattern in conv.get("key_patterns", []):
                        training_examples.append({
                            "instruction": "Respond to the prospect using world-class sales techniques",
                            "input": f"Situation: {conv.get('metadata', {}).get('industry', 'unknown')} industry",
                            "output": pattern.get("text", ""),
                            "context": {
                                "technique": pattern.get("technique"),
                                "effectiveness": pattern.get("effectiveness"),
                                "outcome": conv.get("metadata", {}).get("outcome")
                            }
                        })

                return training_examples

            except Exception as e:
                print(f"Error exporting from JSON: {e}")
                return []

    def get_world_class_patterns(
        self,
        framework: Optional[str] = None,
        min_effectiveness: float = 0.85
    ) -> List[Dict[str, Any]]:
        """
        Get world-class patterns from the database

        Args:
            framework: Filter by framework (e.g., "SPIN", "Challenger")
            min_effectiveness: Minimum effectiveness score

        Returns:
            List of world-class patterns
        """
        filters = {
            "effectiveness_score": {"$gte": min_effectiveness}
        }

        if framework:
            filters["techniques_used"] = {"$contains": framework}

        if self.use_chromadb:
            try:
                results = self.collection.get(
                    where=filters,
                    limit=100
                )

                return results.get("metadatas", [])

            except Exception as e:
                print(f"Error getting world-class patterns: {e}")
                return []

        else:
            # Get from JSON
            try:
                with open(self.json_db_path, 'r') as f:
                    data = json.load(f)

                conversations = data.get("conversations", [])

                # Filter for high effectiveness
                world_class = [
                    conv for conv in conversations
                    if conv.get("effectiveness_score", 0) >= min_effectiveness
                ]

                # Filter by framework if specified
                if framework:
                    world_class = [
                        conv for conv in world_class
                        if any(framework in p.get("technique", "") for p in conv.get("key_patterns", []))
                    ]

                return world_class

            except Exception as e:
                print(f"Error getting world-class patterns from JSON: {e}")
                return []

    def _prepare_document(self, analysis) -> str:
        """Prepare document text for storage"""
        # Combine key information into searchable text
        patterns_text = " | ".join([
            f"{p.get('technique')}: {p.get('text', '')}"
            for p in analysis.key_patterns
        ])

        buyer_signals_text = f"Intent: {analysis.buyer_signals.get('intent_score')}, Pain: {analysis.buyer_signals.get('pain_level')}"

        document = f"""
        Outcome: {analysis.outcome_classification}
        Effectiveness: {analysis.effectiveness_score}
        Patterns: {patterns_text}
        Buyer Signals: {buyer_signals_text}
        Tags: {', '.join(analysis.pattern_tags)}
        """

        return document.strip()

    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        if self.use_chromadb:
            try:
                count = self.collection.count()
                return {
                    "total_conversations": count,
                    "database_type": "chromadb",
                    "collection_name": self.collection_name
                }
            except:
                return {"error": "Could not retrieve statistics"}

        else:
            try:
                with open(self.json_db_path, 'r') as f:
                    data = json.load(f)

                conversations = data.get("conversations", [])

                return {
                    "total_conversations": len(conversations),
                    "database_type": "json",
                    "positive_outcomes": len([c for c in conversations if c.get("outcome_classification") == "positive"]),
                    "high_training_value": len([c for c in conversations if c.get("training_value") == "high"]),
                    "avg_effectiveness_score": sum(c.get("effectiveness_score", 0) for c in conversations) / len(conversations) if conversations else 0
                }

            except Exception as e:
                return {"error": str(e)}
