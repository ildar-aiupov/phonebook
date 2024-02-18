from pydantic import BaseModel


class CheckDataResp(BaseModel):
    phone: str
    address: str

    class Config:
        from_attributes = True
