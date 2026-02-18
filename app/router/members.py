from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.models.engine import get_db
from app.models.models import Member
from app.schema.member import MemberDetailResponse, MemberRequest, MemberResponse

members_router = APIRouter(prefix="/members", tags=["Members"])


@members_router.get(path="/", response_model=list[MemberResponse])
def get_members(db: Session = Depends(get_db)):
    query = select(Member)
    members = db.exec(query).all()

    return members


@members_router.get(path="/{id}", response_model=MemberDetailResponse)
def get_member_by_id(id: int, db: Session = Depends(get_db)):
    member = db.get(Member, id)

    return member


@members_router.post(path="/", status_code=status.HTTP_201_CREATED, response_model=MemberResponse)
def create_member(body: MemberRequest, db: Session = Depends(get_db)):
    new_member = Member(**body.model_dump())
    db.add(new_member)
    db.commit()
    db.refresh(new_member)  # Get the ID and computed properties

    return new_member


@members_router.delete("/{id}")
def delete_member(id: int, db: Session = Depends(get_db)):
    member = db.get(Member, id)
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")

    # Check if member has unreturned books using the property
    if len(member.currently_borrowed_books) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete member. Member still has unreturned book(s).",
        )

    # Member can be deleted (no unreturned books)
    db.delete(member)
    db.commit()

    return {
        "success": True,
        "message": "Member deleted successfully.",
    }
