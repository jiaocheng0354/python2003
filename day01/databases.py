import MySQLdb


class Database:
    conn = MySQLdb.connect(
        host='127.0.0.1',  # mysql所在主机的ip
        port=3306,  # mysql的端口号
        user="root",  # mysql 用户名
        password="123456",  # mysql 的密码
        db="textdb_1",  # 要使用的库名
        charset="utf8"  # 连接中使用的字符集
    )
    table = "work"
    def __init__(self,table):
        self.table=table
    def get(self,url):
        try:
            cursor = self.conn.cursor()
            sql = "select id from "+ self.table + " where url='%s'"% url
            row_count = cursor.execute(sql)
            if row_count==1:
                return True
            else:
                return False
        except:
            pass

    def get_page(self, page):
        try:
            cursor = self.conn.cursor()
            sql = "select id from " + self.table + " where page='%s'" %page
            row_count = cursor.execute(sql)
            if row_count == 0:
                return False
            else:
                return True
        except:
            pass

    def set(self,keys,values):
        try:
            keys = str(tuple(keys)).replace("'","")
            cursor = self.conn.cursor()
            sql = "insert into "+ self.table + "%s values %s" % (keys, str(tuple(values)))
            # print(sql)
            row_count = cursor.execute(sql)
            cursor.close()
            self.conn.commit()
        except:
            pass

    def closed(self):
        self.conn.close()
if __name__ == "__main__":
    data = Database("work")
    keys = ["name","url","salary"]
    values = ["Mr_lee","html","202"]
    data.set(keys,values)
    data.closed()
