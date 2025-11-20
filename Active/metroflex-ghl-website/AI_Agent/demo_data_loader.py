#!/usr/bin/env python3
"""
Circuit OS Demo Data Loader
Populate the RAG system with sample data for investor demos.

Usage:
    python demo_data_loader.py --scenario [full|quick]
"""

import requests
import time
import argparse
from typing import List, Dict


class DemoDataLoader:
    """Load demo data into Circuit OS for investor presentations"""

    def __init__(self, base_url: str = "http://localhost:5001"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/rag"

    def ingest_url(self, url: str, metadata: Dict = None) -> Dict:
        """Ingest a URL into the knowledge base"""
        response = requests.post(
            f"{self.api_url}/ingest_url",
            json={"url": url, "metadata": metadata or {}}
        )
        return response.json()

    def query(self, query_text: str, agent_id: str = None) -> Dict:
        """Run a query and get results"""
        response = requests.post(
            f"{self.api_url}/query",
            json={"query": query_text, "agent_id": agent_id}
        )
        return response.json()

    def log_business_event(self, query_id: str, event_type: str, event_value: float = None):
        """Log a business event for ROI tracking"""
        response = requests.post(
            f"{self.api_url}/business_event",
            json={
                "query_id": query_id,
                "event_type": event_type,
                "event_value": event_value
            }
        )
        return response.json()

    def get_roi_dashboard(self, days: int = 30) -> Dict:
        """Get ROI dashboard metrics"""
        response = requests.get(
            f"{self.api_url}/roi_dashboard",
            params={"days": days}
        )
        return response.json()

    def load_quick_demo(self):
        """Load minimal demo data (< 1 minute)"""
        print("🚀 Loading quick demo data...\n")

        # Sample URLs (replace with your actual content)
        demo_urls = [
            {
                "url": "https://npcnewsonline.com/about-npc",
                "metadata": {"category": "about", "source": "demo"}
            },
            {
                "url": "https://npcnewsonline.com/2026-classic-rules",
                "metadata": {"category": "events", "source": "demo"}
            }
        ]

        print("📥 Ingesting sample documents...")
        for item in demo_urls:
            try:
                result = self.ingest_url(item["url"], item["metadata"])
                if result.get('success'):
                    print(f"  ✅ {item['url'][:60]}... ({result.get('chunks_created')} chunks)")
                else:
                    print(f"  ⚠️  {item['url'][:60]}... (FAILED: {result.get('error')})")
            except Exception as e:
                print(f"  ❌ {item['url'][:60]}... (ERROR: {e})")
            time.sleep(0.5)

        print("\n🔍 Running sample queries...")
        demo_queries = [
            {"query": "What is NPC?", "agent_id": "demo_agent", "high_intent": False},
            {"query": "I want to open a gym franchise, what are the requirements?",
             "agent_id": "licensing_agent", "high_intent": True, "value": 50000},
            {"query": "What are the 2026 Better Bodies Classic rules?",
             "agent_id": "events_agent", "high_intent": False}
        ]

        for item in demo_queries:
            try:
                result = self.query(item["query"], item.get("agent_id"))
                if result.get('count', 0) > 0:
                    print(f"  ✅ '{item['query'][:50]}...' → {result['count']} results")

                    # Log business event if high intent
                    if item.get('high_intent') and result.get('query_id'):
                        self.log_business_event(
                            result['query_id'],
                            'high_intent_detected'
                        )
                        print(f"     💰 Logged as high-intent query")

                        # Simulate conversion for demo
                        if item.get('value'):
                            time.sleep(0.2)
                            self.log_business_event(
                                result['query_id'],
                                'deal_closed',
                                item['value']
                            )
                            print(f"     💵 Simulated ${item['value']:,.0f} deal")

                else:
                    print(f"  ⚠️  '{item['query'][:50]}...' → No results")
            except Exception as e:
                print(f"  ❌ '{item['query'][:50]}...' (ERROR: {e})")
            time.sleep(0.5)

        print("\n📊 Generating ROI dashboard...")
        try:
            dashboard = self.get_roi_dashboard(days=30)
            if dashboard.get('success'):
                print("\n" + "="*60)
                print("INVESTOR-READY METRICS")
                print("="*60)

                qv = dashboard.get('query_volume', {})
                print(f"Query Volume: {qv.get('total')} total")
                print(f"  Cache Hit Rate: {qv.get('cache_hit_rate_pct')}%")
                print(f"  High-Intent Rate: {qv.get('high_intent_rate_pct')}%")
                print(f"  Conversion Rate: {qv.get('conversion_rate_pct')}%")

                perf = dashboard.get('performance', {})
                print(f"\nPerformance:")
                print(f"  Avg Query Time: {perf.get('avg_query_time_ms')}ms")
                print(f"  Avg Cached Time: {perf.get('avg_cached_time_ms')}ms")
                print(f"  Time Savings: {perf.get('time_savings_hours')}hrs")

                revenue = dashboard.get('revenue_attribution', {})
                print(f"\nRevenue Attribution:")
                print(f"  Total Revenue: ${revenue.get('total_revenue_usd'):,.2f}")
                print(f"  Avg Deal Size: ${revenue.get('average_deal_size_usd'):,.2f}")
                print(f"  ROI Multiple: {revenue.get('roi_multiple')}x")

                claims = dashboard.get('investor_claims_validation', {})
                print(f"\nClaims Validation:")
                print(f"  Cache Hit Rate: {claims.get('actual_cache_hit_rate')} " +
                      f"(target: {claims.get('claim_cache_hit_rate_target')})")
                print(f"  Time Savings: {claims.get('actual_time_savings')} " +
                      f"(target: {claims.get('claim_time_savings_target')})")
                print(f"  Cost Reduction: {claims.get('actual_cost_reduction')} " +
                      f"(target: {claims.get('claim_cost_reduction_target')})")
                print("="*60)
            else:
                print(f"  ⚠️  Dashboard generation failed: {dashboard.get('error')}")
        except Exception as e:
            print(f"  ❌ Dashboard error: {e}")

        print("\n✅ Quick demo data loaded successfully!")
        print(f"\n🌐 Access the system at: {self.base_url}")
        print(f"📊 ROI Dashboard: {self.api_url}/roi_dashboard")
        print(f"🔍 Query Explainability: {self.api_url}/explain/<query_id>\n")

    def load_full_demo(self):
        """Load comprehensive demo data (5-10 minutes)"""
        print("🚀 Loading full demo dataset (this may take 5-10 minutes)...\n")
        print("⚠️  Full demo requires more URLs. For now, running quick demo.\n")
        self.load_quick_demo()

    def health_check(self) -> bool:
        """Check if the RAG system is running"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False


def main():
    parser = argparse.ArgumentParser(description="Load demo data for Circuit OS investor demos")
    parser.add_argument(
        '--scenario',
        choices=['quick', 'full'],
        default='quick',
        help='Demo scenario to load (default: quick)'
    )
    parser.add_argument(
        '--base-url',
        default='http://localhost:5001',
        help='Base URL for Circuit OS API (default: http://localhost:5001)'
    )

    args = parser.parse_args()

    loader = DemoDataLoader(base_url=args.base_url)

    # Health check
    print("🔍 Checking Circuit OS health...")
    if not loader.health_check():
        print(f"❌ Circuit OS is not running at {args.base_url}")
        print("\nStart the system first:")
        print("  docker compose up -d")
        print("  # or")
        print("  python unified_api_server.py")
        return 1

    print(f"✅ Circuit OS is running at {args.base_url}\n")

    # Load data
    if args.scenario == 'quick':
        loader.load_quick_demo()
    else:
        loader.load_full_demo()

    return 0


if __name__ == '__main__':
    exit(main())
