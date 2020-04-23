from connection import conn
import logging
import os
from extract_schema import get_tables
import click

logger = logging.getLogger("create_views")

@click.command()
@click.option('--scale', default=100)
@click.option('--typed/--not-typed', default=False)
def main(scale, typed):
    tables = get_tables()
    cur = conn.cursor()
    schema_name = f"TPCH_SF{scale}"
    logger.info("Using schema %s", schema_name)
    cur.execute(f"USE DATABASE TCPH_SCHEMALESS;")
    cur.execute(f"USE SCHEMA {schema_name};")
    for tbl, cols in tables.items():
        col_sels = []
        for col, type in cols:
            type_str = ""
            if typed:
                type_str = f"::{type}"
            col_sels.append(f"src:{col}{type_str} as {col}")
        col_sel = ",\n\t".join(col_sels)
        sql = f"""select
        {col_sel}
    from {tbl}_RAW"""
        with open(os.path.join("views", f"{tbl}.sql"), "w") as f:
            f.write(sql)
        logger.info("Creating view %s with sql %s", tbl, sql)
        cur.execute(f"CREATE OR REPLACE VIEW {schema_name}.{tbl} AS {sql}")
    cur.close()

if __name__ == "__main__":
    main()