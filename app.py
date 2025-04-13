import json
import os
from flask import Flask, request, jsonify, session, render_template, Response
from flask_cors import CORS
import logging
from dotenv import load_dotenv
import openai
from typing import List, Dict
import mysql.connector
from functools import wraps
import time
from colorama import init, Fore, Style
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from flask import Response, stream_with_context, jsonify
import json
import tiktoken 

# Initialize colorama
init()

# Logger configuration
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app, supports_credentials=True)

# Load environment variables
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Add these constants at the top of the file after imports
GPT35_PROMPT_COST_PER_1K = 0.0010  # $0.0010 per 1K input tokens
GPT35_COMPLETION_COST_PER_1K = 0.0020  # $0.0020 per 1K output tokens

USERS = {
    os.getenv('VALID_USERNAME'): {'password': os.getenv('VALID_PASSWORD'), 'role': 'admin'},
    os.getenv('USER_NAME'): {'password': os.getenv('PASSWORD'), 'role': 'user'}
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({"error": "Please log in to continue"}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({"error": "Please log in to continue"}), 401
        if session.get('role') != 'admin':
            return jsonify({"error": "Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated_function

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="legal_knowledge_base"
        )
        return connection
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise

def fetch_knowledge_base():
    try:
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        
        # Fetch all documents from knowledge_base
        cursor.execute("SELECT id, title, intent, summary FROM knowledge_base")
        knowledge_base = {}
        
        for row in cursor.fetchall():
            doc_id = row['id']
            knowledge_base[doc_id] = {
                'title': row['title'].strip(),
                'description': row['summary'].strip(),  # Use summary as description
                'keywords': ''  # Will be populated from kb_keywords
            }
            
            # Fetch keywords for this document
            cursor.execute("SELECT keyword FROM kb_keywords WHERE kb_id = %s", (doc_id,))
            keywords = [kw['keyword'].strip() for kw in cursor.fetchall()]
            knowledge_base[doc_id]['keywords'] = ', '.join(keywords)
            
            # Fetch details for this document and append to description
            cursor.execute("SELECT instruction FROM kb_details WHERE kb_id = %s ORDER BY step_order", (doc_id,))
            details = [detail['instruction'].strip() for detail in cursor.fetchall()]
            if details:
                knowledge_base[doc_id]['description'] += "\nSteps:\n" + "\n".join(f"{i+1}. {step}" for i, step in enumerate(details))
        
        cursor.close()
        connection.close()
        logger.debug(f"Fetched knowledge base: {knowledge_base}")
        return knowledge_base
    except Exception as e:
        logger.error(f"Error fetching knowledge base: {str(e)}")
        return {}

def fetch_system_prompt():
    try:
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT template FROM prompts WHERE name = 'Custom Prompt'")
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result['template'] if result else None
    except Exception as e:
        logger.error(f"Error fetching system prompt: {str(e)}")
        return None

class ChatSession:
    def __init__(self):
        self.messages: List[Dict] = []

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def get_messages(self) -> List[Dict]:
        return self.messages[-10:]  # Limit to last 10 messages for context

chat_sessions = {}

def get_relevant_knowledge(user_message: str, knowledge_base: Dict) -> str:
    if not knowledge_base:
        logger.warning("Knowledge base is empty")
        return "No relevant knowledge found."
        
    # user_message_lower = user_message.lower().strip()
    # user_words = set(user_message_lower.split())
    user_message_lower = user_message.lower().strip().rstrip('!?.,')
    user_words = set(user_message_lower.split())
    
    best_match = None
    highest_score = 0
    best_doc_id = None
    
    for doc_id, doc in knowledge_base.items():
        title_lower = doc['title'].lower().strip()
        description_lower = doc['description'].lower().strip()
        keywords = set(kw.strip().lower() for kw in doc['keywords'].split(','))
        
        # Scoring: Adjust weights to prioritize specific terms
        score = 0
        title_matches = len(user_words.intersection(title_lower.split())) * 3  # Title weight
        desc_matches = len(user_words.intersection(description_lower.split())) * 2  # Description weight
        keyword_matches = len(user_words.intersection(keywords)) * 2  # Increase keyword weight
        
        score = title_matches + desc_matches + keyword_matches
        
        # Log scoring details for debugging
        logger.debug(f"Doc ID {doc_id} ('{doc['title']}'): title_matches={title_matches}, desc_matches={desc_matches}, keyword_matches={keyword_matches}, total_score={score}")
        
        if score > highest_score:
            highest_score = score
            best_match = f"{doc['title']}\n{doc['description']}"
            best_doc_id = doc_id
    
    # Check if the best match is relevant to critical terms (e.g., "deliverability")
    if highest_score >= 2 and "deliverability" in user_message_lower:
        if "deliverability" not in best_match.lower():
            logger.debug(f"Best match (ID {best_doc_id}) with score {highest_score} lacks 'deliverability' relevance")
            return "No relevant knowledge found."
    
    # Threshold for low-quality matches
    if highest_score < 2:
        logger.debug(f"No strong match found for '{user_message}', highest score: {highest_score}")
        return "No relevant knowledge found."
    
    logger.debug(f"Best match found with score {highest_score}: {best_match}")
    return best_match

def calculate_cost(prompt_tokens, completion_tokens):
    # Convert to cost per thousand tokens
    prompt_cost = (prompt_tokens / 1000) * GPT35_PROMPT_COST_PER_1K
    completion_cost = (completion_tokens / 1000) * GPT35_COMPLETION_COST_PER_1K
    total_cost = prompt_cost + completion_cost
    return {
        "prompt_cost": round(prompt_cost, 4),
        "completion_cost": round(completion_cost, 4),
        "total_cost": round(total_cost, 4)
    }


# Initialize Sentence Transformer model for embeddings
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# FAISS index setup
d = 384  # Dimensionality of sentence embeddings
index = faiss.IndexFlatL2(d)  # L2 (Euclidean) distance index
knowledge_base_map = {}  # Mapping from FAISS indices to knowledge_base entries

# Function to populate FAISS index
def build_faiss_index(knowledge_base):
    global index, knowledge_base_map
    docs = []
    knowledge_base_map.clear()
    
    for i, (doc_id, doc) in enumerate(knowledge_base.items()):
        text = doc['title'] + " " + doc['description']
        docs.append(text)
        knowledge_base_map[i] = doc  # Store mapping
    
    embeddings = embedding_model.encode(docs, convert_to_numpy=True)
    index.add(embeddings)

# Function to retrieve relevant knowledge using FAISS
def get_relevant_knowledge_faiss(user_message: str, k=3):
    query_embedding = embedding_model.encode([user_message], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, k)
    
    relevant_docs = []
    for i in indices[0]:
        if i in knowledge_base_map:
            relevant_docs.append(f"{knowledge_base_map[i]['title']}\n{knowledge_base_map[i]['description']}")
    
    return "\n\n".join(relevant_docs) if relevant_docs else "No relevant knowledge found."

# Load knowledge base and build FAISS index
def initialize_knowledge_base():
    knowledge_base = fetch_knowledge_base()
    build_faiss_index(knowledge_base)
    return knowledge_base

knowledge_base = initialize_knowledge_base()

@app.route("/ask", methods=["POST"])
@login_required
def chat():
    data = request.json
    user_message = data.get("question")
    session_id = data.get("session_id")
    show_thinking = data.get("show_thinking", True)
    
    if not user_message or not session_id:
        return jsonify({"error": "Question or session_id missing"}), 400
    
    if session_id not in chat_sessions:
        chat_sessions[session_id] = ChatSession()
    
    chat_session = chat_sessions[session_id]
    chat_session.add_message("user", user_message)
    
    try:
        system_prompt_template = fetch_system_prompt()
        if not system_prompt_template:
            return jsonify({"error": "System prompt not found"}), 500
        
        knowledge_context = get_relevant_knowledge_faiss(user_message)
        system_prompt = system_prompt_template.replace("{{context}}", knowledge_context).replace("{{question}}", user_message)
        
        messages = chat_session.get_messages()[:-1]
        messages.insert(0, {"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_message})

        # Tokenization setup
        enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
        input_tokens = sum(len(enc.encode(msg["content"])) for msg in messages)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500,
            stream=True
        )

        def generate():
            assistant_response = ""
            completion_tokens = 0  # Track output tokens

            # Ensure thinking section is formatted correctly
            yield json.dumps({"thinking": knowledge_context}, ensure_ascii=False) + "\n"

            try:
                for chunk in response:
                    if "choices" in chunk and chunk["choices"]:
                        text_chunk = chunk["choices"][0]["delta"].get("content", "")
                        if text_chunk:
                            assistant_response += text_chunk  # Append chunk to full response
                            completion_tokens += len(enc.encode(text_chunk))  # Count tokens
                            yield json.dumps({"chunk": text_chunk}, ensure_ascii=False) + "\n"  # Stream JSON chunks
            except Exception as e:
                logger.error(f"Streaming error: {str(e)}")
            finally:
                # Save the full assistant response at the end
                chat_session.add_message("assistant", assistant_response)
                save_chat_session(session_id, chat_session.get_messages())

                # Calculate costs
                costs = calculate_cost(input_tokens, completion_tokens)

                # Save token usage to DB
                save_token_usage(
                    session_id,
                    input_tokens,
                    completion_tokens,
                    input_tokens + completion_tokens,
                    costs["prompt_cost"],
                    costs["completion_cost"],
                    costs["total_cost"]
                )

                # Send final cost info
                yield json.dumps({
                    "token_usage": {
                        "input_tokens": input_tokens,
                        "output_tokens": completion_tokens,
                        "total_tokens": input_tokens + completion_tokens,
                        "input_cost": costs["prompt_cost"],
                        "output_cost": costs["completion_cost"],
                        "total_cost": costs["total_cost"]
                    }
                }, ensure_ascii=False) + "\n"

        return Response(stream_with_context(generate()), mimetype='application/x-ndjson')

    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        return jsonify({"error": "Something went wrong, please try again later"}), 500

@app.route("/token_stats", methods=["GET"])
@login_required
def get_token_stats():
    try:
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                SUM(input_tokens) as total_input_tokens,
                SUM(output_tokens) as total_output_tokens,
                SUM(total_tokens) as total_tokens,
                SUM(input_cost) as total_input_cost,
                SUM(output_cost) as total_output_cost,
                SUM(total_cost) as total_cost,
                COUNT(*) as total_interactions
            FROM token_usage
        """)
        stats = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not stats:
            return jsonify({
                "total_input_tokens": 0,
                "total_output_tokens": 0,
                "total_tokens": 0,
                "total_input_cost": 0,
                "total_output_cost": 0,
                "total_cost": 0,
                "total_interactions": 0
            })
            
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error fetching token stats: {str(e)}")
        return jsonify({"error": str(e)}), 500

def save_token_usage(session_id, input_tokens, output_tokens, total_tokens, input_cost, output_cost, total_cost):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO token_usage 
            (session_id, input_tokens, output_tokens, total_tokens, input_cost, output_cost, total_cost)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (session_id, input_tokens, output_tokens, total_tokens, input_cost, output_cost, total_cost))
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        logger.error(f"Error saving token usage: {str(e)}")

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in USERS and USERS[username]['password'] == password:
        session['username'] = username
        session['role'] = USERS[username]['role']
        return jsonify({"success": True, "role": USERS[username]['role']})
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True})

@app.route("/get_prompt", methods=["GET"])
@admin_required
def get_prompt():
    try:
        prompt = fetch_system_prompt()
        if not prompt:
            return jsonify({"error": "No prompt found"}), 404
        return jsonify({"template": prompt}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/update_prompt", methods=["POST"])
@admin_required
def update_prompt():
    try:
        data = request.get_json()
        template = data.get('template')
        
        if not template:
            return jsonify({"error": "No template provided"}), 400

        connection = connect_to_db()
        cursor = connection.cursor()
        
        cursor.execute("""
            UPDATE prompts 
            SET template = %s 
            WHERE name = 'Custom Prompt'
        """, (template,))
        
        if cursor.rowcount == 0:
            print(f"{Fore.BLUE}Inserting new prompt template...{Style.RESET_ALL}")
            cursor.execute("""
                INSERT INTO prompts (name, template) 
                VALUES ('Custom Prompt', %s)
            """, (template,))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({"message": "Prompt updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/chat_history/<session_id>", methods=["GET"])
@login_required
def get_chat_history(session_id):
    if session_id not in chat_sessions:
        return jsonify({"error": "Session not found"}), 404
    
    return jsonify({"messages": chat_sessions[session_id].get_messages()})


def save_chat_session(session_id, messages):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (session_id, messages) VALUES (%s, %s) ON DUPLICATE KEY UPDATE messages=%s",
                   (session_id, json.dumps(messages), json.dumps(messages)))
    conn.commit()
    cursor.close()
    conn.close()

def load_chat_sessions():
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT session_id, messages FROM chat_history")
    for row in cursor.fetchall():
        chat_sessions[row['session_id']] = ChatSession()
        chat_sessions[row['session_id']].messages = json.loads(row['messages'])
    cursor.close()
    conn.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)