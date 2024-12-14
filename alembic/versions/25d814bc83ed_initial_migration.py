"""initial migration

Revision ID: 25d814bc83ed
Revises: 
Create Date: 2024-04-21 09:51:44.977108
"""

from alembic import op
import sqlalchemy as sa
from app.utils.security import hash_password
import uuid

# revision identifiers, used by Alembic
revision = '25d814bc83ed'  # Unique revision ID
down_revision = None  # No previous migration if this is the first migration
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create the 'users' table
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('nickname', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=True),
        sa.Column('last_name', sa.String(length=100), nullable=True),
        sa.Column('bio', sa.String(length=500), nullable=True),
        sa.Column('profile_picture_url', sa.String(length=255), nullable=True),
        sa.Column('linkedin_profile_url', sa.String(length=255), nullable=True),
        sa.Column('github_profile_url', sa.String(length=255), nullable=True),
        sa.Column('role', sa.Enum('ANONYMOUS', 'AUTHENTICATED', 'MANAGER', 'ADMIN', name='UserRole'), nullable=False),
        sa.Column('is_professional', sa.Boolean(), nullable=True),
        sa.Column('professional_status_updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('failed_login_attempts', sa.Integer(), nullable=True),
        sa.Column('is_locked', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('verification_token', sa.String(), nullable=True),
        sa.Column('email_verified', sa.Boolean(), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_nickname'), 'users', ['nickname'], unique=True)

    # Insert admin user
    hashed_password = hash_password("Admin1234!")  # Replace with your desired password
    op.execute(
        f"""
        INSERT INTO users (
            id,
            nickname,
            email,
            hashed_password,
            role,
            email_verified,
            created_at,
            updated_at
        ) VALUES (
            '{str(uuid.uuid4())}',
            'admin',
            'admin@example.com',
            '{hashed_password}',
            'ADMIN',
            TRUE,
            now(),
            now()
        )
        """
    )

def downgrade() -> None:
    op.drop_index(op.f('ix_users_nickname'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
