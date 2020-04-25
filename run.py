from connection import conn, conn_vw
import os
import sys
import logging
import log
from query import load_queries, query
import time
import numpy as np
from concurrent.futures.thread import ThreadPoolExecutor
import click

logger = logging.getLogger("run")

def run_query(q: query, conn):
    #q.build_args()
    sql = q.get_sql()
    cur = conn.cursor()
    start = time.time()
    cur.execute(sql)
    diff = time.time() - start
    cur.close()
    return diff

def time_query(q: query, conn, warmups: int = 5, runs: int = 3):
    logger.info("Running query %s with %d warmups and %d runs", q.desc, warmups, runs)
    for i in range(warmups):
        run_query(q, conn)

    timings = []
    for i in range(runs):
        timings.append(run_query(q, conn))
    timings = np.array(timings)
    timings *= 1000 # miliseconds
    avg = np.average(timings)
    std = np.std(timings)
    logger.info("Query %s got average: %0.2f ms +- %0.2f", q.desc, avg, std)
    return timings, avg, std

def write_row(f, elems):
    f.write(",".join(elems) + "\n")
    f.flush()

@click.command()
@click.option('--scale', default=100)
@click.option('--schema/--no-schema', default=True)
@click.option('--runs', default=3, help='Number of runs to do.')
@click.option('--warm', default=5, help='Number of runs to do for warming caches.')
@click.option('--end', default=22, help='Last query to execute')
def main(scale, schema, runs, warm, end):
    queries = load_queries()
    logger.info("Loaded %d queries", len(queries))
    db = "SNOWFLAKE_SAMPLE_DATA" if schema else "TCPH_SCHEMALESS"
    schema_name = f"TPCH_SF{scale}"
    schema_id = "SCHEMA" if schema else "SCHEMALESS"

    with conn_vw(name = f'TEMPORARY_{schema_id}_SF{scale}', size='MEDIUM') as conn:
        logger.info("Running on database %s", db)
        cur = conn.cursor()
        cur.execute(f"USE DATABASE {db};")

        
        logger.info("Running on schema %s", db)
        cur.execute(f"USE SCHEMA {schema_name};")
        
        logger.info("Disabling result set cache!")
        cur.execute("ALTER SESSION SET USE_CACHED_RESULT = FALSE;")
        cur.close()

        
        filename = f"results_{schema_id}_SF{scale}.csv"
        filepath = os.path.join("results", filename)
        logger.info("Writing results to %s", filepath)
        with open(filepath, "w") as f:
            header = ["Query"]+[f"Run {i+1}" for i in range(runs)] + ["Average", "Standard Deviation"]
            write_row(f, header)
            for q in queries[:end]:
                timings, avg, std = time_query(q, conn, runs=runs, warmups=warm)
                timings = list(timings)
                timings += [avg / 1000.0, std / 1000.0]
                timings = [f"{q.num}"] + [f"{x:.06f}" for x in timings]
                write_row(f, timings)

if __name__ == "__main__":
    main()