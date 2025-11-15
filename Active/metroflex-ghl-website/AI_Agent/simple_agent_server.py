#!/usr/bin/env python3
"""
Simple MetroFlex AI Agent Server
Minimal working version for testing purposes
"""

import json
import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions

app = Flask(__name__)
CORS(app)

# Initialize OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
client = OpenAI(api_key=OPENAI_API_KEY)

# Load knowledge base
with open("METROFLEX_KNOWLEDGE_BASE.json", 'r') as f:
    kb = json.load(f)

# Initialize ChromaDB
chroma_client = chromadb.Client()
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = chroma_client.get_or_create_collection(
    name="metroflex_simple",
    embedding_function=embedding_function
)

# Build simple vector database
def build_simple_vectordb():
    """Build a simple vector database from knowledge base"""
    docs = []
    ids = []
    metadatas = []
    doc_id = 0

    # Add events
    for event_name, event_data in kb.get('events', {}).items():
        doc_text = f"{event_name}: Date: {event_data.get('date', 'TBD')}, Location: {event_data.get('location', 'TBD')}, Venue: {event_data.get('venue', 'TBD')}"
        if 'registration_url' in event_data:
            doc_text += f" Register at: {event_data['registration_url']}"
        docs.append(doc_text)
        ids.append(f"doc_{doc_id}")
        metadatas.append({"category": "event", "event_name": event_name})
        doc_id += 1

    # Add NPC divisions (simplified)
    for division, rules in kb.get('npc_division_rules', {}).items():
        doc_text = f"{division} division: {rules.get('description', '')}. Suit: {rules.get('suit_requirements', '')}"
        if 'weight_classes' in rules:
            classes = [wc.get('class', '') for wc in rules['weight_classes']]
            doc_text += f" Weight classes: {', '.join(classes)}"
        docs.append(doc_text)
        ids.append(f"doc_{doc_id}")
        metadatas.append({"category": "division", "division": division})
        doc_id += 1

    # Add registration info
    reg = kb.get('competition_procedures', {}).get('registration', {})
    doc_text = f"Registration: Methods: {', '.join(reg.get('methods', []))}. NPC card required: {reg.get('npc_card_required', 'Yes')}"
    docs.append(doc_text)
    ids.append(f"doc_{doc_id}")
    metadatas.append({"category": "registration"})
    doc_id += 1

    # Add music requirements
    music = kb.get('competition_procedures', {}).get('posing_music', {})
    doc_text = f"Posing music: Required for {', '.join(music.get('required_for', []))}. Max length: {music.get('max_length', '60 seconds')}. Format: {', '.join(music.get('format', []))}"
    docs.append(doc_text)
    ids.append(f"doc_{doc_id}")
    metadatas.append({"category": "music"})
    doc_id += 1

    # Add to collection
    if docs:
        collection.add(documents=docs, ids=ids, metadatas=metadatas)

    print(f"✅ Built vector database with {len(docs)} documents")

# Build database on startup
try:
    build_simple_vectordb()
except Exception as e:
    print(f"Warning: Could not build vector database: {e}")

# System prompt
SYSTEM_PROMPT = """You are the MetroFlex Events AI Assistant - an expert on NPC bodybuilding competitions.

Your role:
- Help competitors understand division rules, registration, and procedures
- Answer sponsor inquiries
- Provide event information (dates, venues, registration links)
- Maintain a professional, helpful, and confident tone

Key information:
- All events use MuscleWare for registration: https://www.muscleware.com
- NPC membership card required for all competitions
- 8 NPC divisions available for men and women
- Contact: brian@metroflexgym.com or 817-465-9331

Be concise, accurate, and always include relevant registration links or contact information when applicable.
"""

# Conversation memory
conversations = {}

@app.route('/webhook/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.json
        message = data.get('message', '')
        session_id = data.get('session_id', 'default')

        if not message:
            return jsonify({"error": "No message provided"}), 400

        # Retrieve relevant context
        try:
            results = collection.query(query_texts=[message], n_results=3)
            context_docs = results['documents'][0] if results['documents'] else []
            context = "\n".join([f"[Context]: {doc}" for doc in context_docs])
        except:
            context = ""

        # Get or create conversation history
        if session_id not in conversations:
            conversations[session_id] = []

        # Build messages
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
        ]

        if context:
            messages.append({"role": "system", "content": f"Retrieved Information:\n{context}"})

        # Add conversation history (last 5 exchanges)
        messages.extend(conversations[session_id][-10:])

        # Add current message
        messages.append({"role": "user", "content": message})

        # Call OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=300
        )

        assistant_message = response.choices[0].message.content

        # Update conversation history
        conversations[session_id].append({"role": "user", "content": message})
        conversations[session_id].append({"role": "assistant", "content": assistant_message})

        return jsonify({
            "success": True,
            "response": assistant_message,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "response": "I apologize, but I'm experiencing technical difficulties. Please contact Brian Dobson at brian@metroflexgym.com or call 817-465-9331."
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "agent": "MetroFlex AI Assistant (Simple)",
        "version": "1.0"
    })

if __name__ == "__main__":
    print("🚀 MetroFlex Simple AI Agent starting...")
    print("📊 Vector database ready")
    print("💬 Chat endpoint: POST /webhook/chat")
    print("❤️  Health check: GET /health")
    print("🌐 Running on http://localhost:5001")
    print()
    app.run(host='0.0.0.0', port=5001, debug=False)
