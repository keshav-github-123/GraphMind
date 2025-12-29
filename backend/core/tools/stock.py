"""Stock market data tool."""
from typing import Dict
import httpx
from langchain.tools import tool
from backend.config import settings

@tool
async def get_stock_price(symbol: str) -> Dict:
    """📈 Stock Price Tool"""
    if not settings.alpha_vantage_api_key:
        return {"error": "Alpha Vantage API key not configured"}
    
    url = (
        f"https://www.alphavantage.co/query"
        f"?function=GLOBAL_QUOTE&symbol={symbol}"
        f"&apikey={settings.alpha_vantage_api_key}"
    )
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        return {"error": f"Failed to fetch stock price: {str(e)}"}