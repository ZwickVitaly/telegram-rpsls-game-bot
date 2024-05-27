from datetime import datetime

from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from ..base import Base


class Group(Base):
    __tablename__ = "groups"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    owner_id = Column(
        BigInteger, ForeignKey("users.id", ondelete="SET NULL"), default=None
    )
    added = Column(DateTime(timezone=True), default=datetime.now())
    inactive = Column(Boolean, default=False)

    moderators = relationship(
        "User",
        secondary="groups_moderators",
        backref="moderated_chats",
        lazy="selectin",
    )

    owner = relationship(
        "User",
        foreign_keys="Group.owner_id",
        backref="owned_groups",
        lazy="selectin",
    )
