CREATE TABLE IF NOT EXISTS logs_pipeline (
    id SERIAL PRIMARY KEY,
    etapa VARCHAR(50),
    nombre_archivo VARCHAR(150),
    cantidad_registros INTEGER,
    estado VARCHAR(50),
    mensaje TEXT,
    fecha_ejecucion TIMESTAMP DEFAULT NOW()
);

DROP TABLE IF EXISTS reservas;

CREATE TABLE reservas (
    id_reserva INTEGER PRIMARY KEY,
    nombre_cliente VARCHAR(150) NOT NULL,
    destino VARCHAR(100) NOT NULL,
    fecha_viaje DATE NOT NULL,
    correo VARCHAR(150) NOT NULL,
    plataforma VARCHAR(100) NOT NULL,
    fecha_carga TIMESTAMP DEFAULT NOW()
);
