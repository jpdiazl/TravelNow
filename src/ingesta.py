from pathlib import Path
from datetime import datetime
import os

import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient

from utils import escribir_log, guardar_log_db

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"


def ejecutar_ingesta():
    escribir_log("Semana 1 - Inicio de ingesta desde MongoDB Atlas")

    try:
        mongo_uri = os.getenv("MONGO_URI")
        mongo_db = os.getenv("MONGO_DB", "travelnow")
        mongo_collection = os.getenv("MONGO_COLLECTION", "reservas")

        if not mongo_uri:
            mensaje = "No existe MONGO_URI en el archivo .env"
            escribir_log(mensaje)
            guardar_log_db("Ingesta", "mongodb", 0, "ERROR", mensaje)
            return None

        cliente = MongoClient(mongo_uri)
        coleccion = cliente[mongo_db][mongo_collection]

        documentos = list(coleccion.find({}, {"_id": 0}))

        if not documentos:
            mensaje = f"La colección {mongo_db}.{mongo_collection} no tiene datos"
            escribir_log(mensaje)
            guardar_log_db("Ingesta", mongo_collection, 0, "ERROR", mensaje)
            return None

        RAW_DIR.mkdir(parents=True, exist_ok=True)

        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_destino = f"reservas_raw_{fecha}.csv"
        destino = RAW_DIR / nombre_destino

        df = pd.DataFrame(documentos)
        df.to_csv(destino, index=False, encoding="utf-8-sig")

        cantidad = len(df)
        mensaje = f"Datos extraídos desde MongoDB Atlas y guardados en data/raw con {cantidad} registros"

        escribir_log(mensaje)
        guardar_log_db("Ingesta", nombre_destino, cantidad, "OK", mensaje)
        escribir_log("Semana 1 - Fin de ingesta")

        cliente.close()
        return destino

    except Exception as error:
        mensaje = f"Error en ingesta desde MongoDB Atlas: {error}"
        escribir_log(mensaje)
        guardar_log_db("Ingesta", "mongodb", 0, "ERROR", mensaje)
        return None


if __name__ == "__main__":
    ejecutar_ingesta()
