"""Initial revision

Revision ID: 36e04eadb38a
Revises:
Create Date: 2024-05-12 10:48:58.868495

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "36e04eadb38a"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

event_type_enum = postgresql.ENUM(
    "standup",
    "concerts",
    "exhibitions",
    "theater",
    "musicals",
    "children",
    "show",
    "festivals",
    name="event_type",
)
user_type_enum = postgresql.ENUM("ADMIN", "REGULAR", name="user_type")
feature_value_enum = postgresql.ENUM("AVAILABLE", "NOT_AVAILABLE", name="feature_value")


def upgrade() -> None:
    op.create_table(
        "feature",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.Column("slug", sa.String(length=256), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__feature")),
    )
    op.create_index(op.f("ix__feature__name"), "feature", ["name"], unique=False)
    op.create_index(op.f("ix__feature__slug"), "feature", ["slug"], unique=True)
    op.create_table(
        "place",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.Column("description", sa.String(length=256), nullable=True),
        sa.Column("address", sa.String(length=256), nullable=True),
        sa.Column("url", sa.String(length=1024), nullable=True),
        sa.Column("image_url", sa.String(length=1024), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__place")),
    )
    op.create_index(op.f("ix__place__name"), "place", ["name"], unique=False)
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("type", user_type_enum, nullable=False),
        sa.Column("username", sa.String(length=256), nullable=False),
        sa.Column("password_hash", sa.String(length=256), nullable=False),
        sa.Column(
            "properties",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default="{}",
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__user")),
    )
    op.create_index(op.f("ix__user__type"), "user", ["type"], unique=False)
    op.create_index(op.f("ix__user__username"), "user", ["username"], unique=True)
    op.create_table(
        "event",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("place_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.Column("description", sa.String(length=256), nullable=True),
        sa.Column("event_type", event_type_enum, nullable=False),
        sa.Column("url", sa.String(length=1024), nullable=True),
        sa.Column("image_url", sa.String(length=1024), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["place_id"],
            ["place.id"],
            name=op.f("fk__event__place_id__place"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__event")),
    )
    op.create_index(op.f("ix__event__ended_at"), "event", ["ended_at"], unique=False)
    op.create_index(op.f("ix__event__name"), "event", ["name"], unique=False)
    op.create_index(op.f("ix__event__place_id"), "event", ["place_id"], unique=False)
    op.create_index(
        op.f("ix__event__started_at"), "event", ["started_at"], unique=False
    )
    op.create_table(
        "place_feature",
        sa.Column("place_id", sa.Integer(), nullable=False),
        sa.Column("feature_id", sa.Integer(), nullable=False),
        sa.Column(
            "value",
            feature_value_enum,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["feature_id"],
            ["feature.id"],
            name=op.f("fk__place_feature__feature_id__feature"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["place_id"],
            ["place.id"],
            name=op.f("fk__place_feature__place_id__place"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "place_id", "feature_id", name=op.f("pk__place_feature")
        ),
    )
    op.create_index(
        op.f("ix__place_feature__feature_id"),
        "place_feature",
        ["feature_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix__place_feature__place_id"), "place_feature", ["place_id"], unique=False
    )
    op.create_table(
        "event_feature",
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("feature_id", sa.Integer(), nullable=False),
        sa.Column("value", feature_value_enum, nullable=False),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["event.id"],
            name=op.f("fk__event_feature__event_id__event"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["feature_id"],
            ["feature.id"],
            name=op.f("fk__event_feature__feature_id__feature"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "event_id", "feature_id", name=op.f("pk__event_feature")
        ),
    )
    op.create_index(
        op.f("ix__event_feature__event_id"), "event_feature", ["event_id"], unique=False
    )
    op.create_index(
        op.f("ix__event_feature__feature_id"),
        "event_feature",
        ["feature_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix__event_feature__feature_id"), table_name="event_feature")
    op.drop_index(op.f("ix__event_feature__event_id"), table_name="event_feature")
    op.drop_table("event_feature")
    op.drop_index(op.f("ix__place_feature__place_id"), table_name="place_feature")
    op.drop_index(op.f("ix__place_feature__feature_id"), table_name="place_feature")
    op.drop_table("place_feature")
    op.drop_index(op.f("ix__event__started_at"), table_name="event")
    op.drop_index(op.f("ix__event__place_id"), table_name="event")
    op.drop_index(op.f("ix__event__name"), table_name="event")
    op.drop_index(op.f("ix__event__ended_at"), table_name="event")
    op.drop_table("event")
    op.drop_index(op.f("ix__user__username"), table_name="user")
    op.drop_index(op.f("ix__user__type"), table_name="user")
    op.drop_table("user")
    op.drop_index(op.f("ix__place__name"), table_name="place")
    op.drop_table("place")
    op.drop_index(op.f("ix__feature__slug"), table_name="feature")
    op.drop_index(op.f("ix__feature__name"), table_name="feature")
    op.drop_table("feature")

    conn = op.get_bind()
    event_type_enum.drop(conn)
    user_type_enum.drop(conn)
    feature_value_enum.drop(conn)
