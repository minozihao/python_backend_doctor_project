"""API request and response models (Data transfer object dto)"""
from pydantic import BaseModel, Field


class CreateDoctorReqDTO(BaseModel):
    first_name: str = Field(examples=['Amber'])
    last_name: str = Field(examples=['Tang'])
    first_name_cn: str = Field(examples=['兆鹏'])
    last_name_cn: str = Field(examples=['汤'])
    consultation_fee: float = Field(default=0, description='consultation fee', examples=[540, 150])
    consultation_fee_detail: str = Field(description='extra detail info about consultation fee',
                                         examples=['inclusive 3 days of western medicine'])
    consultation_fee_detail_cn: str = Field(default=None, description='extra detail info about consultation fee',
                                            examples=['包含3日西药'])
    category: str = Field(examples=['General Practitioner'])
    phone: str = Field(examples=['28773222,28773888'])
    street: str
    room: str | None = None
    district: str
    city: str
    street_cn: str | None = None
    room_cn: str | None = None
    district_cn: str | None = None
    city_cn: str | None = None
    schedule_monday: str
    schedule_tuesday: str
    schedule_wednesday: str
    schedule_thursday: str
    schedule_friday: str
    schedule_saturday: str
    schedule_sunday: str
    public_holiday: str


class ScheduleDTO(BaseModel):
    day_in_week: str = Field(default=None, description='taking value monday to sunday respectively and public_holiday',
                             examples=['monday', 'sunday', 'public_holiday'])
    working_hours: str = Field(default=None, description='taking string values like "9:00-12:00, 1:00-4:00"',
                               examples=['9:00-12:00, 1:00-4:00'])


class AddressDTO(BaseModel):
    street: str | None = None
    room: str | None = None
    district: str | None = None
    city: str | None = None


class CategoryDTO(BaseModel):
    name: str | None = None

class DoctorDTO(BaseModel):
    first_name: str
    last_name: str
    consultation_fee: float
    consultation_fee_detail: str | None = None
    phone: str
    category: CategoryDTO | None = None
    schedule: list[ScheduleDTO] | None = None
    address: AddressDTO | None = None


class GetDoctorDTO(BaseModel):
    data: DoctorDTO | None = None
    err_message: str = ''


class QueryDoctorsDTO(BaseModel):
    data: list[DoctorDTO] = []
    rows: int = 0
    err_message: str = ''


class DefaultResponseDTO(BaseModel):
    err_message: str = ''
