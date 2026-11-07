from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from .db import get_session
from .models import CountyResult, Race

router = APIRouter()


class RaceOut(BaseModel):
    year: int
    office: str
    state_fips: str
    district: str
    is_final: bool


class CountyOut(BaseModel):
    county_fips: str
    county_name: str
    candidates: dict[str, dict[str, int | str]]  # candidate -> {party, votes}
    total_votes: int


@router.get("/races", response_model=list[RaceOut])
def list_races(
    state_fips: str | None = None,
    office: str | None = None,
    session: Session = Depends(get_session),
):
    q = select(Race).order_by(Race.year.desc())
    if state_fips:
        q = q.where(Race.state_fips == state_fips)
    if office:
        q = q.where(Race.office == office)
    return session.scalars(q).all()


@router.get("/races/{year}/{office}/{state_fips}/counties", response_model=list[CountyOut])
def county_results(
    year: int,
    office: str,
    state_fips: str,
    district: str = "",
    session: Session = Depends(get_session),
):
    race = session.scalar(
        select(Race).where(
            Race.year == year,
            Race.office == office,
            Race.state_fips == state_fips,
            Race.district == district,
        )
    )
    if race is None:
        raise HTTPException(404, "race not found")

    counties: dict[str, CountyOut] = {}
    for r in session.scalars(select(CountyResult).where(CountyResult.race_id == race.id)):
        c = counties.setdefault(
            r.county_fips,
            CountyOut(county_fips=r.county_fips, county_name=r.county_name, candidates={}, total_votes=0),
        )
        c.candidates[r.candidate] = {"party": r.party, "votes": r.votes}
        c.total_votes += r.votes
    return list(counties.values())
