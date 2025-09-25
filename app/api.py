from fastapi import APIRouter
from app.models import QueryRequest, QueryResponse
from app.rag import get_retriever, load_and_index
from app.agent import agent
router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Hello, IntelliCourse!"}

@router.post("/echo", response_model=QueryResponse)
def echo_query(request: QueryRequest):
    return QueryResponse(answer=f"You asked: {request.query}", source_tool="echo")

# 🔹 NEW: Ask course-related questions
@router.post("/ask", response_model=QueryResponse)
def ask_course(request: QueryRequest):
    retriever = get_retriever()
    results = retriever.get_relevant_documents(request.query)

    # Just join top results for now
    answer = " | ".join([r.page_content[:150] for r in results])
    return QueryResponse(answer=answer, source_tool="RAG")


@router.post("/chat", response_model=QueryResponse)
def chat(request: QueryRequest):
    result = agent.invoke({"query": request.query})
    return QueryResponse(answer=result["final_answer"], source_tool="agent")
