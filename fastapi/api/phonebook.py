from typing import Annotated

from fastapi import APIRouter, Depends, status

from services.phonebook import PhoneBookService, get_phonebook_service
from schemas.responses import CheckDataResp
from schemas.requests import WriteDataReq


router = APIRouter()
CommonsDep = Annotated[PhoneBookService, Depends(get_phonebook_service)]


@router.get(
    "/check_data",
    response_model=CheckDataResp,
    status_code=status.HTTP_200_OK,
    summary="Get address by phone number",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Record not found"}}
)
async def check_data(phone: str, phonebook_service: CommonsDep) -> CheckDataResp:
    record = await phonebook_service.get_record(phone)
    return CheckDataResp(**record.model_dump())


@router.post(
    "/write_data",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new record",
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Bad request"}}
)
async def create_data(
    write_data_req: WriteDataReq, phonebook_service: CommonsDep
) -> None:
    await phonebook_service.set_record(data=write_data_req)


@router.patch(
    "/write_data",
    status_code=status.HTTP_200_OK,
    summary="Update adress in a record",
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Bad request"}}
)
async def change_address(
    write_data_req: WriteDataReq, phonebook_service: CommonsDep
) -> None:
    await phonebook_service.update_record(data=write_data_req)
