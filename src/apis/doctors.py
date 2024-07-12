from fastapi import APIRouter, status, Response, Request
from typing import List

from src.models.dtos import CreateDoctorReqDTO, GetDoctorDTO, QueryDoctorsDTO, DefaultResponseDTO
from src.logger import log
from .doctors_logic import DoctorLogic

doctor_router = APIRouter()


@doctor_router.get(path='/{id}', status_code=status.HTTP_200_OK, response_model=GetDoctorDTO)
async def get_doctor_by_id(request: Request, response: Response, id: int) -> GetDoctorDTO:
    log.info(f"get doctor by id: {id}")
    resp = GetDoctorDTO()
    # validate request payload
    if not id or id <= 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        resp.err_message = 'invalid doctor id'
        return resp
    try:
        logic = DoctorLogic()
        doctor = logic.get_doctor_by_id(id)
        if doctor is None:
            resp.err_message = 'id not found'
            return resp
        resp.data = doctor
        return resp
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        resp.err_message = e.__str__()
        return resp


@doctor_router.get(path='', status_code=status.HTTP_200_OK, response_model=QueryDoctorsDTO)
async def query_doctors(request: Request, response: Response, district: str | None = None, category: str | None = None,
                        price_range: str | None = None, language: str | None = None) -> QueryDoctorsDTO:
    log.info(f'query doctors by district: [{district}]. category: [{category}].'
             f' price range: [{price_range}]. language: [{language}]')
    resp = QueryDoctorsDTO()
    # payload validation
    if language and language != "en" and language != "cn":
        response.status_code = status.HTTP_400_BAD_REQUEST
        resp.err_message = 'unexpected language code'
        return resp
    if not language:
        language = 'en'
    try:
        logic = DoctorLogic()
        doctors = logic.query_doctors(district, category, price_range, language)
        resp.data = doctors
        resp.rows = len(doctors)
        return resp
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        resp.err_message = e.__str__()
        return resp


@doctor_router.post(path='', status_code=status.HTTP_200_OK, response_model=DefaultResponseDTO)
async def create_doctors(request: Request, response: Response, doctors: List[CreateDoctorReqDTO]) -> DefaultResponseDTO:
    log.info(f"create doctors: {doctors}")
    resp = DefaultResponseDTO(message='success')
    if len(doctors) == 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        resp.err_message = 'no doctors entity found in payload'
        return resp
    if len(doctors) > 500:
        response.status_code = status.HTTP_400_BAD_REQUEST
        resp.err_message = 'limit 500 entity reached'
        return resp
    try:
        logic = DoctorLogic()
        logic.create_doctors(doctors)
        return resp
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        resp.err_message = e.__str__()
        return resp
