# from models import User # Replace with the actual path to your models
from models import User
from pydantic import BaseModel
from fastapi import APIRouter

userRouter = APIRouter()
class UserInput(BaseModel):
    username: str
    email: str
    role: str
    score:int

@userRouter.post("/")
async def create_user(user: UserInput):
    """
    Endpoint to create a new user in the database.
    """
    new_user = User(**user.model_dump())
    await new_user.save()  # Save the new user to the database
    return {"message": f"User {new_user.username} created successfully!"}
@userRouter.get("/")
async def get_users():
    """
    Endpoint to get all users.
    """
    # Fetch all users as a list of documents
    users = await User.find_all().to_list()
    
    # Return the list of users
    return {
        "users": [
            {**user.model_dump(), "id": str(user.id)} for user in users
        ]
    }
