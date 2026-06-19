from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.schemas.budget import BudgetCreate, BudgetUpdate


def create_budget(db: Session, user_id: int, budget_data: BudgetCreate) -> Budget:
    existing = (
        db.query(Budget)
        .filter(
            Budget.user_id == user_id,
            Budget.category == budget_data.category,
            Budget.month == budget_data.month,
            Budget.year == budget_data.year,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Budget already exists for this category and month",
        )

    budget = Budget(**budget_data.model_dump(), user_id=user_id)
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


def get_budgets(db: Session, user_id: int) -> list[Budget]:
    return (
        db.query(Budget)
        .filter(Budget.user_id == user_id)
        .order_by(Budget.year.desc(), Budget.month.desc(), Budget.category)
        .all()
    )


def get_budget(db: Session, user_id: int, budget_id: int) -> Budget:
    budget = db.query(Budget).filter(Budget.id == budget_id, Budget.user_id == user_id).first()
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    return budget


def update_budget(db: Session, user_id: int, budget_id: int, budget_data: BudgetUpdate) -> Budget:
    budget = get_budget(db, user_id, budget_id)
    update_data = budget_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(budget, field, value)
    db.commit()
    db.refresh(budget)
    return budget


def delete_budget(db: Session, user_id: int, budget_id: int) -> None:
    budget = get_budget(db, user_id, budget_id)
    db.delete(budget)
    db.commit()
