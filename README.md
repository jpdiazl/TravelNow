# TravelNow ETL Cloud

Flujo del proyecto:

MongoDB Atlas -> Python ETL -> CSV intermedios -> Oracle Autonomous Database

## 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 2. Configurar `.env`

El archivo `.env` contiene la conexión a MongoDB Atlas y Oracle Autonomous.

Debes completar estos valores:

```env
ORACLE_USER=travelnow_etl
ORACLE_PASSWORD=TU_CLAVE_DEL_USUARIO
ORACLE_DSN=travelnow_low
ORACLE_WALLET_DIR=/home/ubuntu/Wallet_travelnow
ORACLE_WALLET_PASSWORD=TU_CLAVE_WALLET
```

Importante: `ORACLE_WALLET_DIR` debe apuntar a la carpeta donde descomprimiste la Wallet.

## 3. Crear usuario Oracle

Conéctate en SQL Developer como `ADMIN` y ejecuta:

```sql
CREATE USER travelnow_etl IDENTIFIED BY TravelNow2026;
GRANT CONNECT, RESOURCE TO travelnow_etl;
ALTER USER travelnow_etl QUOTA UNLIMITED ON DATA;
```

Después usa ese usuario en el `.env`.

## 4. Cargar el CSV inicial a MongoDB Atlas

Este paso se usa solo para llenar la colección inicial en MongoDB Atlas:

```bash
python3 src/cargar_csv_a_mongo.py
```

## 5. Ejecutar pipeline completo

```bash
python3 src/pipeline.py
```

## 6. Revisar en Oracle

```sql
SELECT * FROM reservas;
SELECT * FROM logs_pipeline;
```
