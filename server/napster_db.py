import mariadb, sys
from dataclasses import dataclass, field

@dataclass
class DBNapsterConnector:
    __conn : mariadb.Connection = field(default_factory=lambda: mariadb.connect(
            user='root',
            password='sistemasdistribuidos',
            host='localhost',
            port=3306,
            database='napster')
    )

    def insert_peer_content(self, 
            nickname: str,
            distro: str,
            version: str,
            arch:str,
            SHA256: str,
            size: int,
            filename: str) -> None:
        """Inserts a row in Content table
            Args:
                nickname (str): The client's nickname
                ip (str): The client's host IP address
                port (int): The port number where the client listen to HTTP requests
                distro (str): The name of the GNU/Linux distribution
                version (str): The version of the GNU/Linux distribution
                arch (str): The hardware architecture compatible with the distro
                SHA256 (str): A 256-bit key that identifies the content
                size (int): The size of the distro in bytes
                filename (str): The filename used to request the distro
        """
        cursor = self.__conn.cursor()
        cursor.execute(
        """INSERT INTO tblContent (distro,version,arch,SHA256,size)\
        VALUES (?, ?, ?, ?, ?)""",(distro,version,arch,SHA256,size))
        cursor.execute(
        """INSERT INTO tblContent (distro,version,arch,SHA256,size)\
        VALUES (?, ?, ?, ?, ?)""",(distro,version,arch,SHA256,size))

    def remove_content(self, nickname: str) -> bool:
        pass

    def search_user_email(self, nickname: str, password: str) -> str:
        user_email = ''
        cursor = self.__conn.cursor()
        cursor.execute('SELECT email FROM tblUser WHERE nickname=? AND password=?', (nickname, password))
        result = cursor.fetchone()
        if result:
            user_email = result[0]
        return user_email

    def search_content(self, kwords: list[str]) -> list[str]:
        pass

    def insert_netw_data(self, user: str, ip: str, port: int):
        cursor = self.__conn.cursor()
        cursor.execute('DELETE FROM tblUserNetworkData WHERE nickname=?', 
                (user,))
        cursor.execute('INSERT INTO tblUserNetworkData VALUES (?, ?, ?)', 
                (ip, port, user))
        cursor.execute('SELECT * FROM tblUserNetworkData')
        self.__conn.commit()

    def close(self):
        self.__conn.close()
