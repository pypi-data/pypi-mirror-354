"""
Token search functions using various mesh API agents.
"""

import logging
import aiohttp
import os
import json
from typing import Dict, List, Optional, Any, Union
from .mesh_api import call_mesh_api, HEURIST_API_KEY

try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

logger = logging.getLogger(__name__)


class TokenSearchError(Exception):
    """Custom exception for token search errors."""
    pass


async def search_dex_pairs(token_name: str, chain_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Search for trading pairs on decentralized exchanges.
    
    Args:
        token_name: Name or symbol of the token to search
        chain_name: Optional chain name to filter results
        
    Returns:
        Dictionary containing DEX pair information
    """
    try:
        search_term = token_name
        if chain_name:
            search_term = f"{token_name} {chain_name}"
        
        request_data = {
            "agent_id": "DexScreenerTokenInfoAgent",
            "input": {
                "tool": "search_pairs",
                "tool_arguments": {"search_term": search_term}
            }
        }
        
        if HEURIST_API_KEY:
            request_data["api_key"] = HEURIST_API_KEY
        
        result = await call_mesh_api("mesh_request", method="POST", json=request_data)
        return result
        
    except Exception as e:
        logger.error(f"Error searching DEX pairs for {token_name}: {str(e)}")
        raise TokenSearchError(f"Failed to search DEX pairs: {str(e)}")


async def get_specific_pair_info(chain: str, pair_address: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific trading pair.
    
    Args:
        chain: Chain identifier (e.g., 'ethereum', 'bsc', 'polygon')
        pair_address: The pair contract address
        
    Returns:
        Dictionary containing detailed pair information
    """
    try:
        request_data = {
            "agent_id": "DexScreenerTokenInfoAgent",
            "input": {
                "tool": "get_specific_pair_info",
                "tool_arguments": {
                    "chain": chain,
                    "pair_address": pair_address
                }
            }
        }
        
        if HEURIST_API_KEY:
            request_data["api_key"] = HEURIST_API_KEY
        
        result = await call_mesh_api("mesh_request", method="POST", json=request_data)
        return result
        
    except Exception as e:
        logger.error(f"Error getting pair info for {chain}:{pair_address}: {str(e)}")
        raise TokenSearchError(f"Failed to get pair info: {str(e)}")


async def get_token_pairs(chain: str, token_address: str) -> Dict[str, Any]:
    """
    Get all trading pairs for a specific token on a blockchain.
    
    Args:
        chain: Chain identifier
        token_address: The token contract address
        
    Returns:
        Dictionary containing all pairs for the token
    """
    try:
        request_data = {
            "agent_id": "DexScreenerTokenInfoAgent",
            "input": {
                "tool": "get_token_pairs",
                "tool_arguments": {
                    "chain": chain,
                    "token_address": token_address
                }
            }
        }
        
        if HEURIST_API_KEY:
            request_data["api_key"] = HEURIST_API_KEY
        
        result = await call_mesh_api("mesh_request", method="POST", json=request_data)
        return result
        
    except Exception as e:
        logger.error(f"Error getting token pairs for {chain}:{token_address}: {str(e)}")
        raise TokenSearchError(f"Failed to get token pairs: {str(e)}")


async def get_token_security_details(contract_address: str, 
                                   chain_id: Union[str, int] = 1) -> Dict[str, Any]:
    """
    Fetch security details of a blockchain token contract by contract address.
    
    Args:
        contract_address: The token contract address
        chain_id: The blockchain chain ID or 'solana' for Solana tokens
        
    Returns:
        Dictionary containing security analysis of the token
    """
    try:
        request_data = {
            "agent_id": "GoAuditAgent",
            "input": {
                "tool": "fetch_security_details",
                "tool_arguments": {
                    "contract_address": contract_address,
                    "chain_id": str(chain_id)
                }
            }
        }
        
        if HEURIST_API_KEY:
            request_data["api_key"] = HEURIST_API_KEY
        
        result = await call_mesh_api("mesh_request", method="POST", json=request_data)
        return result
        
    except Exception as e:
        logger.error(f"Error getting security details for {contract_address}: {str(e)}")
        raise TokenSearchError(f"Failed to get security details: {str(e)}")


async def summarize_with_llm(search_results: Dict[str, Any], token_name: str) -> Optional[str]:
    """
    Use OpenAI LLM to summarize the token search results.
    
    Args:
        search_results: Dictionary containing results from different search tools
        token_name: The token name being searched
        
    Returns:
        String summary from LLM or None if OpenAI is not available
    """
    if not OPENAI_AVAILABLE:
        logger.warning("OpenAI library not available for summarization")
        return None
    
    # openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_api_key = "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"
    if not openai_api_key:
        logger.warning("OPENAI_API_KEY not found, skipping LLM summarization")
        return None
    
    try:
        client = AsyncOpenAI(api_key=openai_api_key)
        
        # Prepare the data for summarization (remove error entries and limit size)
        summary_data = {}
        for source, data in search_results.items():
            if isinstance(data, dict) and "error" not in data:
                # Limit the data size to avoid token limits
                data_str = json.dumps(data, default=str)
                if len(data_str) > 3000:  # Truncate large responses
                    summary_data[source] = f"{data_str[:3000]}... [truncated]"
                else:
                    summary_data[source] = data
            else:
                summary_data[source] = "No data available"
        
        prompt = f"""
        Please provide a comprehensive summary of the token "{token_name}" based on the following data from multiple sources:
        
        {json.dumps(summary_data, indent=2, default=str)}
        
        Please focus on and include:
        1. **Token Address & Chain Information**: List all token contract addresses found and their respective blockchain networks (Ethereum, BSC, Polygon, etc.)
        2. **Liquidity Analysis**: Analyze liquidity levels across different DEX pairs, including total liquidity in USD and most liquid trading pairs
        3. **Chain Distribution**: Which blockchains the token is available on and the trading activity on each chain
        4. **Current Market Metrics**: Price, market cap, 24h volume if available
        5. **Top Trading Pairs**: Most active trading pairs by volume and liquidity
        6. **DEX Presence**: Which decentralized exchanges have the token listed and their liquidity levels
        
        Prioritize token addresses, chain information, and liquidity data in your analysis. Keep the summary concise but detailed on these specific aspects.
        """
        
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a cryptocurrency analyst providing concise, factual summaries of token data."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.3
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Error generating LLM summary: {str(e)}")
        return None


# Convenience function for comprehensive token search by name
async def comprehensive_token_search(token_name: str, chain_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Perform a comprehensive search for a token by token name.
    
    Args:
        token_name: Name or symbol of the token
        chain_name: Optional chain name to filter DEX results
        
    Returns:
        Dictionary containing comprehensive token information
    """
    results = {}
    
    try:
        # DEX pair search (with optional chain filter)
        try:
            results['dex_pairs'] = await search_dex_pairs(token_name, chain_name)
        except Exception as e:
            logger.warning(f"Failed to get DEX data: {str(e)}")
            results['dex_pairs'] = {"error": str(e)}
        
        # Generate LLM summary of all results
        try:
            llm_summary = await summarize_with_llm(results, token_name)
            if llm_summary:
                results['llm_summary'] = llm_summary
            else:
                results['llm_summary'] = {"error": "LLM summarization not available"}
        except Exception as e:
            logger.warning(f"Failed to generate LLM summary: {str(e)}")
            results['llm_summary'] = {"error": str(e)}
        
        return results
        
    except Exception as e:
        logger.error(f"Error in comprehensive token search for {token_name}: {str(e)}")
        raise TokenSearchError(f"Comprehensive search failed: {str(e)}") 