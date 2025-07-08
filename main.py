import uvicorn
from fastapi import FastAPI

from api.google import serper
from api.huoshan import translate

app = FastAPI()

app.include_router(translate.router)
app.include_router(serper.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", workers=4)
