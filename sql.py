"""
Context manager for SQL session and operations
"""
import logging
import contextlib

from sqlalchemy.orm import sessionmaker

from src import models


logger = logging.getLogger("sql")


Session = sessionmaker(bind=models.engine)


class SessionManager(object):
    """
    Context manager for SQL session and operations
    """
    def __init__(self):
        pass

    def __enter__(self):
        try:
            self.session = Session()
            logger.debug("SQL session opened")
        except Exception as ex:
            logger.error('Could not create SQL session. Exception: {0}'.format(ex))

    def __exit__(self, exception_type, exception_value, traceback):
        try:
            self.session.close()
            logger.debug("SQL session closed")
        except Exception as ex:
            logger.error('Could not close session. Exception: {0}'.format(ex))

    def query(self, *args, **kwargs):
        return self.session(*args, **kwargs)


@contextlib.contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
    except Exception as ex:
        logger.error('Could not create SQL session. Exception: {0}'.format(ex))
    finally:
        session.close()
