import os
import mysql.connector


def get_connect(config):
    return mysql.connector.connect(**config)


if __name__ == "__main__":
    print("start app")
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

    cursor_sandbox.execute('set foreign_key_checks = 0')
    connection_sandbox.commit()

    cursor_prod.execute('set foreign_key_checks = 0')
    connection_prod.commit()

    cursor_sandbox.execute('SET SQL_SAFE_UPDATES = 0')
    connection_sandbox.commit()

    cursor_sandbox.execute('truncate dim_answer')
    connection_sandbox.commit()
    cursor_prod.execute('SELECT id, text, value, is_other, other_text, extra, color FROM dim_answer')
    data = cursor_prod.fetchall()

    # end
    connection_prod.close()
    connection_sandbox.close()
    print("end app")
