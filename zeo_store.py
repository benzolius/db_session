"""
Context manager for ZEO connection
"""
import time
import logging
import contextlib
import copy

from ZEO import ClientStorage
from ZODB import DB
import transaction


logger = logging.getLogger("zeo")


@contextlib.contextmanager
def zeo_connection():
    """Provide a transactional scope around a series of operations."""
    storage = ClientStorage.ClientStorage(('localhost', 50001))
    db = DB(storage)
    conn = db.open()
    try:
        yield conn.root()
    except Exception as ex:
        logger.error('Could not connect to ZEO. Exception: {0}'.format(ex))
    finally:
        conn.close()
        db.close()


def save(key='default', value={}):
    """
    Saves value in the ZODB with the received key
    Should retry transaction commit when conflict occurs
    """
    saved_obj = None
    for i in range(10):
        with zeo_connection() as db_root:
            try:
                store = db_root[key]
            except KeyError:
                store = {}
            store.update(value)
            db_root[key] = store
            try:
                transaction.commit()
                saved_obj = copy.deepcopy(store)
                break
            except Exception as ex:
                logger.debug('Unknown exception: {0}'.format(ex))
                time.sleep(0.2)

    return saved_obj
