from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.models.engine import get_db
from app.models.models import Member
from app.schema.member import MemberRequest, MemberResponse

members_router = APIRouter(prefix="/members", tags=["Members"])


@members_router.get(path="/", response_model=list[MemberResponse])
def get_members(db: Session = Depends(get_db)):
    query = select(Member)
    members = db.exec(query).all()

    return members


@members_router.get(path="/{id}", response_model=MemberResponse)
def get_member_by_id(id: int, db: Session = Depends(get_db)):
    member = db.get(Member, id)
    return member


@members_router.post(path="/")
def create_member(body: MemberRequest, db: Session = Depends(get_db)):
    new_member = Member(name=body.name, email=body.email)
    db.add(new_member)
    db.commit()
    db.refresh(new_member)  # Get the ID and computed properties
    return new_member
