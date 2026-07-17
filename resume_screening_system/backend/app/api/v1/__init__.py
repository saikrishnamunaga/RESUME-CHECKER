from fastapi import APIRouter
from . import auth, login, register, screening

router = APIRouter()
router.include_router(auth.router)
router.include_router(login.router)
router.include_router(register.router)
router.include_router(screening.router)
