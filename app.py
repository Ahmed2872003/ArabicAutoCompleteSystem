from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles

from model import aragpt2_baseModel

import re

app = FastAPI()
api_router = APIRouter()

ara2gpt_baseModel = aragpt2_baseModel()


app.mount("/api/v1/static", StaticFiles(directory="static", html=True), name="static")




@api_router.get("/suggestions")
def getSuggestions(input: str = "", nOfSequences: int = 5):

    input = re.sub(r'[^a-zA-Z0-9.? \u0600-\u06FF]', ' ', input)

    return { "suggestions":  ara2gpt_baseModel.generate_sentences(input, nOfSequences)}


app.include_router(api_router, prefix="/api/v1")





