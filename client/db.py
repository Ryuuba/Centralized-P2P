import mariadb
import sys

# Connecto to mariadb
__conn = mariadb.connect(
    user='root',
    password='sistemasdistribuidos',
    host='localhost',
    port=3306,
    database='napster')

def search_content(kword:str)->list[str]:
    cursor = __conn.cursor()
    cursor.execute('SELECT * FROM tblcontent WHERE distro=?', (kword,))
    results = cursor.fetchall()
    __conn.close()
    return results
    

