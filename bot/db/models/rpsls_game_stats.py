from sqlalchemy import Column, Integer, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from ..base import Base
from settings import logger


class RPSLSStats(Base):
    __tablename__ = "rpc_stats"

    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="NO ACTION"), primary_key=True)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)

    user = relationship(
        "User",
        foreign_keys="RPSLSStats.user_id",
        backref="rpc_stats",
        lazy="selectin",
    )
