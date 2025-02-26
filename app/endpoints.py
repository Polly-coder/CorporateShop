from fastapi import APIRouter, Depends
from app.schemas.users import TransferCreate, UserCreate, UserOut
from app.services.user_service import UserService
from app.auth.auth import signJWT
from app.auth.auth_bearer import JWTBearer


router = APIRouter(prefix='/api', tags=['Работа с api'])

@router.get(
        "/info", 
        summary="Получить информацию о монетах, инвентаре и истории транзакций пользователя"
)
async def get_user_info(token: str = Depends(JWTBearer())) -> UserOut:
    return await UserService.get_user_data(token)

@router.post(
        "/auth", 
        summary="Аутентификация и получение JWT-токена"
)
async def get_auth_token(user: UserCreate):
    # поиск существующего пользователя
    if old_user:=await UserService.get_user_by_name_data(user.username):
        if old_user['password'] == user.password:
            return signJWT({'user_id':old_user['id'], 'username':user.username})
        else:
            return {'result':'Неверный пароль'}
    # создание пользователя
    new_user_id = await UserService.create_user(user.model_dump())
    # возвращаем токен
    return signJWT({'user_id':new_user_id, 'username':user.username})

@router.post(
        "/sendCoin", 
        summary="Отправить монеты другому пользователю"
)
async def send_coins_to_user(transfer_data: TransferCreate, token: str = Depends(JWTBearer())):
    transfer_data_dict = transfer_data.model_dump()
    transfer_data_dict['from_user_id'] = await UserService.get_current_user_id(token)
    transfer_result = await UserService.transfer_coins_to_user(transfer_data_dict)
    return transfer_result