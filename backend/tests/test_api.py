from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.db import Base, get_session
from app.main import app
from app.models import CountyResult, Race


def make_client() -> TestClient:
    engine = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    with Session(engine) as s:
        race = Race(year=2020, office="senate", state_fips="42")
        s.add(race)
        s.flush()
        s.add_all(
            [
                CountyResult(race_id=race.id, county_fips="42001", county_name="Adams",
                             candidate="A", party="DEMOCRAT", votes=10),
                CountyResult(race_id=race.id, county_fips="42001", county_name="Adams",
                             candidate="B", party="REPUBLICAN", votes=30),
            ]
        )
        s.commit()
    def override():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override
    return TestClient(app)


def test_county_results():
    client = make_client()
    body = client.get("/api/races/2020/senate/42/counties").json()
    assert body[0]["total_votes"] == 40
    assert body[0]["candidates"]["B"]["party"] == "REPUBLICAN"


def test_missing_race_404():
    assert make_client().get("/api/races/1999/senate/42/counties").status_code == 404
