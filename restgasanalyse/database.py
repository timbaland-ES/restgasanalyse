from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from restgasanalyse.models import Measurement, Base

class Database:
    def __init__(self, url: str):
        db = create_engine(url)

        # create the tables
        Base.metadata.create_all(db)

        self.Session = sessionmaker(bind=db)

    def store(self, data: Measurement) -> None:
        with self.Session() as session:       
            session.add(data)
            session.commit()
            