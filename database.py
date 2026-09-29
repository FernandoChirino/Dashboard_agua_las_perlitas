# Conexion a MySQL usando PyMySQL
import os 
import pymysql
import pymysql.cursors

# Variables de entorno 
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = int(os.environ.get("DB_PORT", 3306))
DB_USER = os.environ.get("DB_USER", "root")   # usuario de MySQL local
DB_PASSWORD = os.environ.get("DB_PASSWORD", "") # contraseña del usuario de MySQL local 
DB_NAME = os.environ.get("DB_NAME", "electropura")

def get_connection():
    """
    Conexion a la base de datos electropura

    pymysql.cursors.DictCursor, hace que cada fila que devuelva una consulta sea un 
    diccionario ({"id": 1, "username": "operador1"}) en vez de una tupla

    """
    connection = pymysql.connect(
        host= DB_HOST, 
        port= DB_PORT, 
        user= DB_USER, 
        password= DB_PASSWORD, 
        database= DB_NAME, 
        charset= "utf8mb4",
        cursorclass= pymysql.cursors.DictCursor,
        autocommit= False
    )
    return connection

if __name__ == "__main__":
    # Prueba rapida: si esto corre sin errores e imprime la version de
    # MySQL, la conexion esta bien configurada.
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT VERSION()")
        version = cur.fetchone()
        print("Conectado correctamente. Version de MySQL:", version)
    conn.close()