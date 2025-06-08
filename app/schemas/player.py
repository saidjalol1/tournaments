from pydantic import BaseModel, EmailStr, Field


class PlayerRegister(BaseModel):
    name: str = Field(..., max_length=100)
    email: EmailStr


class PlayerOut(BaseModel):
    name: str
    email: EmailStr



    model_config = {
        "from_attributes": True,
    }