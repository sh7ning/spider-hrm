# coding=utf-8

import psycopg2


class Repository(object):
    def __init__(self):
        self.conn = Conn()

    def insert_article(self, name, cover):
        return self.conn.insert(
            "INSERT INTO article(name, cover) VALUES (%s, %s)",
            (name, cover)
        )

    def insert_pics(self, pics):
        return self.conn.insert_many(
            "INSERT INTO pic (article_id, url) VALUES ",
            "(%s,%s)",
            'id',
            pics
        )


class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance


class Conn(Singleton):
    def __init__(self):
        self.conn = psycopg2.connect(
            database="pt_dev",
            user="postgres",
            password="a123123",
            host="121.43.190.6",
            port="54322"
        )

        self.cur = self.conn.cursor()

    # print pg.insert("INSERT INTO article(name, cover) VALUES (%s, %s)", ('name_test', 'cover_img_test'))
    def insert(self, sql, param):
        self.cur.execute(sql + " RETURNING id;", param)
        insert_id = self.cur.fetchone()[0]
        self.conn.commit()
        return insert_id

    # print pg.insert_many(
    #     "INSERT INTO article (name, cover) VALUES ",
    #     "(%s,%s)",
    #     'id',
    #     [('name_test', 'cover_img_test'), ('name_test1', 'cover_img_test1')]
    # )
    def insert_many(self, sql, placeholder, id_column, data):
        args_str = ','.join(self.cur.mogrify(placeholder, x) for x in data)
        self.cur.execute(sql + args_str + " RETURNING " + id_column + ";")
        self.conn.commit()
        return [t[0] for t in self.cur.fetchall()]

    def disconnect(self):
        self.cur.close()
        self.conn.close()
