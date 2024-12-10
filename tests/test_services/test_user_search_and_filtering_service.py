from builtins import range
import pytest
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from app.dependencies import get_settings
from app.models.user_model import User, UserRole
from app.services.user_service import UserService
from app.utils.nickname_gen import generate_nickname
from datetime import datetime


pytestmark = pytest.mark.asyncio

@pytest.mark.asyncio
async def test_search_users_by_username(db_session, users_with_same_role_50_users):
    filters = {"username": "john"}
    users, total = await UserService.search_and_filter_users(db_session, filters, 0, 10)
    assert total > 0
    assert all("john" in user.nickname.lower() for user in users)

@pytest.mark.asyncio
async def test_filter_users_by_role(db_session, users_with_same_role_50_users):
    filters = {"role": UserRole.ADMIN.name}
    users, total = await UserService.search_and_filter_users(db_session, filters, 0, 10)
    assert total > 0
    assert all(user.role == UserRole.ADMIN for user in users)

@pytest.mark.asyncio
async def test_filter_users_by_account_status(db_session, users_with_same_role_50_users):
    filters = {"account_status": True}
    users, total = await UserService.search_and_filter_users(db_session, filters, 0, 10)
    assert total > 0
    assert all(user.email_verified for user in users)

@pytest.mark.asyncio
async def test_filter_users_by_registration_date(db_session, users_with_same_role_50_users):
    filters = {
        "registration_date_start": datetime(2023, 1, 1),
        "registration_date_end": datetime(2023, 12, 31)
    }
    users, total = await UserService.search_and_filter_users(db_session, filters, 0, 10)
    assert total > 0
    assert all(
        datetime(2023, 1, 1) <= user.created_at <= datetime(2023, 12, 31)
        for user in users
    )

@pytest.mark.asyncio
async def test_filter_users_by_email(db_session, users_with_same_role_50_users):
    """
    Test filtering users by email in the service layer.
    """
    filters = {"email": users_with_same_role_50_users[0].email}
    users, total = await UserService.search_and_filter_users(db_session, filters, 0, 10)
    
    assert len(users) == 1, f"Expected 1 user but got {len(users)}"
    assert users[0].email == users_with_same_role_50_users[0].email


@pytest.mark.asyncio
async def test_combination_of_filters(db_session, users_with_same_role_50_users):
    """
    Test combination of multiple filters.
    """
    filters = {
        "username": users_with_same_role_50_users[0].nickname,
        "role": "AUTHENTICATED",
        "account_status": False,
    }
    users, total = await UserService.search_and_filter_users(db_session, filters, 0, 10)

    assert len(users) == 1, f"Expected 1 user but got {len(users)}"
    assert users[0].nickname == users_with_same_role_50_users[0].nickname
    # Compare the role using the enum value to match the format
    assert users[0].role.value == "AUTHENTICATED"



@pytest.mark.asyncio
async def test_filter_users_case_insensitive(db_session, users_with_same_role_50_users):
    """
    Test case-insensitive filtering for username and email.
    """
    filters_username = {"username": users_with_same_role_50_users[0].nickname.upper()}
    users_by_username, _ = await UserService.search_and_filter_users(db_session, filters_username, 0, 10)
    
    assert len(users_by_username) == 1, "Case-insensitive username filter should match one user"
    assert users_by_username[0].nickname == users_with_same_role_50_users[0].nickname

    filters_email = {"email": users_with_same_role_50_users[0].email.upper()}
    users_by_email, _ = await UserService.search_and_filter_users(db_session, filters_email, 0, 10)
    
    assert len(users_by_email) == 1, "Case-insensitive email filter should match one user"
    assert users_by_email[0].email == users_with_same_role_50_users[0].email
