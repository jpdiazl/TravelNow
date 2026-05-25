from pathlib import Path
from datetime import datetime
import pandas as pd

from utils import escribir_log, guardar_log_db

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def obtener_ultimo_raw():
    archivos = list(RAW_DIR.glob("reservas_raw_*.csv"))
    if not archivos:
        return None
    return max(archivos, key=lambda x: x.stat().st_mtime)


def normalizar_texto(valor):
    if pd.isna(valor):
        return ""
    return str(valor).strip().title()


def limpiar_reservas():
    escribir_log("Semana 2 - Inicio de limpieza y transformación")

    try:
        archivo_raw = obtener_ultimo_raw()

        if archivo_raw is None:
            mensaje = "No existen archivos raw para limpiar"
            escribir_log(mensaje)
            guardar_log_db("Limpieza", "sin_archivo", 0, "ERROR", mensaje)
            return None

        df = pd.read_csv(archivo_raw)

        columnas_requeridas = [
            "id_reserva",
            "nombre_cliente",
            "destino",
            "fecha_viaje",
            "correo",
            "plataforma"
        ]

        for columna in columnas_requeridas:
            if columna not in df.columns:
                raise ValueError(f"Falta la columna obligatoria: {columna}")

        df["id_reserva"] = df["id_reserva"].astype(str).str.strip()
        df["nombre_cliente"] = df["nombre_cliente"].apply(normalizar_texto)
        df["destino"] = df["destino"].apply(normalizar_texto)
        df["correo"] = df["correo"].astype(str).str.strip().str.lower()
        df["plataforma"] = df["plataforma"].apply(normalizar_texto)

        def convertir_fecha(valor):
            formatos = ["%d-%m-%Y", "%Y/%m/%d", "%Y-%m-%d"]

            for formato in formatos:
                try:
                    return pd.to_datetime(valor, format=formato)
                except:
                    pass

            return pd.NaT

        df["fecha_viaje"] = df["fecha_viaje"].apply(convertir_fecha)

        df = df.drop_duplicates(subset=["id_reserva"], keep="first")

        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_salida = f"reservas_limpias_{fecha}.csv"
        salida = PROCESSED_DIR / nombre_salida

        df.to_csv(salida, index=False, encoding="utf-8-sig")

        mensaje = f"Archivo limpio generado con {len(df)} registros"
        escribir_log(mensaje)
        guardar_log_db("Limpieza", nombre_salida, len(df), "OK", mensaje)
        escribir_log("Semana 2 - Fin de limpieza")

        return salida

    except Exception as error:
        mensaje = f"Error en limpieza: {error}"
        escribir_log(mensaje)
        guardar_log_db("Limpieza", "reservas_limpias", 0, "ERROR", mensaje)
        return None


if __name__ == "__main__":
    limpiar_reservas()
