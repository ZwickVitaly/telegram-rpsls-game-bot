"""
Module of base sqlalchemy settings
"""
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from settings import DATABASES, DEBUG, logger


def create_db_url(db_settings, debug):
    logger.debug("Computing db url")
    if debug:
        logger.debug("SQLite db, because DEBUG set to True")
        sqlite = db_settings['debug']
        return f"{sqlite['driver']}:///{sqlite['path']}"

    logger.debug("PostgreSQL db, because debug set to False")
    postgres = db_settings['main']
    return (f"{postgres['driver']}:"
            f"//{postgres.get('username') or postgres['default_user_name']}:"
            f"{postgres.get('password') or postgres['default_user_name']}@"
            f"{postgres['host']}:{postgres['port']}/{postgres['db_name']}")


db_url = create_db_url(DATABASES, DEBUG)

logger.debug("Creating engine")
engine = create_async_engine(db_url)
logger.debug("Creating declarative base")
Base = declarative_base()
logger.debug("Creating async session maker")
async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
)
