import os
from typing import Any

import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


class APIClient:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url.rstrip("/")

    def _headers(self, token: str | None = None) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    def _request(
        self,
        method: str,
        endpoint: str,
        token: str | None = None,
        json: dict | None = None,
        params: dict | None = None,
    ) -> tuple[bool, Any]:
        url = f"{self.base_url}{endpoint}"

        print("=================================")
        print("URL:", url)    
        print("METHOD:", method)
        print("JSON:", json)
        print("=================================")

        try:    
            response = requests.request(
                method=method,
                url=url,
                headers=self._headers(token),
                json=json,
                params=params,
                timeout=30,
            )
            if response.status_code == 204:
                return True, None
            if response.ok:
                return True, response.json()
            try:
                detail = response.json().get("detail", response.text)
            except Exception:
                detail = response.text
            return False, detail
        except requests.RequestException as exc:
            return False, f"Connection error: {exc}"
    def register(self, username: str, email: str, password: str):
        return self._request(
            "POST",
            "/auth/register",   
            json={"username": username, "email": email, "password": password},
        )

    def login(self, username: str, password: str):
        return self._request(
            "POST",
            "/auth/login",
            json={"username": username, "password": password},
        )

    def refresh(self, refresh_token: str) -> tuple[bool, Any]:
        return self._request(
            "POST",
            "/auth/refresh",
            json={"refresh_token": refresh_token},
        )

    def logout(self, token: str) -> tuple[bool, Any]:
        return self._request("POST", "/auth/logout", token=token)

    def get_expenses(self, token: str) -> tuple[bool, Any]:
        return self._request("GET", "/expenses", token=token)

    def create_expense(self, token: str, data: dict) -> tuple[bool, Any]:
        return self._request("POST", "/expenses", token=token, json=data)

    def update_expense(self, token: str, expense_id: int, data: dict) -> tuple[bool, Any]:
        return self._request("PUT", f"/expenses/{expense_id}", token=token, json=data)

    def delete_expense(self, token: str, expense_id: int) -> tuple[bool, Any]:
        return self._request("DELETE", f"/expenses/{expense_id}", token=token)

    def get_income(self, token: str) -> tuple[bool, Any]:
        return self._request("GET", "/income", token=token)

    def create_income(self, token: str, data: dict) -> tuple[bool, Any]:
        return self._request("POST", "/income", token=token, json=data)

    def update_income(self, token: str, income_id: int, data: dict) -> tuple[bool, Any]:
        return self._request("PUT", f"/income/{income_id}", token=token, json=data)

    def delete_income(self, token: str, income_id: int) -> tuple[bool, Any]:
        return self._request("DELETE", f"/income/{income_id}", token=token)

    def get_budgets(self, token: str) -> tuple[bool, Any]:
        return self._request("GET", "/budget", token=token)

    def create_budget(self, token: str, data: dict) -> tuple[bool, Any]:
        return self._request("POST", "/budget", token=token, json=data)

    def update_budget(self, token: str, budget_id: int, data: dict) -> tuple[bool, Any]:
        return self._request("PUT", f"/budget/{budget_id}", token=token, json=data)

    def delete_budget(self, token: str, budget_id: int) -> tuple[bool, Any]:
        return self._request("DELETE", f"/budget/{budget_id}", token=token)

    def get_dashboard_summary(self, token: str, month: int | None = None, year: int | None = None) -> tuple[bool, Any]:
        params = {}
        if month:
            params["month"] = month
        if year:
            params["year"] = year
        return self._request("GET", "/dashboard/summary", token=token, params=params or None)

    def get_category_wise(self, token: str, month: int | None = None, year: int | None = None) -> tuple[bool, Any]:
        params = {}
        if month:
            params["month"] = month
        if year:
            params["year"] = year
        return self._request("GET", "/dashboard/category-wise", token=token, params=params or None)

    def get_monthly_expenses(self, token: str, year: int | None = None) -> tuple[bool, Any]:
        params = {"year": year} if year else None
        return self._request("GET", "/dashboard/monthly", token=token, params=params)

    def get_monthly_report(self, token: str, year: int | None = None) -> tuple[bool, Any]:
        params = {"year": year} if year else None
        return self._request("GET", "/reports/monthly", token=token, params=params)

    def get_category_report(self, token: str, month: int | None = None, year: int | None = None) -> tuple[bool, Any]:
        params = {}
        if month:
            params["month"] = month
        if year:
            params["year"] = year
        return self._request("GET", "/reports/category", token=token, params=params or None)

    def get_income_vs_expense(self, token: str, year: int | None = None) -> tuple[bool, Any]:
        params = {"year": year} if year else None
        return self._request("GET", "/reports/income-vs-expense", token=token, params=params)


api_client = APIClient()
