import logging
import coloredlogs
fmt = "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
logging.basicConfig(format=fmt, level=logging.INFO)
coloredlogs.install(fmt=fmt, level=logging.INFO)
silence = ["snowflake.connector.json_result", "snowflake.connector.cursor", "snowflake.connector.connection"]
for name in silence:
    logger = logging.getLogger(name)
    logger.setLevel(logging.WARN)