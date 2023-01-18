import sys
# import pymysql
import mariadb


try: con = mariadb.connect( 

    user="uriel", 
    password="1234", 
    host="localhost", 
    port=3306, 
    database="lista_compra" 

)

except mariadb.Error as ex: 

    print(f" Un error ha ocurrido mientras la conexion con mariaDB: {ex}") 
    sys.exit(1) 


# Get Cursor 
cur = con.cursor()

#
# try:
#     cur.execute("CREATE TABLE usuarios (id int, nombre varchar(255))")
# except mariadb.Error as e:
#         print(f"Error: {e}")


try: 
    cur.execute("INSERT INTO usuarios (id,nombre) VALUES (?, ?)", ("1","MARIAJUANADELGADOLUPITAAAAAAA")) 
except mariadb.Error as e: 
    print(f"Error: {e}")


con.commit() 
print(f"Last Inserted ID: {cur.lastrowid}")

con.close()


