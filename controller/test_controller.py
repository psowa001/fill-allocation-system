import pytest
from main import buy_shares


@pytest.fixture
def transaction_payload():
    return {
        "stock": "ABD",
        "price": 10,
        "quantity": 10
    }


@pytest.fixture
def accounts_payload():
    return {
        "account1": {
            "share": 30,
            "shares": {
                "ABD": {
                    "price": 10,
                    "quantity": 1
                }
            }
        },
        "account2": {
            "share": 20,
            "shares": {
                "ABD": {
                    "price": 10,
                    "quantity": 1
                }
            }
        },
        "account3": {
            "share": 50,
            "shares": {
                "ABD": {
                    "price": 10,
                    "quantity": 1
                }
            }
        }
    }


def test_buy_shares(transaction_payload, accounts_payload):
    sum = 0
    for account, details in accounts_payload.items():
        for share, stock in details["shares"].items():
            sum += stock["price"]
    sum += transaction_payload["price"] * transaction_payload["quantity"]
    accounts = buy_shares(transaction_payload, accounts_payload)

    for account, details in accounts.items():
        assert round(details["overall"] / sum * 100) <= details["share"]

