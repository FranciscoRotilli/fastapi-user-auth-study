from fastapi import FastAPI
from .auth import auth_router
from .users import users_router

api = FastAPI(
    title="FastAPI User Auth Study",
    description="API developed to study FastAPI user authentication",
    version="0.1.0"
)

api.include_router(auth_router.router)
api.include_router(users_router.router)

@api.get("/", tags=["Root"])
def read_root():
    """Root endpoint for online check."""
    return {"status": "ok", "project": "FastAPI User Auth Study"}