from fastapi import APIRouter, Depends

from src.api.users import security

router = APIRouter()

@router.get("/protected", dependencies=[Depends(security.access_token_required)])
def protected():
    return {"data": "SECRET"}
