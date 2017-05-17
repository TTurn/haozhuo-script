import MySQLdb


def save(out, db):
    try:
        conn = MySQLdb.connect(host='192.168.1.201', user='haozhuo', passwd='haozhuo2015', port=3306, db=db)
        cur = conn.cursor()
        conn.select_db(db)
        conn.set_character_set('utf8')
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;')
        # cur.execute('create table leave_pred( time datetime,email varchar(20),prob float(4))')

        cur.executemany(
            'insert into toutiao_app(title, keywords, abstract, content, source, article_url, display_url, image_list) values(%s,%s,%s,%s,%s,%s,%s,%s)',
            out)
        conn.commit()
        cur.close()
        conn.close()

    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
