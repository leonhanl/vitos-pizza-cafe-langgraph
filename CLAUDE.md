# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is Vito's Pizza Cafe - an AI customer service application demonstrating AI security vulnerabilities and their mitigation using Palo Alto Networks AI Runtime Security (AIRS). The application is built with LangGraph for conversation flow, RAG for information retrieval, and Streamlit for the web interface.

## Development Commands

### Setup and Installation
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Unix/MacOS
# .venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Running the Application
```bash
# Test the RAG application
python src/vitos_pizza_cafe.py

# Test AIRS API integration
python src/panw_airs.py

# Launch web interface
streamlit run src/app.py
```

### Testing Security Features
```bash
# Enable AIRS protection by uncommenting lines in vitos_pizza_cafe.py:
# - Line 217: @check_message_safety
# - Lines 283-287: safety_check implementation
```

## Architecture Overview

### Core Components
- **LangGraph State Machine** (`src/vitos_pizza_cafe.py`): Manages conversation flow with states for retrieval, generation, and tool usage
- **RAG System**: Uses FAISS vector store with Cohere embeddings and reranking for document retrieval
- **Database Integration**: SQLite in-memory database with customer information, accessed via SQLDatabaseToolkit
- **Security Layer**: AIRS API integration for input/output safety checking
- **Web Interface** (`src/app.py`): Streamlit-based chat interface with conversation management

### Key Files
- `src/vitos_pizza_cafe.py`: Main LangGraph application with VitosClient class
- `src/app.py`: Streamlit web interface
- `src/panw_airs.py`: AIRS API integration for security checks
- `Vitos-Pizza-Cafe-KB/`: Knowledge base markdown files for RAG
- `customer_db.sql`: SQLite database schema with customer data

### Data Flow
1. User input → AIRS security check (optional)
2. Vector similarity search in knowledge base
3. Cohere reranking of retrieved documents
4. LLM generation with context and optional database queries
5. Response → AIRS output safety check (optional)

## API Keys Required

Configure these in `.env`:
- `COHERE_API_KEY`: For embeddings and reranking
- `DEEPSEEK_API_KEY`: For LLM responses and tool execution
- `X_PAN_TOKEN`: For AIRS security API
- `LANGSMITH_API_KEY`: Optional for tracing

## Security Testing

The application demonstrates these attack vectors:
- Prompt injection (goal hijacking, system prompt leak)
- PII disclosure
- Data poisoning (malicious URLs, toxic content)
- Excessive agency (database tampering)

Use the test cases in README.md to verify security protections are working.

## Development Notes

- The vector store index is cached in `Vitos-Pizza-Cafe-KB/faiss_index/`
- Database runs in-memory and is recreated on each startup
- LangGraph checkpoints use MemorySaver for conversation persistence
- Security checks can be toggled by commenting/uncommenting decorator lines