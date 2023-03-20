import uvicorn
from fastapi import FastAPI

from routers import router

app = FastAPI(
    title="Blog Api"
)


@app.get("/")
def main():
    return {"Hello": "World"}


app.include_router(router=router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8080)
