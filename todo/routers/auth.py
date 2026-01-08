from fastapi import FastAPI, APIRouter

# app = FastAPI()  # use router for routing
router = APIRouter()

@router.get('/auth')
async def get_user():
    return {"user" : "authenticated"}