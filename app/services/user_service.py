from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from app.models import User, UserItem, Transfer
from app.database import async_session_maker
from app.auth.auth import decodeJWT


class UserService:
    """Класс для работы с пользователями"""
    
    @classmethod
    async def create_user(cls, user_data: dict):
        async with async_session_maker() as session:
            async with session.begin():
                new_user = User(**user_data)
                session.add(new_user)
                await session.flush()
                new_user_id = new_user.id
                await session.commit()
                return new_user_id
        
    @classmethod
    async def get_user_by_name_data(cls, username: str):
        async with async_session_maker() as session:
            query = select(User).options(joinedload(User.inventory).joinedload(UserItem.item)).filter_by(username=username)
            result = await session.execute(query)
            user = result.unique().scalar_one_or_none()
            
            if not user:
                return None

            user_dict = user.to_dict()
            user_dict['inventory'] = [{"type": item.item.type, "amount": item.amount} for item in user.inventory]
            return user_dict
        
    @classmethod
    async def get_user_by_id(cls, id: int) -> User | None:
        async with async_session_maker() as session:
            query = select(User).filter_by(id=id)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if not user:
                return None
            return user
        
    @classmethod
    async def get_user_data(cls, token: str):
        payload = decodeJWT(token)
        return await cls.get_user_by_name_data(payload["username"])
    
    @classmethod
    async def get_current_user_id(cls, token: str):
        payload = decodeJWT(token)
        return payload["user_id"]
    
    @classmethod
    async def transfer_coins_to_user(cls, transfer_data: dict) -> dict[str, str]:
        """Перевод монет другому пользователю"""
        # transfer_data: кто, кому, сколько
        async with async_session_maker() as session:
            async with session.begin():
                # 1 проверить что у пользователя 1 достаточно монет
                from_user = await cls.get_user_by_id(transfer_data['from_user_id'])
                if from_user.coins < transfer_data['amount']:
                    return {"transfer_result":"Не хватает монет"}
                # 2 списать монеты у пользователя 1
                update_coins_at_user_1 = (
                    update(User)
                    .where(User.id==transfer_data['from_user_id'])
                    .values(coins=User.coins-transfer_data['amount'])
                )
                # 3 добавить монеты пользователю 2
                update_coins_at_user_2 = (
                    update(User)
                    .where(User.id==transfer_data['to_user_id'])
                    .values(coins=User.coins+transfer_data['amount'])
                )
                await session.execute(update_coins_at_user_1)
                await session.execute(update_coins_at_user_2)
                # 4 зарегистрировать транзакцию
                new_transfer = Transfer(**transfer_data)
                session.add(new_transfer)
                await session.flush()
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return {"transfer_result":"Перевод прошело успешно"}

