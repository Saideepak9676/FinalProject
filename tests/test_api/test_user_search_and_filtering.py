from builtins import str
import pytest
from httpx import AsyncClient
from app.main import app
from app.models.user_model import User, UserRole
from app.utils.nickname_gen import generate_nickname
from app.utils.security import hash_password
from app.services.jwt_service import decode_token  # Import your FastAPI app
from pydantic import ValidationError  # Import ValidationError
from app.services.user_service import UserService  # Import UserService
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
import json
from urllib.parse import urlencode
from sqlalchemy.exc import DBAPIError




@pytest.mark.asyncio
async def test_search_users_api(async_client, admin_token):
    """
    Test the `/users` endpoint with valid parameters.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    query_params = {
        "username": "john",
        "role": "ADMIN",
        "account_status": True,  # Boolean passed as expected by the API
    }

    response = await async_client.get(
        f"/users?{urlencode(query_params)}",
        headers=headers
    )

    # Debugging block to capture details in case of failure
    if response.status_code != 200:
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {response.headers}")
        try:
            print(f"Response content: {response.json()}")
        except Exception as e:
            print(f"Failed to parse JSON response: {e}")

    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"

    data = response.json()
    assert "items" in data, "Response should include 'items' key"
    assert isinstance(data["items"], list), "'items' should be a list"
    assert all("nickname" in user for user in data["items"]), "Each user should have a 'nickname'"
    assert all("email" in user for user in data["items"]), "Each user should have an 'email'"
    
    
    
@pytest.mark.asyncio
async def test_empty_filters_api(async_client, admin_token):
    """
    Test the `/users` endpoint with no filters provided.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    query_params = {}  # No filters applied

    response = await async_client.get(f"/users?{urlencode(query_params)}", headers=headers)
    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
    data = response.json()
    assert isinstance(data["items"], list), "Response items should be a list"
    assert data["total"] > 0, "Response should return at least one user"

@pytest.mark.asyncio
async def test_fetch_all_users(async_client, admin_token):
    """
    Test the `/users` endpoint with no filters to fetch all users.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    query_params = {"skip": 0, "limit": 10}  # Basic pagination parameters

    response = await async_client.get(f"/users?{urlencode(query_params)}", headers=headers)

    # Assert the API response
    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
    data = response.json()
    assert "items" in data, "Response should include an 'items' key"
    assert isinstance(data["items"], list), "'items' should be a list"
    assert data["total"] >= 0, "Total users count should be a non-negative integer"


@pytest.mark.asyncio
async def test_search_users_pagination(async_client, admin_token):
    """
    Test the `/users` endpoint with pagination parameters.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    query_params = {"skip": 0, "limit": 5}  # Test fetching the first 5 users

    response = await async_client.get(f"/users?{urlencode(query_params)}", headers=headers)

    # Assert the response
    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
    data = response.json()

    assert "items" in data, "Response should include an 'items' key"
    assert isinstance(data["items"], list), "'items' should be a list"
    assert len(data["items"]) <= 5, "Number of users in the response should not exceed the limit"
    assert data["total"] >= len(data["items"]), "Total users should be greater or equal to the returned items"

    # Test the next page
    query_params = {"skip": 5, "limit": 5}  # Test fetching the next 5 users
    response = await async_client.get(f"/users?{urlencode(query_params)}", headers=headers)

    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
    data = response.json()

    assert "items" in data, "Response should include an 'items' key"
    assert isinstance(data["items"], list), "'items' should be a list"
    assert len(data["items"]) <= 5, "Number of users in the response should not exceed the limit"


