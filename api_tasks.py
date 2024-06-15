import csv
import random
import string
from datetime import datetime

import pytz

__all_accounts__ = []


def _read_all_accounts_(file_path: str):
    accounts = set()
    with open(file_path, "r") as csv_f:
        reader = csv.DictReader(csv_f)
        for row in reader:
            accounts.add(row["account_num"])
    return list(accounts)


def _random_characters_(length: int) -> str:
    """Generate a string of random characters of specified length."""
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def rand_fund_transfer_request(csv_file: str):
    global __all_accounts__

    if len(__all_accounts__) == 0:
        __all_accounts__ = _read_all_accounts_(csv_file)

    debit_account = random.choice(__all_accounts__)
    credit_account = random.choice(__all_accounts__)
    amount = random.randint(300, 1000)
    now_dt = datetime.now(pytz.timezone("Asia/Singapore"))

    return {
        "trx_date": now_dt.strftime("%Y-%m-%d"),
        "debit_account_num": debit_account,
        "credit_account_num": credit_account,
        "amount": float(amount / 100),
        "currency": "USD",
        "memo": _random_characters_(16),
        "created_at": now_dt.isoformat(),
    }
