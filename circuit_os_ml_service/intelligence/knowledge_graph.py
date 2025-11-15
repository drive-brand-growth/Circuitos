"""
Knowledge Graph - Entity Relationship Management
Graph queries for semantic understanding beyond schema joins
"""

from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class KnowledgeGraph:
    """
    Knowledge Graph for entity relationships

    In production, this would connect to Neo4j.
    For demo, uses in-memory graph structure.
    """

    def __init__(self, neo4j_uri: str = None, neo4j_user: str = None, neo4j_password: str = None):
        self.neo4j_uri = neo4j_uri
        self.neo4j_user = neo4j_user
        self.neo4j_password = neo4j_password

        # In-memory graph for demo
        self.nodes = {}
        self.relationships = []

        # Initialize with sample data
        self._initialize_sample_graph()

    def _initialize_sample_graph(self):
        """Initialize with sample graph data"""
        # Companies
        self.add_node("Company", {
            "id": "company_1",
            "name": "TechCorp",
            "industry": "Technology",
            "market_share": 0.25,
            "revenue": 500000000
        })

        self.add_node("Company", {
            "id": "company_2",
            "name": "InnovateSoft",
            "industry": "Technology",
            "market_share": 0.18,
            "revenue": 350000000
        })

        self.add_node("Company", {
            "id": "company_3",
            "name": "DataDynamics",
            "industry": "Technology",
            "market_share": 0.15,
            "revenue": 280000000
        })

        # Relationships
        self.add_relationship("company_1", "company_2", "COMPETES_WITH", {"intensity": "high"})
        self.add_relationship("company_1", "company_3", "COMPETES_WITH", {"intensity": "medium"})
        self.add_relationship("company_2", "company_3", "COMPETES_WITH", {"intensity": "low"})

        # Products
        self.add_node("Product", {
            "id": "product_1",
            "name": "AI Platform",
            "company_id": "company_1"
        })

        self.add_relationship("company_1", "product_1", "OFFERS", {})

        logger.info("Initialized sample knowledge graph")

    def add_node(self, label: str, properties: Dict[str, Any]):
        """Add a node to the graph"""
        node_id = properties.get('id')
        if not node_id:
            raise ValueError("Node must have 'id' property")

        self.nodes[node_id] = {
            "label": label,
            "properties": properties,
            "created_at": datetime.now().isoformat()
        }

    def add_relationship(
        self,
        from_id: str,
        to_id: str,
        rel_type: str,
        properties: Dict[str, Any] = None
    ):
        """Add a relationship between nodes"""
        self.relationships.append({
            "from": from_id,
            "to": to_id,
            "type": rel_type,
            "properties": properties or {},
            "created_at": datetime.now().isoformat()
        })

    async def query(self, cypher: str, **params) -> List[Dict]:
        """
        Execute Cypher query

        In production, this would use Neo4j driver.
        For demo, implements simple pattern matching.
        """
        logger.info(f"Executing graph query: {cypher}")

        # Simple pattern matching for demo
        # In production, this would use actual Neo4j
        if "COMPETES_WITH" in cypher:
            return await self._find_competitors(params.get('company_id'))

        return []

    async def find_competitors(self, company_id: str) -> List[Dict]:
        """Find competitors for a company"""
        competitors = []

        for rel in self.relationships:
            if rel['type'] == 'COMPETES_WITH':
                if rel['from'] == company_id:
                    competitor = self.nodes.get(rel['to'])
                    if competitor:
                        competitors.append({
                            **competitor['properties'],
                            "relationship": rel['properties']
                        })
                elif rel['to'] == company_id:
                    competitor = self.nodes.get(rel['from'])
                    if competitor:
                        competitors.append({
                            **competitor['properties'],
                            "relationship": rel['properties']
                        })

        # Sort by market share
        competitors.sort(key=lambda x: x.get('market_share', 0), reverse=True)

        logger.info(f"Found {len(competitors)} competitors")
        return competitors

    async def _find_competitors(self, company_id: str) -> List[Dict]:
        """Internal method for finding competitors"""
        return await self.find_competitors(company_id)

    async def infer_relationships(
        self,
        entity_id: str,
        similarity_threshold: float = 0.85
    ) -> List[Dict]:
        """
        ML-powered relationship inference

        Uses embeddings to find similar entities and create inferred relationships
        """
        logger.info(f"Inferring relationships for {entity_id}")

        # Get entity
        entity = self.nodes.get(entity_id)
        if not entity:
            return []

        inferred = []

        # Simple similarity based on properties (in production, use embeddings)
        for node_id, node in self.nodes.items():
            if node_id == entity_id:
                continue

            # Calculate simple similarity
            similarity = self._calculate_similarity(
                entity['properties'],
                node['properties']
            )

            if similarity > similarity_threshold:
                inferred.append({
                    "entity_id": node_id,
                    "entity": node['properties'],
                    "relationship": "SIMILAR_TO",
                    "confidence": similarity
                })

        logger.info(f"Inferred {len(inferred)} relationships")
        return inferred

    def _calculate_similarity(self, props1: Dict, props2: Dict) -> float:
        """Calculate simple similarity between two nodes"""
        similarity = 0.0
        comparisons = 0

        # Industry match
        if props1.get('industry') == props2.get('industry'):
            similarity += 1.0
            comparisons += 1

        # Market share similarity
        if 'market_share' in props1 and 'market_share' in props2:
            diff = abs(props1['market_share'] - props2['market_share'])
            similarity += (1.0 - diff)
            comparisons += 1

        return similarity / comparisons if comparisons > 0 else 0.0

    async def add_entity_from_data(
        self,
        entity_type: str,
        entity_data: Dict[str, Any]
    ):
        """Add entity from external data source"""
        self.add_node(entity_type, entity_data)
        logger.info(f"Added {entity_type} entity: {entity_data.get('id')}")

    async def connect_entities(
        self,
        from_id: str,
        to_id: str,
        relationship_type: str,
        confidence: float = 1.0
    ):
        """Create relationship between entities"""
        self.add_relationship(
            from_id,
            to_id,
            relationship_type,
            {"confidence": confidence}
        )
        logger.info(f"Connected {from_id} -> {to_id} ({relationship_type})")

    def get_statistics(self) -> Dict[str, Any]:
        """Get graph statistics"""
        labels = {}
        for node in self.nodes.values():
            label = node['label']
            labels[label] = labels.get(label, 0) + 1

        relationship_types = {}
        for rel in self.relationships:
            rel_type = rel['type']
            relationship_types[rel_type] = relationship_types.get(rel_type, 0) + 1

        return {
            "total_nodes": len(self.nodes),
            "total_relationships": len(self.relationships),
            "node_labels": labels,
            "relationship_types": relationship_types
        }
