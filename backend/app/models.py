from beanie import Document
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime,timezone
from typing import Literal

# User model
class User(Document):
    username: str
    email: str
    score: int = 0
    role: Literal["admin", "user"]="user"  # Restrict role to "admin" or "user"

    created_at: datetime = datetime.now(timezone.utc)  # Use timezone-aware UTC datetime
    quizzes: List[dict] = []  # List of dicts to store quiz references and scores
    
    class Settings:
        name = "users"  # MongoDB collection name
    async def add_quiz_score(self, quiz_id, score: int):
        """
        Helper function to add quiz score to the user.
        """
        self.quizzes.append({"quiz_id": quiz_id, "current_score": score})
        await self.save()

# Question model
class Question(BaseModel):
    question_text: str
    options: List[str]
    correct_option: int  # Index of the correct option

    # Validation to ensure correct_option is within the range of options
    def validate_correct_option(self):
        if not (0 <= self.correct_option < len(self.options)):
            raise ValueError("correct_option must be a valid index in the options list.")

# Quiz model
class Quiz(Document):
    title: str
    description: Optional[str] = None
    questions: List[Question]
    created_at: datetime = datetime.now(timezone.utc)  # Use timezone-aware UTC datetime
    
    class Settings:
        name = "quizzes"

