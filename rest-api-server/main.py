from fastapi import FastAPI
from routers import summarise

app = FastAPI()

app.include_router(summarise.summariseRouter)