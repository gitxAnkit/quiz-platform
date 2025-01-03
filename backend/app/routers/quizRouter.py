from models import Quiz,Question # Replace with the actual path to your models
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from bson import ObjectId

quizRouter = APIRouter()

# Example route to get all quizzes
@quizRouter.get("/")
async def get_all_quizzes():
    """
    Endpoint to fetch all quizzes from the database.
    """
    quizzes = await Quiz.find_all().to_list()
    return {"quizzes": quizzes}

@quizRouter.get("/{quizId}")
async def get_quiz(quizId:str):
    """
    Endpoint to fetch quiz by Id from the database.
    """
    quiz = await Quiz.get(ObjectId(quizId));
    if(quiz):
        return quiz
    return {"error": "quiz not found"}

@quizRouter.post("/")
async def create_quiz(quiz: Quiz):
    """
    Endpoint to create a new quiz in the database.
    """
    # Validate each question in the quiz
    try:
        for question in quiz.questions:
            question.validate_correct_option()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Save the quiz to the database
    await quiz.insert()
    return {"message": f"Quiz '{quiz.title}' created successfully!", "quiz_id": str(quiz.id)}

    