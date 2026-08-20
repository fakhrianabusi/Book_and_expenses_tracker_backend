from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import BookModel, get_db

router = APIRouter(prefix="/books", tags=["Books"])

db_dependency = Annotated[Session, Depends(get_db)]


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    amount: int = Field(..., gt=0)  # Quantity (Required)
    price: float = Field(..., gt=0)  # Price (Required)


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    amount: int | None = Field(default=None, gt=0)
    price: float | None = Field(default=None, gt=0)


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    amount: int
    price: float

    class Config:
        from_attributes = True


@router.get("/", response_model=list[BookResponse])
def books_list(
    db: db_dependency,
    limit: int = Query(default=50, gt=0, le=100),
    offset: int = Query(default=0, ge=0),
):
    return db.query(BookModel).offset(offset).limit(limit).all()


@router.get("/{id}", response_model=BookResponse)
def books_detail(
    db: db_dependency,
    id: int = Path(gt=0),
):
    book = db.query(BookModel).filter(BookModel.id == id).first()
    if book is not None:
        return book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with id {id} not found!",
    )


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    db: db_dependency,
    book: BookCreate,
):
    db_book = BookModel(
        title=book.title,
        author=book.author,
        amount=book.amount,
        price=book.price,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.put("/{id}", response_model=BookResponse)
def update_book(
    db: db_dependency,
    id: int,
    book: BookUpdate,
):
    db_book = db.query(BookModel).filter(BookModel.id == id).first()

    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {id} not found!",
        )

    update_data = book.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_book(
    id: int,
    db: db_dependency,
):
    db_book = db.query(BookModel).filter(BookModel.id == id).first()

    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {id} not found!",
        )

    db.delete(db_book)
    db.commit()
    return {"message": f"Book with id {id} deleted successfully"}
