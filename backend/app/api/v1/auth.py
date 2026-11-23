from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database.session import get_db
from app.models.entities import User, University
from app.schemas.api_schemas import UserRegister, UserLogin, TokenResponse, UserProfile
from app.security.auth import verify_password, get_password_hash, create_access_token, create_refresh_token
from app.api.deps import get_current_user
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse)
async def register(payload: UserRegister, db: AsyncSession = Depends(get_db)):
    # Check if user already exists
    stmt = select(User).where(User.email == payload.email)
    res = await db.execute(stmt)
    if res.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists"
        )
    
    # Check or create default university
    u_stmt = select(University).where(University.code == (payload.university_code or settings.DEFAULT_UNIVERSITY_CODE))
    u_res = await db.execute(u_stmt)
    university = u_res.scalar_one_or_none()
    if not university:
        university = University(
            code=payload.university_code or settings.DEFAULT_UNIVERSITY_CODE,
            name=settings.DEFAULT_UNIVERSITY_NAME,
            domain="geetauniversity.edu.in"
        )
        db.add(university)
        await db.flush()

    new_user = User(
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
        full_name=payload.full_name,
        role=payload.role or "STUDENT",
        university_id=university.id
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    access_token = create_access_token(new_user.id)
    refresh_token = create_refresh_token(new_user.id)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user={
            "id": new_user.id,
            "email": new_user.email,
            "full_name": new_user.full_name,
            "role": new_user.role,
            "university_id": new_user.university_id
        }
    )

@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == payload.email)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user={
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "university_id": user.university_id
        }
    )

@router.get("/me", response_model=UserProfile)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
