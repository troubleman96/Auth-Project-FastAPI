from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api.routes import auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def root():
    return {"message": "FastAPI Auth Project is up and running!"}
