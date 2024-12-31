
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'fe0855140432'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('counts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('adress_type_object', sa.String(length=128), nullable=True),
    sa.Column('electric_time', sa.String(length=128), nullable=True),
    sa.Column('tarif', sa.String(length=128), nullable=True),
    sa.Column('crowl', sa.String(length=128), nullable=True),
    sa.Column('type_crowl', sa.String(length=128), nullable=True),
    sa.Column('type_system', sa.String(length=128), nullable=True),
    sa.Column('power_station', sa.String(length=128), nullable=True),
    sa.Column('acamulator', sa.String(length=128), nullable=True),
    sa.Column('phone', sa.String(length=128), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('registers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('contact', sa.String(length=128), nullable=False),
    sa.Column('pdf_file', sa.LargeBinary(), nullable=True),
    sa.Column('comment', sa.String(length=128), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('username', sa.String(length=128), nullable=True),
    sa.Column('full_name', sa.String(length=128), nullable=False),
    sa.Column('active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
    sa.Column('language', sa.String(length=10), server_default=sa.text("'en'"), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('registers')
    op.drop_table('counts')
    # ### end Alembic commands ###
