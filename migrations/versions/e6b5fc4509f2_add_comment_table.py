"""add comment table

Revision ID: e6b5fc4509f2
Revises: ccb65de4d3bc
Create Date: 2025-05-21 10:49:12.114746

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e6b5fc4509f2'
down_revision: Union[str, None] = 'ccb65de4d3bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "comments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("content", sa.String()),
        sa.Column("post_id", sa.Integer(), sa.ForeignKey("posts.id")),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id")),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index("ix_comments_id", "comments", ["id"], unique=False)

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_comments_id", table_name="comments")
    op.drop_table("comments")