from src.models.dtos import CreateDoctorReqDTO, DoctorDTO, CategoryDTO, AddressDTO, ScheduleDTO

from src.apis.doctors_interface import DoctorLogicAbs


class DoctorLogicMock(DoctorLogicAbs):

    def get_doctor_by_id(self, id) -> DoctorDTO | None:
        if id == 5:  # for testing, id=5 returns None which represents doctor id not found
            return None
        schedule = [ScheduleDTO(day_in_week='monday', working_hours='9:00-12:00'),
                    ScheduleDTO(day_in_week='tuesday', working_hours='9:00-12:00')]
        address = AddressDTO(street='66 qwert st', room='A3', district='futian', city='shenzhen')
        return DoctorDTO(first_name='abc', last_name='efg', consultation_fee=50,
                         consultation_fee_detail='include 3 days medicine', phone='555666777',
                         category=CategoryDTO(name='bone'), schedule=schedule, address=address)

    def query_doctors(self, district: str | None, category: str | None, price_range: str | None,
                      language: str) -> list[DoctorDTO]:
        if district == 'futian' or category == 'bone' or price_range == '0-200':
            schedule = [ScheduleDTO(day_in_week='monday', working_hours='9:00-12:00'),
                        ScheduleDTO(day_in_week='tuesday', working_hours='9:00-12:00')]
            address = AddressDTO(street='66 qwert st', room='A3', district='futian', city='shenzhen')
            return [DoctorDTO(first_name='bob', last_name='john', consultation_fee=50,
                              consultation_fee_detail='include 3 days medicine', phone='555666777',
                              category=CategoryDTO(name='bone'), schedule=schedule, address=address),
                    DoctorDTO(first_name='charlie', last_name='king', consultation_fee=100,
                              consultation_fee_detail='include 3 days medicine', phone='555666777',
                              category=CategoryDTO(name='bone'), schedule=schedule, address=address),
                    ]
        return []

    def create_doctors(self, doctors: list[CreateDoctorReqDTO]) -> None:
        """
        create doctors to db from payload
        :param doctors: list of CreateDoctorReqDTO request payload
        :return: None
        """
        return
