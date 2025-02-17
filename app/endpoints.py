from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from app.schemas.users import UserOut
from app.services.user_service import UserService


router = APIRouter(prefix='/api', tags=['Работа с api'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get(
        "/info", 
        summary="Получить информацию о монетах, инвентаре и истории транзакций пользователя"
)
#async def get_user_info(token: str = Depends(oauth2_scheme)) -> list[UserOut]:
async def get_user_info() -> list[UserOut]:
    return await UserService.get_user()