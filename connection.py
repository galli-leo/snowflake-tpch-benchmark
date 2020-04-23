import snowflake.connector
import os
import sys
import logging
import log
import contextlib

logger = logging.getLogger("connection")

def create_conn(warehouse = 'COMPUTE_WH', database = 'SNOWFLAKE_SAMPLE_DATA', schema = 'TPCH_SF100'):
    return snowflake.connector.connect(
        user='gallileo',
        password='futve2-xumxYj-fojbuf',
        account='PP81778.eu-central-1',
        warehouse= warehouse,
        database=database,
        schema=schema
    )

@contextlib.contextmanager
def conn_vw(size = 'XLARGE', name = 'temporary'):
    logger.info("Creating VW %s of size %s", name, size)
    conn = create_conn()
    cur = conn.cursor()
    cur.execute(f"CREATE WAREHOUSE {name} WITH WAREHOUSE_SIZE = '{size}' WAREHOUSE_TYPE = 'STANDARD' AUTO_SUSPEND = 60 AUTO_RESUME = TRUE;")
    cur.execute(f"USE WAREHOUSE {name};")
    cur.close()
    try:
        yield conn
    finally:
        logger.info("Dropping VW %s", name)
        cur = conn.cursor()
        cur.execute(f"DROP WAREHOUSE {name};")
        cur.close()
        logger.info("Dropped VW %s", name)

conn = create_conn()