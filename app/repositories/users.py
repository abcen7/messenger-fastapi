from app.core.protocols.repositories import BaseRepository
from app.models import Users
from app.schemas.users import UserInDB


class UsersRepository(BaseRepository[Users, UserInDB]):
    model = Users
