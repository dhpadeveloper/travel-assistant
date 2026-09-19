import requests
from mcp.server.fastmcp import FastMCP
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filename="mcp.log",
)

logger = logging.getLogger(__name__)
mcp = FastMCP("Currency Conversion MCP")

@mcp.tool(
    description="Convert monetary values between currencies (e.g., INR, USD, EUR, SGD) "
        "using latest exchange rates. Use this tool whenever a user asks to convert money."
)
def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str,
) -> dict:
    """Convert money using open exchange rate APIs."""
    
    from_curr = from_currency.upper().strip()
    to_curr = to_currency.upper().strip()


    logger.info("[CURRENCY MCP] Converting %s %s to %s", amount, from_currency, to_currency)
    
    if from_curr == to_curr:
        return {
            "amount": amount,
            "from_currency": from_curr,
            "to_currency": to_curr,
            "rate": 1.0,
            "converted_amount": amount,
        }

    # Open exchange rate API supporting INR, SGD, USD, etc.
    url = f"https://open.er-api.com/v6/latest/{from_curr}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("result") == "success" and to_curr in data["rates"]:
            rate = data["rates"][to_curr]
            converted = round(amount * rate, 2)
            return {
                "amount": amount,
                "from_currency": from_curr,
                "to_currency": to_curr,
                "rate": round(rate, 6),
                "converted_amount": converted,
                "source": "Open Exchange Rates API",
            }
        else:
            return {"error": f"Currency {to_curr} not supported."}

    except Exception as e:
        return {"error": f"Conversion failed: {str(e)}"}
    
    
if __name__ == "__main__":

    mcp.run(transport="stdio")
