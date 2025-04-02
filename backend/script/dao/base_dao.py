# base DAO for all DAO base setting
from dotenv import load_dotenv
from sqlalchemy import create_engine
from urllib.parse import quote_plus as urlquote
from sys import exc_info
import os

# Load .env file
load_dotenv()

class BaseDAO:
    def __init__(self):
        # protected access specifier: let class memeber could be accessed by class itself and its subclasses
        self._engine = create_engine(
                        "mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4".format(
                                os.getenv("USER"), 
                                urlquote(os.getenv("PASSWORD")), 
                                os.getenv("HOST"), 
                                os.getenv("NAME")
                            ),
                            echo=False,
                        )
    def query(self, sql, values_list: list=None):
        try:
            with self._engine.connect() as conn:
                response = conn.execute(sql, values_list)
                conn.commit()
                return response
        except Exception as e:
            exc_type, _, exc_tb = exc_info()
            title = "Error on line %d: " % exc_tb.tb_lineno
            msg = title + "(%s) %s" % (exc_type.__name__, e)
            return msg