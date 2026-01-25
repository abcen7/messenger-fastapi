from app.core.repositories import BaseRepository
from app.core.repositories.interfaces import EntityNotFoundError
from app.models import Users
from app.schemas.users import UserCreate, UserInDB


class UsersRepository(BaseRepository[Users, UserInDB]):
    _db_model = Users

    async def is_user_exists_by_email(self, user: UserCreate) -> bool:
        return self.get_one_or_none(self._db_model.email == user.email) is not None

    async def get_user_by_email(self, email: str) -> Users | None:
        return await self.get_one_or_none(self._db_model.email == email)
