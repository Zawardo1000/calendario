from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Assenza(Base):
    __tablename__ = "t_PlannerAssenze"
    id = Column(Integer, primary_key=True)
    IdUtente = Column(Integer)
    Anno = Column(Integer)
    Giorni = Column(String)
    Mese = Column(Integer)

    @classmethod
    def get_giorni_by_anno_mese_utente(cls, session, anno, mese, id_utente):
        return (
            session.query(cls)
            .filter(cls.Anno == anno, cls.Mese == mese, cls.IdUtente == id_utente)
            .first()
        )
