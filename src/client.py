"""Client interface for Vito's Pizza Cafe application."""

import logging
from langchain_core.messages import HumanMessage, AIMessage

from .vitos_pizza_cafe import process_query

logger = logging.getLogger(__name__)

class VitosClient:
    """Client for interacting with Vito's Pizza Cafe assistant."""

    def __init__(self, thread_id: str = "default"):
        """Initialize Vito's Pizza Cafe client."""
        self.thread_id = thread_id
        self.conversation_history = []
        logger.info(f"VitosClient initialized with thread_id: {thread_id}")

    def query(self, user_input: str) -> str:
        """Process user query with simplified workflow."""
        logger.info(f"User input: {user_input}, Thread ID: {self.thread_id}")

        try:
            # Process query with mandatory RAG + React agent
            response = process_query(user_input, self.conversation_history)

            # Add user message to conversation history
            self.conversation_history.append(HumanMessage(content=user_input))

            # Add assistant response to conversation history
            self.conversation_history.append(AIMessage(content=response))

            # Keep conversation history manageable (last 20 messages)
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]

            logger.debug(f"Response: {response[:100]}...")
            return response

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return "I apologize, but I encountered an error while processing your request. Please try again or contact our support team."