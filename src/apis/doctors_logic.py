from typing import List
from sqlmodel import Session, select

from src.models.dtos import CreateDoctorReqDTO, DoctorDTO, CategoryDTO, AddressDTO, ScheduleDTO
from src.models.orms import engine, Doctor, PriceRange, Category, Schedule, Address, AddressCN


class DoctorLogic:

    def get_doctor_by_id(self, id) -> DoctorDTO | None:
        with Session(engine) as session:
            d = session.get(Doctor, id)

            if d is None:
                return None

            # transform doctor db model to dto
            catgo = CategoryDTO(name=d.category.name)
            addr = AddressDTO(street=d.address.street, room=d.address.room, district=d.address.district,
                              city=d.address.city)
            schedules = [ScheduleDTO(day_in_week=s.day_in_week, working_hours=s.working_hours) for s in
                         d.schedule]
            dto = DoctorDTO(first_name=d.first_name, last_name=d.last_name,
                            consultation_fee=d.consultation_fee,
                            consultation_fee_detail=d.consultation_fee_detail, phone=d.phone,
                            category=catgo, schedule=schedules, address=addr)
            return dto

    def query_doctors(self, district: str | None, category: str | None, price_range: str | None,
                      language: str) -> List[DoctorDTO]:
        """
        query doctors based on parameter. assume language takes value 'en', 'cn'
        :param district:
        :param category:
        :param price_range:
        :param language:
        :return:
        """
        with Session(engine) as session:
            statement = select(Doctor).join(Category, isouter=True
                                            ).join(PriceRange, isouter=True
                                                   ).join(Schedule, isouter=True
                                                          ).join(Address, isouter=True).join(AddressCN, isouter=True)
            if category and category != "":
                statement = statement.where(Category.name == category)
            if price_range and price_range != "":
                statement = statement.where(PriceRange.range == price_range)
            if district and district != "":
                statement = statement.where(Address.district == district)
            doctors = session.exec(statement).all()

            results = []
            if len(doctors) == 0:
                return results

            for d in doctors:
                # transform doctor db model to dto
                catgo = CategoryDTO(name=d.category.name)
                addr = AddressDTO(street=d.address.street, room=d.address.room, district=d.address.district,
                                  city=d.address.city)
                schedules = [ScheduleDTO(day_in_week=s.day_in_week, working_hours=s.working_hours) for s in
                             d.schedule]
                data = DoctorDTO(first_name=d.first_name, last_name=d.last_name,
                                 consultation_fee=d.consultation_fee,
                                 consultation_fee_detail=d.consultation_fee_detail, phone=d.phone,
                                 category=catgo, schedule=schedules, address=addr)
                if language == 'cn':
                    data.first_name = d.first_name_cn
                    data.last_name = d.last_name_cn
                    data.consultation_fee_detail = d.consultation_fee_detail_cn
                    catgo = CategoryDTO(name=d.category.name_cn)
                    data.category = catgo
                    addr = AddressDTO(street=d.address_cn.street, room=d.address_cn.room,
                                      district=d.address_cn.district,
                                      city=d.address_cn.city)
                    data.address = addr
                results.append(data)

            return results

    def create_doctors(self, doctors: List[CreateDoctorReqDTO]) -> None:
        """
        create doctors to db from payload
        :param doctors: list of CreateDoctorReqDTO request payload
        :return: None
        """
        with Session(engine) as session:
            # find out category id
            categories = session.exec(select(Category)).all()
            categories_map = {cat.name: cat.id for cat in categories}

            # define new doctors db model instances
            new_doctors = [Doctor(first_name=d.first_name, last_name=d.last_name,
                                  first_name_cn=d.first_name_cn, last_name_cn=d.last_name_cn,
                                  consultation_fee=d.consultation_fee,
                                  consultation_fee_detail=d.consultation_fee_detail,
                                  consultation_fee_detail_cn=d.consultation_fee_detail_cn,
                                  phone=d.phone, category_id=categories_map.get(d.category, None)) for d in doctors]

            # find out the price range id based on the static config table which hold value
            # range have format lowbound-highbound e.g. 0-200
            price_ranges = session.exec(select(PriceRange)).all()

            # data structure to hold low high bound of price range easier to later calculation
            class _PriceRange:
                id = 0
                low_bound = 0
                high_bound = 0

            # list of _PriceRange
            ranges = []
            for pr in price_ranges:
                new_pr = _PriceRange()
                new_pr.id = pr.id

                boundaries = pr.range.split('-')
                if len(boundaries) != 2:
                    continue
                new_pr.low_bound = int(boundaries[0].strip())
                new_pr.high_bound = int(boundaries[1].strip())
                ranges.append(new_pr)

            for doctor in new_doctors:
                for r in ranges:
                    if r.low_bound <= doctor.consultation_fee <= r.high_bound:
                        doctor.price_range_id = r.id

            session.add_all(new_doctors)
            session.commit()

            # handle new address and schedules
            new_addresses = []
            new_addresses_cn = []
            new_schedules = []
            for i in range(len(new_doctors)):
                # get back newly created entries id
                session.refresh(new_doctors[i])
                new_d = new_doctors[i]
                d = doctors[i]
                # address
                new_addr = Address(doctor_id=new_d.id, street=d.street, room=d.room, district=d.district, city=d.city)
                new_addresses.append(new_addr)
                new_addr_cn = AddressCN(doctor_id=new_d.id, street=d.street_cn, room=d.room_cn, district=d.district_cn,
                                      city=d.city_cn)
                new_addresses_cn.append(new_addr_cn)
                # create doctor schedules
                new_ss = [Schedule(doctor_id=new_d.id, day_in_week='monday', working_hours=d.schedule_monday),
                          Schedule(doctor_id=new_d.id, day_in_week='tuesday', working_hours=d.schedule_tuesday),
                          Schedule(doctor_id=new_d.id, day_in_week='wednesday', working_hours=d.schedule_wednesday),
                          Schedule(doctor_id=new_d.id, day_in_week='thursday', working_hours=d.schedule_thursday),
                          Schedule(doctor_id=new_d.id, day_in_week='friday', working_hours=d.schedule_friday),
                          Schedule(doctor_id=new_d.id, day_in_week='saturday', working_hours=d.schedule_saturday),
                          Schedule(doctor_id=new_d.id, day_in_week='sunday', working_hours=d.schedule_sunday),
                          Schedule(doctor_id=new_d.id, day_in_week='public_holiday', working_hours=d.public_holiday)]
                new_schedules.extend(new_ss)

            session.add_all(new_addresses)
            session.add_all(new_addresses_cn)
            session.add_all(new_schedules)
            session.commit()

        return
