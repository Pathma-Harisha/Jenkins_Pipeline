import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Muthupattan@1403",
        database="retail_store",
        cursorclass=pymysql.cursors.DictCursor
    )