# services/user_service.py
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.user_repository import UserRepository
from src.repository.models import User, RoleEnum
from src.schemas import UserCreate


class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)

    async def create_user(self, user_data: UserCreate) -> User:
        try:
            return await self.repository.create_user(user_data)
        except ValueError:
            pass

    async def get_user(self, user_id: int) -> Optional[User]:
        return await self.repository.get_user_by_id(user_id)

    async def update_user(self, user_id: int, update_data: dict) -> User:
        return await self.repository.update_user(user_id, update_data)

    async def delete_user(self, user_id: int) -> None:
        await self.repository.delete_user(user_id)

    async def is_admin(self, user_id: int) -> bool:
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        print(f"{user.role=}\t {RoleEnum.ADMIN=}")
        return user.role == RoleEnum.ADMIN

    async def list_users(self) -> list[User]:
        return await self.repository.get_all_users()
