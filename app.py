import os
import logging
from typing import TypedDict, List, Annotated
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver


from latex_to_pdf import  save_research_to_pdf,arxiv_search,duckduckgo_search

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama

load_dotenv()
tools=[]


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


INITIAL_PROMPT = """You are an expert researcher in physics, mathematics, computer science,

quantitative biology, quantitative finance, statistics, electrical engineering,

systems science, and economics.

You will analyze recent research papers to identify promising directions

and then write a new research paper. Use the tools provided to search,

read, summarize, and propose ideas.

Ask the user for the research topic first, then fetch papers, summarize,

extract ideas, and write a paper in PDF format with proper equations

and references.
”"""



class AgentState(TypedDict):
    messages: Annotated[List, "Conversation messages"]


def build_model_node(provider: str, llm_id: str):
    logger.info(f"Building model: provider={provider}, llm_id={llm_id}")

    if provider == "Google":
        model = ChatGoogleGenerativeAI(model=llm_id, google_api_key=os.getenv("GOOGLE_API_KEY"))
        model = model.bind_tools(tools)
    elif provider == "Groq":
        model = ChatGroq(model=llm_id, api_key=os.getenv("GROQ_API_KEY"))
        model = model.bind_tools(tools)
    elif provider == "OpenRouter":
        model = ChatOpenAI(model=llm_id, api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
        logger.warning("⚠️ OpenRouter models cannot call tools.")
    elif provider == "Ollama":
        model = ChatOllama(model=llm_id, base_url=os.getenv("OLLAMA_BASE_URL"))
        logger.warning("⚠️ OpenRouter models cannot call tools.")
    else:
        raise ValueError(f"Unknown provider: {provider}")

    def call_model(state: AgentState):
        messages = state["messages"]
        response = model.invoke(messages)
        return {"messages": [response]}

    return call_model


def graph(provider: str, llm_id: str):
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", build_model_node(provider, llm_id))
    workflow.set_entry_point("agent")
    workflow.add_edge("agent", END)

    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)
