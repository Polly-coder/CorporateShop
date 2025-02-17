from fastapi import APIRouter, Depends
from app.schemas.users import UserCreate, UserOut
from app.services.user_service import UserService
from app.auth.auth import signJWT
from app.auth.auth_bearer import JWTBearer


router = APIRouter(prefix='/api', tags=['Работа с api'])

@router.get(
        "/info", 
        summary="Получить информацию о монетах, инвентаре и истории транзакций пользователя"
)
async def get_user_info(token: str = Depends(JWTBearer())) -> UserOut:
    return await UserService.get_current_user(token)

@router.post(
        "/auth", 
        summary="Аутентификация и получение JWT-токена"
)
async def get_auth_token(user: UserCreate):
    # создание пользователя
    new_user_id = await UserService.create_user(user.model_dump())
    # возвращаем токен
    return signJWT(user.username)