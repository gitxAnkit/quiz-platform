from fastapi import FastAPI
from contextlib import asynccontextmanager
from db import db
from routers.quizRouter import quizRouter
from routers.userRouter import userRouter

# Define lifespan context manager for startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event 
    await db.connect()
    yield  # This is where FastAPI runs while the app is serving requests
    # Shutdown event 
    await db.close()



# Create FastAPI app with the lifespan context manager
app = FastAPI(lifespan=lifespan)

app.include_router(quizRouter, prefix="/quizzes", tags=["quizzes"])
app.include_router(userRouter,prefix="/users", tags=["users"])

@app.get("/")
async def read_root():
    """
    A simple root endpoint to test the app.
    """
    return {"message": "Welcome to the quiz platform!"}


