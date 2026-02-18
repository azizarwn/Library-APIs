from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.models.engine import get_db
from app.models.models import User
from app.schema.auth import LoginRequest, RegisterRequest
from app.utils.auth import hash_password, is_password_valid

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(body: RegisterRequest, db: Session = Depends(get_db)):
    try:
        hashed_password = hash_password(body.password)
        new_user = User(
            username=body.username,
            email=body.email,
            password=hashed_password,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    # exception must be handled since the email field has a unique constraint,
    # and trying to register with an existing email will raise an IntegrityError.
    # We catch this specific error to return a user-friendly message,
    # while also catching any other unexpected exceptions that may occur during the registration process.
    # if exceptions are not handled, the API will return a generic 500 Internal Server Error,
    # which is not informative for the client and does not provide a good user experience.
    except IntegrityError as e:
        print(e, "User already exist!")  # Log the error for debugging purposes
        # This error occurs when trying to insert a duplicate email due to the unique constraint
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exist!")
    except Exception as e:
        print(e)  # Log the error for debugging purposes
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

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
