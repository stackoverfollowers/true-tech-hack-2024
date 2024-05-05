"""empty message

Revision ID: 85bb83094ff2
Revises: 5152d4474e30
Create Date: 2024-05-05 12:42:11.323860

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '85bb83094ff2'
down_revision: Union[str, None] = '5152d4474e30'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('feature',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('slug', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__feature'))
    )
    op.create_index(op.f('ix__feature__name'), 'feature', ['name'], unique=False)
    op.create_index(op.f('ix__feature__slug'), 'feature', ['slug'], unique=True)
    op.create_table('place_feature',
    sa.Column('place_id', sa.Integer(), nullable=False),
    sa.Column('feature_id', sa.Integer(), nullable=False),
    sa.Column('value', postgresql.ENUM('AVAILABLE', 'NOT_AVAILABLE', name='feature_value'), nullable=False),
    sa.ForeignKeyConstraint(['feature_id'], ['feature.id'], name=op.f('fk__place_feature__feature_id__feature'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['place_id'], ['place.id'], name=op.f('fk__place_feature__place_id__place'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('place_id', 'feature_id', name=op.f('pk__place_feature'))
    )
    op.create_index(op.f('ix__place_feature__feature_id'), 'place_feature', ['feature_id'], unique=False)
    op.create_index(op.f('ix__place_feature__place_id'), 'place_feature', ['place_id'], unique=False)
    op.create_table('event_feature',
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('feature_id', sa.Integer(), nullable=False),
    sa.Column('value', postgresql.ENUM('AVAILABLE', 'NOT_AVAILABLE', name='feature_value'), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], name=op.f('fk__event_feature__event_id__event'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['feature_id'], ['feature.id'], name=op.f('fk__event_feature__feature_id__feature'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('event_id', 'feature_id', name=op.f('pk__event_feature'))
    )
    op.create_index(op.f('ix__event_feature__event_id'), 'event_feature', ['event_id'], unique=False)
    op.create_index(op.f('ix__event_feature__feature_id'), 'event_feature', ['feature_id'], unique=False)
    op.drop_index('ix__event_disability__disability_id', table_name='event_disability')
    op.drop_index('ix__event_disability__event_id', table_name='event_disability')
    op.drop_table('event_disability')
    op.drop_index('ix__user_disability__disability_id', table_name='user_disability')
    op.drop_index('ix__user_disability__user_id', table_name='user_disability')
    op.drop_table('user_disability')
    op.drop_index('ix__disability__group', table_name='disability')
    op.drop_index('ix__disability__name', table_name='disability')
    op.drop_index('ix__place_disability__disability_id', table_name='place_disability')
    op.drop_index('ix__place_disability__place_id', table_name='place_disability')
    op.drop_table('place_disability')
    op.drop_table('disability')
    op.drop_constraint('fk__event__place_id__place', 'event', type_='foreignkey')
    op.create_foreign_key(op.f('fk__event__place_id__place'), 'event', 'place', ['place_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk__event__place_id__place'), 'event', type_='foreignkey')
    op.create_foreign_key('fk__event__place_id__place', 'event', 'place', ['place_id'], ['id'])
    op.create_table('place_disability',
    sa.Column('place_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('disability_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['disability_id'], ['disability.id'], name='fk__place_disability__disability_id__disability'),
    sa.ForeignKeyConstraint(['place_id'], ['place.id'], name='fk__place_disability__place_id__place'),
    sa.PrimaryKeyConstraint('place_id', 'disability_id', name='pk__place_disability')
    )
    op.create_index('ix__place_disability__place_id', 'place_disability', ['place_id'], unique=False)
    op.create_index('ix__place_disability__disability_id', 'place_disability', ['disability_id'], unique=False)
    op.create_table('disability',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('disability_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=256), autoincrement=False, nullable=False),
    sa.Column('group', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('status', postgresql.ENUM('1', '-1', name='disability_status'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='pk__disability'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix__disability__name', 'disability', ['name'], unique=False)
    op.create_index('ix__disability__group', 'disability', ['group'], unique=False)
    op.create_table('user_disability',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('disability_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['disability_id'], ['disability.id'], name='fk__user_disability__disability_id__disability'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='fk__user_disability__user_id__user'),
    sa.PrimaryKeyConstraint('user_id', 'disability_id', name='pk__user_disability')
    )
    op.create_index('ix__user_disability__user_id', 'user_disability', ['user_id'], unique=False)
    op.create_index('ix__user_disability__disability_id', 'user_disability', ['disability_id'], unique=False)
    op.create_table('event_disability',
    sa.Column('event_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('disability_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['disability_id'], ['disability.id'], name='fk__event_disability__disability_id__disability'),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], name='fk__event_disability__event_id__event'),
    sa.PrimaryKeyConstraint('event_id', 'disability_id', name='pk__event_disability')
    )
    op.create_index('ix__event_disability__event_id', 'event_disability', ['event_id'], unique=False)
    op.create_index('ix__event_disability__disability_id', 'event_disability', ['disability_id'], unique=False)
    op.drop_index(op.f('ix__event_feature__feature_id'), table_name='event_feature')
    op.drop_index(op.f('ix__event_feature__event_id'), table_name='event_feature')
    op.drop_table('event_feature')
    op.drop_index(op.f('ix__place_feature__place_id'), table_name='place_feature')
    op.drop_index(op.f('ix__place_feature__feature_id'), table_name='place_feature')
    op.drop_table('place_feature')
    op.drop_index(op.f('ix__feature__slug'), table_name='feature')
    op.drop_index(op.f('ix__feature__name'), table_name='feature')
    op.drop_table('feature')
    # ### end Alembic commands ###