"""
Same-chain DEX quote operations.
"""

import aiohttp
from ..utils.formatters import format_dex_quote, get_slippage_recommendation
from ..utils.blockchain import is_evm_chain


def convert_decimal_to_minimal_units(decimal_amount: str, decimals: int) -> str:
    """Convert decimal amount to minimal divisible units.
    
    Args:
        decimal_amount: Amount in decimal format (e.g., "1.5" for 1.5 tokens)
        decimals: Number of decimals for the token (e.g., 18 for most ERC20 tokens, 6 for USDC)
    
    Returns:
        str: Amount in minimal divisible units (e.g., "1500000000000000000" for 1.5 ETH)
    
    Examples:
        convert_decimal_to_minimal_units("1.0", 18) -> "1000000000000000000"  # 1 ETH
        convert_decimal_to_minimal_units("1.0", 6) -> "1000000"  # 1 USDC
        convert_decimal_to_minimal_units("0.1", 6) -> "100000"  # 0.1 USDC
    """
    try:
        # Convert to float first to handle decimal input
        amount_float = float(decimal_amount)
        # Multiply by 10^decimals to get minimal units
        minimal_units = int(amount_float * (10 ** decimals))
        return str(minimal_units)
    except (ValueError, OverflowError) as e:
        raise ValueError(f"Invalid decimal amount '{decimal_amount}': {str(e)}")


async def get_dex_quote_internal(from_token: str, to_token: str, chain_id: str, 
                               from_address: str, decimal_amount: str,
                               from_token_decimals: int) -> str:
    """Get a DEX trading quote for token swap with improved slippage recommendations.
    
    Args:
        from_token: From token contract address
        to_token: To token contract address  
        chain_id: Chain ID (e.g., "1" for Ethereum, "56" for BSC)
        from_address: The address that will be executing the swap (required)
        decimal_amount: Decimal amount (e.g., "0.1" for 0.1 tokens)
        from_token_decimals: Decimals of the from_token
    """
    if not is_evm_chain(chain_id):
        return f"❌ Error: Only EVM chains are supported for same-chain quote. Chain {chain_id} is not EVM."
    
    if not from_address:
        return "❌ from_address is required. Please provide the wallet address that will execute the swap."
    
    try:
        amount = convert_decimal_to_minimal_units(decimal_amount, from_token_decimals)
    except ValueError as e:
        return f"❌ Error converting decimal amount: {str(e)}"
    
    # Prepare request payload
    payload = {
        "fromTokenAddress": from_token,
        "toTokenAddress": to_token,
        "fromAddress": from_address,
        "amount": amount,
        "chainIndex": chain_id
    }
    
    # Make request to new endpoint
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                "https://mcp-node-server-264441234562.us-central1.run.app/evm/quote",
                json=payload
            ) as response:
                if response.status != 200:
                    return f"❌ API Error: Status {response.status}"
                
                data = await response.json()
                
                if not data:
                    return f"❌ Unable to get quote for {from_token} -> {to_token}."
                
                if "error" in data:
                    return f"❌ API Error: {data['error']}"
                
                # Flatten the response for the formatters
                data_dict = data.get("data", {})
                data_list = data_dict.get("data", [])
                quote_data = data_list[0] if isinstance(data_list, list) and data_list else {}
                if "routerResult" in quote_data:
                    quote_data = quote_data["routerResult"]

                # Format the response
                formatted_quote = format_dex_quote(quote_data)
                slippage_guidance = get_slippage_recommendation(quote_data)
                
                return formatted_quote + slippage_guidance
                
        except Exception as e:
            return f"❌ Error making request: {str(e)}"

def register_same_chain_quote_tools(mcp):
    """Register same-chain quote related MCP tools."""
    
    @mcp.tool()
    async def get_dex_quote(from_token: str, to_token: str, chain_id: str, 
                          from_address: str, decimal_amount: str,
                          from_token_decimals: int) -> str:
        """Get a DEX trading quote for token swap with improved slippage recommendations.

        Args:
            from_token: From token contract address
            to_token: To token contract address  
            chain_id: Chain ID (e.g., "1" for Ethereum, "56" for BSC)
            from_address: The address that will be executing the swap (required)
            decimal_amount: Decimal amount (e.g., "0.1" for 0.1 tokens)
            from_token_decimals: Decimals of the from_token
        """
        return await get_dex_quote_internal(from_token, to_token, chain_id, 
                                          from_address, decimal_amount, from_token_decimals)