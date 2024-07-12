from fastapi import FastAPI

from src.apis.doctors import doctor_router

DOCTOR_URL_PREFIX = '/doctor'


def init_router(app: FastAPI) -> None:
    """
    register routes
    :param app:
    :return: None
    """
    app.include_router(doctor_router, prefix=DOCTOR_URL_PREFIX, tags=[DOCTOR_URL_PREFIX])
