from fastapi import HTTPException, status
from src.app.core.security import get_password_hash
from src.app.models.user import User
from src.app.schemas.user import UserSchema, UserRoleEnum
from src.app.schemas.message import Message
from src.app.repositories.users import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def _is_owner(self, user_id: int, current_user: User):
        if current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
            )

    async def _check_user_authorization(self, user_id: int, current_user: User):
        if current_user.id != user_id or current_user.role != UserRoleEnum.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
            )

    async def _get_user_or_404(self, user_id: int) -> User:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user

    async def create_user(self, user_data: UserSchema) -> User:
        existing_user = await self.user_repository.get_user_by_username_or_email(
            username=user_data.username, email=user_data.email
        )

        if existing_user:
            if existing_user.username == user_data.username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists",
                )
            elif existing_user.email == user_data.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists",
                )

        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password=get_password_hash(user_data.password),
        )

        try:
            return await self.user_repository.add_user(new_user)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating user: {e}")

    async def update_user(
        self, user_id: int, user_data: UserSchema, current_user: User
    ) -> User:
        await self._is_owner(user_id, current_user)

        user = await self._get_user_or_404(user_id)

        user.username = user_data.username
        user.password = get_password_hash(user_data.password)
        user.email = user_data.email

        try:
            return await self.user_repository.update_user(user)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating user: {e}")

    async def get_all_users(self, current_user: User) -> list[User]:
        await self._check_user_authorization(current_user.id, current_user)
        try:
            return await self.user_repository.get_all_users_repository()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving users: {e}")

    async def get_user_by_id(self, user_id: int, current_user: User) -> User:
        await self._check_user_authorization(user_id, current_user)
        return await self._get_user_or_404(user_id)

    async def delete_user(self, user_id: int, current_user: User) -> Message:
        await self._check_user_authorization(user_id, current_user)

        try:
            await self.user_repository.delete_user(user_id)
            return Message(message=f"User {user_id} deleted successfully")
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error deleting user {user_id}: {e}"
            )
