from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import BookModel, get_db

router = APIRouter(prefix="/books", tags=["Books"])

db_dependency = Annotated[Session, Depends(get_db)]


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    price: float | None = None


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    price: float

    class Config:
        from_attributes = True


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: db_dependency):
    new_book = BookModel(
        title=book.title,
        author=book.author,
        price=book.price,
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.get("/", response_model=list[BookResponse])
def get_all_books(db: db_dependency):
    return db.query(BookModel).all()


@router.get("/{book_id}", response_model=BookResponse)
def get_book_by_id(book_id: int, db: db_dependency):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found",
        )
    return book


@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_data: BookUpdate, db: db_dependency):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found",
        )

    if book_data.title is not None:
        book.title = book_data.title
    if book_data.author is not None:
        book.author = book_data.author
    if book_data.price is not None:
        book.price = book_data.price

    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=status.HTTP_200_OK)
def delete_book(book_id: int, db: db_dependency):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found",
        )

    db.delete(book)
    db.commit()
    return {"message": f"Book with ID {book_id} deleted successfully"}
