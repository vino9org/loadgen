import csv
import random
import string
import time
from datetime import datetime, timedelta, timezone
from uuid import uuid4

__all_accounts__: list[str] = []


def read_accounts_from_csv(file_path: str):
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


def get_local_timezone():
    local_time_offset_sec = time.localtime().tm_gmtoff
    local_time_offset = timedelta(seconds=local_time_offset_sec)
    return timezone(local_time_offset)


def rand_fund_transfer_request(all_accounts: list[str], amount: int = 0):
    debit_account = random.choice(all_accounts)
    credit_account = random.choice(all_accounts)
    if amount == 0:
        amount = random.randint(300, 1000)

    return {
        "trx_date": datetime.now().strftime("%Y-%m-%d"),
        "trx_id": uuid4().hex,
        "debit_account_num": debit_account,
        "credit_account_num": credit_account,
        "amount": float(amount / 100),
        "currency": "USD",
        "memo": _random_characters_(16),
    }
