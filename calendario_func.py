from datetime import datetime, timedelta, timezone
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from pathlib import Path
import pytz

# Percorso della directory in cui si trova lo script attuale
current_dir = Path(__file__).parent
romamerda_tz = pytz.timezone("Europe/Rome")

# Percorso al file di credenziali del Service Account
# SERVICE_ACCOUNT_FILE = 'config''service_account.json'
SERVICE_ACCOUNT_FILE = (
    current_dir / "config" / "calendario-provincia-446314-ed00633e1480.json"
)
# Scopi richiesti per Google Calendar
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def giorno_successivo(giorno: str):
    # Converto la stringa in un oggetto datetime
    data = datetime.strptime(giorno, "%Y-%m-%d")
    # Calcolo il giorno successivo
    giorno_successivo = data + timedelta(days=1)
    # Converto di nuovo in stringa
    giorno_successivo_str = giorno_successivo.strftime("%Y-%m-%d")
    return giorno_successivo_str


def get_service():
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build("calendar", "v3", credentials=credentials)
    return service


service = get_service()
calendar_id = (
    "5h3u6qp8cfn5jtl2in615535fk@group.calendar.google.com"  # O un altro calendario
)


def cancella_eventi(giorno: str, stringa_utente: str):
    # Imposta la data in UTC
    timeMin = datetime.strptime(f"{giorno}T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ").astimezone(
        romamerda_tz
    )
    timeMax = datetime.strptime(f"{giorno}T23:59:59Z", "%Y-%m-%dT%H:%M:%SZ").astimezone(
        romamerda_tz
    )
    result = (
        service.events()
        .list(
            calendarId=calendar_id,
            timeMin=timeMin.isoformat(),
            timeMax=timeMax.isoformat(),
            q=stringa_utente
            + "*",  # Criterio di filtro descrizione che inizia con "MP "
            singleEvents=True,
        )
        .execute()
    )
    events = result.get("items", [])
    for event in events:
        service.events().delete(calendarId=calendar_id, eventId=event["id"]).execute()
    return True


def inserisci_evento(giorno: str, stringa: str, colorId: int):
    # Dettagli dell'evento
    event = {
        "summary": stringa,
        "start": {
            "date": giorno,  # Data di inizio (all-day event usa solo "date", non "dateTime")
            "timeZone": "Europe/Rome",
        },
        "end": {
            "date": giorno_successivo(giorno),  # Giorno successivo
            "timeZone": "Europe/Rome",
        },
        "colorId": colorId,  # Imposta il colore (ad esempio, '2' è blu)
    }

    # Inserimento dell'evento
    created_event = (
        service.events().insert(calendarId=calendar_id, body=event).execute()
    )
    return True


# inserisci()
# cancella_eventi("2025-1-8", "MP ")
