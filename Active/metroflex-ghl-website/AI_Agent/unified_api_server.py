#!/usr/bin/env python3
"""
MetroFlex Unified AI Agent API Server
Serves 3 AI agents via REST API:
1. Events Agent (existing)
2. Licensing Qualification Agent (NEW - $40k-60k deals)
3. Gym Member Onboarding Agent (NEW - $2,500 Founder's)

Revenue Coverage: $420k-$975k potential in Year 1
"""

import os
import json
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from licensing_agent import LicensingQualificationAgent
from gym_member_agent import GymMemberOnboardingAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GHL_WEBHOOK_URL = os.getenv('GHL_LEAD_CAPTURE_WEBHOOK', '')
PORT = int(os.getenv('PORT', 5001))

# Initialize agents
logger.info("Initializing AI agents...")

try:
    licensing_agent = LicensingQualificationAgent(
        openai_api_key=OPENAI_API_KEY,
        knowledge_base_path='METROFLEX_EVENTS_KB_V3_EVENTS_ONLY.json'  # Will use licensing section
    )
    logger.info("✅ Licensing Agent initialized")
except Exception as e:
    logger.error(f"❌ Failed to initialize Licensing Agent: {e}")
    licensing_agent = None

try:
    gym_agent = GymMemberOnboardingAgent(
        openai_api_key=OPENAI_API_KEY,
        knowledge_base_path='METROFLEX_GYM_KB_V1.json'
    )
    logger.info("✅ Gym Member Agent initialized")
except Exception as e:
    logger.error(f"❌ Failed to initialize Gym Member Agent: {e}")
    gym_agent = None


def send_to_ghl(payload: dict) -> bool:
    """Send lead to GoHighLevel webhook"""
    if not GHL_WEBHOOK_URL or GHL_WEBHOOK_URL == 'https://placeholder-get-real-webhook-from-brian.com':
        logger.warning("GHL webhook not configured - skipping lead capture")
        return False

    try:
        response = requests.post(GHL_WEBHOOK_URL, json=payload, timeout=10)
        response.raise_for_status()
        logger.info(f"✅ Lead sent to GHL: {payload.get('contact', {}).get('name', 'Unknown')}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to send to GHL: {e}")
        return False


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'agents': {
            'licensing': licensing_agent is not None,
            'gym_member': gym_agent is not None
        },
        'ghl_configured': GHL_WEBHOOK_URL != '' and 'placeholder' not in GHL_WEBHOOK_URL
    }), 200


@app.route('/api/licensing/chat', methods=['POST'])
def licensing_chat():
    """
    Licensing qualification chat endpoint

    Request:
    {
        "query": "I want to open a MetroFlex gym",
        "lead_data": {  // Optional
            "name": "John Smith",
            "email": "john@example.com",
            "phone": "555-1234",
            "liquid_capital": 180000,
            "industry_experience_years": 5,
            "existing_gym": false,
            "existing_gym_sqft": 0,
            "location": "Austin, TX",
            "passion_score": 9
        }
    }

    Response:
    {
        "response": "AI response text",
        "qualification_score": {...},  // If lead_data provided
        "high_intent": true/false,
        "ghl_sent": true/false
    }
    """
    if not licensing_agent:
        return jsonify({'error': 'Licensing agent not available'}), 503

    try:
        data = request.json
        query = data.get('query', '')
        lead_data = data.get('lead_data')

        if not query:
            return jsonify({'error': 'Query is required'}), 400

        # Generate response
        result = licensing_agent.generate_response(query, lead_data)

        # Send to GHL if qualified
        ghl_sent = False
        if 'ghl_payload' in result:
            ghl_sent = send_to_ghl(result['ghl_payload'])

        response = {
            'response': result['response'],
            'high_intent': result.get('high_intent', False),
            'ghl_sent': ghl_sent
        }

        if 'qualification_score' in result:
            response['qualification_score'] = result['qualification_score']

        logger.info(f"Licensing query processed: {query[:50]}... (High intent: {response['high_intent']})")

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error in licensing chat: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/gym/chat', methods=['POST'])
def gym_chat():
    """
    Gym membership chat endpoint

    Request:
    {
        "query": "What are your membership options?",
        "prospect_data": {  // Optional
            "name": "Sarah Johnson",
            "email": "sarah@example.com",
            "phone": "555-5678",
            "workout_frequency": "daily",
            "budget": 3000,
            "commitment_level": 9,
            "location": "Miami, FL"
        }
    }

    Response:
    {
        "response": "AI response text",
        "recommendation": {...},  // If prospect_data provided
        "founders_roi": {...},  // If Founder's recommended
        "high_intent": true/false,
        "ghl_sent": true/false
    }
    """
    if not gym_agent:
        return jsonify({'error': 'Gym member agent not available'}), 503

    try:
        data = request.json
        query = data.get('query', '')
        prospect_data = data.get('prospect_data')

        if not query:
            return jsonify({'error': 'Query is required'}), 400

        # Generate response
        result = gym_agent.generate_response(query, prospect_data)

        # Send to GHL if high intent
        ghl_sent = False
        if 'ghl_payload' in result:
            ghl_sent = send_to_ghl(result['ghl_payload'])

        response = {
            'response': result['response'],
            'high_intent': result.get('high_intent', False),
            'ghl_sent': ghl_sent
        }

        if 'recommendation' in result:
            response['recommendation'] = result['recommendation']

        if 'founders_roi' in result:
            response['founders_roi'] = result['founders_roi']

        logger.info(f"Gym query processed: {query[:50]}... (High intent: {response['high_intent']})")

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error in gym chat: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/events/chat', methods=['POST'])
def events_chat():
    """
    Events chat endpoint (existing functionality)
    Placeholder - integrate existing events agent here
    """
    return jsonify({
        'response': 'Events agent endpoint - integrate existing metroflex_ai_agent_enhanced.py',
        'high_intent': False
    }), 200


@app.route('/api/agents/status', methods=['GET'])
def agents_status():
    """Get status of all agents"""
    return jsonify({
        'agents': {
            'licensing': {
                'available': licensing_agent is not None,
                'endpoint': '/api/licensing/chat',
                'revenue_potential': '$120k-$600k/year',
                'deal_size': '$40k-$60k'
            },
            'gym_member': {
                'available': gym_agent is not None,
                'endpoint': '/api/gym/chat',
                'revenue_potential': '$175k-$250k/year',
                'founders_value': '$2,500 x 100 = $250k'
            },
            'events': {
                'available': True,
                'endpoint': '/api/events/chat',
                'revenue_coverage': '$125k/year'
            }
        },
        'total_revenue_potential': '$420k-$975k/year',
        'ghl_webhook_configured': GHL_WEBHOOK_URL != '' and 'placeholder' not in GHL_WEBHOOK_URL
    }), 200


if __name__ == '__main__':
    logger.info(f"🚀 Starting MetroFlex Unified AI Agent Server on port {PORT}")
    logger.info(f"   Licensing Agent: {'✅ Ready' if licensing_agent else '❌ Not available'}")
    logger.info(f"   Gym Member Agent: {'✅ Ready' if gym_agent else '❌ Not available'}")
    logger.info(f"   GHL Webhook: {'✅ Configured' if GHL_WEBHOOK_URL and 'placeholder' not in GHL_WEBHOOK_URL else '⚠️  Not configured'}")
    logger.info(f"   Revenue Potential: $420k-$975k/year")

    app.run(host='0.0.0.0', port=PORT, debug=False)
