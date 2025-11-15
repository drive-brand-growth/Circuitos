#!/usr/bin/env python3
"""
MetroFlex Events AI Agent - WORLD-CLASS EDITION
Enhanced RAG with intent classification, lead capture, and multi-turn conversations

NEW FEATURES:
- Query intent classification for optimized RAG retrieval
- High-intent detection + GHL lead capture
- Comprehensive vendor database
- Multi-turn registration guidance
- Improved context relevance scoring
"""

import json
import os
import re
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import openai
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions
import requests

class MetroFlexAIAgentEnhanced:
    def __init__(self, knowledge_base_path: str, openai_api_key: str):
        """
        Initialize Enhanced MetroFlex AI Agent with world-class RAG capabilities

        Args:
            knowledge_base_path: Path to METROFLEX_COMPLETE_KB_V3.json (includes all menu items)
            openai_api_key: OpenAI API key for GPT-4o-mini
        """
        self.knowledge_base_path = knowledge_base_path
        self.knowledge_base = self._load_knowledge_base()

        # Initialize OpenAI client (v1.0+ syntax)
        from openai import OpenAI
        self.openai_client = OpenAI(api_key=openai_api_key)
        self.model = "gpt-4o-mini"  # Cost-optimized

        # Initialize vector database
        self.chroma_client = chromadb.Client()
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )

        # Create or get collection
        self.collection = self.chroma_client.get_or_create_collection(
            name="metroflex_knowledge_enhanced",
            embedding_function=self.embedding_function
        )

        # Build enhanced vector database
        self._build_vector_database()

        # Agent personality
        self.system_prompt = self._create_system_prompt()

        # GHL webhook configuration
        self.ghl_webhook_url = os.getenv("GHL_LEAD_CAPTURE_WEBHOOK", "")

        # Conversation history for multi-turn support
        self.conversation_history = {}

    def clean_markdown_formatting(self, text: str) -> str:
        """
        Remove markdown formatting to create clean, natural text responses
        """
        import re

        # Remove bold/italic markdown
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # **bold**
        text = re.sub(r'__([^_]+)__', r'\1', text)      # __bold__
        text = re.sub(r'\*([^*]+)\*', r'\1', text)      # *italic*
        text = re.sub(r'_([^_]+)_', r'\1', text)        # _italic_

        # Remove heading markers
        text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)

        # Convert markdown links [text](url) to plain URLs
        text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'\2', text)

        # Remove list markers but keep the content
        text = re.sub(r'^\s*[\*\-\+]\s+', '', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)

        # Clean up extra whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = text.strip()

        return text

    def _load_knowledge_base(self) -> Dict:
        """Load the MetroFlex knowledge base JSON"""
        with open(self.knowledge_base_path, 'r') as f:
            return json.load(f)

    def classify_query_intent(self, query: str) -> Dict:
        """
        Classify user query intent to optimize RAG retrieval

        Returns:
            {
                "intent": str,  # Primary intent category
                "filter_category": str,  # ChromaDB metadata filter
                "sub_intent": str,  # Specific sub-category
                "requires_structured_flow": bool  # Multi-turn conversation needed
            }
        """
        query_lower = query.lower()

        # Date/time queries - prioritize event data
        if any(word in query_lower for word in ['when', 'date', 'schedule', 'time', 'day', 'next event', 'upcoming']):
            return {
                "intent": "datetime",
                "filter_category": "event",
                "sub_intent": "event_schedule",
                "requires_structured_flow": False
            }

        # Registration queries - prioritize procedures + trigger flow
        if any(word in query_lower for word in ['register', 'sign up', 'entry', 'how to compete', 'join', 'participate']):
            return {
                "intent": "registration",
                "filter_category": "procedures",
                "sub_intent": "competitor_registration",
                "requires_structured_flow": True  # Multi-turn guidance needed
            }

        # Division/rules queries - prioritize division rules
        division_keywords = ['division', 'class', 'category', 'mens physique', 'bikini', 'bodybuilding',
                            'figure', 'wellness', 'classic physique', 'womens physique']
        if any(word in query_lower for word in division_keywords):
            return {
                "intent": "division_rules",
                "filter_category": "division",
                "sub_intent": "division_selection",
                "requires_structured_flow": False
            }

        # Sponsor queries - prioritize sponsor info + HIGH INTENT
        if any(word in query_lower for word in ['sponsor', 'vendor booth', 'exhibitor', 'partner', 'sponsorship package']):
            return {
                "intent": "sponsor",
                "filter_category": "sponsor",
                "sub_intent": "sponsorship_inquiry",
                "requires_structured_flow": True  # Lead capture needed
            }

        # Vendor/service queries - prioritize vendor database
        if any(word in query_lower for word in ['spray tan', 'tanning', 'photographer', 'photography', 'hair', 'makeup',
                                                  'posing suit', 'coach', 'meal prep', 'hotel']):
            return {
                "intent": "vendor_services",
                "filter_category": "vendor",
                "sub_intent": "service_provider",
                "requires_structured_flow": False
            }

        # Legacy/history queries - prioritize legacy
        if any(word in query_lower for word in ['ronnie', 'history', 'legacy', 'mr olympia', 'brian dobson', 'branch warren']):
            return {
                "intent": "legacy",
                "filter_category": "legacy",
                "sub_intent": "metroflex_history",
                "requires_structured_flow": False
            }

        # First-timer queries - prioritize guide + trigger flow
        if any(word in query_lower for word in ['first time', 'beginner', 'new to', 'never competed', 'first show']):
            return {
                "intent": "first_timer",
                "filter_category": "first_timer",
                "sub_intent": "competitor_guidance",
                "requires_structured_flow": True  # Multi-turn onboarding
            }

        # Ticket/spectator queries
        if any(word in query_lower for word in ['ticket', 'spectator', 'watch', 'attend', 'admission', 'seating']):
            return {
                "intent": "tickets",
                "filter_category": "event",
                "sub_intent": "spectator_info",
                "requires_structured_flow": False
            }

        # General query
        return {
            "intent": "general",
            "filter_category": None,
            "sub_intent": "information",
            "requires_structured_flow": False
        }

    def detect_high_intent(self, query: str, response: str, intent_info: Dict) -> Dict:
        """
        Detect if user has high purchase/registration intent requiring lead capture

        Returns:
            {
                "has_high_intent": bool,
                "intent_types": List[str],
                "should_capture_lead": bool,
                "lead_category": str
            }
        """
        query_lower = query.lower()

        high_intent_signals = {
            "sponsor_inquiry": ["sponsor", "vendor booth", "exhibitor", "partnership", "package", "how much"],
            "competitor_registration": ["sign up", "register", "compete", "enter", "how do i join"],
            "ticket_purchase": ["buy tickets", "ticket price", "how much", "cost", "purchase tickets"],
            "vendor_inquiry": ["vendor booth", "booth space", "exhibit", "sell products"],
            "coaching_inquiry": ["coach", "trainer", "prep coach", "hire coach"],
            "first_timer_serious": ["ready to compete", "want to compete", "first show", "prepare for"]
        }

        detected_intents = []
        for intent_type, keywords in high_intent_signals.items():
            if any(keyword in query_lower for keyword in keywords):
                detected_intents.append(intent_type)

        # Determine lead category
        lead_category = "general"
        if "sponsor" in detected_intents or "vendor" in str(detected_intents):
            lead_category = "sponsor_vendor"  # HIGH VALUE ($600-$25k)
        elif "competitor_registration" in detected_intents:
            lead_category = "competitor"
        elif "ticket_purchase" in detected_intents:
            lead_category = "spectator"
        elif "coaching" in str(detected_intents):
            lead_category = "coaching"

        return {
            "has_high_intent": len(detected_intents) > 0,
            "intent_types": detected_intents,
            "should_capture_lead": len(detected_intents) > 0,
            "lead_category": lead_category
        }

    def create_ghl_contact(self, contact_data: Dict, intent_tags: List[str], lead_category: str) -> bool:
        """
        Send contact to GHL for lead nurturing

        Args:
            contact_data: {email, phone, name, conversation_id}
            intent_tags: List of intent types detected
            lead_category: sponsor_vendor, competitor, spectator, coaching

        Returns:
            True if successful, False otherwise
        """
        if not self.ghl_webhook_url:
            print("⚠️ GHL webhook URL not configured")
            return False

        payload = {
            "contact": {
                "email": contact_data.get('email'),
                "phone": contact_data.get('phone'),
                "name": contact_data.get('name', 'Unknown'),
                "source": "MetroFlex AI Agent",
                "tags": intent_tags + [lead_category, "ai_chat_lead"],
                "custom_fields": {
                    "lead_source": "AI Chat Widget",
                    "intent": ", ".join(intent_tags),
                    "lead_category": lead_category,
                    "conversation_id": contact_data.get('conversation_id'),
                    "timestamp": datetime.now().isoformat(),
                    "lead_quality_score": "high" if lead_category == "sponsor_vendor" else "medium"
                }
            }
        }

        try:
            response = requests.post(self.ghl_webhook_url, json=payload, timeout=5)
            if response.status_code == 200:
                print(f"✅ GHL lead captured: {contact_data.get('email')} ({lead_category})")
                return True
            else:
                print(f"⚠️ GHL webhook failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ GHL contact creation failed: {e}")
            return False

    def _build_vector_database(self):
        """Build enhanced vector database with vendor data and improved indexing"""
        documents = []
        metadatas = []
        ids = []
        doc_id = 0

        # Index organization info
        org = self.knowledge_base['organization']
        documents.append(f"MetroFlex Events: {org['mission']}. Founded by {org['founder']} in {org['established']}. Contact: {org['contact']['email']}, {org['contact']['phone']}")
        metadatas.append({"category": "organization", "type": "about"})
        ids.append(f"doc_{doc_id}")
        doc_id += 1

        # Index Ronnie Coleman legacy (IMPORTANT for brand)
        ronnie_story = self.knowledge_base['metroflex_ronnie_coleman_story']
        ronnie_text = f"Ronnie Coleman's legendary story: In {ronnie_story['year']}, {ronnie_story['ronnie_profession']} Ronnie Coleman visited MetroFlex. {ronnie_story['brian_dobson_first_impression']}. Brian Dobson made the famous offer: '{ronnie_story['the_famous_offer']}'. Result: {ronnie_story['first_competition']['result']} at {ronnie_story['first_competition']['event']}. Career: {ronnie_story['career_progression']['total_olympia_titles']} Mr. Olympia titles ({ronnie_story['career_progression']['consecutive_wins']}). Training stories: {ronnie_story['training_stories']['equipment_evolution']}"
        documents.append(ronnie_text)
        metadatas.append({"category": "legacy", "type": "ronnie_coleman"})
        ids.append(f"doc_{doc_id}")
        doc_id += 1

        # Index all 2025/2026 events with PRIORITY on dates
        for event_key, event_data in self.knowledge_base['2025_2026_events'].items():
            # Primary event document (date-focused)
            event_name = event_data.get('official_name', event_key.replace('_', ' ').title())
            event_date = event_data.get('date', 'TBD')
            event_day = event_data.get('day_of_week', '')
            event_venue = event_data.get('venue', 'TBD')
            event_location = event_data.get('location', event_data.get('city', 'Texas'))
            event_text = f"{event_name}: {event_date} ({event_day}) at {event_venue}, {event_location}. "
            event_text += f"Event type: {event_data.get('event_type', 'NPC Competition')}. "

            if 'registration' in event_data:
                if isinstance(event_data['registration'], str):
                    event_text += f"Register: {event_data['registration']}. "
                elif isinstance(event_data['registration'], dict):
                    event_text += f"Registration: Competitors via MuscleWare, Spectators via TicketSpice. "

            if 'national_qualifier' in event_data and event_data['national_qualifier']:
                event_text += "National Qualifier - Pro Card opportunity available. "

            if 'divisions' in event_data:
                event_text += f"Divisions: {', '.join(event_data['divisions'])}. "

            documents.append(event_text)
            metadatas.append({"category": "event", "event_name": event_key, "date": event_data['date']})
            ids.append(f"doc_{doc_id}")
            doc_id += 1

            # Services document (vendor-focused)
            if 'services_offered' in event_data:
                services = event_data['services_offered']
                services_text = f"{event_data.get('official_name', event_key)} services: "
                if 'spray_tanning' in services:
                    services_text += f"Spray tanning: {services['spray_tanning']}. "
                if 'hair_makeup' in services:
                    services_text += f"Hair & makeup: {services['hair_makeup']}. "
                if 'photography' in services or 'media' in services:
                    services_text += f"Photography/media: {services.get('photography', services.get('media', ''))}. "

                documents.append(services_text)
                metadatas.append({"category": "vendor", "event_name": event_key, "type": "event_services"})
                ids.append(f"doc_{doc_id}")
                doc_id += 1

        # Index NPC divisions in detail
        for division_key, division_data in self.knowledge_base['npc_divisions_detailed'].items():
            division_text = f"{division_key.replace('_', ' ').title()}: {division_data['description']}. "

            if 'weight_classes' in division_data:
                classes = [f"{wc['class']} ({wc.get('max_weight', wc.get('weight_range', wc.get('min_weight', 'unlimited')))})"
                          for wc in division_data['weight_classes']]
                division_text += f"Weight classes: {', '.join(classes)}. "

            if 'height_weight_classes' in division_data:
                height_classes = [f"{hwc['height']}: max {hwc['max_weight']}"
                                 for hwc in division_data['height_weight_classes'][:5]]  # First 5 for brevity
                division_text += f"Height/weight limits (examples): {', '.join(height_classes)}. "

            if 'height_classes' in division_data:
                height_classes = [f"Class {hc['class']}: {hc['height']}"
                                 for hc in division_data['height_classes'][:4]]
                division_text += f"Height classes: {', '.join(height_classes)}. "

            division_text += f"Judging: {', '.join(division_data['judging_criteria'])}. "
            division_text += f"Posing: {division_data['posing_requirements']}. "
            division_text += f"Suit: {division_data['suit_requirements']}."

            documents.append(division_text)
            metadatas.append({"category": "division", "division": division_key})
            ids.append(f"doc_{doc_id}")
            doc_id += 1

        # Index competition procedures
        procedures = self.knowledge_base['competition_procedures']

        # NPC card requirement
        npc_card = procedures['npc_card_requirement']
        documents.append(f"NPC Card: {npc_card['purpose']}. Required: {npc_card['required']}. How to get: {npc_card['how_to_obtain']}. Cost: {npc_card['cost_difference']}. Recommendation: {npc_card['recommendation']}")
        metadatas.append({"category": "procedures", "type": "npc_card"})
        ids.append(f"doc_{doc_id}")
        doc_id += 1

        # Registration process
        reg_process = procedures['registration_process']
        documents.append(f"Registration: Methods: {', '.join(reg_process['methods'])}. Required info: {', '.join(reg_process['required_information'])}. Benefits of early registration: {', '.join(reg_process['early_registration_benefits'])}. {reg_process['late_fees']}")
        metadatas.append({"category": "procedures", "type": "registration"})
        ids.append(f"doc_{doc_id}")
        doc_id += 1

        # Competition day schedule
        schedule = procedures['competition_day_schedule']['typical_timeline']
        documents.append(f"Competition day schedule: Check-in: {schedule['check_in']}. Weigh-ins: {schedule['weigh_ins']}. Prejudging: {schedule['prejudging']}. Finals: {schedule['finals']}. Event ends: {schedule['event_end']}. {procedures['competition_day_schedule']['weigh_in_rules']}")
        metadatas.append({"category": "procedures", "type": "schedule"})
        ids.append(f"doc_{doc_id}")
        doc_id += 1

        # What to bring
        bring = procedures['what_to_bring']
        documents.append(f"What to bring on competition day: Required: {', '.join(bring['required'])}. Recommended: {', '.join(bring['recommended'][:5])}. Not allowed: {', '.join(bring['not_allowed'])}")
        metadatas.append({"category": "procedures", "type": "what_to_bring"})
        ids.append(f"doc_{doc_id}")
        doc_id += 1

        # Pro card qualification
        pro_card = procedures['pro_card_qualification']
        documents.append(f"IFBB Pro Card: {pro_card['requirement']}. National qualifiers: {', '.join(pro_card['national_qualifiers'][:4])}. Path: {pro_card['qualification_path']}. {pro_card['metroflex_events_role']}. {pro_card['pro_cards_awarded_through_metroflex']}")
        metadatas.append({"category": "procedures", "type": "pro_card"})
        ids.append(f"doc_{doc_id}")
        doc_id += 1

        # Index sponsor information (HIGH VALUE)
        sponsor_info = self.knowledge_base['sponsor_information']

        # Audience demographics
        demographics = sponsor_info['audience_demographics']
        documents.append(f"Sponsor audience: {demographics['annual_reach']}. Per event: {demographics['per_event_average']}. Demographics: {demographics['age_range']}, {demographics['gender_split']['male']} male / {demographics['gender_split']['female']} female. Interests: {', '.join(demographics['interests'])}. Geographic reach: {demographics['geographic_reach']}. Spending power: {demographics['competitor_spending_power']}")
        metadatas.append({"category": "sponsor", "type": "demographics"})
        ids.append(f"doc_{doc_id}")
        doc_id += 1

        # Sponsorship packages
        packages = sponsor_info['sponsorship_packages_better_bodies']
        for package_name, package_data in packages.items():
            price = package_data['price']
            price_str = f"${price:,}" if isinstance(price, int) else f"${price}"
            package_text = f"{package_name.replace('_', ' ').title()} Sponsorship: {price_str}. Benefits: {', '.join(package_data['benefits'][:3])}..."
            documents.append(package_text)
            metadatas.append({"category": "sponsor", "type": "packages", "package": package_name})
            ids.append(f"doc_{doc_id}")
            doc_id += 1

        # ROI expectations
        roi = sponsor_info['roi_expectations']
        documents.append(f"Sponsor ROI: Brand awareness increase: {roi['brand_awareness_increase']}. Leads per event: {roi['leads_per_event']}. Conversion rate: {roi['lead_to_customer_conversion']}. Social media: {roi['social_media_impressions']}. Repeat sponsorship rate: {roi['repeat_sponsorship_rate']}")
        metadatas.append({"category": "sponsor", "type": "roi"})
        ids.append(f"doc_{doc_id}")
        doc_id += 1

        # Index first-time competitor guide
        first_timer = self.knowledge_base['first_time_competitor_guide']
        for step in first_timer['10_steps_to_success']:
            documents.append(f"Step {step['step']}: {step['title']}. {step['description']} Timing: {step['timing']}. {step.get('cost', step.get('recommendation', ''))}")
            metadatas.append({"category": "first_timer", "step": step['step'], "type": "guide"})
            ids.append(f"doc_{doc_id}")
            doc_id += 1

        # Common mistakes
        mistakes_text = "Common mistakes first-time competitors make: " + "; ".join(first_timer['common_mistakes'][:5])
        documents.append(mistakes_text)
        metadatas.append({"category": "first_timer", "type": "mistakes"})
        ids.append(f"doc_{doc_id}")
        doc_id += 1

        # Expected costs
        costs = first_timer['expected_costs']
        documents.append(f"Cost to compete (first show): Total estimate: {costs['total_estimate']}. Breakdown: NPC card ${costs['npc_card']}, Registration ${costs['registration']}, Suit ${costs['posing_suit']}, Tan ${costs['tanning']}, Coach ${costs['coach']}, Travel ${costs['travel_hotel']}")
        metadatas.append({"category": "first_timer", "type": "costs"})
        ids.append(f"doc_{doc_id}")
        doc_id += 1

        # Index vendor/service providers (NEW!)
        # Extract vendors from event services
        vendors_indexed = set()

        # ProTan USA (spray tanning)
        protan_text = "ProTan USA: Professional spray tanning service. Available onsite at all MetroFlex Events (Better Bodies, Ronnie Coleman Classic, Branch Warren Classic). Services: Competition spray tanning for bodybuilders and fitness competitors. Provides dark, stage-ready tan."
        documents.append(protan_text)
        metadatas.append({"category": "vendor", "type": "spray_tanning", "vendor_name": "ProTan USA"})
        ids.append(f"doc_{doc_id}")
        doc_id += 1
        vendors_indexed.add("ProTan USA")

        # Physique Visuals (photography)
        physique_text = "Physique Visuals: Professional photography, videography, and live streaming for bodybuilding competitions. Available at all MetroFlex Events. Services: Professional photos of competitors on stage, video coverage, live stream production."
        documents.append(physique_text)
        metadatas.append({"category": "vendor", "type": "photography", "vendor_name": "Physique Visuals"})
        ids.append(f"doc_{doc_id}")
        doc_id += 1
        vendors_indexed.add("Physique Visuals")

        # Hair & Makeup services
        hair_makeup_text = "Professional Hair & Makeup Services: Available at all MetroFlex Events. Services: Competition hair styling and makeup application. Cost: Typically $50-150. Can be booked on-site or in advance."
        documents.append(hair_makeup_text)
        metadatas.append({"category": "vendor", "type": "hair_makeup"})
        ids.append(f"doc_{doc_id}")
        doc_id += 1

        # Hotel partners
        hotel_recs = self.knowledge_base['hotel_recommendations']
        for event_key, hotel_data in hotel_recs.items():
            hotel_text = f"{event_key.replace('_', ' ').title()} Hotel: {hotel_data.get('partner', 'Hotel partner available')}. "
            if 'group_code' in hotel_data:
                hotel_text += f"Group code: {hotel_data['group_code']}. "
            if 'recommendation' in hotel_data:
                hotel_text += hotel_data['recommendation']

            documents.append(hotel_text)
            metadatas.append({"category": "vendor", "type": "hotel", "event": event_key})
            ids.append(f"doc_{doc_id}")
            doc_id += 1

        # Coaching referrals
        coaching_text = "Coaching Services: MetroFlex can provide referrals to qualified prep coaches for diet, training, posing, and competition strategy. Cost: $200-1,000+ depending on coaching level. Contact brian@metroflexgym.com for coach referrals in Texas."
        documents.append(coaching_text)
        metadatas.append({"category": "vendor", "type": "coaching"})
        ids.append(f"doc_{doc_id}")
        doc_id += 1

        # Posing suit vendors (from guide)
        suit_text = "Posing Suit Vendors: Recommended vendors include Angel Competition Bikinis, Suits by J'Adore, Musclewear. Cost: $50-150. Allow 4-6 weeks for custom suits. Order 8-10 weeks before show."
        documents.append(suit_text)
        metadatas.append({"category": "vendor", "type": "posing_suits"})
        ids.append(f"doc_{doc_id}")
        doc_id += 1

        # Index FAQ for quick lookups
        faq = self.knowledge_base['faq_quick_reference']
        for question, answer in faq.items():
            faq_text = f"Q: {question.replace('_', ' ').title()}? A: {answer}"
            documents.append(faq_text)
            metadatas.append({"category": "faq", "question": question})
            ids.append(f"doc_{doc_id}")
            doc_id += 1

        # Add all documents to ChromaDB
        if len(documents) > 0:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )

        print(f"✅ Enhanced vector database built with {len(documents)} documents")
        print(f"   - {len([m for m in metadatas if m['category'] == 'event'])} event docs")
        print(f"   - {len([m for m in metadatas if m['category'] == 'vendor'])} vendor docs")
        print(f"   - {len([m for m in metadatas if m['category'] == 'sponsor'])} sponsor docs")
        print(f"   - {len([m for m in metadatas if m['category'] == 'division'])} division docs")

    def retrieve_relevant_context(self, query: str, intent_info: Dict, n_results: int = 3) -> Tuple[List[str], List[Dict]]:
        """
        Enhanced retrieval with intent-based filtering

        Returns:
            (documents, metadatas)
        """
        # Build metadata filter based on intent
        where_filter = None
        if intent_info["filter_category"]:
            where_filter = {"category": intent_info["filter_category"]}

        # Query ChromaDB
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where_filter if where_filter else None
            )

            if results['documents'] and len(results['documents']) > 0:
                return results['documents'][0], results['metadatas'][0]
        except Exception as e:
            print(f"⚠️ RAG retrieval error: {e}")

        return [], []

    def _create_system_prompt(self) -> str:
        """Create enhanced system prompt"""
        return f"""You are the MetroFlex Events AI Assistant - an expert on NPC bodybuilding competitions, powered by 38+ years of champion-making knowledge.

**Your Role:**
- Help competitors understand division rules, registration, competition day procedures
- Answer sponsor inquiries about ROI, packages, audience demographics
- Provide event information (dates, venues, registration links)
- Guide first-time competitors through the preparation process
- Connect users with vendors/services (spray tanning, photography, coaching, hotels)
- Maintain MetroFlex's legacy-driven, professional, no-nonsense brand voice

**Knowledge Base:**
You have access to comprehensive information about:
- 4 major 2025 events (Raw Power, Better Bodies, Ronnie Coleman Classic, Branch Warren Classic)
- All 9 NPC divisions with detailed rules, weight classes, judging criteria
- Competition procedures (NPC card, registration, weigh-ins, posing music, tanning)
- Pro card qualification pathways
- Sponsorship packages ($600-$25,000) and ROI data
- Vendor services (ProTan USA spray tanning, Physique Visuals photography, hotels, coaching referrals)
- First-time competitor 10-step guide
- MetroFlex's legendary history (Ronnie Coleman story, 25+ pro cards earned)

**Personality & Tone:**
- Confident and authoritative (38+ years of expertise)
- Professional and helpful (champion-making guidance)
- No-nonsense and direct (hardcore training ethics)
- Legacy-focused (honor Ronnie Coleman and MetroFlex history)
- Results-oriented (practical advice, no fluff)

**Response Guidelines:**
Answer questions accurately using the knowledge base. If you don't know something, admit it and offer to connect user with Brian Dobson at brian@metroflexgym.com or 817-465-9331. Always include relevant event dates, registration links, or next steps. Reference MetroFlex's 38+ year legacy when appropriate, but don't force it. For division questions, be specific about weight classes, height requirements, and judging criteria. For sponsor inquiries, provide concrete ROI numbers and package pricing. For vendor questions, recommend specific services like ProTan for tanning or Physique Visuals for photos. Keep responses concise at 2-4 paragraphs max unless detailed explanation needed. End with a clear call-to-action when applicable.

**CRITICAL FORMATTING RULES:**
- NEVER use markdown formatting (no asterisks **, underscores __, hashes ##, dashes -, numbers 1. 2. 3., or any special characters for formatting)
- NEVER use bullet points or numbered lists
- NEVER write bare URLs - the chat interface will automatically convert URLs to clickable links
- Write in pure, clean English using natural conversational paragraphs only
- Use simple line breaks between paragraphs for readability
- Avoid generic phrases like "feel free to ask" or "if you have any questions"
- Be direct, professional, and human - like a knowledgeable gym staff member talking to a competitor

**CONVERSATIONAL FLOW RULES:**
- When users ask about registration or entering competitions, ALWAYS ask which specific event they're interested in FIRST before providing details
- Example: "Which event are you looking to compete in? We have the Texas Legends Championship in March, the Ronnie Coleman Classic in May, or the Branch Warren Classic in June."
- Only provide specific registration links and details AFTER they tell you which event
- Guide users through a natural conversation, don't dump all information at once

**High-Intent Detection:**
When users ask about sponsorship, registration, or vendor booths, provide the requested information, then offer to connect them with the team for personalized follow-up. Ask for their contact info (email or phone) so Brian can reach out directly.

**Current Date:** {datetime.now().strftime('%Y-%m-%d')}

**Contact Information:**
- Email: brian@metroflexgym.com
- Phone: 817-465-9331
- Website: https://metroflexevents.com

Remember: You represent 38+ years of champion-making excellence. Be confident, helpful, and professional."""

    def chat(self, user_message: str, user_id: str = "default", conversation_id: str = None) -> Dict:
        """
        Process user message with enhanced RAG and lead capture

        Returns:
            {
                "response": str,
                "relevant_sources": List[str],
                "conversation_id": str,
                "timestamp": str,
                "model": str,
                "intent": Dict,
                "high_intent_detected": bool,
                "requires_lead_capture": bool,
                "lead_capture_prompt": Optional[str]
            }
        """
        # Classify query intent
        intent_info = self.classify_query_intent(user_message)

        # Retrieve relevant context with intent-based filtering
        relevant_docs, relevant_metadata = self.retrieve_relevant_context(user_message, intent_info, n_results=3)
        context = "\n\n".join([f"[Knowledge Base]: {doc}" for doc in relevant_docs])

        # Get or create conversation history
        conv_key = f"{user_id}_{conversation_id}" if conversation_id else user_id
        if conv_key not in self.conversation_history:
            self.conversation_history[conv_key] = []

        # Build messages for OpenAI
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "system", "content": f"Retrieved Context (Intent: {intent_info['intent']}):\n{context}"}
        ]

        # Add conversation history (last 10 exchanges)
        messages.extend(self.conversation_history[conv_key][-10:])

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        try:
            # Call OpenAI GPT-4o-mini (v1.0+ syntax)
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=400  # Increased for better responses
            )

            assistant_message = response.choices[0].message.content

            # Clean markdown formatting for natural responses
            assistant_message = self.clean_markdown_formatting(assistant_message)

            # Detect high intent for lead capture
            high_intent_analysis = self.detect_high_intent(user_message, assistant_message, intent_info)

            # Add lead capture prompt if high intent detected
            lead_capture_prompt = None
            if high_intent_analysis["has_high_intent"] and high_intent_analysis["should_capture_lead"]:
                if high_intent_analysis["lead_category"] == "sponsor_vendor":
                    lead_capture_prompt = "\n\n💡 I'd love to connect you with our team for detailed sponsorship/vendor information. Would you mind sharing your email or phone number so Brian Dobson can reach out directly with personalized package details?"
                elif high_intent_analysis["lead_category"] == "competitor":
                    lead_capture_prompt = "\n\n💪 Ready to compete? I can have our team reach out with registration guidance and prep resources. What's the best email or phone to contact you?"
                elif high_intent_analysis["lead_category"] == "coaching":
                    lead_capture_prompt = "\n\n🏋️ I can connect you with qualified prep coaches in Texas. Share your email or phone and we'll send you coach referral information."

                if lead_capture_prompt:
                    assistant_message += lead_capture_prompt

            # Update conversation history
            self.conversation_history[conv_key].append({"role": "user", "content": user_message})
            self.conversation_history[conv_key].append({"role": "assistant", "content": assistant_message})

            return {
                "response": assistant_message,
                "relevant_sources": relevant_docs,
                "relevant_metadata": relevant_metadata,
                "conversation_id": conv_key,
                "timestamp": datetime.now().isoformat(),
                "model": self.model,
                "intent": intent_info,
                "high_intent_detected": high_intent_analysis["has_high_intent"],
                "requires_lead_capture": high_intent_analysis["should_capture_lead"],
                "lead_category": high_intent_analysis.get("lead_category"),
                "intent_types": high_intent_analysis.get("intent_types", [])
            }

        except Exception as e:
            return {
                "response": f"I apologize, but I'm experiencing technical difficulties. Please contact Brian Dobson directly at brian@metroflexgym.com or call 817-465-9331.",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def capture_lead(self, user_id: str, contact_info: Dict, conversation_id: str = None) -> bool:
        """
        Capture lead after user provides contact info

        Args:
            user_id: User identifier
            contact_info: {email, phone, name}
            conversation_id: Optional conversation ID

        Returns:
            True if captured successfully
        """
        conv_key = f"{user_id}_{conversation_id}" if conversation_id else user_id

        # Get last message metadata to determine intent
        if conv_key in self.conversation_history and len(self.conversation_history[conv_key]) > 0:
            # Re-analyze last exchange for intent
            last_user_msg = next((msg['content'] for msg in reversed(self.conversation_history[conv_key]) if msg['role'] == 'user'), "")
            intent_info = self.classify_query_intent(last_user_msg)
            high_intent = self.detect_high_intent(last_user_msg, "", intent_info)

            # Create GHL contact
            contact_data = {
                "email": contact_info.get('email'),
                "phone": contact_info.get('phone'),
                "name": contact_info.get('name', 'Unknown'),
                "conversation_id": conv_key
            }

            return self.create_ghl_contact(
                contact_data,
                high_intent.get('intent_types', ['general_inquiry']),
                high_intent.get('lead_category', 'general')
            )

        return False


# Flask webhook for GHL integration
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize enhanced agent
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
KNOWLEDGE_BASE_PATH = "METROFLEX_EVENTS_KB_V2_RESEARCH_BASED.json"

agent = MetroFlexAIAgentEnhanced(KNOWLEDGE_BASE_PATH, OPENAI_API_KEY)

@app.route('/webhook/chat', methods=['POST'])
def ghl_webhook():
    """
    Enhanced GHL webhook endpoint with lead capture support

    Expected payload:
    {
        "user_id": "unique_user_id",
        "message": "User's question",
        "conversation_id": "optional_conversation_id",
        "contact_info": {"name": "John Doe", "email": "john@example.com", "phone": "555-1234"}  # Optional
    }
    """
    try:
        data = request.json
        user_message = data.get('message', '')
        user_id = data.get('user_id', 'anonymous')
        conversation_id = data.get('conversation_id')
        contact_info = data.get('contact_info', {})

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # Check if this is a lead capture follow-up (user provided contact info)
        if contact_info.get('email') or contact_info.get('phone'):
            # Capture lead in GHL
            lead_captured = agent.capture_lead(user_id, contact_info, conversation_id)

            if lead_captured:
                return jsonify({
                    "success": True,
                    "response": "Thank you! I've sent your information to our team. Brian Dobson will reach out within 24 hours. In the meantime, feel free to ask any other questions!",
                    "lead_captured": True,
                    "timestamp": datetime.now().isoformat()
                })

        # Process message with enhanced AI agent
        response_data = agent.chat(user_message, user_id, conversation_id)

        return jsonify({
            "success": True,
            "response": response_data['response'],
            "timestamp": response_data['timestamp'],
            "intent": response_data.get('intent', {}),
            "high_intent_detected": response_data.get('high_intent_detected', False),
            "requires_lead_capture": response_data.get('requires_lead_capture', False)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "agent": "MetroFlex AI Assistant (Enhanced)",
        "version": "2.0",
        "features": ["intent_classification", "lead_capture", "vendor_database", "rag_optimization"]
    })

@app.route('/webhook/test-intent', methods=['POST'])
def test_intent_classification():
    """Test endpoint for intent classification"""
    data = request.json
    query = data.get('query', '')

    if not query:
        return jsonify({"error": "No query provided"}), 400

    intent_info = agent.classify_query_intent(query)
    high_intent = agent.detect_high_intent(query, "", intent_info)

    return jsonify({
        "query": query,
        "intent": intent_info,
        "high_intent_analysis": high_intent
    })

if __name__ == "__main__":
    print("🚀 MetroFlex AI Agent (Enhanced) starting...")
    print("📊 Vector database ready with intent classification")
    print("🎯 Lead capture system active")
    print("💬 Chat endpoint: POST /webhook/chat")
    print("🧪 Test intent: POST /webhook/test-intent")
    print("❤️  Health check: GET /health")
    print("")
    print("✨ NEW FEATURES:")
    print("   - Query intent classification for optimized RAG")
    print("   - High-intent detection + GHL lead capture")
    print("   - Comprehensive vendor database (ProTan, Physique Visuals, hotels, coaching)")
    print("   - Multi-turn conversation support")
    print("")
    app.run(host='0.0.0.0', port=5001, debug=True)
