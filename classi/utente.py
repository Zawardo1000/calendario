from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Utente(Base):
    __tablename__ = "t_utenti"
    IdUtente = Column(Integer, primary_key=True)
    Matricola = Column(Integer)
    gcalendar = Column(Integer)
    iniziali = Column(String)
    colorid = Column(Integer)
    gmail = Column(String)

    @classmethod
    def get_utente_by_id(cls, session, id_utente):
        """Restituisce un oggetto Utente dato un IdUtente."""
        return session.query(cls).filter(cls.IdUtente == id_utente).first()
