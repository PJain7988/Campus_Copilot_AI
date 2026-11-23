from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List

from app.database.session import get_db
from app.models.entities import User, Conversation, Message, Citation, DocumentChunk, Document
from app.schemas.api_schemas import (
    ChatMessageRequest, ChatMessageResponse, ConversationItem, CitationItem, FeedbackRequest
)
from app.api.deps import get_current_user
from app.agents.orchestrator import MultiAgentOrchestrator
from app.rag.retriever import KnowledgeRetriever

router = APIRouter(prefix="/chat", tags=["Conversational AI"])

@router.get("/conversations", response_model=List[ConversationItem])
async def list_conversations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = (
        select(Conversation)
        .where(Conversation.user_id == current_user.id)
        .order_by(Conversation.updated_at.desc())
    )
    res = await db.execute(stmt)
    return res.scalars().all()

@router.post("/message", response_model=ChatMessageResponse)
async def send_message(
    payload: ChatMessageRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # 1. Resolve or create conversation
    conv = None
    if payload.conversation_id:
        stmt = select(Conversation).where(
            Conversation.id == payload.conversation_id,
            Conversation.user_id == current_user.id
        )
        res = await db.execute(stmt)
        conv = res.scalar_one_or_none()

    if not conv:
        # Create new conversation with clean title from first query
        conv_title = payload.message[:35] + ("..." if len(payload.message) > 35 else "")
        conv = Conversation(user_id=current_user.id, title=conv_title)
        db.add(conv)
        await db.flush()

    # 2. Record User Message
    user_msg = Message(
        conversation_id=conv.id,
        sender="USER",
        content=payload.message
    )
    db.add(user_msg)
    await db.flush()

    # 3. Classify intent
    category = MultiAgentOrchestrator.classify_intent(payload.message)

    # 4. Search document chunks for grounding
    chunk_stmt = select(DocumentChunk, Document).join(Document, DocumentChunk.document_id == Document.id)
    chunk_res = await db.execute(chunk_stmt)
    all_chunks = chunk_res.all()

    scored_chunks = []
    for chunk, doc in all_chunks:
        score = KnowledgeRetriever.score_relevance(payload.message, chunk.content)
        if score > 0.15:
            scored_chunks.append({
                "chunk_id": chunk.id,
                "document_title": doc.title,
                "page_number": chunk.page_number,
                "content": chunk.content,
                "score": score
            })

    scored_chunks.sort(key=lambda x: x["score"], reverse=True)
    top_candidates = scored_chunks[:3]

    # 5. Run Multi-Agent Orchestrator
    agent_output = MultiAgentOrchestrator.synthesize_answer(payload.message, category, top_candidates)

    # 6. Save Assistant Message
    assistant_msg = Message(
        conversation_id=conv.id,
        sender="ASSISTANT",
        content=agent_output["content"],
        intent_category=agent_output["category"],
        groundedness_score=agent_output["groundedness_score"],
        latency_ms=agent_output["latency_ms"]
    )
    db.add(assistant_msg)
    await db.flush()

    # 7. Save Citations
    citation_items = []
    for c in agent_output["citations"]:
        cit = Citation(
            message_id=assistant_msg.id,
            document_title=c["document_title"],
            page_number=c["page_number"],
            snippet=c["snippet"],
            relevance_score=c["relevance_score"]
        )
        db.add(cit)
        citation_items.append(CitationItem(
            document_title=c["document_title"],
            page_number=c["page_number"],
            snippet=c["snippet"],
            relevance_score=c["relevance_score"]
        ))

    await db.commit()

    return ChatMessageResponse(
        conversation_id=conv.id,
        message_id=assistant_msg.id,
        sender="ASSISTANT",
        content=assistant_msg.content,
        intent_category=assistant_msg.intent_category,
        groundedness_score=assistant_msg.groundedness_score,
        citations=citation_items,
        latency_ms=assistant_msg.latency_ms
    )

@router.post("/feedback")
async def record_feedback(
    payload: FeedbackRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    from app.models.entities import Feedback
    fb = Feedback(
        message_id=payload.message_id,
        user_id=current_user.id,
        rating=payload.rating,
        comment=payload.comment
    )
    db.add(fb)
    await db.commit()
    return {"status": "success", "message": "Feedback recorded"}
