from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str  # another unique field
    first_name: str
    last_name: str
    email: EmailStr  # field
    phone_number: str  # useless field


class UserSchema(User):
    id: int


class UserCreate(User):
    password: str


class UserInDB(User):
    hashed_password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
