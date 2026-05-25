from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_FILE = BASE_DIR / "data" / "source" / "reservas.csv"


def cargar_csv_a_mongo():
    mongo_uri = os.getenv("MONGO_URI")
    mongo_db = os.getenv("MONGO_DB", "travelnow")
    mongo_collection = os.getenv("MONGO_COLLECTION", "reservas")

    if not mongo_uri:
        raise ValueError("Falta MONGO_URI en el archivo .env")

    if not SOURCE_FILE.exists():
        raise FileNotFoundError("No existe data/source/reservas.csv")

    df = pd.read_csv(SOURCE_FILE)
    documentos = df.to_dict(orient="records")

    cliente = MongoClient(mongo_uri)
    coleccion = cliente[mongo_db][mongo_collection]

    coleccion.delete_many({})

    if documentos:
        coleccion.insert_many(documentos)

    print(f"✅ CSV cargado en MongoDB Atlas: {mongo_db}.{mongo_collection}")
    print(f"📌 Registros insertados: {len(documentos)}")

    cliente.close()


if __name__ == "__main__":
    cargar_csv_a_mongo()
