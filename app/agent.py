import os
from app.config import GROQ_API_KEY, TAVILY_API_KEY
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from app.rag import get_retriever

# Initialize Groq LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)

# --- Tool: Course Retriever ---
def course_tool(query: str) -> str:
    retriever = get_retriever()
    docs = retriever.get_relevant_documents(query)
    return " | ".join([d.page_content[:150] for d in docs])

# --- Tool: Web Search (Tavily with fallback) ---
def web_tool(query: str) -> str:
    if TAVILY_API_KEY:
        try:
            from tavily import TavilyClient
            tavily = TavilyClient(api_key=TAVILY_API_KEY)
            results = tavily.search(query, max_results=3)
            return " | ".join([r["content"] for r in results["results"]])
        except Exception as e:
            return f"Web search error: {str(e)}"
    return "Web search unavailable (no Tavily API key)."

# --- Router Node ---
def router(state):
    query = state["query"]
    system_prompt = """Decide if the question is:
    - COURSE if it's about university courses, prerequisites, or catalog
    - GENERAL if it's about general knowledge (jobs, market, etc)."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", query)
    ])
    decision = llm.invoke(prompt.format_messages()).content.strip().upper()
    return {
        "query": query,
        "route": "COURSE" if "COURSE" in decision else "GENERAL"
    }

def generate_node(state):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("user", f"User asked: {state['query']}\nAnswer with context: {state['answer']}")
    ])
    response = llm.invoke(prompt.format_messages())
    return {
        "query": state["query"],
        "final_answer": response.content
    }


# --- Course Node ---
def course_node(state):
    return {
        "query": state["query"],   # keep query
        "answer": course_tool(state["query"])
    }

def web_node(state):
    return {
        "query": state["query"],   # keep query
        "answer": web_tool(state["query"])
    }


# --- Generation Node ---
# def generate_node(state):
#     prompt = ChatPromptTemplate.from_messages([
#         ("system", "You are a helpful assistant."),
#         ("user", f"User asked: {state['query']}\nAnswer with context: {state['answer']}")
#     ])
#     response = llm.invoke(prompt.format_messages())
#     return {"final_answer": response.content}

# --- Build Graph ---
graph = StateGraph(dict)

graph.add_node("router", router)
graph.add_node("course", course_node)
graph.add_node("web", web_node)
graph.add_node("generate", generate_node)

# Conditional routing
def route_condition(state):
    return state["route"]

graph.add_conditional_edges(
    "router",
    route_condition,
    {
        "COURSE": "course",
        "GENERAL": "web"
    }
)

# Normal edges
graph.add_edge("course", "generate")
graph.add_edge("web", "generate")
graph.add_edge("generate", END)


graph.set_entry_point("router")
agent = graph.compile()
