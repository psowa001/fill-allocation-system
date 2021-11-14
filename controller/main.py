from fastapi import FastAPI, status
from aiohttp import ClientSession, ClientConnectionError
from fastapi_utils.tasks import repeat_every


app = FastAPI()
accounts = {}

@app.on_event("startup")
@repeat_every(seconds=10)
async def send_repost():
    async with ClientSession() as session:
        try:
            async with session.post("http://position:8000/positions/", json=accounts, ssl=False) as response:
                response = await response.read()
        except ClientConnectionError as e:
            print('Connection Error', str(e))

def buy_shares(transaction: dict, accounts: dict):
    all_accounts = 0
    for account, details in accounts.items():
        sum = 0
        for share, stock in details.get("shares", {}).items():
            sum += stock["price"]
        details["overall"] = sum
        all_accounts += sum

    all_accounts += transaction["price"] * transaction["quantity"]

    while transaction["quantity"] > 0:
        quantity = transaction["quantity"]
        for account, details in accounts.items():
            if round((details["overall"] + transaction["price"]) / all_accounts * 100) <= details["share"]:
                details["overall"] += transaction["price"]
                if not details["shares"].get(transaction["stock"]):
                    details["shares"][transaction["stock"]] = {"quantity": 0, "price": 0}
                details["shares"][transaction["stock"]]["quantity"] += 1
                details["shares"][transaction["stock"]]["price"] += transaction["price"]
                transaction["quantity"] -= 1
        if transaction["quantity"] == quantity:
            break
    return accounts


@app.post("/aum/", status_code=status.HTTP_200_OK)
async def account_split(split: dict):
    global accounts
    for account, per in split.items():
        if not accounts.get(account):
            accounts[account] = {}
        accounts[account]["share"] = per
        if not accounts[account].get("shares"):
            accounts[account]["shares"] = {}
    return {"details": "Accounts updated."}


@app.post("/fill/", status_code=status.HTTP_200_OK)
async def incoming_transaction(transaction: dict):
    global accounts
    accounts = buy_shares(transaction, accounts)
    return {"details": "Transaction completed."}

