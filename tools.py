from pathlib import Path
from langchain_core.tools import tool
from reportlab.lib.pagesizes import letter
import os

from langchain_community.tools import DuckDuckGoSearchResults, TavilySearchResults
from langchain_community.utilities import ArxivAPIWrapper
from dotenv import load_dotenv
load_dotenv()


arxiv = ArxivAPIWrapper()
duckduckgo = DuckDuckGoSearchResults(max_results=10)
tavily = TavilySearchResults(max_results=3, api_key=os.getenv("TAVILY_API_KEY"))
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from pathlib import Path

@tool(description="Save the last research response as a nicely formatted PDF file.")
def save_research_to_pdf(content: str, filename: str = "research_output.pdf") -> str:
    """
    Save the last research answer into a PDF file with auto-wrapped text.
    """
    try:
        filepath = Path(filename).resolve()
        doc = SimpleDocTemplate(str(filepath), pagesize=letter,
                                rightMargin=50, leftMargin=50,
                                topMargin=50, bottomMargin=50)

        styles = getSampleStyleSheet()
        story = []

        for para in content.split("\n\n"): 
            story.append(Paragraph(para.strip(), styles["Normal"]))
            story.append(Spacer(1, 12))

        doc.build(story)
        return f"✅ Research pdf"
    except Exception as e:
        return f"Error saving PDF: {e}"


    
@tool(description="Search arXiv for research papers by query and return summaries.")
def arxiv_search(query: str) -> str:
    """Search arXiv papers for a given query and return summaries."""
    try:
        return arxiv.run(query)
    except Exception as e:
        return f"Error fetching from arXiv: {e}"
    

@tool(description="Perform a web search using DuckDuckGo and return top results.")
def duckduckgo_search(query: str) -> str:
    """Search DuckDuckGo for a query and return the top results."""
    try:
        return duckduckgo.run(query)
    except Exception as e:
        return f"Error fetching from DuckDuckGo: {e}"


@tool(description="Perform a search using Tavily and return top results.")
def tavily_search(query: str) -> str:
    """Search Tavily for a query and return the top results."""
    try:
        return tavily.run(query)
    except Exception as e:
        return f"Error fetching from Tavily: {e}"        


import wikipedia
from langchain_core.tools import tool

@tool("wiki_summary", return_direct=False)
def wiki_summary(topic: str, sentences: int = 3) -> str:
    """Get a short Wikipedia summary for any topic."""
    try:
        return wikipedia.summary(topic, sentences=sentences)
    except Exception as e:
        return f"Error fetching Wikipedia: {e}"


from langchain_community.utilities import ArxivAPIWrapper
from langchain_core.tools import tool

arxiv = ArxivAPIWrapper()

@tool("search_arxiv", return_direct=False)
def search_arxiv(query: str) -> str:
    """Search recent papers from arXiv and return summaries."""
    try:
        return arxiv.run(query)
    except Exception as e:
        return f"Error fetching from arXiv: {e}"

        
