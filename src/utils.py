from pathlib import Path
from datetime import datetime
import os

import oracledb
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / "docs" / "ejecucion.log"


def escribir_log(mensaje):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{fecha}] {mensaje}"
    print(linea)

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(LOG_FILE, "a", encoding="utf-8") as archivo:
        archivo.write(linea + "\n")


def conectar_oracle():
    wallet_dir = os.getenv("ORACLE_WALLET_DIR")
    wallet_password = os.getenv("ORACLE_WALLET_PASSWORD") or None

    parametros = {
        "user": os.getenv("ORACLE_USER"),
        "password": os.getenv("ORACLE_PASSWORD"),
        "dsn": os.getenv("ORACLE_DSN"),
    }

    if wallet_dir:
        parametros["config_dir"] = wallet_dir
        parametros["wallet_location"] = wallet_dir

    if wallet_password and wallet_password != "CAMBIA_PASSWORD_WALLET":
        parametros["wallet_password"] = wallet_password

    return oracledb.connect(**parametros)


def conectar_db():
    return conectar_oracle()


def guardar_log_db(etapa, nombre_archivo, cantidad_registros, estado, mensaje):
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO logs_pipeline
            (etapa, nombre_archivo, cantidad_registros, estado, mensaje)
            VALUES (:1, :2, :3, :4, :5)
        """, (etapa, nombre_archivo, cantidad_registros, estado, mensaje))

        conexion.commit()
        cursor.close()
        conexion.close()

    except Exception as error:
        escribir_log(f"No se pudo guardar log en Oracle: {error}")
