import uvicorn
from fastapi import FastAPI


app = FastAPI(
    title="Blog Api"
)


@app.get("/")
def main():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8080)
