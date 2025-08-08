from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str

class BookSchema(BookCreate):
    id: int

    class Config:
        orm_mode = True