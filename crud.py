import models
from schemas import BookCreate
from sqlalchemy.orm import Session


def create_book(db: Session, book: BookCreate):
    db_book = models.Book(title=book.title, author=book.author)
    db.add(db_book)
    db.commit()  
    db.refresh(db_book)  
    return db_book

def read_books(db:Session, book_id:int=None):
    if book_id is not None:
        return db.query(models.Book).filter(models.Book.book_id==book_id).first()
    return db.query(models.Book).all()

def delete_book(db:Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.book_id==book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
        return db_book
    
def update_book(db:Session, book_id: int, book: BookCreate):
    db_book = db.query(models.Book).filter(models.Book.book_id==book_id).first()
    if db_book:
        db_book.title=book.title
        db_book.author=book.author
        db.commit()
        db.refresh(db_book)
        return db_book
