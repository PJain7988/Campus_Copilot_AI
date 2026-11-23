from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
import os
import shutil

from app.database.session import get_db
from app.models.entities import Document, DocumentChunk, User
from app.schemas.api_schemas import DocumentItem
from app.api.deps import get_current_user, get_current_admin

router = APIRouter(prefix="/documents", tags=["Document Management"])

UPLOAD_DIR = "./uploaded_documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("", response_model=List[DocumentItem])
async def list_documents(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Document).order_by(Document.created_at.desc())
    res = await db.execute(stmt)
    return res.scalars().all()

@router.post("/upload")
async def upload_document(
    title: str = Form(...),
    category: str = Form("ACADEMIC"),
    version: str = Form("1.0"),
    file: UploadFile = File(...),
    current_admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    file_ext = file.filename.split(".")[-1].upper()
    file_dest = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_dest, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    doc = Document(
        title=title,
        file_path=file_dest,
        file_type=file_ext,
        category=category,
        version=version,
        index_status="READY",
        total_pages=1
    )
    db.add(doc)
    await db.flush()

    # Extract sample content if txt/pdf for ingestion
    try:
        with open(file_dest, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception:
        content = f"Uploaded verified university document: {title}."

    chunk = DocumentChunk(
        document_id=doc.id,
        chunk_index=0,
        page_number=1,
        content=content[:1500]
    )
    db.add(chunk)
    await db.commit()
    await db.refresh(doc)

    return {"status": "success", "document_id": doc.id, "title": doc.title}
