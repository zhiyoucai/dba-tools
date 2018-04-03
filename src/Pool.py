import pymysql

list = []


def init(host, port, user, password, dbname, pool_size):

    for i in range(0, pool_size):
        list.append(pymysql.connect(host=host, port=port, user=user, password=password))
    return list


def get_connection():
    for connection in list:
        cur = connection.cursor()
        if (cur.execute('select 1') == 1):
            list.remove(connection)
            return connection
        else:
            continue


def close_pool_connection(connection):
    list.append(connection)


if __name__ == '__main__':
    init('127.0.0.1', 3306, 'root', '123456', 'test', 1)
    conn = get_connection()
    cur = conn.cursor()
    r = cur.execute('select sysdate()')
    print(r)
    close_pool_connection(conn)
