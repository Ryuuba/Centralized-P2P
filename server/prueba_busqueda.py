# Program to display the data
import mariadb
from dataclasses import dataclass, field


import mariadb, sys
from dataclasses import dataclass, field

@dataclass
class DBNapsterConnector:
    __conn : mariadb.Connection = field(default_factory=lambda: mariadb.connect(
            user='alanbc',
            password='seer1234',
            host='localhost',
            port=3306,
            database='napster')
    )

    def insert_content(self, nickname: str, distro: str, version: str, arch:str,
            sha256: str, size: int, target: str) -> None:
        """Inserts a row in Content table
            Args:
                distro (str): The name of the GNU/Linux distribution
                version (str): The version of the GNU/Linux distribution
                arch (str): The hardware architecture compatible with the distro
                SHA256 (str): A 256-bit key that identifies the content
                size (int): The size of the distro in bytes
                target (str): The kind of supported hardware, e.g., server o workstation
        """
        cursor = self.__conn.cursor()
        try:
            cursor.execute(
            'INSERT INTO tblContent (distro, version, arch, SHA256, size, target) VALUES (?, ?, ?, ?, ?, ?)',(distro, version, arch, sha256, size, target))
            self.__conn.commit()
            print(f'Napster DB Connector: Insert new content from {nickname} is OK')
        except mariadb.IntegrityError:
            print(f'Napster Database connector:\n distro: {distro}\n with SHA256 key {sha256} is already registered')

    def search_user_email(self, nickname: str, password: str) -> str:
        user_email = ''
        cursor = self.__conn.cursor()
        cursor.execute('SELECT email FROM tblUser WHERE nickname=? AND password=?', (nickname, password))
        result = cursor.fetchone()
        if result:
            user_email = result[0]
        return user_email
    
    
    def search_content(self, kwords: list[str]) -> list[str]:
        cursor = self.__conn.cursor()
        cursor.execute('SELECT * FROM tblUserNetworkData')
        result = cursor.fetchall()
        for all in result:
            kwords.append(all)
            print(all)


    def close(self):
        self.__conn.close()


db_conn = DBNapsterConnector()
db_conn.search_content()