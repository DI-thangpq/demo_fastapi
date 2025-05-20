from fastapi import FastAPI
from app.routers import auth, post, user

app = FastAPI()


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)