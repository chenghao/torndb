# coding:utf-8
__author__ = 'chenghao'

import torndb

conn = torndb.Connection("%s:%s" % ('192.168.1.103', "3306"), 'test', 'root', '123456',
                         time_zone="+8:00", auto_commit=True)
t_conn = torndb.Connection("%s:%s" % ('192.168.1.103', "3306"), 'test', 'root', '123456',
                           time_zone="+8:00", auto_commit=False)


@torndb.transaction(conn=t_conn)
def add_article(title, content, category_title):
    """
    add article
    :param title:
    :param content:
    :param category_title: Plurality ',' separated
    :return:
    """
    sql = "insert into article(title, content) values(%s, %s)"
    article_id = t_conn.insert(sql, title, content)
    if article_id:
        cid = []
        params = []
        titles = category_title.split(",")
        for t in titles:
            result = get_category(t)
            if result:
                cid.append(result["pid"])
            else:
                category_id = add_category(t)
                cid.append(category_id)

        for i in cid:
            params.append((article_id, i))

        z = 10 / 0
        print z

        sql = "insert into article_category(article_id, category_id) values(%s, %s)"
        t_conn.executemany(sql, params)


def get_category(title):
    sql = "select pid, title from category where title=%s"
    return conn.get(sql, title)


def add_category(title):
    sql = "insert into category(title) values(%s)"
    return conn.insert(sql, title)

if __name__ == '__main__':
    add_article("test3", "test3 content3 123456789", "demo1,demo2,test2")