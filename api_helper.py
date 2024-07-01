import csv
import os
import random
import string
import time
from datetime import datetime, timedelta, timezone
from uuid import uuid4


def read_accounts_from_csv(file_path: str):
    accounts = set()
    with open(file_path, "r") as csv_f:
        reader = csv.DictReader(csv_f)
        for row in reader:
            accounts.add(row["account_num"])
    return list(accounts)


data_file_name = os.environ.get("LOCUST_DATA_FILE", "seed.csv")
print(f"loading data from {data_file_name}")
all_accounts: list[str] = read_accounts_from_csv(data_file_name)
print(f"loaded {len(all_accounts)} accounts")


def _random_characters_(length: int) -> str:
    """Generate a string of random characters of specified length."""
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def get_local_timezone():
    local_time_offset_sec = time.localtime().tm_gmtoff
    local_time_offset = timedelta(seconds=local_time_offset_sec)
    return timezone(local_time_offset)


def rand_fund_transfer_request(amount: int = 0):
    global all_accounts

    debit_account, credit_account = tuple(random.sample(all_accounts, 2))
    if amount == 0:
        amount = random.randint(300, 20000)
    amount_str = f"{int(amount/100)}.{amount%100:02}"

    return {
        "trx_date": datetime.now().strftime("%Y-%m-%d"),
        "ref_id": uuid4().hex,
        "debit_account_num": debit_account,
        "credit_account_num": credit_account,
        "amount": amount_str,
        "currency": "USD",
        "memo": _random_characters_(16),
    }
