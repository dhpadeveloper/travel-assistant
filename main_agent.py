from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
import logging
from rag import answer_from_rag
from mcp_client import get_mcp_tools

logger = logging.getLogger(__name__)

# ==================================================
# LLM
# ==================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
)



# ==================================================
# PROMPT
# ==================================================

AGENT_SYSTEM_PROMPT = """You are an AI Travel Assistant for Singapore.

ROUTING & TOOL SELECTION INSTRUCTIONS:
- For static Singapore facts (attractions, transport, culture, itineraries, indoor/outdoor activities):
  Execute `search_singapore_knowledge`.
- For real-time weather forecasts or current conditions:
  Execute `get_singapore_weather`.
- For currency conversion or budget math:
  Execute `convert_currency`.

STRICT ANSWERING RULES:
1. GROUNDING: Destination facts MUST come strictly from `search_singapore_knowledge`. Never invent facts or use pre-trained knowledge if RAG returns insufficient data.
2. NON-SINGAPORE QUERIES: If asked about another destination, respond: "The knowledge base only contains information about Singapore, so I do not have enough information to answer this question."
3. COMBINED REQUESTS (e.g., Weather-Aware Itineraries):
   - Step 1: Call `search_singapore_knowledge` to retrieve attractions and itineraries.
   - Step 2: Call `get_singapore_weather` to get the forecast.
   - Step 3: Combine both outputs, automatically replacing outdoor plans with indoor alternatives on rainy days.
4. TRANSPARENCY: Always explicitly cite source titles/URLs from RAG results and tag real-time tool results with "[Retrieved via Weather/Currency MCP]".
"""


# ==================================================
# RAG TOOL
# ==================================================

@tool
def search_singapore_knowledge(question: str) -> str:
    """
    Search the Singapore travel knowledge base for destination facts,
    attractions, neighbourhoods, transport, food, and itineraries.

    Use this tool BEFORE making up any destination facts.
    """
    logger.info(f"[TOOL] Querying Singapore Knowledge Base: {question}")

    result = answer_from_rag(
        question,
    )

    if not result:
        return "NO_KNOWLEDGE_FOUND: The knowledge base does not contain sufficient information on this topic."

    answer = result.get("answer", "")
    sources = result.get("sources", [])

    source_text = ""

    if sources:
        source_text = "\n\nSources:\n"
        for source in sources:
            source_text += f"- {source['title']}: {source['url']}\n"
    return answer + source_text


# ==================================================
# CREATE AGENT
# ==================================================

async def create_travel_agent():

    mcp_tools = await get_mcp_tools()

    weather_tool = mcp_tools.get("get_singapore_weather")

    currency_tool = mcp_tools.get("convert_currency")

    tools = [search_singapore_knowledge]

    if weather_tool:
        tools.append(weather_tool)

    if currency_tool:
        tools.append(currency_tool)

    # Create agent
    agent = create_agent(model=llm, tools=tools, system_prompt=AGENT_SYSTEM_PROMPT)

    return agent
