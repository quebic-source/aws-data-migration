import os
import time
from helper.logger_util import get_logger
import mysql.connector

logger = get_logger(__name__)


def get_connect(config):
    return mysql.connector.connect(**config)


def migration(table, select_script, insert_script):
    _start_time = time.time()
    logger.info("start migration for table %s", table)
    cursor_sandbox.execute("truncate {}".format(table))
    connection_sandbox.commit()
    cursor_prod.execute(select_script)
    data = cursor_prod.fetchall()
    index = 0
    while True:
        chunk = data[index:index + chunk_size]
        if not chunk:
            break
        cursor_sandbox.executemany(
            insert_script,
            chunk)
        connection_sandbox.commit()
        index += chunk_size
    logger.info("completed migration for table %s. took %r seconds", table, (time.time() - _start_time))


if __name__ == "__main__":
    logger.info("start execution")
    chunk_size = 75000
    start_time = time.time()

    source_config = {
        'user': os.environ.get("SOURCE_DB_USER"),
        'password': os.environ.get("SOURCE_DB_PASSWORD"),
        'host': os.environ.get("SOURCE_DB_HOST"),
        'database': os.environ.get("SOURCE_DB_DATABASE"),
        'raise_on_warnings': True
    }
    connection_prod = get_connect(source_config)

    target_config = {
        'user': os.environ.get("TARGET_DB_USER"),
        'password': os.environ.get("TARGET_DB_PASSWORD"),
        'host': os.environ.get("TARGET_DB_HOST"),
        'database': os.environ.get("TARGET_DB_DATABASE"),
        'raise_on_warnings': True
    }
    connection_sandbox = get_connect(target_config)

    cursor_prod = connection_prod.cursor()
    cursor_sandbox = connection_sandbox.cursor()

    # init
    cursor_sandbox.execute('set foreign_key_checks = 0')
    connection_sandbox.commit()

    cursor_prod.execute('set foreign_key_checks = 0')
    connection_prod.commit()

    cursor_sandbox.execute('SET SQL_SAFE_UPDATES = 0')
    connection_sandbox.commit()
    # end init

    # migration
    migration('dim_answer', 'SELECT id, text, value, is_other, other_text, extra, color FROM dim_answer',
              'INSERT INTO dim_answer (id, text, value, is_other, other_text, extra, color) VALUES( %s, %s, %s, %s, %s, %s, %s)')
    # end migration

    # end
    connection_prod.close()
    connection_sandbox.close()
    logger.info("end execution. took %r seconds", (time.time() - start_time))
