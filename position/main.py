from fastapi import FastAPI, status


app = FastAPI()


@app.post("/positions/", status_code=status.HTTP_200_OK)
async def print_positions(positions: dict):
    print(positions)
    