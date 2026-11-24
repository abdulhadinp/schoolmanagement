# This makes PyMySQL work as a drop-in replacement for mysqlclient.
# It lets Django talk to MySQL using a pure-Python library, which is
# much easier to install on Windows than mysqlclient.
import pymysql

pymysql.install_as_MySQLdb()
