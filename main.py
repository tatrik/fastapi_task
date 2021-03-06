import uvicorn
from fastapi import FastAPI
from src.db import database
from src import endpoints


app = FastAPI(title="Social Network Task")
app.include_router(endpoints.user_router, prefix="/users", tags=["users"])
app.include_router(endpoints.auth_router, prefix="/auth", tags=["auth"])
app.include_router(endpoints.post_router, prefix="/posts", tags=["posts"])
app.include_router(endpoints.like_router, prefix="/likes", tags=["likes"])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)
