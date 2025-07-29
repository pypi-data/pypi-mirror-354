"""
StackOverflow MCP Server using FastMcp framework.
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from fastmcp import FastMCP
from fastmcp.resources import Resource

from .config import ServerConfig
from .logging import get_logger
from .stackoverflow_client import StackOverflowClient, RequestPriority

logger = get_logger("fastmcp_server")

# Initialize FastMcp
mcp = FastMCP("StackOverflow MCP Server")


class StackOverflowServer:
    """FastMcp-based StackOverflow server."""
    
    def __init__(self, config: ServerConfig):
        self.config = config
        self.client: Optional[StackOverflowClient] = None
        
    async def initialize(self):
        """Initialize the StackOverflow client."""
        if not self.client:
            self.client = StackOverflowClient(self.config)
            await self.client.__aenter__()
    
    async def cleanup(self):
        """Cleanup resources."""
        if self.client:
            await self.client.__aexit__(None, None, None)
    

# Global server instance
server = StackOverflowServer(ServerConfig())


@mcp.tool()
async def search_questions(
    query: str,
    limit: int = 10,
    page: int = 1,
    sort: str = "relevance"
) -> Dict[str, Any]:
    """
    Search StackOverflow questions by keywords.
    
    Args:
        query: Search query keywords
        limit: Maximum number of results (1-50)
        page: Page number for pagination (minimum 1)
        sort: Sort order (relevance, activity, votes, creation)
    """
    await server.initialize()
    
    try:
        result = await server.client.search_questions(
            query=query,
            page=page,
            page_size=min(max(1, limit), 50),
            sort=sort,
            priority=RequestPriority.NORMAL
        )
        
        logger.info(f"Search completed: {query} -> {result.get('total', 0)} results")
        return result
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        return {
            "error": str(e),
            "success": False,
            "total": 0,
            "questions": []
        }


@mcp.tool()
async def search_by_tags(
    tags: List[str],
    limit: int = 10,
    page: int = 1,
    sort: str = "activity"
) -> Dict[str, Any]:
    """
    Search StackOverflow questions by programming tags.
    
    Args:
        tags: List of tags to search for (e.g., ['python', 'async'])
        limit: Maximum number of results (1-50)
        page: Page number for pagination (minimum 1)
        sort: Sort order (activity, votes, creation, relevance)
    """
    await server.initialize()
    
    try:
        result = await server.client.search_by_tags(
            tags=tags,
            page=page,
            page_size=min(max(1, limit), 50),
            sort=sort,
            priority=RequestPriority.NORMAL
        )
        
        logger.info(f"Tag search completed: {tags} -> {result.get('total', 0)} results")
        return result
        
    except Exception as e:
        logger.error(f"Tag search error: {e}")
        return {
            "error": str(e),
            "success": False,
            "total": 0,
            "questions": []
        }


@mcp.tool()
async def get_question(
    question_id: int,
    include_answers: bool = True,
    convert_to_markdown: bool = True
) -> Dict[str, Any]:
    """
    Get detailed information about a specific question.
    
    Args:
        question_id: StackOverflow question ID
        include_answers: Whether to include answers
        convert_to_markdown: Convert HTML content to markdown
    """
    await server.initialize()
    
    try:
        result = await server.client.get_question_details(
            question_id=question_id,
            include_answers=include_answers,
            priority=RequestPriority.HIGH
        )
        
        logger.info(f"Question details retrieved: {question_id}")
        return result
        
    except Exception as e:
        logger.error(f"Get question error: {e}")
        return {
            "error": str(e),
            "success": False,
            "question_id": question_id
        }


@mcp.tool()
async def get_question_with_answers(
    question_id: int,
    max_answers: int = 5,
    convert_to_markdown: bool = True
) -> Dict[str, Any]:
    """
    Get comprehensive question details including all answers.
    
    Args:
        question_id: StackOverflow question ID
        max_answers: Maximum number of answers to include (1-20)
        convert_to_markdown: Convert HTML content to markdown
    """
    await server.initialize()
    
    try:
        result = await server.client.get_question_details(
            question_id=question_id,
            include_answers=True,
            priority=RequestPriority.HIGH
        )
        
        # Limit answers if needed
        if "answers" in result and len(result["answers"]) > max_answers:
            result["answers"] = result["answers"][:max_answers]
            result["answers_limited"] = True
            result["total_answers"] = len(result["answers"])
        
        logger.info(f"Question with answers retrieved: {question_id}")
        return result
        
    except Exception as e:
        logger.error(f"Get question with answers error: {e}")
        return {
            "error": str(e),
            "success": False,
            "question_id": question_id
        }


@mcp.tool()
async def get_rate_limit_status() -> Dict[str, Any]:
    """Get current rate limiting status and quotas for monitoring."""
    await server.initialize()
    
    try:
        status = server.client.get_rate_limit_status()
        logger.debug("Rate limit status retrieved")
        return status
        
    except Exception as e:
        logger.error(f"Rate limit status error: {e}")
        return {
            "error": str(e),
            "success": False
        }


@mcp.tool()
async def get_authentication_status() -> Dict[str, Any]:
    """Get current API authentication status and quota information."""
    await server.initialize()
    
    try:
        status = server.client.get_authentication_status()
        logger.debug("Authentication status retrieved")
        return status
        
    except Exception as e:
        logger.error(f"Authentication status error: {e}")
        return {
            "error": str(e),
            "success": False
        }


@mcp.tool()
async def get_queue_status() -> Dict[str, Any]:
    """Get current request queue status, cache statistics, and auto-switching information."""
    await server.initialize()
    
    try:
        status = server.client.get_queue_status()
        logger.debug("Queue status retrieved")
        return status
        
    except Exception as e:
        logger.error(f"Queue status error: {e}")
        return {
            "error": str(e),
            "success": False
        }


@mcp.resource("stackoverflow://status")
async def server_status() -> Resource:
    """Current server status and configuration."""
    await server.initialize()
    
    try:
        status_data = {
            "server": "StackOverflow MCP Server",
            "version": "0.2.2",
            "config": {
                "host": server.config.host,
                "port": server.config.port,
                "log_level": server.config.log_level,
                "api_key_configured": bool(server.config.stackoverflow_api_key)
            },
            "client_status": {
                "authenticated": server.client.get_authentication_status() if server.client else None,
                "rate_limit": server.client.get_rate_limit_status() if server.client else None,
                "queue": server.client.get_queue_status() if server.client else None
            }
        }
        
        return Resource(
            uri="stackoverflow://status",
            name="Server Status",
            description="Current server status and configuration", 
            text=json.dumps(status_data, indent=2)
        )
        
    except Exception as e:
        logger.error(f"Server status error: {e}")
        error_data = {
            "error": str(e),
            "server": "StackOverflow MCP Server",
            "status": "error"
        }
        
        return Resource(
            uri="stackoverflow://status",
            name="Server Status (Error)",
            description="Server status with error",
            text=json.dumps(error_data, indent=2)
        )


async def run_server(config: ServerConfig):
    """Run the FastMcp server."""
    global server
    server = StackOverflowServer(config)
    
    try:
        logger.info("Starting StackOverflow MCP Server with FastMcp")
        logger.info(f"Host: {config.host}, Port: {config.port}")
        
        # Start FastMcp server with proper asyncio handling
        try:
            await mcp.run(transport="stdio")
        except RuntimeError as e:
            if "already running" in str(e).lower():
                logger.warning("AsyncIO loop already running, using alternative startup method")
                # Alternative: create a new event loop in a thread
                import threading
                import asyncio
                
                def run_in_thread():
                    new_loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(new_loop)
                    try:
                        new_loop.run_until_complete(mcp.run(transport="stdio"))
                    finally:
                        new_loop.close()
                
                thread = threading.Thread(target=run_in_thread, daemon=True)
                thread.start()
                
                # Keep main thread alive
                try:
                    while thread.is_alive():
                        await asyncio.sleep(1)
                except KeyboardInterrupt:
                    logger.info("Received interrupt signal")
            else:
                raise
        
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise
    finally:
        await server.cleanup()
        logger.info("Server shutdown complete")


def create_app(config: ServerConfig):
    """Create FastMcp app instance."""
    global server
    server = StackOverflowServer(config)
    return mcp 