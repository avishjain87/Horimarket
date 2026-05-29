import json
from markets import MARKETS

def search_market(query):
    """
    Search for a market by name (partial match supported)
    """
    if not query:
        return None
    
    results = {}
    query_lower = query.lower()
    
    for name, symbol in MARKETS.items():
        if query_lower in name.lower():
            results[name] = symbol
    
    return results if results else None


def get_market_details(symbol):
    """
    Get market details by symbol
    """
    for name, sym in MARKETS.items():
        if sym == symbol:
            return {"name": name, "symbol": symbol}
    return None


def list_all_markets():
    """
    Get all available markets
    """
    return MARKETS


def search_by_symbol(symbol):
    """
    Search market by symbol
    """
    for name, sym in MARKETS.items():
        if sym.lower() == symbol.lower():
            return {name: symbol}
    return None
