from pydantic import BaseModel, Field, EmailStr

class LoginData(BaseModel):
    email: EmailStr = Field(description="user email", examples=["alice@example.com"])
    password: str = Field(min_length=8, description="user password", examples=["hashed_password_1"])

class RegisterData(LoginData):
    name: str = Field(min_length=3, description="user name", examples=["User Name"])

class Token(BaseModel):
    access_token:str
    token_type: str =  Field(default="bearer")