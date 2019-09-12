from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import contextlib
from loguru import logger
import typing

BaseModel = declarative_base()


class BaseManager(object):
    pass


class MySQLManager(BaseManager):
    def __init__(self, url: str, port: int, user: str, password: str, db_name: str):
        self.url: str = url
        self.port: int = port
        self.user: str = user
        self.password: str = password
        self.db_name: str = db_name

        self.engine: typing.Optional[Engine] = None
        self.session_maker: typing.Optional[typing.Type] = None

        self.models: typing.Dict[str, BaseModel] = {}

    def heartbeat(self) -> bool:
        if (not self.engine) or (not self.session_maker):
            return False
        try:
            self.engine.execute('SELECT "HELLO"')
        except OperationalError:
            return False
        return True

    def connect(self, *args, **kwargs):
        self.engine = create_engine(
            (
                f"mysql+pymysql://"
                f"{self.user}:{self.password}"
                f"@"
                f"{self.url}:{self.port}"
                f"/"
                f"{self.db_name}"
            ),
            *args,
            **kwargs,
        )
        self.session_maker = scoped_session(sessionmaker(bind=self.engine))
        assert self.heartbeat(), "connect failed"
        logger.info(f"connected to {self.url}:{self.port}, db: {self.db_name}")

    def add_model(self, model: BaseModel):
        table_name = model.__tablename__
        self.models[table_name] = model
        logger.info(f"model of {table_name} added")

    def remove_model(self, model: BaseModel):
        table_name = model.__tablename__
        del self.models[table_name]
        logger.info(f"model of {table_name} removed")

    # TODO maybe these events should be handled by queue?
    def insert(self, data):
        try:
            with session_scope(self.session_maker) as session:
                session.add(data)
                session.commit()
                session.flush()
        except:
            return False
        else:
            return True


@contextlib.contextmanager
def session_scope(maker: typing.Type):
    """Provide a transactional scope around a series of operations."""
    session = maker()
    try:
        yield session
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise e
    finally:
        session.close()
