from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlmodel import Session

from app.models.engine import get_db
from app.models.models import User
from app.utils.auth import validate_token

security = HTTPBearer()


def get_current_user(token=Depends(security), db: Session = Depends(get_db)):
    user_id = validate_token(token.credentials)

    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    return user
