from fastapi import APIRouter

from src.api.files import router as file_router
from src.api.users import router as user_router
from src.api.protected import router as protected_router

main_router = APIRouter()

main_router.include_router(file_router, prefix="/files", tags=["files"])
main_router.include_router(user_router, prefix="/users", tags=["users"])
main_router.include_router(protected_router, tags=["protected"])