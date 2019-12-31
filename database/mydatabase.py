# -*- coding: utf-8 -*-

import cx_Oracle

conn = cx_Oracle.connect("coretest", "UL13_T5st_db", cx_Oracle.makedsn('10.10.108.5', 1521, 'coretest'))
cursor = conn.cursor()

# 执行查询 语句
cursor.execute("""select * from AA2""")

# 获取一条记录
one = cursor.fetchone()

print('1: A:%s,B:%s' % one)

# 获取两条记录!!!注意游标已经到了第二条
two = cursor.fetchmany(2)
print('2 and 3:', two[0], two[1])

# 获取其余记录!!!注意游标已经到了第四条
three = cursor.fetchall()
for row in three:
    print(row)  # 打印所有结果

print('条件查询')
cursor.prepare("""select * from aa2 where A <= :id""")
cursor.execute(None, {'id': '5'})
# 相当于fetchall()
for row in cursor:
    print(row)

cursor.close()
conn.close()
