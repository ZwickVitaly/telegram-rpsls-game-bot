from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer
from sqlalchemy.sql import func

from ..base import Base


class GroupModerator(Base):
    __tablename__ = "groups_moderators"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(BigInteger, ForeignKey("groups.id", ondelete="NO ACTION"))
    moderator = Column(BigInteger, ForeignKey("users.id", ondelete="NO ACTION"))
    added = Column(DateTime(timezone=True), server_default=func.now())
