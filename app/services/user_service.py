from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.models import User, UserItem
from app.database import async_session_maker
from app.schemas.items import UserItemOut


class UserService:
    @classmethod
    async def get_user(cls):
        async with async_session_maker() as session:
            query = select(User).options(joinedload(User.inventory))
            #query = select(User)
            user = await session.execute(query)
            user_info = user.scalars().all()
            #return user_info
            user_data = []
            for user in user_info:
                user_dict = user.to_dict()
                if user.inventory:
                    ...
                user_dict['inventory'] = [user.inventory if user.inventory else None]
    
    @classmethod
    async def get_user_by_username(cls, username: str):
        async with async_session_maker() as session:
            query = select(User).filter_by(username=username)
            user = await session.execute(query)
            return user
        
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