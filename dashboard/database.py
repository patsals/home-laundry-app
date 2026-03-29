import pandas as pd
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
    select,
    text,
    func
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

def get_accelerometer_signal_log_data_last_6_hours(
    device_id: int,
):    
    select_statement = (
        select(
            accelerometer_signal_logs_table.c.timestamp,
            accelerometer_signal_logs_table.c.x,
            accelerometer_signal_logs_table.c.y,
            accelerometer_signal_logs_table.c.z,
        )
        .where(
            (
                accelerometer_signal_logs_table.c.device_id == str(device_id)
            ) & (
                accelerometer_signal_logs_table.c.timestamp >=
                    (func.now() - text("INTERVAL '6 hours'"))
            )
        )
    )
    return pd.read_sql(select_statement, DATABASE_ENGINE)


def is_device_active(
    device_id: int
):
    ...