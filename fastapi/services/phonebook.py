from typing import Annotated
from functools import lru_cache
import logging

from fastapi import Depends, HTTPException, status

from models.record import Record
from db.storage_interface import StorageInterface
from db.current_storage import get_current_storage
from schemas.requests import WriteDataReq


@lru_cache()
def get_phonebook_service(
    storage: Annotated[StorageInterface, Depends(get_current_storage)],
) -> "PhoneBookService":
    return PhoneBookService(storage)


class PhoneBookService:
    def __init__(self, storage: StorageInterface):
        self.storage = storage

    async def get_record(self, phone: str) -> Record | None:
        if address := await self.storage.get_entry(key=phone):
            logging.info(f"Value {address} by key {phone} was taken from storage")
            return Record(phone=phone, address=address)
        logging.error(f"Value {address} by key {phone} was not taken from storage")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="A record with this phone number is not found",
        )

    async def set_record(self, data: WriteDataReq) -> None:
        phone = data.phone
        address = data.address
        if await self.storage.get_entry(key=phone):
            logging.error(f"Failure creating new record ({phone}, {address}). The key ({phone}) is busy")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="A record with this phone number already exists",
            )
        await self.storage.set_entry(key=phone, value=address)
        logging.info(f"New record ({phone}, {address}) was created")

    async def update_record(self, data: WriteDataReq) -> None:
        phone = data.phone
        address = data.address
        if not await self.storage.get_entry(key=phone):
            logging.error(f"Failure updating record ({phone}, {address}). The record with the key ({phone}) does not exist.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="A record with this phone number does not exist",
            )
        await self.storage.set_entry(key=phone, value=address)
        logging.info(f"The record ({phone}, {address}) was updated")
