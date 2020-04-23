from connection import conn
import logging
import os
logger = logging.getLogger("extract_queries")

logger.info("creating cursor")
cur = conn.cursor()

try:
    cur.execute("show views;")
    for row in cur:
        name = row[1]
        text = row[7]
        logger.info("Found view %s", name)
        if "_" not in name:
            # we only want raw queries!
            # extract sql statement
            as_idx = text.index("as ")
            select_stmt = text[as_idx + 3:]
            logger.debug("%s SQL: %s", name, select_stmt)
            # save query to file
            filename = f"{name}.sql"
            with open(os.path.join("queries", filename), "w") as f:
                f.write(select_stmt)
            logger.info("saved sql to %s", filename)
finally:
    cur.close()