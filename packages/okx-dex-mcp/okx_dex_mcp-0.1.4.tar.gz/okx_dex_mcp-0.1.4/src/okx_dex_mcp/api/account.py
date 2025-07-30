"""
Account and wallet analysis functionality using Zerion Wallet Analysis Agent (EVM) and SolWalletAgent (Solana).
"""

from .mesh_api import call_mesh_api, HEURIST_API_KEY


async def fetch_evm_wallet_tokens_internal(wallet_address: str) -> str:
    """
    Fetch token holdings of an EVM wallet using ZerionWalletAnalysisAgent.
    
    Args:
        wallet_address: The EVM wallet address (starting with 0x and 42-character long) 
                       to analyze. Can also use 'SELF' for user's own wallet address.
    
    Returns:
        Formatted string containing EVM wallet token holdings information
    """
    try:
        # Validate wallet address format (unless it's 'SELF')
        if wallet_address.upper() != 'SELF':
            if not wallet_address.startswith('0x') or len(wallet_address) != 42:
                return "❌ Invalid wallet address format. Please provide a valid EVM wallet address starting with 0x and 42 characters long."
        
        # Build request data for ZerionWalletAnalysisAgent
        request_data = {
            "agent_id": "ZerionWalletAnalysisAgent",
            "input": {
                "tool": "fetch_wallet_tokens",
                "tool_arguments": {
                    "wallet_address": wallet_address
                }
            }
        }
        
        # Add API key if available
        if HEURIST_API_KEY:
            request_data["api_key"] = HEURIST_API_KEY
        
        # Call the mesh API
        result = await call_mesh_api("mesh_request", method="POST", json=request_data)
        
        # Debug: Print the raw response to understand the structure
        print("=== RAW API RESPONSE ===")
        print(f"Result type: {type(result)}")
        print(f"Result: {result}")
        print("========================")
        
        # Handle the mesh response format
        if not result:
            return "❌ Failed to get response from Zerion Wallet Analysis Agent."
        
        # Extract data from nested response structure
        response_data = result.get("data", {})
        if isinstance(response_data, dict) and "data" in response_data:
            wallet_data = response_data["data"]
        else:
            wallet_data = response_data
        
        print("=== WALLET DATA ===")
        print(f"Wallet data type: {type(wallet_data)}")
        print(f"Wallet data: {wallet_data}")
        print("===================")
        
        # Check if we have valid wallet data
        if not wallet_data:
            return f"❌ No wallet data found for address: {wallet_address}"
        
        # Handle different response formats
        tokens = []
        if isinstance(wallet_data, dict):
            # Check for error in response
            if "error" in wallet_data:
                return f"❌ Error fetching wallet data: {wallet_data['error']}"
            
            # Try different possible field names for tokens
            possible_token_fields = ["tokens", "holdings", "balances", "assets", "data"]
            for field in possible_token_fields:
                if field in wallet_data and wallet_data[field]:
                    tokens = wallet_data[field]
                    print(f"Found tokens in field: {field}")
                    break
                    
            if not tokens:
                # If no tokens found, check if wallet_data itself is the token list
                if all(isinstance(item, dict) for item in wallet_data.values()) and len(wallet_data) > 0:
                    # wallet_data might be a dict where each value is a token
                    tokens = list(wallet_data.values())
                    print("Using wallet_data values as tokens")
                else:
                    return f"📊 Wallet {wallet_address} appears to have no token holdings. Available fields: {list(wallet_data.keys())}"
        elif isinstance(wallet_data, list):
            tokens = wallet_data
            print("Using wallet_data as token list")
        else:
            return f"❌ Unexpected wallet data format received for address: {wallet_address}"
        
        if not tokens:
            return f"📊 Wallet {wallet_address} has no token holdings."
        
        # Debug: Print first token structure
        if tokens:
            print("=== FIRST TOKEN STRUCTURE ===")
            print(f"First token type: {type(tokens[0])}")
            print(f"First token: {tokens[0]}")
            print(f"First token keys: {list(tokens[0].keys()) if isinstance(tokens[0], dict) else 'Not a dict'}")
            print("=============================")
        
        # Format the response
        formatted_address = wallet_address if wallet_address.upper() != 'SELF' else 'SELF (User Wallet)'
        result_text = f"🔍 EVM Wallet Analysis for {formatted_address}\n"
        result_text += f"📊 Total tokens found: {len(tokens)}\n\n"
        
        # Calculate total portfolio value if available
        total_value = 0
        
        for i, token in enumerate(tokens[:20]):  # Show top 20 tokens
            # Try multiple possible field names for each attribute
            symbol = (token.get('symbol') or token.get('token_symbol') or 
                     token.get('name') or token.get('ticker') or 'Unknown')
            
            name = (token.get('name') or token.get('token_name') or 
                   token.get('display_name') or token.get('full_name') or 'Unknown Token')
            
            # Try different amount field names
            amount = (token.get('amount') or token.get('balance') or 
                     token.get('quantity') or token.get('value') or 
                     token.get('balance_raw') or 0)
            
            # Try different USD value field names
            usd_value = (token.get('usd_value') or token.get('value_usd') or 
                        token.get('total_value') or token.get('market_value') or 
                        token.get('worth') or 0)
            
            # Try different price change field names
            price_change_24h = (token.get('price_change_24h') or token.get('change_24h') or 
                               token.get('price_change') or token.get('change') or 0)
            
            # Try different contract address field names
            contract_address = (token.get('contract_address') or token.get('address') or 
                               token.get('token_address') or token.get('contract') or 'N/A')
            
            # Try different chain field names
            chain = (token.get('chain') or token.get('network') or 
                    token.get('blockchain') or 'Unknown')
            
            # Add to total value
            if isinstance(usd_value, (int, float)):
                total_value += usd_value
            
            result_text += f"--- Token {i+1} ---\n"
            result_text += f"🪙 {symbol} ({name})\n"
            result_text += f"💰 Amount: {amount:,.6f}\n"
            
            if usd_value and usd_value > 0:
                result_text += f"💵 USD Value: ${usd_value:,.2f}\n"
            
            if price_change_24h:
                change_emoji = "📈" if price_change_24h > 0 else "📉"
                result_text += f"{change_emoji} 24h Change: {price_change_24h:+.2f}%\n"
            
            result_text += f"🔗 Contract: {contract_address}\n"
            result_text += f"⛓️ Chain: {chain}\n\n"
        
        # Add total portfolio value if calculated
        if total_value > 0:
            result_text += f"💎 Total Portfolio Value: ${total_value:,.2f}\n"
        
        # Add note if there are more tokens
        if len(tokens) > 20:
            result_text += f"\n📝 Note: Showing top 20 tokens out of {len(tokens)} total tokens.\n"
        
        return result_text
        
    except Exception as e:
        return f"❌ Error fetching EVM wallet tokens: {str(e)}"


async def fetch_solana_wallet_assets_internal(owner_address: str) -> str:
    """
    Fetch token holdings of a Solana wallet using BitQuery streaming API.
    
    Args:
        owner_address: The Solana wallet address to analyze
    
    Returns:
        Formatted string containing Solana wallet asset information
    """
    try:
        # Validate Solana address format (basic validation - Solana addresses are typically 32-44 characters)
        if not owner_address or len(owner_address) < 32:
            return "❌ Invalid Solana wallet address format. Please provide a valid Solana wallet address."
        
        # GraphQL query for BitQuery
        query = """
        query MyQuery {
          Solana {
            BalanceUpdates(
              where: {BalanceUpdate: {Account: {Owner: {is: "%s"}}}}
              orderBy: {descendingByField: "BalanceUpdate_Balance_maximum"}
            ) {
              BalanceUpdate {
                Balance: PostBalance(maximum: Block_Slot)
                Currency {
                  Name
                  Symbol
                }
              }
            }
          }
        }
        """ % owner_address
        
        # Build request data for BitQuery
        request_data = {
            "query": query,
            "variables": "{}"
        }
        
        # Headers for BitQuery API
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ory_at_HSpZUPo3ESsTINOwynzljQRk-0JnVAtBb84oDVmX8v4.z6RReaku_7XBpifW4r-JoRIdxxJQp2SUPP6FV5W6I9g'
        }
        
        # Make the HTTP request
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.post(
                'https://streaming.bitquery.io/eap',
                headers=headers,
                json=request_data
            )
            
            if response.status_code != 200:
                return f"❌ Failed to fetch Solana wallet data. HTTP status: {response.status_code}"
            
            result = response.json()
        
        # Handle the BitQuery response format
        if not result:
            return "❌ Failed to get response from BitQuery API."
        
        # Extract data from BitQuery response structure
        if "data" not in result or "Solana" not in result["data"] or "BalanceUpdates" not in result["data"]["Solana"]:
            if "errors" in result:
                error_msg = result["errors"][0].get("message", "Unknown error")
                return f"❌ GraphQL error: {error_msg}"
            return f"❌ No wallet data found for Solana address: {owner_address}"
        
        balance_updates = result["data"]["Solana"]["BalanceUpdates"]
        
        if not balance_updates:
            return f"📊 Solana wallet {owner_address} has no token holdings."
        
        # Format the response
        result_text = f"🔍 Solana Wallet Analysis for {owner_address}\n"
        result_text += f"📊 Total assets found: {len(balance_updates)}\n\n"
        
        for i, update in enumerate(balance_updates[:20]):  # Show top 20 assets
            balance_update = update.get("BalanceUpdate", {})
            balance = balance_update.get("Balance", "0")
            currency = balance_update.get("Currency", {})
            
            symbol = currency.get("Symbol", "Unknown")
            name = currency.get("Name", "Unknown Asset")
            
            # Convert balance to float for formatting
            try:
                balance_float = float(balance)
            except (ValueError, TypeError):
                balance_float = 0
            
            result_text += f"--- Asset {i+1} ---\n"
            result_text += f"🪙 {symbol} ({name})\n"
            result_text += f"💰 Balance: {balance_float:,.6f}\n\n"
        
        # Add note if there are more assets
        if len(balance_updates) > 20:
            result_text += f"📝 Note: Showing top 20 assets out of {len(balance_updates)} total assets.\n"
        
        return result_text
        
    except Exception as e:
        return f"❌ Error fetching Solana wallet assets: {str(e)}"


def register_account_tools(mcp):
    """Register account-related MCP tools."""
    
    @mcp.tool()
    async def fetch_evm_wallet_tokens(wallet_address: str) -> str:
        """
        Fetch token holdings of an EVM wallet using ZerionWalletAnalysisAgent.
        
        Args:
            wallet_address: The EVM wallet address (starting with 0x and 42-character long) 
                           to analyze. Can also use 'SELF' for user's own wallet address.
        """
        return await fetch_evm_wallet_tokens_internal(wallet_address)
    
    @mcp.tool()
    async def fetch_solana_wallet_assets(owner_address: str) -> str:
        """
        Fetch token holdings of a Solana wallet using BitQuery streaming API.
        
        Args:
            owner_address: The Solana wallet address to analyze
        """ 
        return await fetch_solana_wallet_assets_internal(owner_address) 