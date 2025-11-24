"""
Simple API server for the chatbot
Deploy this to Replit, Railway, or any Python hosting service
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from chatbot import VitalMechanicalChatbot

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Store chatbot instances per session
# In production, use Redis or similar for session management
chatbot_sessions = {}


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "vital-mechanical-chatbot"}), 200


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint

    Expected JSON body:
    {
        "message": "user message here",
        "session_id": "optional-session-id"
    }

    Returns:
    {
        "response": "bot response",
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
                chatbot_sessions[session_id] = VitalMechanicalChatbot()
            except ValueError as e:
                return jsonify({"error": str(e)}), 500

        chatbot = chatbot_sessions[session_id]

        # Get response
        response = chatbot.chat(user_message)

        return jsonify({
            "response": response,
            "session_id": session_id
        }), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route('/api/reset', methods=['POST'])
def reset_session():
    """
    Reset a conversation session

    Expected JSON body:
    {
        "session_id": "session-id-to-reset"
    }
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default')

        if session_id in chatbot_sessions:
            chatbot_sessions[session_id].reset_conversation()
            return jsonify({"message": "Session reset successfully"}), 200
        else:
            return jsonify({"message": "Session not found"}), 404

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route('/api/info', methods=['GET'])
def get_info():
    """Get chatbot information"""
    from chatbot_config import COMPANY_INFO

    return jsonify({
        "company": COMPANY_INFO['name'],
        "founded": COMPANY_INFO['founded'],
        "location": COMPANY_INFO['location'],
        "core_values": [v['name'] for v in COMPANY_INFO['core_values']],
        "services": [s['category'] for s in COMPANY_INFO['services']]
    }), 200


if __name__ == '__main__':
    # Get port from environment variable (for deployment platforms)
    port = int(os.environ.get('PORT', 5000))

    # Check if API key is set
    if not os.environ.get('ANTHROPIC_API_KEY'):
        print("WARNING: ANTHROPIC_API_KEY environment variable not set!")
        print("The chatbot will not work without an API key.")

    # Run the server
    app.run(host='0.0.0.0', port=port, debug=False)
