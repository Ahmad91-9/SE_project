import pymysql
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def get_db():
    """Return a direct PyMySQL connection to the production database."""
    return pymysql.connect(
        host="sql100.infinityfree.com",
        user="if0_40456990",
        password="zUm1OE0J2jm3w",
        database="if0_40456990_uos_event_manager",
        port=3306,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )
