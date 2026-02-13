from pydantic import BaseModel


class MemberRequest(BaseModel):
    name: str
    email: str


class MemberResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True
