from sqlalchemy import ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class Race(Base):
    """One contest in one state, e.g. 2022 Senate in PA."""

    __tablename__ = "race"
    __table_args__ = (UniqueConstraint("year", "office", "state_fips", "district"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int]
    office: Mapped[str] = mapped_column(String(32))  # president | senate | governor | house | ...
    state_fips: Mapped[str] = mapped_column(String(2))
    district: Mapped[str] = mapped_column(String(16), default="")  # House / special-election tag
    is_final: Mapped[bool] = mapped_column(default=True)  # False while 2026 counts are in flux

    results: Mapped[list["CountyResult"]] = relationship(back_populates="race")


class CountyResult(Base):
    """Votes for one candidate in one county."""

    __tablename__ = "county_result"
    __table_args__ = (Index("ix_result_race_county", "race_id", "county_fips"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    race_id: Mapped[int] = mapped_column(ForeignKey("race.id"))
    county_fips: Mapped[str] = mapped_column(String(5))
    county_name: Mapped[str] = mapped_column(String(128))
    candidate: Mapped[str] = mapped_column(String(128))
    party: Mapped[str] = mapped_column(String(32))  # DEMOCRAT | REPUBLICAN | OTHER ...
    votes: Mapped[int]

    race: Mapped[Race] = relationship(back_populates="results")
