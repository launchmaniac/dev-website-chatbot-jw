"""
Enhanced API Server with Lead Capture, Booking, and Quote Capabilities
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from datetime import datetime
from chatbot_enhanced import EnhancedVitalMechanicalChatbot

app = Flask(__name__)
CORS(app)

# Store chatbot instances per session
chatbot_sessions = {}

# Directory for storing data
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)


@app.route('/', methods=['GET'])
def home():
    """API information endpoint"""
    return jsonify({
        "service": "Vital Mechanical Chatbot API",
        "version": "2.0",
        "features": {
            "chat": True,
            "lead_capture": True,
            "booking": False,  # Will enable later
            "quotes": False    # Will enable later
        },
        "endpoints": {
            "chat": "/api/chat",
            "leads": "/api/leads",
            "health": "/health"
        }
    }), 200


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "vital-mechanical-chatbot",
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint with tool support

    Expected JSON:
    {
        "message": "user message",
        "session_id": "optional-session-id"
    }

    Returns:
    {
        "response": "bot response",
        "actions": [...],  // Any actions taken (lead capture, booking, etc.)
        "session_id": "session-id"
    }
    """
    try:
        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify({"error": "Missing 'message' in request body"}), 400

        user_message = data['message']
        session_id = data.get('session_id', 'default')

        # Get or create chatbot for this session
        if session_id not in chatbot_sessions:
            try:
                chatbot_sessions[session_id] = EnhancedVitalMechanicalChatbot()
            except ValueError as e:
                return jsonify({"error": str(e)}), 500

        chatbot = chatbot_sessions[session_id]

        # Get response with any tool calls
        result = chatbot.chat(user_message)

        return jsonify({
            "response": result["response"],
            "actions": result.get("actions", []),
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route('/api/leads', methods=['GET'])
def get_leads():
    """
    Get all captured leads
    Protected endpoint - add authentication in production!
    """
    try:
        leads_file = os.path.join(DATA_DIR, "leads.json")

        if not os.path.exists(leads_file):
            return jsonify({"leads": [], "count": 0}), 200

        with open(leads_file, 'r') as f:
            leads = json.load(f)

        return jsonify({
            "leads": leads,
            "count": len(leads)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/leads/export', methods=['GET'])
def export_leads():
    """
    Export leads as CSV
    Protected endpoint - add authentication in production!
    """
    try:
        leads_file = os.path.join(DATA_DIR, "leads.json")

        if not os.path.exists(leads_file):
            return "No leads to export", 404

        with open(leads_file, 'r') as f:
            leads = json.load(f)

        # Convert to CSV
        import csv
        import io

        output = io.StringIO()
        if leads:
            writer = csv.DictWriter(output, fieldnames=leads[0].keys())
            writer.writeheader()
            writer.writerows(leads)

        response = app.response_class(
            response=output.getvalue(),
            status=200,
            mimetype='text/csv'
        )
        response.headers["Content-Disposition"] = "attachment; filename=leads.csv"
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/reset', methods=['POST'])
def reset_session():
    """Reset a conversation session"""
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default')

        if session_id in chatbot_sessions:
            chatbot_sessions[session_id].reset_conversation()
            return jsonify({"message": "Session reset successfully"}), 200
        else:
            return jsonify({"message": "Session not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/features', methods=['GET'])
def get_features():
    """Get current feature status"""
    try:
        # Create a temp chatbot to check features
        chatbot = EnhancedVitalMechanicalChatbot()
        return jsonify(chatbot.features), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/features/<feature_name>', methods=['POST'])
def toggle_feature(feature_name):
    """
    Enable/disable features
    Protected endpoint - add authentication in production!

    Body: {"enabled": true/false}
    """
    try:
        data = request.get_json()
        enabled = data.get('enabled', True)

        # Update all active sessions
        for session_id, chatbot in chatbot_sessions.items():
            if enabled:
                chatbot.enable_feature(feature_name)
            else:
                chatbot.disable_feature(feature_name)

        return jsonify({
            "feature": feature_name,
            "enabled": enabled,
            "message": f"Feature {feature_name} {'enabled' if enabled else 'disabled'}"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    Get chatbot usage statistics
    """
    try:
        leads_file = os.path.join(DATA_DIR, "leads.json")

        stats = {
            "active_sessions": len(chatbot_sessions),
            "total_leads": 0,
            "leads_by_urgency": {},
            "leads_by_service": {},
            "recent_activity": []
        }

        if os.path.exists(leads_file):
            with open(leads_file, 'r') as f:
                leads = json.load(f)

            stats["total_leads"] = len(leads)

            # Count by urgency
            for lead in leads:
                urgency = lead.get('urgency', 'normal')
                stats["leads_by_urgency"][urgency] = stats["leads_by_urgency"].get(urgency, 0) + 1

            # Count by service
            for lead in leads:
                service = lead.get('service_interest', 'Unknown')
                stats["leads_by_service"][service] = stats["leads_by_service"].get(service, 0) + 1

            # Get recent leads (last 5)
            stats["recent_activity"] = sorted(
                leads,
                key=lambda x: x.get('timestamp', ''),
                reverse=True
            )[:5]

        return jsonify(stats), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Serve the widget HTML (for testing)
@app.route('/widget')
def widget():
    """Serve the chat widget for testing"""
    return send_from_directory('.', 'web_widget_enhanced.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    if not os.environ.get('ANTHROPIC_API_KEY'):
        print("⚠️  WARNING: ANTHROPIC_API_KEY environment variable not set!")
        print("   The chatbot will not work without an API key.")
        print("   Get one at: https://console.anthropic.com")
    else:
        print("✅ API key found")

    print(f"\n🚀 Starting Enhanced Vital Mechanical Chatbot API")
    print(f"   Port: {port}")
    print(f"   Features: Lead Capture ✅ | Booking ⏳ | Quotes ⏳")
    print(f"\n📊 Endpoints:")
    print(f"   Health: http://localhost:{port}/health")
    print(f"   Chat: http://localhost:{port}/api/chat")
    print(f"   Leads: http://localhost:{port}/api/leads")
    print(f"   Stats: http://localhost:{port}/api/stats")
    print(f"   Widget Test: http://localhost:{port}/widget")
    print(f"\n")

    app.run(host='0.0.0.0', port=port, debug=False)
