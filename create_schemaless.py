from connection import conn, conn_vw
import logging
import os
from extract_schema import get_tables
import click

@click.command()
@click.option('--scale', default=100, help='Scale Factor of TPCH data to copy')
def main(scale):
    logger = logging.getLogger("create_schemaless")

    tables = get_tables()

    logger.info("Creating schemaless version of scale factor %d", scale)
    schema_name = f"TPCH_SF{scale}"
    with conn_vw(name='temporary2') as conn:
        logger.info("Creating schema %s", schema_name)
        cur = conn.cursor()
        cur.execute("use database TCPH_SCHEMALESS;")
        cur.execute(f"create or replace schema {schema_name}")
        cur.execute(f"use schema {schema_name}")
        logger.info("Creating stage TMP")
        cur.execute(f"CREATE OR REPLACE STAGE TCPH_SCHEMALESS.{schema_name}.TMP")
        logger.info(f"Creating export file format")
        cur.execute(f"CREATE OR REPLACE FILE FORMAT TCPH_SCHEMALESS.{schema_name}.export TYPE = 'JSON' COMPRESSION = 'AUTO' ENABLE_OCTAL = FALSE ALLOW_DUPLICATE = FALSE STRIP_OUTER_ARRAY = FALSE STRIP_NULL_VALUES = TRUE IGNORE_UTF8_ERRORS = FALSE;")

        for tbl, cols in tables.items():
            table_name = f"{tbl}_RAW"
            logger.info("Creating table %s", table_name)
            cur.execute(f"CREATE OR REPLACE TABLE \"{table_name}\" (\"SRC\" VARIANT);")
            stage_path = f"@TMP/{tbl}/"
            logger.info("Copying data for table %s to temp files %s", tbl, stage_path)
            cur.execute(f"copy into {stage_path} from (select object_construct(*) from \"SNOWFLAKE_SAMPLE_DATA\".\"{schema_name}\".\"{tbl}\") file_format = (format_name = export)")
            logger.info("Copying data from temp path %s into actual table", stage_path)
            cur.execute(f"copy into {table_name} from {stage_path} file_format = (format_name = export)")
            logger.info("Deleting temp files from %s", stage_path)
            cur.execute(f"rm {stage_path}")
        cur.close()

if __name__ == '__main__':
    main()