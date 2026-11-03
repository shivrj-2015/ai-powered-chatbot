import sqlite3
from flask import Flask, render_template_string, request, jsonify
from database import init_db, save_chat
import nltk
from nltk.tokenize import word_tokenize

# NLTK Data initialization
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

app = Flask(__name__)

# Initialize SQLite database on startup
init_db()

# Extended System Response Knowledge Base
CHATBOT_KNOWLEDGE_BASE = {
    "greetings": {
        "keywords": ["hello", "hi", "hey", "greetings", "good morning", "good evening", "good afternoon", "sup"],
        "response": "Hello Shivraj! Welcome to Customer Support System. How can I assist you with your queries today?"
    },
    "identity": {
        "keywords": ["name", "who are you", "what are you", "identify", "bot name"],
        "response": "I am an Intelligent AI-Powered Support Assistant integrated with real-time SQLite conversation logging."
    },
    "status": {
        "keywords": ["how are you", "how's it going", "status", "working fine"],
        "response": "I am running smoothly on local host and ready to resolve customer queries 24/7!"
    },
    "order_tracking": {
        "keywords": ["order", "track", "delivery", "shipping", "package", "where is my order", "dispatch"],
        "response": "To track your shipment, please provide your 8-digit Order Reference ID or check your email confirmation link."
    },
    "refund_policy": {
        "keywords": ["refund", "return", "money back", "cancel order", "reimbursement", "exchange"],
        "response": "Our return policy allows items to be returned within 14 days of receipt. Refunds are processed within 5-7 working days."
    },
    "billing_payment": {
        "keywords": ["payment", "invoice", "bill", "credit card", "upi", "debit card", "payment failed", "charge"],
        "response": "We support credit/debit cards, Net Banking, and UPI payments. If your account was debited without confirmation, it auto-refunds in 48 hours."
    },
    "account_management": {
        "keywords": ["password", "account", "login", "reset", "profile", "change password", "forgot password", "username"],
        "response": "To reset your password, navigate to Account Settings > Security > Password Reset, or click on 'Forgot Password' on the login tab."
    },
    "technical_support": {
        "keywords": ["bug", "error", "crash", "not working", "slow", "issue", "problem", "broken", "app fail"],
        "response": "Sorry to hear that! Please try clearing your app cache or browser cookies. If the issue persists, share the exact error code."
    },
    "business_hours": {
        "keywords": ["hours", "open", "timing", "schedule", "working hours", "available", "support time"],
        "response": "Our automated AI support is active 24/7. Human support agents are online Monday to Friday, 9:00 AM to 6:00 PM."
    },
    "security": {
        "keywords": ["safe", "secure", "privacy", "data", "encryption", "gdpr", "confidential"],
        "response": "Your privacy is protected. Conversations are encrypted and safely stored in local database repositories for service quality auditing."
    },
    "human_agent": {
        "keywords": ["agent", "human", "representative", "person", "call me", "speak to human", "talk to support"],
        "response": "I am transferring your session metadata to a live support agent. Average wait time is currently under 3 minutes."
    },
    "gratitude": {
        "keywords": ["thanks", "thank you", "awesome", "great", "perfect", "good job", "helpful"],
        "response": "You're very welcome! I'm glad I could help. Let me know if there's anything else you need."
    },
    "farewell": {
        "keywords": ["bye", "goodbye", "exit", "close", "see you", "quit"],
        "response": "Thank you for reaching out to us today. Have a productive day ahead!"
    }
}

def analyze_intent_nlp(user_input):
    """
    Advanced NLP Tokenization and Keyword Matching Strategy
    """
    cleaned_input = user_input.lower().strip()
    
    # Tokenizing words using NLTK
    tokens = set(word_tokenize(cleaned_input))
    
    highest_score = 0
    matched_intent = None

    for intent, data in CHATBOT_KNOWLEDGE_BASE.items():
        score = 0
        for keyword in data["keywords"]:
            # Token match or direct substring match check
            if keyword in tokens or keyword in cleaned_input:
                score += 1
        
        if score > highest_score:
            highest_score = score
            matched_intent = intent

    if matched_intent and highest_score > 0:
        return CHATBOT_KNOWLEDGE_BASE[matched_intent]["response"]
    else:
        return "Thank you for contacting us. Your query has been logged into our support queue, and our technical team will review it shortly."

# High-quality Enterprise Responsive UI Template
ENTERPRISE_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Customer Service & Support Portal</title>
    <style>
        :root {
            --primary-color: #2563eb;
            --secondary-color: #1e40af;
            --bg-color: #f1f5f9;
            --chat-bg: #ffffff;
            --bot-bubble: #e2e8f0;
            --user-bubble: #2563eb;
            --text-dark: #0f172a;
        }

        body {
            font-family: 'Segoe UI', Inter, Roboto, Helvetica, Arial, sans-serif;
            background: var(--bg-color);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .chat-card {
            width: 480px;
            height: 650px;
            background: var(--chat-bg);
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .chat-header {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 16px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .chat-header h2 {
            margin: 0;
            font-size: 1.1rem;
            font-weight: 600;
        }

        .chat-header span {
            font-size: 0.8rem;
            background: rgba(255, 255, 255, 0.2);
            padding: 4px 8px;
            border-radius: 12px;
        }

        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
            background: #f8fafc;
        }

        .message-bubble {
            max-width: 75%;
            padding: 12px 16px;
            border-radius: 12px;
            font-size: 0.95rem;
            line-height: 1.4;
            word-wrap: break-word;
        }

        .message-user {
            align-self: flex-end;
            background: var(--user-bubble);
            color: white;
            border-bottom-right-radius: 2px;
        }

        .message-bot {
            align-self: flex-start;
            background: var(--bot-bubble);
            color: var(--text-dark);
            border-bottom-left-radius: 2px;
        }

        .chat-footer {
            padding: 16px;
            background: #ffffff;
            border-top: 1px solid #e2e8f0;
            display: flex;
            gap: 10px;
        }

        .chat-input {
            flex: 1;
            padding: 12px 16px;
            border: 1px solid #cbd5e1;
            border-radius: 24px;
            outline: none;
            font-size: 0.95rem;
            transition: border-color 0.2s;
        }

        .chat-input:focus {
            border-color: var(--primary-color);
        }

        .send-btn {
            background: var(--primary-color);
            color: white;
            border: none;
            border-radius: 50%;
            width: 44px;
            height: 44px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.2s;
        }

        .send-btn:hover {
            background: var(--secondary-color);
        }

        .analytics-info {
            font-size: 0.75rem;
            text-align: center;
            color: #64748b;
            padding: 6px;
            background: #f1f5f9;
        }
    </style>
</head>
<body>

    <div class="chat-card">
        <div class="chat-header">
            <div>
                <h2>AI Customer Service</h2>
                <small style="opacity:0.8;">NLP & SQLite Powered</small>
            </div>
            <span>Online 24/7</span>
        </div>

        <div class="chat-messages" id="chatBox">
            <div class="message-bubble message-bot">
                Hello! Welcome to Customer Support. How can I assist you with your orders, billing, or accounts today?
            </div>
        </div>

        <div class="analytics-info">
            All user messages are logged in local database logs for auditing.
        </div>

        <div class="chat-footer">
            <input type="text" id="userInput" class="chat-input" placeholder="Type your query here..." onkeypress="handleKeyPress(event)">
            <button class="send-btn" onclick="sendQuery()">➔</button>
        </div>
    </div>

    <script>
        function handleKeyPress(e) {
            if (e.key === 'Enter') {
                sendQuery();
            }
        }

        async function sendQuery() {
            const inputField = document.getElementById('userInput');
            const message = inputField.value.trim();
            if (!message) return;

            const chatBox = document.getElementById('chatBox');

            // User Message Appending
            const userDiv = document.createElement('div');
            userDiv.className = 'message-bubble message-user';
            userDiv.textContent = message;
            chatBox.appendChild(userDiv);

            inputField.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                const response = await fetch('/get_response', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });

                const data = await response.json();

                // Bot Response Appending
                const botDiv = document.createElement('div');
                botDiv.className = 'message-bubble message-bot';
                botDiv.textContent = data.reply;
                chatBox.appendChild(botDiv);

                chatBox.scrollTop = chatBox.scrollHeight;
            } catch (err) {
                console.error("Communication Error:", err);
            }
        }
    </script>
</body>
</html>
"""

# Web Routes Implementation
@app.route('/')
def index_route():
    """Renders main chatbot UI screen"""
    return render_template_string(ENTERPRISE_HTML_TEMPLATE)

@app.route('/get_response', methods=['POST'])
def process_chat_query():
    """
    Processes incoming text requests, triggers NLP evaluation logic,
    stores logs into database, and sends JSON response back.
    """
    request_payload = request.get_json()
    user_query = request_payload.get('message', '')
    
    if not user_query:
        return jsonify({'reply': 'Invalid input received.'}), 400

    # Calculate NLP response logic
    bot_reply = analyze_intent_nlp(user_query)

    # Save interaction to SQLite database via database.py
    try:
        save_chat(user_query, bot_reply)
    except Exception as db_err:
        print(f"Database insertion failed: {db_err}")

    return jsonify({'reply': bot_reply, 'status': 'success'})

@app.route('/logs', methods=['GET'])
def view_database_logs():
    """
    Internal Developer Route to view stored database records
    """
    try:
        conn = sqlite3.connect('chat_history.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, user_message, bot_response FROM logs ORDER BY id DESC LIMIT 50")
        records = cursor.fetchall()
        conn.close()
        return jsonify({'total_records': len(records), 'logs': records})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Local Application Server Runner
    print("Starting AI Chatbot Engine on http://127.0.0.1:5000 ...")
    app.run(host='127.0.0.1', port=5000, debug=True)