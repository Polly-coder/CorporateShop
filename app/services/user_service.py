from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.models import User
from app.database import async_session_maker


class UserService:
    @classmethod
    async def get_user(cls):
        async with async_session_maker() as session:
            #query = select(User).options(joinedload(User.inventory))
            query = select(User)
            user = await session.execute(query)
            user_info = user.scalars().all()
            return user_info
            '''user_data = []
            for user in user_info:
                user_dict = user.to_dict()
                if user.inventory:
                    ...
                user_dict['inventory'] = [user.inventory if user.inventory else None]'''
    
    @classmethod
    async def get_user_by_username(cls, username: str):
        async with async_session_maker() as session:
            query = select(User).filter_by(username=username)
            user = await session.execute(query)
            return user

        
