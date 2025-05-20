from fastapi import FastAPI
from app.routers import auth, user
from app.models import user as user_model

app = FastAPI()


app.include_router(auth.router)
app.include_router(user.router)