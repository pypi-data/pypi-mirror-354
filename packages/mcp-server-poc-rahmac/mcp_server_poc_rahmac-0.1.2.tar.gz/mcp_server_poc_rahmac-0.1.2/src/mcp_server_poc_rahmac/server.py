#!/usr/bin/env python3
"""A simple MCP Server example."""

import asyncio
import json
import sys
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    GetPromptRequest,
    GetPromptResult,
    ListPromptsRequest,
    ListPromptsResult,
    ListResourcesRequest,
    ListResourcesResult,
    ListToolsRequest,
    ListToolsResult,
    Prompt,
    ReadResourceRequest,
    ReadResourceResult,
    Resource,
    TextContent,
    Tool,
)
from pydantic import BaseModel


class GreetingArgs(BaseModel):
    """Arguments for the greeting tool."""
    name: str
    greeting_type: Optional[str] = "hello"


class CalculatorArgs(BaseModel):
    """Arguments for the calculator tool."""
    operation: str
    a: float
    b: float


# Create the server instance
server = Server("mcp-server-example")

# Sample data for resources
SAMPLE_DATA = {
    "users": [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
    ],
    "products": [
        {"id": 1, "name": "Widget", "price": 19.99},
        {"id": 2, "name": "Gadget", "price": 29.99},
    ],
}


@server.list_resources()
async def list_resources() -> ListResourcesResult:
    """List available resources."""
    resources = [
        Resource(
            uri="sample://users",
            name="Sample Users",
            mimeType="application/json",
            description="A list of sample users",
        ),
        Resource(
            uri="sample://products",
            name="Sample Products",
            mimeType="application/json",
            description="A list of sample products",
        ),
    ]
    return ListResourcesResult(resources=resources)


@server.read_resource()
async def read_resource(request: ReadResourceRequest) -> ReadResourceResult:
    """Read a specific resource."""
    uri = request.uri
    
    if uri == "sample://users":
        content = json.dumps(SAMPLE_DATA["users"], indent=2)
    elif uri == "sample://products":
        content = json.dumps(SAMPLE_DATA["products"], indent=2)
    else:
        raise ValueError(f"Unknown resource: {uri}")
    
    return ReadResourceResult(
        contents=[
            TextContent(
                type="text",
                text=content,
            )
        ]
    )


@server.list_tools()
async def list_tools() -> ListToolsResult:
    """List available tools."""
    tools = [
        Tool(
            name="greeting",
            description="Generate a personalized greeting",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the person to greet",
                    },
                    "greeting_type": {
                        "type": "string",
                        "description": "Type of greeting (hello, hi, howdy)",
                        "enum": ["hello", "hi", "howdy"],
                        "default": "hello",
                    },
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="calculator",
            description="Perform basic arithmetic operations",
            inputSchema={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "description": "The operation to perform",
                        "enum": ["add", "subtract", "multiply", "divide"],
                    },
                    "a": {
                        "type": "number",
                        "description": "First number",
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number",
                    },
                },
                "required": ["operation", "a", "b"],
            },
        ),
    ]
    return ListToolsResult(tools=tools)


@server.call_tool()
async def call_tool(request: CallToolRequest) -> CallToolResult:
    """Handle tool calls."""
    if request.name == "greeting":
        args = GreetingArgs(**request.arguments)
        greeting_map = {
            "hello": "Hello",
            "hi": "Hi",
            "howdy": "Howdy",
        }
        greeting = greeting_map.get(args.greeting_type, "Hello")
        message = f"{greeting}, {args.name}! Welcome to the MCP Server example."
        
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=message,
                )
            ]
        )
    
    elif request.name == "calculator":
        args = CalculatorArgs(**request.arguments)
        
        operations = {
            "add": lambda x, y: x + y,
            "subtract": lambda x, y: x - y,
            "multiply": lambda x, y: x * y,
            "divide": lambda x, y: x / y if y != 0 else None,
        }
        
        if args.operation not in operations:
            raise ValueError(f"Unknown operation: {args.operation}")
        
        result = operations[args.operation](args.a, args.b)
        
        if result is None:
            message = "Error: Division by zero"
        else:
            message = f"{args.a} {args.operation} {args.b} = {result}"
        
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=message,
                )
            ]
        )
    
    else:
        raise ValueError(f"Unknown tool: {request.name}")


@server.list_prompts()
async def list_prompts() -> ListPromptsResult:
    """List available prompts."""
    prompts = [
        Prompt(
            name="code_review",
            description="Generate a code review checklist",
            arguments=[
                {
                    "name": "language",
                    "description": "Programming language",
                    "required": True,
                },
                {
                    "name": "complexity",
                    "description": "Code complexity level (basic, intermediate, advanced)",
                    "required": False,
                },
            ],
        ),
    ]
    return ListPromptsResult(prompts=prompts)


@server.get_prompt()
async def get_prompt(request: GetPromptRequest) -> GetPromptResult:
    """Get a specific prompt."""
    if request.name == "code_review":
        language = request.arguments.get("language", "Python")
        complexity = request.arguments.get("complexity", "intermediate")
        
        checklist_items = {
            "basic": [
                "Code follows naming conventions",
                "No obvious syntax errors",
                "Basic functionality works as expected",
            ],
            "intermediate": [
                "Code follows naming conventions",
                "Proper error handling",
                "Code is well-documented",
                "Unit tests are present",
                "No code duplication",
            ],
            "advanced": [
                "Code follows SOLID principles",
                "Comprehensive error handling",
                "Extensive documentation and comments",
                "Full test coverage",
                "Performance considerations",
                "Security best practices",
                "Code maintainability",
            ],
        }
        
        items = checklist_items.get(complexity, checklist_items["intermediate"])
        checklist = "\n".join([f"- {item}" for item in items])
        
        prompt_text = f"""Code Review Checklist for {language} ({complexity} level):

{checklist}

Please review the code against these criteria and provide detailed feedback."""
        
        return GetPromptResult(
            description=f"Code review checklist for {language}",
            messages=[
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": prompt_text,
                    },
                }
            ],
        )
    
    else:
        raise ValueError(f"Unknown prompt: {request.name}")


async def run_server() -> None:
    """Run the MCP server."""
    # Run the server using stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def main() -> None:
    """Main entry point for the CLI."""
    asyncio.run(run_server())


if __name__ == "__main__":
    main()

