from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_my_engine():
    with open("URI.txt", "r") as f:
        URI = f.read()

    engine = create_engine(URI)

    return engine


engine = create_my_engine()
Session = sessionmaker(engine)
session = Session()
