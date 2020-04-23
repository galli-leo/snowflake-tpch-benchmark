from connection import conn
import logging
import os

def get_tables():
    ret = {}
    logger = logging.getLogger("extract_schema")

    logger.info("creating cursor")
    cur = conn.cursor()

    try:
        cur.execute("show tables;")
        for row in cur:
            name = row[1]
            logger.info("Found table %s", name)
            cur2 = conn.cursor()
            cur2.execute(f"describe table {name};")
            col = []
            for row2 in cur2:
                cname = row2[0]
                type = row2[1]
                col.append((cname, type))
                logger.debug("Found column %s (%s)", cname, type)
            cur2.close()
            ret[name] = col
    finally:
        cur.close()
    return ret

if __name__ == "__main__":
    tables = get_tables()
