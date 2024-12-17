from builtins import repr
from datetime import datetime, timezone
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_model import User, UserRole

@pytest.mark.asyncio
async def test_user_role(session: AsyncSession, user: User):
    """
    Tests that the default role is assigned correctly and can be updated.
    """
    assert user.role == UserRole.AUTHENTICATED, "Default role should be USER"

@pytest.mark.asyncio
async def test_has_role(user: User, admin_user: User, manager_user: User):
    """
    Tests the has_role method to ensure it accurately checks the user's role.
    """
    assert user.has_role(UserRole.AUTHENTICATED), "User should have USER role"
    assert not user.has_role(UserRole.ADMIN), "User should not have ADMIN role"
    assert admin_user.has_role(UserRole.ADMIN), "Admin user should have ADMIN role"
    assert manager_user.has_role(UserRole.MANAGER), "Pro user should have PRO role"

@pytest.mark.asyncio
async def test_user_repr(user: User):
    """
    Tests the __repr__ method for accurate representation of the User object.
    """
    assert repr(user) == f"<User {user.nickname}, Role: {user.role.name}>", "__repr__ should include nickname and role"

@pytest.mark.asyncio
async def test_failed_login_attempts_increment(session: AsyncSession, user: User):
    """
    Tests that failed login attempts can be incremented and persisted correctly.
    """
    initial_attempts = user.failed_login_attempts
    user.failed_login_attempts += 1
    await session.commit()
    await session.refresh(user)
    assert user.failed_login_attempts == initial_attempts + 1, "Failed login attempts should increment"

@pytest.mark.asyncio
async def test_last_login_update(session: AsyncSession, user: User):
    """
    Tests updating the last login timestamp.
    """
    new_last_login = datetime.now()
    user.last_login_at = new_last_login
    await session.commit()
    await session.refresh(user)
    
    assert user.last_login_at.replace(tzinfo=None) == new_last_login.replace(tzinfo=None), "Last login timestamp should update correctly"

@pytest.mark.asyncio
async def test_account_lock_and_unlock(session: AsyncSession, user: User):
    """
    Tests locking and unlocking the user account.
    """
    # Initially, the account should not be locked.
    assert not user.is_locked, "Account should initially be unlocked"

    # Lock the account and verify.
    user.lock_account()
    await session.commit()
    await session.refresh(user)
    assert user.is_locked, "Account should be locked after calling lock_account()"

    # Unlock the account and verify.
    user.unlock_account()
    await session.commit()
    await session.refresh(user)
    assert not user.is_locked, "Account should be unlocked after calling unlock_account()"

@pytest.mark.asyncio
async def test_email_verification(session: AsyncSession, user: User):
    """
    Tests the email verification functionality.
    """
    # Initially, the email should not be verified.
    assert not user.email_verified, "Email should initially be unverified"

    # Verify the email and check.
    user.verify_email()
    await session.commit()
    await session.refresh(user)
    assert user.email_verified, "Email should be verified after calling verify_email()"

@pytest.mark.asyncio
async def test_user_profile_pic_url_update(session: AsyncSession, user: User):
    """
    Tests the profile pic update functionality.
    """
    # Initially, the profile pic should be updated.

    # Verify the email and check.
    profile_pic_url = "http://myprofile/picture.png"
    user.profile_picture_url = profile_pic_url
    await session.commit()
    await session.refresh(user)
    assert user.profile_picture_url == profile_pic_url, "The profile pic did not update"

@pytest.mark.asyncio
async def test_user_linkedin_url_update(session: AsyncSession, user: User):
    """
    Tests the profile pic update functionality.
    """
    # Initially, the linkedin should  be updated.

    # Verify the linkedin profile url.
    profile_linkedin_url = "http://www.linkedin.com/profile"
    user.linkedin_profile_url = profile_linkedin_url
    await session.commit()
    await session.refresh(user)
    assert user.linkedin_profile_url == profile_linkedin_url, "The profile pic did not update"


@pytest.mark.asyncio
async def test_user_github_url_update(session: AsyncSession, user: User):
    """
    Tests the profile pic update functionality.
    """
    # Initially, the linkedin should  be updated.

    # Verify the linkedin profile url.
    profile_github_url = "http://www.github.com/profile"
    user.github_profile_url = profile_github_url
    await session.commit()
    await session.refresh(user)
    assert user.github_profile_url == profile_github_url, "The github did not update"


@pytest.mark.asyncio
async def test_update_user_role(session: AsyncSession, user: User):
    """
    Tests updating the user's role and ensuring it persists correctly.
    """
    user.role = UserRole.ADMIN
    await session.commit()
    await session.refresh(user)
    assert user.role == UserRole.ADMIN, "Role update should persist correctly in the database"

@pytest.mark.asyncio
async def test_role_transition_to_manager(session, verified_user):
    """Test transitioning a user's role to manager"""
    verified_user.role = UserRole.MANAGER
    await session.commit()
    await session.refresh(verified_user)
    assert verified_user.role == UserRole.MANAGER

@pytest.mark.asyncio
async def test_role_transition_history(session, verified_user):
    """Test tracking role transition history"""
    original_role = verified_user.role
    verified_user.role = UserRole.MANAGER
    await session.commit()
    await session.refresh(verified_user)
    assert verified_user.role != original_role
