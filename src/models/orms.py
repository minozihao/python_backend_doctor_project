"""Database models

create engine's check_same_thread args
By default SQLite will only allow one thread to communicate with it, assuming that each thread would handle an independent request.
This is to prevent accidentally sharing the same connection for different things (for different requests).
But in FastAPI, using normal functions (def) more than one thread could interact with the database for the same request, so we need to make SQLite know that it should allow that with connect_args={"check_same_thread": False}.
Also, we will make sure each request gets its own database connection session in a dependency, so there's no need for that default mechanism
"""
from sqlmodel import Field, SQLModel, Relationship, create_engine


class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    name_cn: str = Field(unique=True)

    doctors: list["Doctor"] = Relationship(back_populates="category")


class PriceRange(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    range: str = Field(unique=True, description='format low_bound-high_bound e.g. 0-200')

    doctors: list["Doctor"] = Relationship(back_populates="price_range")


# composite primary key doctor_id and day_in_week to ensure entry uniqueness
class Schedule(SQLModel, table=True):
    doctor_id: int = Field(primary_key=True, foreign_key='doctor.id')
    day_in_week: int = Field(primary_key=True,
                             description='taking value monday to sunday respectively and public_holiday')
    working_hours: str = Field(description='taking string values like "9:00-12:00, 1:00-4:00"')

    doctor: "Doctor" = Relationship(back_populates="schedule")


class Doctor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    first_name_cn: str
    last_name_cn: str
    consultation_fee: float | None = 0
    consultation_fee_detail: str = Field(description='extra detail info about consultation fee'
                                                     ' e.g. inclusive 3 days of western medicine')
    consultation_fee_detail_cn: str
    phone: str
    category_id: int = Field(default=None, foreign_key='category.id')
    price_range_id: int | None = Field(default=None, foreign_key='pricerange.id')

    category: Category | None = Relationship(back_populates="doctors")
    price_range: PriceRange | None = Relationship(back_populates='doctors')
    schedule: list["Schedule"] = Relationship(back_populates='doctor')
    address: "Address" = Relationship(back_populates="doctor")
    address_cn: "AddressCN" = Relationship(back_populates="doctor")


class Address(SQLModel, table=True):
    doctor_id: int = Field(primary_key=True, foreign_key='doctor.id')
    street: str
    room: str | None = None
    district: str = Field(index=True)
    city: str

    doctor: Doctor = Relationship(back_populates="address")


class AddressCN(SQLModel, table=True):
    doctor_id: int = Field(primary_key=True, foreign_key='doctor.id')
    street: str
    room: str | None = None
    district: str
    city: str

    doctor: Doctor = Relationship(back_populates="address_cn")


sqlite_file_name = "doctors.db"
sqlite_url = f"sqlite:////Users/caizihao/repo/Zihao_Cai_Senior_Backend_Engineer_Technical_Assessment/{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False, 'timeout': 60})

if __name__ == '__main__':
    # create tables to db based on defined orms
    SQLModel.metadata.create_all(engine)