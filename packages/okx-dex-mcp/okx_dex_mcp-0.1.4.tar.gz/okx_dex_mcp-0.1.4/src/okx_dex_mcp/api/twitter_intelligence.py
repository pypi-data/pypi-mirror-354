"""
Twitter intelligence functions using ElfaTwitterIntelligenceAgent.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from .mesh_api import call_mesh_api, HEURIST_API_KEY

logger = logging.getLogger(__name__)


class TwitterIntelligenceError(Exception):
    """Custom exception for Twitter intelligence errors."""
    pass


async def search_mentions(keywords: List[str], days_ago: int = 20, limit: int = 20) -> Dict[str, Any]:
    """
    Search for mentions of specific tokens or topics on Twitter.
    
    This tool finds discussions about cryptocurrencies, blockchain projects, or other topics of interest.
    It provides the tweets and mentions of smart accounts (only influential ones) and does not contain all tweets.
    Use this when you want to understand what influential people are saying about a particular token or topic on Twitter.
    Each of the search keywords should be one word or phrase. A maximum of 5 keywords are allowed.
    One key word should be one concept. Never use long sentences or phrases as keywords.
    
    Args:
        keywords: List of keywords to search for (maximum 5 keywords)
        days_ago: Number of days to look back (default: 20)
        limit: Maximum number of results (minimum: 20, maximum: 30, default: 20)
        
    Returns:
        Dictionary containing Twitter mentions and discussions
        
    Raises:
        TwitterIntelligenceError: If there's an error searching for mentions
    """
    # Validate inputs
    if not keywords:
        raise TwitterIntelligenceError("Keywords list cannot be empty")
    
    if len(keywords) > 5:
        raise TwitterIntelligenceError("Maximum of 5 keywords are allowed")
    
    if limit < 20:
        limit = 20
    elif limit > 30:
        limit = 30
    
    request_data = {
        "agent_id": "ElfaTwitterIntelligenceAgent",
        "input": {
            "tool": "search_mentions",
            "tool_arguments": {
                "keywords": keywords,
                "days_ago": days_ago,
                "limit": limit
            }
        }
    }
    
    if HEURIST_API_KEY:
        request_data["api_key"] = HEURIST_API_KEY
    
    try:
        result = await call_mesh_api("mesh_request", method="POST", json=request_data)
        return result
    except Exception as e:
        logger.error(f"Error searching Twitter mentions for keywords {keywords}: {str(e)}")
        raise TwitterIntelligenceError(f"Failed to search Twitter mentions: {str(e)}")


async def search_account(username: str, days_ago: int = 30, limit: int = 20) -> Dict[str, Any]:
    """
    Search for a Twitter account with both mention search and account statistics.
    
    This tool provides engagement metrics, follower growth, and mentions by smart users.
    It does not contain all tweets, but only those of influential users. It also identifies
    the topics and cryptocurrencies they frequently discuss. Data comes from ELFA API
    and can analyze several weeks of historical activity.
    
    Args:
        username: Twitter username to analyze (without @)
        days_ago: Number of days to look back for mentions (default: 30)
        limit: Maximum number of mention results (default: 20)
        
    Returns:
        Dictionary containing account statistics and mentions
        
    Raises:
        TwitterIntelligenceError: If there's an error analyzing the account
    """
    try:
        if not username:
            raise TwitterIntelligenceError("Username cannot be empty")
        
        # Remove @ if present
        username = username.lstrip('@')
        
        request_data = {
            "agent_id": "ElfaTwitterIntelligenceAgent",
            "input": {
                "tool": "search_account",
                "tool_arguments": {
                    "username": username,
                    "days_ago": days_ago,
                    "limit": limit
                }
            }
        }
        
        if HEURIST_API_KEY:
            request_data["api_key"] = HEURIST_API_KEY
        
        result = await call_mesh_api("mesh_request", method="POST", json=request_data)
        return result
        
    except Exception as e:
        logger.error(f"Error analyzing Twitter account {username}: {str(e)}")
        raise TwitterIntelligenceError(f"Failed to analyze Twitter account: {str(e)}")


async def get_trending_tokens(time_window: str = "24h") -> Dict[str, Any]:
    """
    Get current trending tokens on Twitter.
    
    This tool identifies which cryptocurrencies and tokens are generating the most buzz on Twitter right now.
    The results include token names, their relative popularity, and sentiment indicators.
    Use this when you want to discover which cryptocurrencies are currently being discussed
    most actively on social media. Data comes from ELFA API and represents real-time trends.
    
    Args:
        time_window: Time window to analyze (default: "24h")
        
    Returns:
        Dictionary containing trending tokens and their metrics
        
    Raises:
        TwitterIntelligenceError: If there's an error fetching trending tokens
    """
    try:
        request_data = {
            "agent_id": "ElfaTwitterIntelligenceAgent",
            "input": {
                "tool": "get_trending_tokens",
                "tool_arguments": {
                    "time_window": time_window
                }
            }
        }
        
        if HEURIST_API_KEY:
            request_data["api_key"] = HEURIST_API_KEY
        
        result = await call_mesh_api("mesh_request", method="POST", json=request_data)
        return result
        
    except Exception as e:
        logger.error(f"Error getting trending tokens: {str(e)}")
        raise TwitterIntelligenceError(f"Failed to get trending tokens: {str(e)}")


# Internal wrapper functions to return string results for MCP tools
async def search_mentions_internal(keywords: List[str], days_ago: int = 20, limit: int = 20) -> str:
    """Internal wrapper for search_mentions that returns formatted string."""
    try:
        result = await search_mentions(keywords, days_ago, limit)
        
        # Format the result for display
        if isinstance(result, dict) and "data" in result:
            response_data = result["data"]
            if isinstance(response_data, dict) and "data" in response_data:
                inner_data = response_data["data"]
                
                # Check for the actual structure: data.data.data (list of mentions)
                if isinstance(inner_data, dict) and "data" in inner_data:
                    mentions = inner_data["data"]
                    if isinstance(mentions, list) and mentions:
                        formatted_result = f"Twitter mentions for keywords {keywords} (last {days_ago} days):\n\n"
                        formatted_result += f"Total mentions found: {len(mentions)}\n"
                        formatted_result += f"Status: {response_data.get('status', 'N/A')}\n"
                        formatted_result += f"Success: {inner_data.get('success', 'N/A')}\n\n"
                        
                        # Limit the number of mentions to display
                        display_limit = min(limit, len(mentions))
                        for i, mention in enumerate(mentions[:display_limit]):
                            formatted_result += f"--- Mention {i+1} ---\n"
                            formatted_result += f"Content: {mention.get('content', 'N/A')}\n"
                            formatted_result += f"Date: {mention.get('mentioned_at', 'N/A')}\n"
                            formatted_result += f"Type: {mention.get('type', 'N/A')}\n"
                            formatted_result += f"Sentiment: {mention.get('sentiment', 'N/A')}\n"
                            
                            # Format metrics
                            metrics = mention.get('metrics', {})
                            if metrics:
                                formatted_result += f"Metrics:\n"
                                formatted_result += f"  - Likes: {metrics.get('like_count', 0)}\n"
                                formatted_result += f"  - Replies: {metrics.get('reply_count', 0)}\n"
                                formatted_result += f"  - Reposts: {metrics.get('repost_count', 0)}\n"
                                formatted_result += f"  - Views: {metrics.get('view_count', 0)}\n"
                            formatted_result += "\n"
                        
                        if len(mentions) > display_limit:
                            formatted_result += f"... and {len(mentions) - display_limit} more mentions\n"
                        
                        return formatted_result
                
                # Fallback for different structure (mentions key)
                elif isinstance(inner_data, dict) and "mentions" in inner_data:
                    mentions = inner_data["mentions"]
                    if mentions:
                        formatted_result = f"Twitter mentions for keywords {keywords} (last {days_ago} days):\n\n"
                        for i, mention in enumerate(mentions[:limit]):
                            formatted_result += f"--- Mention {i+1} ---\n"
                            formatted_result += f"Author: {mention.get('author', 'N/A')}\n"
                            formatted_result += f"Text: {mention.get('text', 'N/A')}\n"
                            formatted_result += f"Engagement: {mention.get('engagement', 'N/A')}\n"
                            formatted_result += f"Date: {mention.get('date', 'N/A')}\n\n"
                        return formatted_result
        
        # Return full result if structure doesn't match expected format
        return f"Twitter mentions search completed for keywords: {keywords}\n\nFull result:\n{str(result)}"
        
    except Exception as e:
        return f"Error searching Twitter mentions: {str(e)}"


async def search_account_internal(username: str, days_ago: int = 30, limit: int = 20) -> str:
    """Internal wrapper for search_account that returns formatted string."""
    try:
        result = await search_account(username, days_ago, limit)
        
        # Format the result for display
        if isinstance(result, dict) and "data" in result and "data" in result["data"]:
            # The structure is: result['data']['data'] contains the actual data
            data = result["data"]["data"]
            formatted_result = f"Twitter account analysis for @{username}:\n\n"
            
            # Extract account stats
            if "account_stats" in data and "data" in data["account_stats"]:
                stats = data["account_stats"]["data"]
                formatted_result += "📊 Account Statistics:\n"
                formatted_result += f"   • Smart Following Count: {stats.get('smartFollowingCount', 'N/A')}\n"
                formatted_result += f"   • Average Engagement: {stats.get('averageEngagement', 'N/A')}\n"
                formatted_result += f"   • Follower Engagement Ratio: {stats.get('followerEngagementRatio', 'N/A')}\n\n"
            
            # Extract mentions
            if "mentions" in data and "data" in data["mentions"]:
                mentions = data["mentions"]["data"]
                formatted_result += f"🐦 Recent Mentions ({len(mentions)} total):\n\n"
                
                for i, mention in enumerate(mentions, 1):  # Show ALL mentions
                    content = mention.get('content', '')  # Show full content without truncation
                    metrics = mention.get('metrics', {})
                    sentiment = mention.get('sentiment', 'neutral')
                    mention_type = mention.get('type', 'unknown')
                    mentioned_at = mention.get('mentioned_at', '')
                    
                    formatted_result += f"{i}. [{mention_type.upper()}] {mentioned_at}\n"
                    formatted_result += f"   Content: {content}\n"
                    formatted_result += f"   Metrics: ❤️{metrics.get('like_count', 0)} 🔄{metrics.get('repost_count', 0)} 💬{metrics.get('reply_count', 0)} 👀{metrics.get('view_count', 0)}\n"
                    formatted_result += f"   Sentiment: {sentiment}\n\n"
            
            return formatted_result
        
        return f"Twitter account analysis completed for @{username}\n\nFull result:\n{str(result)}"
        
    except Exception as e:
        return f"Error analyzing Twitter account: {str(e)}"


async def get_trending_tokens_internal(time_window: str = "24h") -> str:
    """Internal wrapper for get_trending_tokens that returns formatted string."""
    try:
        result = await get_trending_tokens(time_window)
        
        # Format the result for display
        if isinstance(result, dict) and "data" in result:
            response_data = result["data"]
            if isinstance(response_data, dict) and "data" in response_data:
                inner_data = response_data["data"]
                
                # Check for the actual structure from the response
                if isinstance(inner_data, dict) and "data" in inner_data:
                    tokens_data = inner_data["data"]
                    if isinstance(tokens_data, dict) and "data" in tokens_data:
                        tokens = tokens_data["data"]
                        if tokens:
                            formatted_result = f"Trending tokens on Twitter ({time_window}):\n\n"
                            formatted_result += f"Total tokens: {tokens_data.get('total', 'N/A')}\n"
                            formatted_result += f"Page: {tokens_data.get('page', 'N/A')}\n"
                            formatted_result += f"Page Size: {tokens_data.get('pageSize', 'N/A')}\n\n"
                            
                            for i, token in enumerate(tokens):
                                formatted_result += f"--- Rank {i+1} ---\n"
                                formatted_result += f"Token: {token.get('token', 'N/A')}\n"
                                formatted_result += f"Current Count: {token.get('current_count', 'N/A')}\n"
                                formatted_result += f"Previous Count: {token.get('previous_count', 'N/A')}\n"
                                formatted_result += f"Change Percent: {token.get('change_percent', 'N/A')}%\n\n"
                            return formatted_result
                
                # If trending_tokens structure (fallback)
                elif isinstance(inner_data, dict) and "trending_tokens" in inner_data:
                    tokens = inner_data["trending_tokens"]
                    if tokens:
                        formatted_result = f"Trending tokens on Twitter ({time_window}):\n\n"
                        for i, token in enumerate(tokens):
                            formatted_result += f"--- Rank {i+1} ---\n"
                            formatted_result += f"Symbol: {token.get('symbol', 'N/A')}\n"
                            formatted_result += f"Mentions: {token.get('mentions', 'N/A')}\n"
                            formatted_result += f"Sentiment: {token.get('sentiment', 'N/A')}\n"
                            formatted_result += f"Trend Score: {token.get('trend_score', 'N/A')}\n\n"
                        return formatted_result
        
        # Return full result if structure doesn't match expected format
        return f"Trending tokens analysis completed ({time_window}):\n\n{str(result)}"
        
    except Exception as e:
        return f"Error getting trending tokens: {str(e)}"


def register_twitter_intelligence_tools(mcp):
    """Register Twitter intelligence related MCP tools."""
    
    @mcp.tool()
    async def search_twitter_mentions(keywords: List[str], days_ago: int = 20, limit: int = 20) -> str:
        """Search for mentions of specific tokens or topics on Twitter.
        
        This tool finds discussions about cryptocurrencies, blockchain projects, or other topics of interest.
        It provides the tweets and mentions of smart accounts (only influential ones) and does not contain all tweets.
        Use this when you want to understand what influential people are saying about a particular token or topic on Twitter.
        Each of the search keywords should be one word or phrase. A maximum of 5 keywords are allowed.
        One key word should be one concept. Never use long sentences or phrases as keywords.

        Args:
            keywords: List of keywords to search for (maximum 5 keywords)
            days_ago: Number of days to look back (default: 20)
            limit: Maximum number of results (minimum: 20, maximum: 30, default: 20)
        """
        return await search_mentions_internal(keywords, days_ago, limit)
    
    @mcp.tool()
    async def search_twitter_account(username: str, days_ago: int = 30, limit: int = 20) -> str:
        """Search for a Twitter account with both mention search and account statistics.
        
        This tool provides engagement metrics, follower growth, and mentions by smart users.
        It does not contain all tweets, but only those of influential users. It also identifies
        the topics and cryptocurrencies they frequently discuss. Data comes from ELFA API
        and can analyze several weeks of historical activity.

        Args:
            username: Twitter username to analyze (without @)
            days_ago: Number of days to look back for mentions (default: 30)
            limit: Maximum number of mention results (default: 20)
        """
        return await search_account_internal(username, days_ago, limit)
    
    @mcp.tool()
    async def get_twitter_trending_tokens(time_window: str = "24h") -> str:
        """Get current trending tokens on Twitter.
        
        This tool identifies which cryptocurrencies and tokens are generating the most buzz on Twitter right now.
        The results include token names, their relative popularity, and sentiment indicators.
        Use this when you want to discover which cryptocurrencies are currently being discussed
        most actively on social media. Data comes from ELFA API and represents real-time trends.

        Args:
            time_window: Time window to analyze (default: "24h")
        """
        return await get_trending_tokens_internal(time_window)
 