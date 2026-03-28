from sqlalchemy.engine import URL
from sqlalchemy import (
    create_engine,
    MetaData, 
    Table, 
    Column, 
    Integer, 
    String, 
    Float, 
    TIMESTAMP,
    insert
)

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username="user",
    password="password",
    host="db",
    port=5432,
    database="laundry"
)

DATABASE_ENGINE = create_engine(DATABASE_URL)

metadata = MetaData()

accelerometer_signal_logs_table = Table(
    "accelerometer_signal_logs",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("device_id", String, nullable=False),
    Column("timestamp", TIMESTAMP, nullable=False),
    Column("x", Float),
    Column("y", Float),
    Column("z", Float),
    schema="laundry",
)

def insert_accelerometer_signal_log_data(
    data: dict,
):    
    with DATABASE_ENGINE.connect() as conn:
        insert_statement = (
            insert(accelerometer_signal_logs_table)
            .values(data)
        )
        conn.execute(insert_statement)
        conn.commit()