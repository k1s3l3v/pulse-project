from sqlalchemy.orm import Session

from ..db import create_session


def get_db() -> Session:
    db = create_session()
    try:
        yield db
    finally:
        db.close()
