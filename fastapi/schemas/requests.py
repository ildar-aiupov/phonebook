from pydantic import BaseModel, validator


class WriteDataReq(BaseModel):
    phone: str
    address: str

    @validator("phone")
    def validate_digits(cls, phone: str):
        if not phone.isdigit():
            raise ValueError("Bad phone number. It must contain only digits")
        return phone
