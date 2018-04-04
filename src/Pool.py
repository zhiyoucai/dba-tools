import pymysql
from time import sleep


class Connection():

    def __init__(self, connection, busy):
        self.busy = busy
        self.connection = connection

    def check(self):
        if self.busy:
            return True
        else:
            return False


list = []


def init(host, port, user, password, dbname, pool_size):

    for i in range(0, pool_size):
        original_connection = pymysql.connect(host=host, port=port, user=user, password=password, db=dbname)
        connection = Connection(original_connection, False)
        list.append(connection)
    return list


def get_connection():
    for conn in list:
        if conn.busy:
            continue
        cur = conn.connection.cursor()
        if (cur.execute('select 1') == 1):
            list.remove(conn)
            conn.busy = True
            cur.close()
            return conn
        else:
            continue


def close_pool_connection(conn):
    conn.busy = False
    list.append(conn)


if __name__ == '__main__':
    init('127.0.0.1', 3306, 'root', '123456', 'test', 3)
    conn = get_connection()
    while True:
        cur = conn.connection.cursor()
        cur.execute('select count(*) from test;')
        r = cur.fetchone()
        print(r)
        cur.close()
        close_pool_connection(conn)
        sleep(3)
