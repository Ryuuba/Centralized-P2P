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
    cursor.execute('SELECT tblcontent.distro, tblcontent.version, tblcontent.arch, tblcontent.size, tblcontent.target, tblusercontent.url, tblusernetworkdata.ip, tblusernetworkdata.port'
                   + ' FROM tblcontent INNER JOIN tblusercontent ON tblcontent.SHA256 = tblusercontent.SHA256 INNER JOIN tbluser ON tblusercontent.nickname = tbluser.nickname' 
                   + ' INNER JOIN tblusernetworkdata ON tbluser.nickname = tblusernetworkdata.nickname WHERE ? IN (tblcontent.distro, tblcontent.version, tblcontent.arch, tblcontent.target)',  (kword,))
    #cursor.execute('SELECT * FROM tblcontent WHERE distro=?', (kword,))
    results = cursor.fetchall()
    return results

def close_connection():
    __conn.close()
    
