from sqlalchemy import BigInteger, Boolean, Column, DateTime
from sqlalchemy.sql import func

from ..base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    added = Column(DateTime(timezone=True), server_default=func.now())
    rpsls_active = Column(Boolean, default=True)
