from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr  # field
    full_name: str


class UserSchema(User):
    id: int


class UserCreate(User):
    password: str


class UserInDB(User):
    hashed_password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
