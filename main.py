from crud import create_book, delete_book, read_books, update_book
from fastapi import FastAPI, Depends, HTTPException,Query
import models, crud
from schemas import BookCreate, BookSchema
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import schemas
from typing import List, Union

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/books/", response_model = BookSchema)
def book_create(book:BookCreate, db: Session = Depends(get_db)):
    return create_book(db, book)

@app.get("/books/", response_model=Union[List[BookSchema], BookSchema])
def books_read(book_id: int = Query(default=None), db: Session = Depends(get_db)):
    if book_id is not None:
        book = read_books(db=db, book_id=book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book
    return read_books(db=db)

@app.delete("/books/{book_id}")
def book_delete(book_id: int, db: Session=Depends(get_db)):
    success = delete_book(db=db, book_id=book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted"}

@app.put("/books/{book_id}", response_model=BookSchema)
def book_update(book_id: int, updated_data: BookCreate, db: Session = Depends(get_db)):
    book = update_book(db=db, book_id=book_id, book_data=updated_data)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book