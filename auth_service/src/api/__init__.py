from fastapi import APIRouter

from auth_service.src.api.register import router as register
from auth_service.src.api.auth import router as users_router


main_router = APIRouter()

main_router.include_router(users_router, prefix="/users", tags=["users"])
main_router.include_router(register, prefix="/register_users", tags=["register_users"])
