from utils import escribir_log, conectar_db


def ejecutar_ddl(cursor, sql):
    try:
        cursor.execute(sql)
    except Exception as error:
        if "ORA-00955" in str(error):
            return
        raise


def crear_tablas():
    escribir_log("Creando tablas si no existen en Oracle Autonomous Database")

    conexion = conectar_db()
    cursor = conexion.cursor()

    ejecutar_ddl(cursor, """
        CREATE TABLE logs_pipeline (
            id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            etapa VARCHAR2(50),
            nombre_archivo VARCHAR2(150),
            cantidad_registros NUMBER,
            estado VARCHAR2(50),
            mensaje CLOB,
            fecha_ejecucion TIMESTAMP DEFAULT SYSTIMESTAMP
        )
    """)

    ejecutar_ddl(cursor, """
        CREATE TABLE reservas (
            id_reserva NUMBER PRIMARY KEY,
            nombre_cliente VARCHAR2(150) NOT NULL,
            destino VARCHAR2(100) NOT NULL,
            fecha_viaje DATE NOT NULL,
            correo VARCHAR2(150) NOT NULL,
            plataforma VARCHAR2(100) NOT NULL,
            fecha_carga TIMESTAMP DEFAULT SYSTIMESTAMP
        )
    """)

    conexion.commit()
    cursor.close()
    conexion.close()

    escribir_log("Tablas verificadas correctamente en Oracle")


if __name__ == "__main__":
    crear_tablas()
