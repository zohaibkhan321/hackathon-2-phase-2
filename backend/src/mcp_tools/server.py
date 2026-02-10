from typing import List, Dict, Any
from uuid import UUID
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import json
import logging

from ..models.task import Task
from .task_tools import add_task, list_tasks, complete_task, delete_task, update_task

logger = logging.getLogger(__name__)

# Create MCP server
server = Server("todo-task-tools")

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="add_task",
            description="Add a new task to the user's todo list",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Title of the task"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional description of the task"
                    }
                },
                "required": ["title"]
            }
        ),
        Tool(
            name="list_tasks",
            description="List all tasks for the user",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="complete_task",
            description="Mark a task as completed",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "ID of the task to complete"
                    }
                },
                "required": ["task_id"]
            }
        ),
        Tool(
            name="delete_task",
            description="Delete a task from the todo list",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "ID of the task to delete"
                    }
                },
                "required": ["task_id"]
            }
        ),
        Tool(
            name="update_task",
            description="Update an existing task",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "ID of the task to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title for the task"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description for the task"
                    },
                    "completed": {
                        "type": "boolean",
                        "description": "Whether the task is completed"
                    }
                },
                "required": ["task_id"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Execute an MCP tool."""
    try:
        # Extract user_id from arguments (should be passed from the AI agent)
        user_id = arguments.pop("user_id", None)
        if not user_id:
            return [TextContent(
                type="text",
                text="Error: user_id is required for all tool operations"
            )]
        
        user_uuid = UUID(user_id)
        
        # Import database session - this should be injected by the caller
        from sqlmodel import Session
        from ..config.database import engine
        
        with Session(engine) as db:
            if name == "add_task":
                result = await add_task(db, user_uuid, **arguments)
                return [TextContent(
                    type="text",
                    text=f"Task added successfully: {json.dumps(result, indent=2)}"
                )]
            
            elif name == "list_tasks":
                tasks = await list_tasks(db, user_uuid)
                if not tasks:
                    return [TextContent(
                        type="text",
                        text="You have no tasks."
                    )]
                return [TextContent(
                    type="text",
                    text=f"Your tasks:\n{json.dumps(tasks, indent=2)}"
                )]
            
            elif name == "complete_task":
                result = await complete_task(db, user_uuid, **arguments)
                return [TextContent(
                    type="text",
                    text=f"Task completed: {json.dumps(result, indent=2)}"
                )]
            
            elif name == "delete_task":
                success = await delete_task(db, user_uuid, **arguments)
                if success:
                    return [TextContent(
                        type="text",
                        text="Task deleted successfully."
                    )]
                else:
                    return [TextContent(
                        type="text",
                        text="Failed to delete task."
                    )]
            
            elif name == "update_task":
                result = await update_task(db, user_uuid, **arguments)
                return [TextContent(
                    type="text",
                    text=f"Task updated: {json.dumps(result, indent=2)}"
                )]
            
            else:
                return [TextContent(
                    type="text",
                    text=f"Unknown tool: {name}"
                )]
                
    except Exception as e:
        logger.error(f"Error executing tool {name}: {str(e)}")
        return [TextContent(
            type="text",
            text=f"Error executing {name}: {str(e)}"
        )]

async def run_mcp_server():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_mcp_server())