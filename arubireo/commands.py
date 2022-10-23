import random
import re
from datetime import datetime

from arubireo.database import connection
from arubireo.utils import validate_date, validate_date_md

__commands__ = ("echo", "roll", "record", "audit")


def echo(**kwargs) -> str:
    msg = kwargs.get("msg", "")
    return msg


def roll(**kwargs) -> str:
    msg = kwargs.get("msg", "")
    msg = msg.strip()
    res = ""
    if msg.isdigit():
        num = int(msg)
        if num <= 0:
            return ""
        res = random.randint(1, num)
    elif re.match(r"^\-?\d+\s*\-?\d+$", msg):
        a, b = msg.split()
        a, b = int(a), int(b)
        if a > b:
            return ""
        res = random.randint(a, b)
    elif re.match(r"^\d+\s*[Dd]\s*\d+$", msg):
        a, b = msg.lower().split("d")
        a, b = int(a), int(b)
        if b <= 0:
            return ""
        res = [random.randint(1, b) for _ in range(a)]
    else:
        return ""
    return str(res)


def record(**kwargs) -> str:
    msg = kwargs.get("msg", "")
    user_id = kwargs.get("user_id", "")
    if not msg or not user_id:
        return "Failure"
    description, amount = msg.rsplit(" ", 1)
    if amount.isdigit():
        connection.add_bill(user_id, description, amount)
        return "Success"
    return "Failure"


def audit(**kwargs) -> str:
    msg = kwargs.get("msg", "")
    user_id = kwargs.get("user_id", "")
    if not msg or not user_id:
        return "Failure"
    msg = msg.strip()
    dates = msg.replace("/", "-").split()
    seen = set()
    total = 0
    res = ""
    bills = []
    if len(dates) == 1:
        date = dates[0]
        if not validate_date(date):
            if not validate_date_md(date):
                return "Failure"
            date = f"{datetime.utcnow().year}-{date}"
        bills = connection.get_date(user_id, date)
    elif len(dates) > 2:
        return "Failure"
    else:
        start, end = dates
        if not validate_date(start):
            if not validate_date_md(start):
                return "Failure"
            start = f"{datetime.utcnow().year}-{start}"
        if not validate_date(end):
            if not validate_date_md(end):
                return "Failure"
            end = f"{datetime.utcnow().year}-{end}"
        bills = connection.get_dates(user_id, start, end)
    for bill in bills:
        bill_time = re.sub(r"\.\d*", "", str(bill.time))  # Need to use copy
        if bill.date not in seen:
            seen.add(bill.date)
            res += f"--- {bill.date} ---\n"
        total += int(bill.amount)
        res += f"{bill_time:>8} {bill.description},{bill.amount}$\n"
    res += f"total: {total}"

    return str(res)


def add_user(**kwargs):
    user_id = kwargs.get("user_id", None)
    if not user_id:
        return ""


# def calc(expr: str) -> str:
#     expr = expr.replace("^", "**")
#     expr = expr.replace("x", "*")
#     expr = expr.replace("÷", "/")
#     expr = expr.replace("mod", "%")
#     if re.findall(f"[^0-9 {re.escape('+-*/%^().')}]", expr):
#         return ""
#     return eval(expr)
