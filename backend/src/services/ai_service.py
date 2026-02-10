from typing import List, Dict, Any, Optional
from uuid import UUID
import json
import logging
import os
from sqlmodel import Session, select

from ..models.conversation import Conversation, Message, MessageCreate
from ..models.user import User
from ..mcp_tools.task_tools import add_task, list_tasks, complete_task, delete_task, update_task

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self, openai_api_key: Optional[str] = None):
        # OpenAI key is optional for the current rule-based implementation.
        self.openai_api_key = openai_api_key
        
    async def get_or_create_conversation(self, db: Session, user_id: UUID) -> Conversation:
        """Get existing conversation or create new one for user."""
        # For now, create a new conversation each time. 
        # Later can be modified to continue existing conversations
        conversation = Conversation(user_id=user_id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation
    
    async def save_message(self, db: Session, conversation_id: UUID, role: str, content: str):
        """Save a message to the conversation."""
        message = MessageCreate(conversation_id=conversation_id, role=role, content=content)
        db_message = Message(**message.dict())
        db.add(db_message)
        db.commit()
        
    async def get_conversation_context(self, db: Session, conversation_id: UUID, limit: int = 10) -> List[Dict[str, str]]:
        """Get recent messages for conversation context."""
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
            .limit(limit)
        )
        messages = db.exec(statement).all()
        
        return [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
    
    async def execute_tool(self, db: Session, tool_name: str, user_id: UUID, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tool with database session."""
        try:
            if tool_name == "add_task":
                return await add_task(db, user_id, **arguments)
            elif tool_name == "list_tasks":
                return await list_tasks(db, user_id)
            elif tool_name == "complete_task":
                return await complete_task(db, user_id, **arguments)
            elif tool_name == "delete_task":
                return await delete_task(db, user_id, **arguments)
            elif tool_name == "update_task":
                return await update_task(db, user_id, **arguments)
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
        except Exception as e:
            logger.error(f"Tool execution error: {str(e)}")
            return {"error": str(e)}
    
    def parse_intent(self, message: str) -> tuple[str, Dict[str, Any]]:
        """Simple rule-based intent parsing."""
        message_lower = message.lower().strip()
        
        # Add task patterns
        if any(word in message_lower for word in ["add", "create", "new"]):
            if "task" in message_lower:
                # Extract task title
                title = message.replace("add task", "").replace("create task", "").replace("new task", "").strip()
                return "add_task", {"title": title}
        
        # List tasks patterns
        if any(word in message_lower for word in ["list", "show", "what", "my tasks"]):
            return "list_tasks", {}
        
        # Complete task patterns
        if any(word in message_lower for word in ["complete", "done", "finish"]):
            return "complete_task", {"task_id": "latest"}  # Simplified
        
        # Delete task patterns  
        if any(word in message_lower for word in ["delete", "remove"]):
            return "delete_task", {"task_id": "latest"}  # Simplified
        
        # Default to no tool
        return "none", {}
    
    async def process_message(self, db: Session, user_id: UUID, message: str) -> Dict[str, Any]:
        """Process user message with rule-based AI and return response."""
        
        # Get or create conversation
        conversation = await self.get_or_create_conversation(db, user_id)
        
        # Save user message
        await self.save_message(db, conversation.id, "user", message)
        
        # Parse intent and get response
        tool_name, tool_args = self.parse_intent(message)
        
        tool_results = []
        response_text = "I'm your todo assistant. How can I help you manage your tasks?"
        
        if tool_name != "none":
            # Execute the tool
            result = await self.execute_tool(db, tool_name, user_id, tool_args)
            tool_results.append({
                "tool": tool_name,
                "arguments": tool_args,
                "result": result
            })
            
            # Generate response based on tool result
            if tool_name == "add_task" and "error" not in result:
                response_text = f"I've added '{result['title']}' to your todo list."
            elif tool_name == "list_tasks":
                if isinstance(result, list) and result:
                    tasks_text = "\n".join([f"- {task['title']}" for task in result])
                    response_text = f"Here are your tasks:\n{tasks_text}"
                else:
                    response_text = "You don't have any tasks yet."
            elif tool_name == "complete_task" and "error" not in result:
                response_text = f"Great! I've marked '{result['title']}' as complete."
            elif tool_name == "delete_task" and isinstance(result, bool) and result:
                response_text = "I've deleted that task."
            elif "error" in result:
                response_text = f"Sorry, I encountered an error: {result['error']}"
        
        # Save assistant response
        await self.save_message(db, conversation.id, "assistant", response_text)
        
        return {
            "response": response_text,
            "tool_results": tool_results,
            "conversation_id": conversation.id
        }