# zx_mysql

`zx_mysql` 是一个用于连接和操作 MySQL 数据库的 Python 库。

## 安装

```bash
pip install zx_mysql


from mysql_cloud import MySqlCloud

# 初始化数据库连接
test = MySqlCloud('localhost', 3306, 'user', 'password')
# 连接数据库
connection = test.connect_database('test_db')



