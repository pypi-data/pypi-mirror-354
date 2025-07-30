"""
Market data and token information from OKX DEX API.
"""
from dotenv import load_dotenv

from ..utils.constants import OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE, OKX_API_BASE
from ..utils.formatters import format_chain_tokens
from .okx_client import make_okx_request
from .mesh_api import call_mesh_api, HEURIST_API_KEY

# Load environment variables for mesh API
load_dotenv()


async def get_supported_dex_chains_internal() -> str:
    """Get list of supported chains for DEX operations."""
    if not all([OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE]):
        return "❌ OKX API credentials not configured. Please set OKX_API_KEY, OKX_SECRET_KEY, and OKX_PASSPHRASE in .env file."
    
    url = f"{OKX_API_BASE}/api/v5/dex/aggregator/supported/chain"
    data = await make_okx_request(url)

    if not data:
        return "Unable to fetch supported DEX chains."

    if data.get("code") != "0":
        return f"API Error: {data.get('msg', 'Unknown error')}"

    chains = data.get("data", [])
    if not chains:
        return "No supported chains found."

    result = "Supported DEX Chains:\n\n"
    for chain in chains:
        chain_id = chain.get('chainId', 'Unknown')
        chain_name = chain.get('chainName', 'Unknown')
        
        result += f"• {chain_name} (ID: {chain_id})\n"
    
    return result


async def get_chain_top_tokens_internal(chain_id: str, limit: int = 20) -> str:
    """Get top tokens by market cap on a specific chain."""
    if not all([OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE]):
        return "❌ OKX API credentials not configured. Please set OKX_API_KEY, OKX_SECRET_KEY, and OKX_PASSPHRASE in .env file."
    
    if limit > 50:
        limit = 50
        
    url = f"{OKX_API_BASE}/api/v5/dex/aggregator/all-tokens?chainId={chain_id}&limit={limit}"
    data = await make_okx_request(url)

    if not data:
        return f"Unable to fetch top tokens for chain {chain_id}."

    if data.get("code") != "0":
        return f"API Error: {data.get('msg', 'Unknown error')}"

    tokens = data.get("data", [])
    if not tokens:
        return f"No tokens found for chain {chain_id}."

    return format_chain_tokens(tokens, chain_id)


def normalize(s):
    return s.lower().replace('.', '').replace('-', '').replace(' ', '')


async def search_dex_tokens_internal(token_name: str, chain_name: str = "") -> str:
    """Search for DEX tokens by name or symbol using DexScreener mesh agent."""
    try:
        # Build search term by concatenating token name and chain name if provided
        search_term = token_name
        if chain_name:
            search_term = f"{token_name} {chain_name}"
        
        # Call DexScreener mesh agent - using the correct structure from server.py
        request_data = {
            "agent_id": "DexScreenerTokenInfoAgent",
            "input": {
                "tool": "search_pairs",
                "tool_arguments": {"search_term": search_term}
            }
        }
        
        # Add API key if available (as per server.py implementation)
        if HEURIST_API_KEY:
            request_data["api_key"] = HEURIST_API_KEY
        
        result = await call_mesh_api("mesh_request", method="POST", json=request_data)
        
        # Handle the actual mesh response format - nested structure
        # The result structure is: result -> data -> data -> pairs
        response_data = result.get("data", {})
        if isinstance(response_data, dict) and "data" in response_data:
            inner_data = response_data["data"]
            if isinstance(inner_data, dict) and "pairs" in inner_data:
                pairs = inner_data["pairs"]
            else:
                pairs = []
        else:
            pairs = []
        
        if not pairs:
            return f"No DEX tokens found matching: {search_term}"
        
        # Extract unique tokens from pairs
        unique_tokens = {}
        for pair in pairs:
            base_token = pair.get("baseToken", {})
            quote_token = pair.get("quoteToken", {})
            chain_info = pair.get("chainId", "")
            
            # Process base token
            if base_token.get("address"):
                token_address = base_token["address"]
                
                if token_address not in unique_tokens:
                    unique_tokens[token_address] = {
                        "tokenSymbol": base_token.get("symbol", "N/A"),
                        "tokenName": base_token.get("name", "N/A"),
                        "tokenContractAddress": token_address,
                        "chainId": chain_info,
                        "decimals": "N/A",  # DexScreener doesn't always provide decimals
                        "priceUsd": pair.get("priceUsd", "N/A"),
                        "dexId": pair.get("dexId", "N/A"),
                        "liquidity": pair.get("liquidity", {}).get("usd", "N/A")
                    }
            
            # Process quote token
            if quote_token.get("address"):
                token_address = quote_token["address"]
                
                if token_address not in unique_tokens:
                    unique_tokens[token_address] = {
                        "tokenSymbol": quote_token.get("symbol", "N/A"),
                        "tokenName": quote_token.get("name", "N/A"),
                        "tokenContractAddress": token_address,
                        "chainId": chain_info,
                        "decimals": "N/A",
                        "priceUsd": "N/A",  # Quote tokens don't have price in this context
                        "dexId": pair.get("dexId", "N/A"),
                        "liquidity": pair.get("liquidity", {}).get("usd", "N/A")
                    }
        
        if not unique_tokens:
            return f"No DEX tokens found matching: {search_term}"
        
        # Format the response
        tokens_list = list(unique_tokens.values())
        result_text = f"DEX tokens matching '{search_term}' ({len(tokens_list)} found):\n\n"
        
        for i, token in enumerate(tokens_list[:10]):  # Top 10 results
            symbol = token.get('tokenSymbol', 'N/A')
            name = token.get('tokenName', 'N/A')
            address = token.get('tokenContractAddress', 'N/A')
            chain = token.get('chainId', 'Unknown')
            decimals = token.get('decimals', 'N/A')
            price_usd = token.get('priceUsd', 'N/A')
            dex_id = token.get('dexId', 'N/A')
            liquidity = token.get('liquidity', 'N/A')
            
            result_text += f"--- Result {i+1} ---\n"
            result_text += f"Token Symbol: {symbol}\n"
            result_text += f"Token Name: {name}\n"
            result_text += f"Contract Address: {address}\n"
            result_text += f"Chain ID: {chain}\n"
            result_text += f"Decimals: {decimals}\n"
            if price_usd != "N/A":
                result_text += f"Price USD: ${price_usd}\n"
            if liquidity != "N/A":
                result_text += f"Liquidity USD: ${liquidity}\n"
            result_text += f"Primary DEX: {dex_id}\n\n"
        
        return result_text
        
    except Exception as e:
        return f"Error searching for tokens: {str(e)}"


async def get_dex_market_summary_internal(token_query: str, chain_id: str = "1") -> str:
    """Get a comprehensive DEX market summary for a token."""
    if not all([OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE]):
        return "❌ OKX API credentials not configured. Please set OKX_API_KEY, OKX_SECRET_KEY, and OKX_PASSPHRASE in .env file."
    
    # First search for the token
    search_results = await search_dex_tokens_internal(token_query)
    
    if "No DEX tokens found" in search_results:
        return search_results
    
    # Try to get additional chain information
    chains_info = await get_supported_dex_chains_internal()
    
    result = f"=== DEX MARKET SUMMARY FOR {token_query.upper()} ===\n\n"
    result += "TOKEN SEARCH RESULTS:\n"
    result += search_results + "\n"
    result += "=" * 60 + "\n\n"
    result += "AVAILABLE CHAINS:\n"
    result += chains_info[:500] + "..." if len(chains_info) > 500 else chains_info
    
    return result


def register_market_data_tools(mcp):
    """Register market data related MCP tools."""
    
    @mcp.tool()
    async def get_supported_dex_chains() -> str:
        """Get list of supported chains for DEX operations."""
        return await get_supported_dex_chains_internal()
    
    @mcp.tool()
    async def get_chain_top_tokens(chain_id: str, limit: int = 20) -> str:
        """Get top tokens by market cap on a specific chain.

        Args:
            chain_id: Chain ID (e.g., "1" for Ethereum, "56" for BSC)
            limit: Number of tokens to return (max 50)
        """
        return await get_chain_top_tokens_internal(chain_id, limit)
    
    @mcp.tool()
    async def search_dex_tokens(token_name: str, chain_name: str = "") -> str:
        """Search for DEX tokens by name or symbol.

        Args:
            token_name: Token name or symbol to search for
            chain_name: Optional chain name to include in search (e.g., "Polygon", "Ethereum")
        """
        return await search_dex_tokens_internal(token_name, chain_name)
    
    @mcp.tool()
    async def get_dex_market_summary(token_query: str, chain_id: str = "1") -> str:
        """Get a comprehensive DEX market summary for a token.

        Args:
            token_query: Token symbol or name to search for
            chain_id: Chain ID to search on (default: "1" for Ethereum)
        """
        return await get_dex_market_summary_internal(token_query, chain_id) 