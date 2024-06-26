from collections.abc import Mapping
from datetime import datetime
from enum import StrEnum, unique
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from tth.common.users.base import UserType
from tth.db.base import Base, TimestampMixin
from tth.db.utils import make_pg_enum


@unique
class FeatureValue(StrEnum):
    AVAILABLE = "AVAILABLE"
    NOT_AVAILABLE = "NOT_AVAILABLE"


@unique
class EventType(StrEnum):
    STANDUP = "standup"
    CONCERTS = "concerts"
    EXHIBITIONS = "exhibitions"
    THEATER = "theater"
    MUSICALS = "musicals"
    CHILDREN = "children"
    SHOW = "show"
    FESTIVALS = "festivals"


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


class Place(Base, TimestampMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(256), nullable=True)
    address: Mapped[str] = mapped_column(String(256), nullable=True)
    url: Mapped[str] = mapped_column(String(1024), nullable=True)
    image_url: Mapped[str] = mapped_column(String(1024), nullable=True)

    def __repr__(self) -> str:
        return (
            f"Place(id={self.id!r}, name={self.name!r}, address={self.address!r}, "
            f"description={self.description!r}, url={self.url!r}, "
            f"image_url={self.image_url!r}, )"
        )


class Event(Base, TimestampMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    place_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("place.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(256), nullable=True)
    event_type: Mapped[EventType] = mapped_column(
        make_pg_enum(EventType, name="event_type"),
        nullable=False)
    url: Mapped[str] = mapped_column(String(1024), nullable=True)
    image_url: Mapped[str] = mapped_column(String(1024), nullable=True)

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    ended_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )


class Feature(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(
        String(256), nullable=False, unique=True, index=True
    )


class PlaceFeature(Base):
    place_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("place.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        primary_key=True,
    )
    feature_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("feature.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        primary_key=True,
    )
    value: Mapped[FeatureValue] = mapped_column(
        make_pg_enum(FeatureValue, name="feature_value"),
        nullable=False,
    )


class EventFeature(Base):
    event_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("event.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        primary_key=True,
    )
    feature_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("feature.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        primary_key=True,
    )
    value: Mapped[FeatureValue] = mapped_column(
        make_pg_enum(FeatureValue, name="feature_value"),
        nullable=False,
    )
