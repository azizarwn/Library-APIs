from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.models.engine import get_db
from app.models.models import User
from app.schema.auth import LoginRequest, RegisterRequest
from app.utils.auth import hash_password, is_password_valid

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(body: RegisterRequest, db: Session = Depends(get_db)):
    hashed_password = hash_password(body.password)

    new_user = User(
        username=body.username,
        email=body.email,
        password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"success": True, "message": "User registered successfully"}


@auth_router.post("/login")
def login_user(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.exec(select(User).where(User.email == body.email)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not is_password_valid(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # beetwen the two cases, the user is not found or the password is incorrect,
    # we return the same error message to avoid giving hints to potential attackers
    # about which part of the credentials is wrong (UX Security).
    return {"success": True, "message": "Login successful"}
