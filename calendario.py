import sys
from flask import Blueprint, jsonify
from sqlalchemy import create_engine, text
from classi.SQLServerConnection import SQLServerConnection
from classi.utente import Utente
from classi.assenza import Assenza
from classi.codice import Codice
import calendario_func as func


def get_stringa_calendario(anno, mese, giorno, id_utente):
    try:
        db_conn = SQLServerConnection()
        engine = db_conn.connect()
        session = db_conn.create_session()
        utente = Utente.get_utente_by_id(session, id_utente)
        giorni = Assenza.get_giorni_by_anno_mese_utente(session, anno, mese, id_utente)
        valori = giorni.Giorni.split(",")
        assenza_cod = valori[int(giorno) - 1]  # posizione 1-indexed
        assenza = Codice.get_by_cod(session, assenza_cod)
        if assenza is None:
            return False
        return utente.iniziali + " " + assenza.descrizione
    except Exception as e:
        raise
    finally:
        db_conn.close()


def get_utente(id_utente):
    try:
        db_conn = SQLServerConnection()
        engine = db_conn.connect()
        session = db_conn.create_session()
        utente = Utente.get_utente_by_id(session, id_utente)
        return utente
    except Exception as e:
        raise
    finally:
        db_conn.close()


app1 = Blueprint("calendario", __name__, url_prefix="/calendario")


@app1.route("/insert", methods=["GET"])
@app1.route("/insert/<anno>", methods=["GET"])
@app1.route("/insert/<anno>/<mese>", methods=["GET"])
@app1.route("/insert/<anno>/<mese>/<giorno>", methods=["GET"])
@app1.route("/insert/<anno>/<mese>/<giorno>/<user_id>", methods=["GET"])
def insert(anno=None, mese=None, giorno=None, user_id=None):
    # Verifica se i parametri sono stati passati
    if not anno or not mese or not giorno or not user_id:
        return jsonify({"error": "parametri obbligatori mancanti"}), 400
    try:
        data = str(anno) + "-" + str(mese) + "-" + str(giorno)
        utente = get_utente(user_id)
        stringa_del = utente.iniziali + " "
        cancellazione = func.cancella_eventi(data, stringa_del)
        if cancellazione is not True:
            return jsonify({"error": "Errore durante la cancellazione"}), 400
        stringa = get_stringa_calendario(anno, mese, giorno, user_id)
        if stringa:
            inserimento = func.inserisci_evento(data, stringa, utente.colorid)
            if inserimento:
                return jsonify({"message": "OK"}), 200
            else:
                return jsonify({"error": "Errore durante l'inserimento"}), 400
        return jsonify({"message": "OK"}), 200
    except Exception as e:
        print(e)
