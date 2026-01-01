from fastapi import APIRouter,HTTPException
from schemas.chat_models import ChatRequest, ChatResponse
from app.graph import graph
from langchain_core.messages import HumanMessage
import asyncio

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        # graph.get_graph().draw_mermaid_png(output_file_path='output.png')
        if not req.session_id :
            return ChatResponse(answer="Session ID is mandatory")
        
        result = await asyncio.to_thread(
            graph.invoke,
            {"messages": [HumanMessage(content=req.query)],"needs_fallback": False,"fallback_used":False},
            {"configurable": {"thread_id": req.session_id}},
        )

        messages = result.get("messages", [])

        final_answer = messages[-1].content

        return ChatResponse(answer=final_answer)

    except Exception as e :
        return ChatResponse(answer="Something went wrong. Please try again later.")
