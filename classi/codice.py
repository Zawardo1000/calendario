from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Codice(Base):
    __tablename__ = "t_codici"
    codice = Column(String, primary_key=True)
    descrizione = Column(String)

    @classmethod
    def get_by_cod(cls, session, cod):
        return session.query(cls).filter(cls.codice == cod).first()
