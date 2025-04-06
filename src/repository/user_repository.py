# repositories/user_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.repository.models import User
from src.schemas import UserCreate

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user_data: UserCreate) -> User:
        existing_user = await self.session.get(User, user_data.id)
        if existing_user:
            raise ValueError("User already exists")
        
        user = User(**user_data.model_dump())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def get_all_users(self) -> list[User]:
        result = await self.session.execute(select(User))
        return result.scalars().all()

    async def update_user(self, user_id: int, update_data: dict) -> User:
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        for key, value in update_data.items():
            setattr(user, key, value)
        
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete_user(self, user_id: int) -> None:
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        await self.session.delete(user)
        await self.session.commit()