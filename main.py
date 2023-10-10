import os
from dotenv import load_dotenv
from fastapi import Body, Depends, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi_sqlalchemy import DBSessionMiddleware
import requests
from sqlalchemy.orm import Session

from db import get_db
from models import Question

load_dotenv('.env')

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

@app.post('/trivia/')
def trivia(db: Session = Depends(get_db), data=Body()):
    number = data.get('questions_num')
    question_ids = []
    for i in db.query(Question).all():
        j_data = jsonable_encoder(i)
        question_ids.append(j_data.get('id'))
    iter_counter = 0
    while True:
        response = requests.get('https://jservice.io/api/random', {"count": int(number) - iter_counter})
        for elem in response.json():
            if elem.get('id') not in question_ids:
                question_instance = Question(
                    id=elem.get('id'),
                    question=elem.get('question'),
                    answer=elem.get('answer'),
                    created_at=elem.get('created_at')
                )
                db.add(question_instance)
                db.commit()
                db.refresh(question_instance)
                iter_counter += 1
        if iter_counter == int(number):
            break
    json_data = jsonable_encoder(db.query(Question).all()[-1])
    return json_data.get('question')
