from sqlalchemy.orm import declarative_base  # type:ignore
from sqlalchemy.orm.session import sessionmaker,Session
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.engine import create_engine,Engine
from config import Config

#this code is heavily ispired by:https://github.com/hugapi/hug/blob/8b5ac00632543addfdcecc326d0475a685a0cba7/examples/sqlalchemy_example/demo/context.py

DeclarativeBase = declarative_base()

session_factory = lambda engine:scoped_session(sessionmaker(bind=engine))


class SqlAlchemyContext(object):
    _engine:Engine
    _db:Session
    
    def __init__(self):
        config = Config()
        self._engine = create_engine(config.SQLALCHEMY_DATABASE_URI,echo=config.SQLALCHEMY_TRACK_MODIFICATIONS,future=True)
        self._db = session_factory(self._engine)

    @property
    def db(self):
        return self._db
    
    def cleanup(self,exception=None):
        if exception:
            self.db.rollback()
            return
        self.db.commit()

