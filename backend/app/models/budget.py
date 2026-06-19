from sqlalchemy import Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Budget(Base):
    __tablename__ = "budgets"
    __table_args__ = (
        UniqueConstraint("user_id", "category", "month", "year", name="uq_user_category_month_year"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    monthly_limit: Mapped[float] = mapped_column(Float, nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="budgets")
