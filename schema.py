from pydantic import BaseModel

class Question(BaseModel):
    question: str
    answer: str

    class Config:
        orm_mode = True