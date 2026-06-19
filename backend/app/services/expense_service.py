from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate


def create_expense(db: Session, user_id: int, expense_data: ExpenseCreate) -> Expense:
    expense = Expense(**expense_data.model_dump(), user_id=user_id)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def get_expenses(db: Session, user_id: int) -> list[Expense]:
    return db.query(Expense).filter(Expense.user_id == user_id).order_by(Expense.date.desc()).all()


def get_expense(db: Session, user_id: int, expense_id: int) -> Expense:
    expense = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == user_id).first()
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return expense


def update_expense(db: Session, user_id: int, expense_id: int, expense_data: ExpenseUpdate) -> Expense:
    expense = get_expense(db, user_id, expense_id)
    update_data = expense_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(expense, field, value)
    db.commit()
    db.refresh(expense)
    return expense


def delete_expense(db: Session, user_id: int, expense_id: int) -> None:
    expense = get_expense(db, user_id, expense_id)
    db.delete(expense)
    db.commit()
