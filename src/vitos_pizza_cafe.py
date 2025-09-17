"""Simplified workflow for Vito's Pizza Cafe application."""

from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent

from src.config import logger
from src.knowledge_base import retrieve_context
from src.database import get_database_tools

# System prompt for Vito's Pizza Cafe
SYSTEM_PROMPT = """You are the intelligent assistant for Vito's Pizza Cafe, well-versed in the company background, account management, menus and orders, delivery and pickup, dining, and payment information. Please provide users with precise answers regarding registration, login, order inquiries, placing orders, discounts, and refund policies, always offering help in a friendly and professional tone and responding in the language used in the user's query. For questions beyond the above scope, please inform the user that you can only provide information related to the aforementioned services, and suggest that they contact the in-store staff or visit the official website for further assistance. Use the following content as the knowledge you have learned, enclosed within <context></context> XML tags. When you need to reference the content in the context, please use the original text without any arbitrary modifications, including URL addresses, etc."""

def process_query(user_input: str, conversation_history: list = None) -> str:
    """Process user query with mandatory RAG retrieval + React agent."""

    # 1. Always retrieve context first (mandatory RAG)
    context = retrieve_context(user_input)
    logger.debug(f"Retrieved context for query: {user_input}")

    # 2. Get database tools and LLM
    tools, llm = get_database_tools()

    # 3. Create React agent
    react_agent = create_react_agent(
        model=llm,
        tools=tools
    )

    # 4. Prepare messages
    messages = []

    # Add system prompt with context
    system_message = f"{SYSTEM_PROMPT}\n\n{context}"
    messages.append(SystemMessage(content=system_message))

    # Add conversation history if provided
    if conversation_history:
        messages.extend(conversation_history[-10:])  # Keep last 10 messages

    # Add current user query
    messages.append(HumanMessage(content=user_input))

    # 5. Get response from React agent
    result = react_agent.invoke({"messages": messages})
    response = result["messages"][-1].content

    logger.debug(f"Generated response: {response[:100]}...")
    return response

logger.info("Simplified workflow initialized")