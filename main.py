from contextlib import asynccontextmanager

import redis.asyncio as redis
import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI

from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware

from src.routes import contacts, auth, users


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    The lifespan function is a coroutine that runs before and after the application.
    It's used to initialize the FastAPILimiter class with Redis connection information,
    and then close it when the app shuts down.

    :param _app: FastAPI: Pass the fastapi object to the lifespan function
    :return: A context manager
    :doc-author: Trelent
    """
    r = await redis.Redis(
        host='localhost', port=6379, db=0, encoding="utf-8",
        decode_responses=True
    )
    await FastAPILimiter.init(r)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(users.router, prefix='/api')


origins = [
    "http://localhost:3000"
    ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.on_event("startup")
# async def startup():
#     r = await redis.Redis(
#         host='localhost', port=6379, db=0, encoding="utf-8",
#         decode_responses=True
#     )
#     await FastAPILimiter.init(r)


@app.get("/")
def read_root():
    """
    The read_root function returns a dictionary with the key &quot;message&quot; and value &quot;Hello World&quot;.

    :return: A dictionary with a single key:message
    :doc-author: Trelent
    """
    return {"message": "Hello World"}


if __name__ == "__main__":
    load_dotenv()
    uvicorn.run(app, host="127.0.0.1", port=8000)

