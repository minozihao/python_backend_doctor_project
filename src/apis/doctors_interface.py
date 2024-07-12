from abc import ABC, abstractmethod

from src.models.dtos import DoctorDTO, CreateDoctorReqDTO


class DoctorLogicAbs(ABC):
    @abstractmethod
    def get_doctor_by_id(self, id) -> DoctorDTO | None:
        pass

    @abstractmethod
    def query_doctors(self, district: str | None, category: str | None, price_range: str | None,
                      language: str) -> list[DoctorDTO]:
        pass

    @abstractmethod
    def create_doctors(self, doctors: list[CreateDoctorReqDTO]) -> None:
        pass
