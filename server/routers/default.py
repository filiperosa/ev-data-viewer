from fastapi import HTTPException, APIRouter

default_router = APIRouter()

@default_router.get("/")
async def root():
    return {"message": "Hello World"}