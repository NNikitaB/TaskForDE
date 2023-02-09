from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from classDTO import RocketDTO, MissionDTO, LaunchDTO


class Base(DeclarativeBase):
    pass


class Rockets(Base):
    __tablename__ = "rockets"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(251))
    wikipedia: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    launch_ids: Mapped[List["Launches"]] = relationship(
        back_populates="rocket", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Rockets(id={self.id!r}, name={self.name!r})"


class Launches(Base):
    __tablename__ = "launches"

    id: Mapped[str] = mapped_column(primary_key=True)
    rocket_id: Mapped[str] = mapped_column(ForeignKey("rockets.id"))
    detail: Mapped[Optional[str]]
    launch_date_utc: Mapped[Optional[str]]
    rocket: Mapped["Rockets"] = relationship(back_populates="launch_ids")
    mission_ids: Mapped[List["Missions"]] = relationship(
        back_populates="launch", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Launches(id={self.id!r}, launch_date_utc={self.launch_date_utc!r})"


class Missions(Base):
    __tablename__ = "missions"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    launch: Mapped["Launches"] = relationship(back_populates="mission_ids")
    launch_id: Mapped[str] = mapped_column(ForeignKey("launches.id"))

    def __repr__(self) -> str:
        return f"Missions(id={self.id!r}, name={self.name!r})"


def convert_dto_to_class_db(missions: list[MissionDTO], rockets: list[RocketDTO], launches: list[LaunchDTO]):
    rockets = list(map(lambda r: Rockets(id=r.id, name=r.name, description=r.description), rockets))
    launches = list(map(lambda l: Launches(
        id=l.id,
        launch_date_utc=l.launch_date_utc,
        detail=l.detail,
        rocket_id=l.rocket.rocket.id,
        mission_ids=list(map(lambda m: Missions(id=m, name=l.mission_name), l.mission_id))
    ), launches))
    return rockets, launches
