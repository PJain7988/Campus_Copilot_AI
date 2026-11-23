from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.session import init_db
from app.api.v1 import auth, chat, documents, admin

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables automatically
    await init_db()
    
    # Pre-seed verified university data for Geeta University
    from app.database.session import async_session
    from app.models.entities import University, Document, DocumentChunk, User
    from app.security.auth import get_password_hash
    from sqlalchemy.future import select

    async with async_session() as db:
        # 1. Seed University
        u_stmt = select(University).where(University.code == settings.DEFAULT_UNIVERSITY_CODE)
        res = await db.execute(u_stmt)
        univ = res.scalar_one_or_none()
        if not univ:
            univ = University(
                code=settings.DEFAULT_UNIVERSITY_CODE,
                name=settings.DEFAULT_UNIVERSITY_NAME,
                domain="geetauniversity.edu.in"
            )
            db.add(univ)
            await db.flush()

        # 2. Seed Default Admin
        admin_stmt = select(User).where(User.email == "admin@geetauniversity.edu.in")
        a_res = await db.execute(admin_stmt)
        if not a_res.scalar_one_or_none():
            admin_user = User(
                email="admin@geetauniversity.edu.in",
                hashed_password=get_password_hash("Admin@CampusCopilot2026"),
                full_name="Academic Registrar Office",
                role="ADMIN",
                university_id=univ.id
            )
            db.add(admin_user)

        # 3. Seed Default Student Demo
        student_stmt = select(User).where(User.email == "student@geetauniversity.edu.in")
        s_res = await db.execute(student_stmt)
        if not s_res.scalar_one_or_none():
            student_user = User(
                email="student@geetauniversity.edu.in",
                hashed_password=get_password_hash("Student@2026"),
                full_name="Riya Sharma",
                role="STUDENT",
                university_id=univ.id
            )
            db.add(student_user)

        # 4. Seed Verified University Documents & Chunks
        doc_stmt = select(Document).where(Document.title == "Academic Regulations & Ordinance 2026")
        d_res = await db.execute(doc_stmt)
        if not d_res.scalar_one_or_none():
            doc1 = Document(
                university_id=univ.id,
                title="Academic Regulations & Ordinance 2026",
                file_path="/documents/academic_ordinance_2026.pdf",
                file_type="PDF",
                category="ACADEMIC",
                version="2026.1",
                index_status="READY",
                total_pages=45
            )
            db.add(doc1)
            await db.flush()

            chunks_data = [
                (1, 14, "Minimum attendance requirement: Students must maintain a minimum of 75% attendance in each registered subject to be eligible to sit for the End Semester Examinations. A relaxation up to 10% (bringing requirement to 65%) may be sanctioned by the Dean on valid medical grounds upon submitting verified medical documentation within 7 calendar days."),
                (2, 28, "End semester examinations for odd semesters are conducted between December 1st and December 22nd. Even semester examinations are held from May 10th to June 5th. Admit cards (Hall Tickets) are generated online 7 days before commencement."),
                (3, 35, "Fee submission deadline: Semester tuition fee must be cleared on or before the 15th of the commencement month of the semester. A late fine of INR 100 per day applies for the first 15 days, after which student portal access is temporarily frozen until payment clearance."),
                (4, 42, "Placement Registration Criteria: Students are eligible for placement drives starting in Semester 7, provided they hold a minimum CGPA of 6.5 with zero active backlogs at the time of company registration. Required documents include: updated 1-page resume, semester grade cards, NOC from department, and university ID card.")
            ]

            for idx, page, content in chunks_data:
                db.add(DocumentChunk(
                    document_id=doc1.id,
                    chunk_index=idx,
                    page_number=page,
                    content=content
                ))

        await db.commit()

    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Production-Ready AI University Information Assistant for Geeta University, Panipat",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(chat.router, prefix=settings.API_V1_STR)
app.include_router(documents.router, prefix=settings.API_V1_STR)
app.include_router(admin.router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "institution": settings.DEFAULT_UNIVERSITY_NAME,
        "version": "1.0.0"
    }
