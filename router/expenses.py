from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import ExpenseModel, get_db

router = APIRouter(prefix="/expenses", tags=["Expenses"])

db_dependency = Annotated[Session, Depends(get_db)]


class ExpenseCreate(BaseModel):
    title: str = Field(..., min_length=1)
    amount: int = Field(..., gt=0)
    price: float = Field(..., gt=0)
    category: str = Field(default="General")


class ExpenseUpdate(BaseModel):
    title: str | None = None
    amount: int | None = Field(default=None, gt=0)
    price: float | None = Field(default=None, gt=0)
    category: str | None = None


class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: int
    price: float
    category: str

    class Config:
        from_attributes = True


@router.get("/", response_model=list[ExpenseResponse])
def expenses_list(
    db: db_dependency,
    min_price: float | None = Query(default=None, gt=0),
    category: str | None = Query(default=None),
    limit: int = Query(default=50, gt=0, le=100),
    offset: int = Query(default=0, ge=0),
):
    query = db.query(ExpenseModel)

    if min_price is not None:
        query = query.filter(ExpenseModel.price >= min_price)

    if category is not None:
        query = query.filter(ExpenseModel.category == category)

    return query.offset(offset).limit(limit).all()


@router.get("/{id}", response_model=ExpenseResponse)
def expenses_detail(
    db: db_dependency,
    id: int = Path(gt=0, le=99999),
):
    expense = db.query(ExpenseModel).filter(ExpenseModel.id == id).first()
    if expense is not None:
        return expense

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Expense with id {id} not found!",
    )


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def expenses_create(
    db: db_dependency,
    expense: ExpenseCreate,
):
    db_expense = ExpenseModel(
        title=expense.title,
        amount=expense.amount,
        price=expense.price,
        category=expense.category,
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


@router.patch("/{id}", response_model=ExpenseResponse)
def expenses_update(
    db: db_dependency,
    id: int,
    expense: ExpenseUpdate,
):
    db_expense = db.query(ExpenseModel).filter(ExpenseModel.id == id).first()

    if db_expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id {id} not found!",
        )

    update_data = expense.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_expense, key, value)

    db.commit()
    db.refresh(db_expense)
    return db_expense


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def expenses_delete(
    id: int,
    db: db_dependency,
):
    db_expense = db.query(ExpenseModel).filter(ExpenseModel.id == id).first()

    if db_expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id {id} not found!",
        )

    db.delete(db_expense)
    db.commit()
    return {"message": f"Expense with id {id} deleted successfully"}
