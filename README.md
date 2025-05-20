git clone https://your-repo-url.git
cd demo-fastapi

python -m venv venv
.\venv\Scripts\activate

pip install -r requirements.txt

.env:
DATABASE_URL=
JWT_SECRET_KEY=
JWT_ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=

alembic upgrade head

uvicorn app.main:app --reload
