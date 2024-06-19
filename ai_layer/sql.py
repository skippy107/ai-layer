from langchain_community.utilities import SQLDatabase

import os

from sqlalchemy.engine import URL, create_engine

class MakeURL(object):
    def __new__(cls):
        
        return URL.create(
            drivername=os.getenv('DB_DRIVER'),
            username=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME')
        )

class MakeEngine(object):
    def __new__(cls):

        the_url = MakeURL()

        return create_engine(the_url)

class MakeSQLDatabase(object):
    def __new__(cls):

        return SQLDatabase(MakeEngine())
