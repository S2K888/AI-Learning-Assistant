import sqlite3
# sqlite3 是 Python 自带的 SQLite 数据库操作模块，不需要额外安装。

from app.core.config import settings #项目中的配置对象。settings.database_name获取数据库文件的名称或者路径。
# connect()：  连接数据库。
# cursor()：   创建游标，执行 SQL。
# execute()：  执行 SQL 语句。
# commit()：   提交数据库修改。
# fetchall()： 获取查询结果。
# close()：    关闭数据库连接。


def init_db(): #初始化数据表
    conn = sqlite3.connect(settings.database_name)
    cursor = conn.cursor()
    #conn：负责建立和管理数据库连接。
    #cursor：负责执行 SQL 语句、获取查询结果。
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        role TEXT,
        content TEXT
    )
    """)#这里的 SQL 是创建数据表的语句。
        #id INTEGER PRIMARY KEY AUTOINCREMENT,表示 id 是这张表的主键，用于唯一标识每条记录。
        #AUTOINCREMENT：自动递增，每次插入新记录时，数据库会自动生成一个新的递增 ID。
    conn.commit() #提交事务，让数据库修改正式生效。
    conn.close()  #关闭数据库连接，释放资源。


def save_message(session_id, role, content): #保存聊天信息，这个函数的作用是向数据库插入一条聊天记录。
    conn = sqlite3.connect(settings.database_name)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO messages (session_id, role, content)
    VALUES (?, ?, ?)
    """, (session_id, role, content))# 这三个参数会依次替换 SQL 中的三个 ?
    conn.commit()
    conn.close()
    # 执行 SQL 时，用户提供的数据应该通过参数传递，而不是直接拼接进 SQL 字符串。


def get_messages(session_id): #获取聊天记录，这段代码涉及 SQL 查询和 Python 列表处理。
    conn = sqlite3.connect(settings.database_name)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT role, content
    FROM messages
    WHERE session_id = ?
    ORDER BY id
    """, (session_id,)) # 从 messages 表中查询 role 和 content 两个字段。
                        # WHERE：筛选数据，意思是只查询指定会话 ID 的聊天记录。
                        # ORDER BY：排序
    rows = cursor.fetchall() # fetchall() 会把查询到的所有记录取出来，返回一个列表。
    conn.close()
    return [{"role": row[0], "content": row[1]} for row in rows] # 遍历 rows，把每个元组转换成字典。


def delete_messages(session_id): # 删除聊天记录，这个函数负责删除指定会话的所有聊天记录。
    conn = sqlite3.connect(settings.database_name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))# 删除 messages 表中，session_id 等于指定值的所有记录。
    deleted_count = cursor.rowcount # rowcount：获取影响的记录数量
    conn.commit()
    conn.close()
    return deleted_count # 因为 Router 需要知道删除了多少条记录，才能判断删除是否成功。
    # deleted_count = 2说明这次删除了两条记录。
