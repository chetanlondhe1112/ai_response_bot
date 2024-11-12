from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def hello():
    return {"helo world"}


@app.get("/items/{item_id}")
async def items(item_id : int):
    return {"item_id":item_id}
