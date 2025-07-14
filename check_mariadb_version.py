import MySQLdb

try:
    conn = MySQLdb.connect(
        host="localhost",
        port=3306,
        user="root",  # Change if your DB user is different
        passwd="",    # Change if your DB password is set
    )
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION();")
    version = cursor.fetchone()[0]
    print(f"MariaDB/MySQL version: {version}")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
