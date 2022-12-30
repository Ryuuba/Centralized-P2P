import mariadb, sys
from dataclasses import dataclass, field

def __create_connection(
        password:str, database: str, user:str='root', ip: str='localhost', 
        port: int=3306) -> mariadb.Connection:
    """This function creates a Maria DB connector that may be used to create a cursor to access the database

    Args:
        password (str): the user's password to access the SQL server
        database (str): the name of the database to connect
        user (str, optional): The user's nick to access the SQL server. Defaults to 'root'.
        ip (str, optional): The IP address of the SQL server. Defaults to 'localhost'.
        port (int, optional): The number of the port identifying the SQL server. Defaults to 3306.

    Returns:
        mariadb.Connection: Object to get a database cursor
    """
    try:
        conn = mariadb.connect(
            user=user,
            password=password,
            host=ip,
            port=port,
            database=database
        )
    except mariadb.Error as e:
        print(f'Error connecting to MariaDB Platform: {e}')
        sys.exit(1)
    return conn

@dataclass
class DBNapsterConnector:
    conn = field(default_factory=__create_connection(
        password='sistemasdistribuidos', database='napster'
    ))

    def print_user_list(self) -> None:
        """Prints the user list given a DB connector. Use this function to print
        short tables

        Args:
            conn (mariadb.Connection): _description_
        """
        cursor = self.conn.cursor()
        for nick, email in cursor:
            print(f'{nick},\t{email}')

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
        cursor = self.conn.cursor()
        cursor.execute(
        """INSERT INTO tblContent (distro,version,arch,SHA256,size)\
        VALUES (?, ?, ?, ?, ?)""",(distro,version,arch,SHA256,size))
        cursor.execute(
        """INSERT INTO tblContent (distro,version,arch,SHA256,size)\
        VALUES (?, ?, ?, ?, ?)""",(distro,version,arch,SHA256,size))

    def remove_content(nickname: str) -> bool:
        pass

    def search_email_user(nickname: str) -> str:
        pass
