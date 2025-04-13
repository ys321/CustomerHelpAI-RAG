# CustomerHelpAI-RAG


CustomerHelpAI-RAG is a **Customer Support Agent** powered by **Retrieval-Augmented Generation (RAG)**. It combines conversational AI with information retrieval to assist customers with accurate, context-based answers.

## Features
- 🧠 **RAG-based AI**: Combines information retrieval and language generation for accurate answers.
- 💬 **Support Chat**: A robust chat interface for handling customer support queries.
- 🛠️ **Admin Panel**: Admins can manage and customize the AI's responses.
- 💸 **Token Management**: Tracks the number of tokens used and calculates costs based on OpenAI's pricing.
- 🔄 **Multi-session Support**: Supports multiple concurrent user sessions.

## Requirements
- Python 3.8 or higher
- Flask
- OpenAI API Key
- MySQL Database
- `dotenv` for environment variables management
- `faiss` for similarity search
- `sentence-transformers` for embeddings

## Setup Instructions

### 1. Clone the repository
First, clone the repository to your local machine:
```bash
git clone https://github.com/ys321/CustomerHelpAI-RAG.git
cd CustomerHelpAI-RAG
```

### 2. Create a Virtual Environment

#### Ubuntu / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows:
```bash
python -m venv venv
.env\Scriptsctivate
```

### 3. Install Dependencies
With the virtual environment activated, install the required dependencies:
```bash
pip install -r requirements.txt
```

### 4. Set up your environment variables
Create a `.env` file in the root of your project and add the following:
```env
OPENAI_API_KEY="sk-..."  # Replace with your actual OpenAI API key
VALID_USERNAME="Test"  # Username for Admin login
VALID_PASSWORD="Admin@123"  # Admin password
USER_NAME="User"  # Username for User login
PASSWORD="Test@123"  # User password
```
Make sure to replace `sk-...` with your actual OpenAI API key.

### 5. Set up the MySQL Database
Ensure you have a MySQL database running and set up the following schema:
```sql
CREATE DATABASE legal_knowledge_base;

USE legal_knowledge_base;

-- Table to store user sessions
CREATE TABLE chat_history (
    session_id VARCHAR(255) PRIMARY KEY,
    messages TEXT
);

-- Table to store token usage information
CREATE TABLE token_usage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(255),
    input_tokens INT,
    output_tokens INT,
    total_tokens INT,
    input_cost DECIMAL(10, 4),
    output_cost DECIMAL(10, 4),
    total_cost DECIMAL(10, 4),
    FOREIGN KEY (session_id) REFERENCES chat_history(session_id)
);

-- Table to store knowledge base entries
CREATE TABLE knowledge_base (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    summary TEXT,
    intent VARCHAR(255)
);

-- Table to store keyword information
CREATE TABLE kb_keywords (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kb_id INT,
    keyword VARCHAR(255),
    FOREIGN KEY (kb_id) REFERENCES knowledge_base(id)
);

-- Table to store additional details for knowledge base entries
CREATE TABLE kb_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kb_id INT,
    instruction TEXT,
    step_order INT,
    FOREIGN KEY (kb_id) REFERENCES knowledge_base(id)
);

-- Table for custom system prompt
CREATE TABLE prompts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    template TEXT
);
```

### 6. Running the Application
To run the Flask application, use the following command:
```bash
python app.py
```
The app will run on http://0.0.0.0:5000.

### 7. Access the Application
Login: Use the credentials defined in your `.env` file to log in:
- Admin: Test / Admin@123
- User: User / Test@123

## API Endpoints
1. **/ask (POST)**
   - Purpose: User submits a question, and the AI responds with an answer based on the knowledge base.
   - Request Body:
   ```json
   {
     "question": "What is RAG?",
     "session_id": "unique_session_id"
   }
   ```

2. **/login (POST)**
   - Purpose: Allows users to log in.
   - Request Body:
   ```json
   {
     "username": "Test",
     "password": "Admin@123"
   }
   ```

3. **/logout (POST)**
   - Purpose: Allows users to log out.

4. **/token_stats (GET)**
   - Purpose: Admin can view the token usage statistics.

5. **/chat_history/<session_id> (GET)**
   - Purpose: Fetch chat history for a specific session.

6. **/get_prompt (GET)**
   - Purpose: Admin can view the current system prompt template.

7. **/update_prompt (POST)**
   - Purpose: Admin can update the system prompt template.

## Contact
For further inquiries, please reach out to the project maintainer at:
- Email: ys0302010@gmail.com

