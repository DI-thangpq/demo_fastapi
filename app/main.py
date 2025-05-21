from fastapi import FastAPI
from app.routers import auth, comment, post, user

app = FastAPI()


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)