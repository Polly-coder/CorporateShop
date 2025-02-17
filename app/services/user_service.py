from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.models import User, UserItem
from app.database import async_session_maker
from app.auth.auth import decodeJWT


class UserService:
    """Класс для работы с пользователями"""
    
    @classmethod
    async def create_user(cls, user_data: dict):
        pass
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
    async def get_current_user(cls, token: str):
        payload = decodeJWT(token)
        return await cls.get_user_by_name_data(payload["username"])
