import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from config import dati as DATI


class SQLServerConnection:
    def __init__(
        self,
        username=DATI.username,
        password=DATI.password,
        host=DATI.host,
        port=DATI.port,
        database=DATI.database,
    ):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.engine: Engine = None
        self.session: Session = None
        self.SessionMaker = None

    def connect(self) -> Engine:
        """Estabilisce e ritorna l'engine SQLAlchemy con la connessione al database."""
        connection_string = f"mssql+pymssql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        self.engine = create_engine(connection_string)
        self.SessionMaker = sessionmaker(bind=self.engine)  # Crea una SessionMaker
        return self.engine

    def create_session(self) -> Session:
        """Crea e ritorna una nuova sessione."""
        if not self.SessionMaker:
            raise Exception("SessionMaker not initialized. Call connect() first.")
        self.session = self.SessionMaker()
        return self.session

    def execute_query(self, query: str):
        """Esegue una query SQL e ritorna i risultati."""
        if not self.engine:
            raise Exception("Engine not initialized. Call connect() first.")
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            return list(result)

    def execute_in_session(self, query: str):
        """Esegue una query SQL usando una sessione."""
        if not self.session:
            raise Exception("Session not initialized. Call create_session() first.")
        result = self.session.execute(text(query))
        self.session.commit()
        return list(result)

    def close(self):
        """Chiude la connessione al database e la sessione."""
        if self.session:
            self.session.close()
        if self.engine:
            self.engine.dispose()
