from pydantic import BaseModel


class Record(BaseModel):
    phone: str
    address: str
