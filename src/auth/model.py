from pydantic import BaseModel, Field, EmailStr

class LoginData(BaseModel):
    email: EmailStr = Field(description="user email", examples=["user@example.com"])
    password: str = Field(min_length=8, description="user password", examples=["user1234"])

class RegisterData(LoginData):
    name: str = Field(min_length=3, description="user name", examples=["User Name"])