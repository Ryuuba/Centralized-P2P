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

    def insert_peer_content(self, nickname: str, sha256: str, url: str):
        """Inserts a row in UserContent table

        Args:
            nickname (str): the nickname of the napster client
            SHA256 (str): the SHA256 key of the linux ISO (hex format)
            url (str): The URL to get the linux ISO via HTTP
        """
        cursor = self.__conn.cursor()
        try:
            cursor.execute('INSERT INTO tblUserContent (nickname, SHA256, url) VALUES (?, ?, ?)', (nickname, sha256, url))
            self.__conn.commit()
            print(f'Napster DB connector: Insert peer content from {nickname} is OK')
        except mariadb.IntegrityError:
            print(f'Napster Database connector:\n file: {url}\n from user {nickname} is already registered')


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

    def search_content(self, kword: str) -> list[str]:
        cursor = self.__conn.cursor()
        cursor.execute('SELECT tblcontent.distro, tblcontent.version, tblcontent.arch, tblcontent.size, tblcontent.target, tblusercontent.url, tblusernetworkdata.ip, tblusernetworkdata.port'
                   + ' FROM tblcontent INNER JOIN tblusercontent ON tblcontent.SHA256 = tblusercontent.SHA256 INNER JOIN tbluser ON tblusercontent.nickname = tbluser.nickname' 
                   + ' INNER JOIN tblusernetworkdata ON tbluser.nickname = tblusernetworkdata.nickname WHERE ? IN (tblcontent.distro, tblcontent.version, tblcontent.arch, tblcontent.target)',  (kword,))
        results = cursor.fetchall()
        return results


    def insert_netw_data(self, user: str, ip: str, port: int):
        cursor = self.__conn.cursor()
        cursor.execute('DELETE FROM tblUserNetworkData WHERE nickname=?', 
                (user,))
        cursor.execute('INSERT INTO tblUserNetworkData VALUES (?, ?, ?)', 
                (ip, port, user))
        cursor.execute('SELECT * FROM tblUserNetworkData')
        self.__conn.commit()

    # TODO: delete content when no peer shares it
    def delete_peer_content(self, user: str):
        cursor = self.__conn.cursor()
        cursor.execute('DELETE FROM tblUserContent WHERE nickname=?', (user,))
        self.__conn.commit()

    def close(self):
        self.__conn.close()
