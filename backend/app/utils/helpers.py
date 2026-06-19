from datetime import date

MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def month_name(month: int) -> str:
    if 1 <= month <= 12:
        return MONTH_NAMES[month - 1]
    return str(month)


def month_year_label(month: int, year: int) -> str:
    return f"{month_name(month)} {year}"


def parse_month_year(month: int | None, year: int | None) -> tuple[int, int]:
    today = date.today()
    return month or today.month, year or today.year
