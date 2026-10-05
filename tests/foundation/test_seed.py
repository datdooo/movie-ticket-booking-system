import os
import subprocess
import sys
from pathlib import Path

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from app.db.models import MovieModel, RoomModel, SeatModel, ShowtimeModel


def test_seed_can_run_twice_without_duplicate_data(tmp_path: Path) -> None:
    database_url = f"sqlite:///{tmp_path / 'seed.db'}"
    environment = dict(os.environ, DATABASE_URL=database_url)
    for _ in range(2):
        subprocess.run(
            [sys.executable, "-m", "scripts.seed"], env=environment, capture_output=True, check=True
        )
    engine = create_engine(database_url)
    try:
        with Session(engine) as session:
            for model, count in [
                (MovieModel, 4),
                (RoomModel, 2),
                (SeatModel, 40),
                (ShowtimeModel, 6),
            ]:
                assert session.scalar(select(func.count()).select_from(model)) == count
    finally:
        engine.dispose()
