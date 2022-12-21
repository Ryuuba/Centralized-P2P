import mariadb, sys

def create_connection(
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

def print_user_list(conn: mariadb.Connection) -> None:
    cur = conn.cursor()
    for nick, email in cur:
        print(f'{nick},\t{email}')

