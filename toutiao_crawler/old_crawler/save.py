import MySQLdb
# coding: utf-8

def save_text(out, tablename):
    try:
        conn = MySQLdb.connect(host='192.168.1.201', user='zixun', passwd='zixun', port=3306, db="zixun")
        cur = conn.cursor()
        conn.select_db("zixun")
        conn.set_character_set('utf8')
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;')
        # cur.execute('create table leave_pred( time datetime,email varchar(20),prob float(4))')

        cur.executemany(
            'insert into '+ tablename+'(title, keywords, abstract, content, source, article_url, display_url, image_list,htmls,create_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            out)
        conn.commit()
        cur.close()
        conn.close()

    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
def save_img(out, tablename):
    try:
        conn = MySQLdb.connect(host='192.168.1.201', user='zixun', passwd='zixun', port=3306, db='zixun')
        cur = conn.cursor()
        conn.select_db('zixun')
        conn.set_character_set('utf8')
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;')
        # cur.execute('create table leave_pred( time datetime,email varchar(20),prob float(4))')

        cur.executemany(
            'insert into '+ tablename+'(url,binarytext) values(%s,%s)',
            out)
        conn.commit()
        cur.close()
        conn.close()

    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

# conn = MySQLdb.connect(host='192.168.1.201', user='haozhuo', passwd='haozhuo2015', port=3306, db="qwz")
# cur = conn.cursor()
# conn.select_db("qwz")
# conn.set_character_set('utf8')
# cur.execute('SET NAMES utf8;')
# cur.execute('SET CHARACTER SET utf8;')
# cur.execute('SET character_set_connection=utf8;')
# selectString = "SELECT binarytext FROM toutiao_pc_img WHERE url = %s"
# url="http://p3.pstatp.com/large/21370000ea57a970f228"
# cur.execute(selectString, (url,))
# data = cur.fetchone()[0]
# imgout = open("d://test/my.png", 'wb')
# imgout.write(data)