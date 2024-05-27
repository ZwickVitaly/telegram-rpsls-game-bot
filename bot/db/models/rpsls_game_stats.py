from sqlalchemy import BigInteger, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from settings import logger

from ..base import Base


class RPSLSStats(Base):
    __tablename__ = "rpc_stats"

    user_id = Column(
        BigInteger, ForeignKey("users.id", ondelete="NO ACTION"), primary_key=True
    )
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)

    user = relationship(
        "User",
        foreign_keys="RPSLSStats.user_id",
        backref="rpc_stats",
        lazy="selectin",
    )
