CREATE TABLE logs_pipeline (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    etapa VARCHAR2(50),
    nombre_archivo VARCHAR2(150),
    cantidad_registros NUMBER,
    estado VARCHAR2(50),
    mensaje CLOB,
    fecha_ejecucion TIMESTAMP DEFAULT SYSTIMESTAMP
);

CREATE TABLE reservas (
    id_reserva NUMBER PRIMARY KEY,
    nombre_cliente VARCHAR2(150) NOT NULL,
    destino VARCHAR2(100) NOT NULL,
    fecha_viaje DATE NOT NULL,
    correo VARCHAR2(150) NOT NULL,
    plataforma VARCHAR2(100) NOT NULL,
    fecha_carga TIMESTAMP DEFAULT SYSTIMESTAMP
);
