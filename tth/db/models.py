from collections.abc import Mapping
from datetime import datetime
from enum import IntEnum, unique
from typing import Any

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tth.common.users.base import UserType
from tth.db.base import Base, TimestampMixin
from tth.db.utils import make_pg_enum


@unique
class DisabilityStatus(IntEnum):
    ADVATAGE = 1
    DISADVANTAGE = -1


class User(Base, TimestampMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[UserType] = mapped_column(
        make_pg_enum(UserType, name="user_type"),
        nullable=False,
        index=True,
        default=UserType.REGULAR.value,
    )
    username: Mapped[str] = mapped_column(
        String(256),
        unique=True,
        nullable=False,
        index=True,
    )
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    properties: Mapped[Mapping[str, Any]] = mapped_column(
        JSONB(),
        server_default="{}",
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"


class Telegram(Base, TimestampMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id"), nullable=False, index=True, unique=True
    )
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    is_banned: Mapped[bool] = mapped_column(nullable=False, default=False)

    user: Mapped[User] = relationship("User", backref="telegram", uselist=False)

    def __repr__(self) -> str:
        return (
            f"Telegram(id={self.id!r}, user_id={self.user_id!r}, "
            f"chat_id={self.chat_id!r}, is_banned={self.is_banned!r})"
        )


class Place(Base, TimestampMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(256), nullable=False)
    address: Mapped[str] = mapped_column(String(256), nullable=False)

    def __repr__(self) -> str:
        return (
            f"Place(id={self.id!r}, name={self.name!r}, address={self.address!r}, "
            f"description={self.description!r})"
        )


class Event(Base, TimestampMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    place_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("place.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(256), nullable=False)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    ended_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )


class Disability(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    group: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    status: Mapped[DisabilityStatus] = mapped_column(
        make_pg_enum(DisabilityStatus, name="disability_status"),
    )


class PlaceDisability(Base):
    place_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("place.id"),
        nullable=False,
        index=True,
        primary_key=True,
    )
    disability_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("disability.id"),
        nullable=False,
        index=True,
        primary_key=True,
    )


class EventDisability(Base):
    event_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("event.id"),
        nullable=False,
        index=True,
        primary_key=True,
    )
    disability_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("disability.id"),
        nullable=False,
        index=True,
        primary_key=True,
    )


class UserDisability(Base):
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id"),
        nullable=False,
        index=True,
        primary_key=True,
    )
    disability_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("disability.id"),
        nullable=False,
        index=True,
        primary_key=True,
    )
