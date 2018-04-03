import pymysql
from time import sleep
import argparse

dic = {}
dic['qps'] = ('Com_insert', 'Com_select', 'Com_delete', 'Com_update', 'Com_replace', 'Questions', 'Queries')
dic['lock'] = ('Table_locks_immediate', 'Table_locks_waited')
dic['connection'] = ('Max_used_connections', 'Connections')


def init_pool():
    connection = pymysql.connect(host=args['host'], port=args['port'], user=args['user'], password=args['pass'],
                                 db=args['db'])
    return connection


def check_status():
    status_dict = {}
    sql = 'show global status'
    connection = init_pool()
    cur = connection.cursor()
    cur.execute(sql)
    for status in cur:
        status_dict[status[0]] = status[1]
    cur.close()
    connection.close()
    return status_dict


def check():
    monitor = args['type']
    print('开始进行' + monitor + '的输出')
    for name in dic[monitor]:
        print('     {}'.format(name), end='')
    print()
    i = 0
    while True:
        status_dict1 = check_status()
        sleep(args['interval'])
        status_dict2 = check_status()
        print(args['avg'])
        if args['avg'] is True:
            for s in dic[monitor]:
                print('     ' + str(round((int(status_dict2[s]) - int(status_dict1[s])) / args['interval'], 2)).center(
                    len(s)), end='')
            print()
            i += 1
            if i % 10 == 0:
                for name in dic[monitor]:
                    print('     {}'.format(name), end='')
                print()
        else:
            for s in dic[monitor]:
                print('     ' + str(round((int(status_dict2[s]) - int(status_dict1[s])), 2)).center(
                    len(s)), end='')
            print()
            i += 1
            if i % 10 == 0:
                for name in dic[monitor]:
                    print('     {}'.format(name), end='')
                print()


def read_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='输入数据库的IP', default='127.0.0.1')
    parser.add_argument('--port', default=3306, type=int)
    parser.add_argument('--type', default='qps')
    parser.add_argument('--user', default='root')
    parser.add_argument('--pass')
    parser.add_argument('--db')
    parser.add_argument('--interval', default=3, type=int)
    parser.add_argument('--avg', default=False, type=bool)
    global args
    args = vars(parser.parse_args())


if __name__ == '__main__':
    read_arg()
    check()
