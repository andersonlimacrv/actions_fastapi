from fastapi import HTTPException, status
from src.app.core.security import get_password_hash
from src.app.core.config import settings
from src.app.models.user import User
from src.app.schemas.user import UserSchema, UserRoleEnum
from src.app.schemas.message import Message
from src.app.repositories.users import UserRepository
from src.app.exceptions.messages import Except
from src.app.exceptions.exceptions import UsernameAlreadyExists


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def _is_owner_or_admin(self, user_id: int, current_user: User):
        if current_user.id != user_id and current_user.role != UserRoleEnum.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=Except.not_allowed_403(),
            )

    async def _is_admin(self, current_user: User):
        if current_user.role != UserRoleEnum.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=Except.not_allowed_403(),
            )

    async def _get_user_or_404(self, user_id: int) -> User:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=Except.user_not_found_404(user_id),
            )
        return user

    async def create_user(self, user_data: UserSchema) -> User:
        existing_user = await self.user_repository.get_user_by_username(
            username=user_data.username
        )

        if existing_user:
            if existing_user.username == user_data.username:
                raise UsernameAlreadyExists(
                    message=Except.bad_request_400(f"Username {user_data.username}")
                )

        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password=get_password_hash(user_data.password),
        )

        try:
            return await self.user_repository.add_user(new_user)
        except Exception as e:
            raise HTTPException(status_code=500, detail=Except.error_creating_user(e))

    async def update_user(
        self, user_id: int, user_data: UserSchema, current_user: User
    ) -> User:
        await self._is_owner_or_admin(user_id, current_user)
        user = await self._get_user_or_404(user_id)

        already_username_exists = await self.user_repository.get_user_by_username(
            username=user_data.username
        )
        if (
            already_username_exists
            and already_username_exists.username != user.username
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=Except.bad_request_400("Username"),
            )

        user.username = user_data.username
        user.password = get_password_hash(user_data.password)
        user.email = user_data.email

        try:
            return await self.user_repository.update_user(user)
        except Exception as e:
            raise HTTPException(status_code=500, detail=Except.error_updating_user(e))

    async def activate_or_deactivate_user(
        self, user_id: int, current_user: User
    ) -> User:
        await self._is_admin(current_user)
        user = await self._get_user_or_404(user_id)
        if user.username == settings.ROOT_USERNAME:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=Except.not_allowed_403(),
            )
        user.is_active = not user.is_active
        try:
            return await self.user_repository.update_user(user)
        except Exception as e:
            raise HTTPException(status_code=500, detail=Except.error_updating_user(e))

    async def get_all_users(self, current_user: User) -> list[User]:
        await self._is_admin(current_user)
        try:
            return await self.user_repository.get_all_users_repository()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving users: {e}")

    async def get_user_by_id(self, user_id: int, current_user: User) -> User:
        await self._is_owner_or_admin(user_id, current_user)
        return await self._get_user_or_404(user_id)

    async def delete_user(self, user_id: int, current_user: User) -> Message:
        user = await self._get_user_or_404(user_id)
        await self._is_owner_or_admin(user_id, current_user)
        if user.username == settings.ROOT_USERNAME:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=Except.not_allowed_403(),
            )
        try:
            await self.user_repository.delete_user(user_id)
            return Message(message=f"User {user_id} deleted successfully")
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=Except.error_deleting_user(user_id, e)
            )
