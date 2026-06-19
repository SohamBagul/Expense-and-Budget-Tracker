from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth, budget, dashboard, expenses, income, reports

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Expense Tracking & Budget Management API",
    description="Full-stack expense tracker with JWT authentication",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(expenses.router)
app.include_router(income.router)
app.include_router(budget.router)
app.include_router(dashboard.router)
app.include_router(reports.router)


@app.get("/")
def root():
    return {"message": "Expense Tracking & Budget Management API", "docs": "/docs"}
