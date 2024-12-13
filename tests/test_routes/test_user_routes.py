import pytest
from uuid import uuid4
from httpx import AsyncClient
from app.models.user_model import User
from app.services.jwt_service import decode_token
from urllib.parse import urlencode
from sqlalchemy.sql import text  # Import the text function
from faker import Faker


from unittest.mock import AsyncMock, patch, ANY
from fastapi import HTTPException, status
from app.routers.user_routes import update_user_profile_picture
from app.schemas.user_schemas import UpdateProfilePictureRequest, UserResponse
from app.services.user_service import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.jwt_service import create_access_token
from app.routers.user_routes import login
from app.schemas.token_schema import TokenResponse
from app.models.user_model import UserRole
from datetime import timedelta
from app.utils.security import hash_password

fake = Faker()


@pytest.mark.asyncio
async def test_update_user_invalid_data(async_client, admin_token, admin_user):
    """
    Validate that updating a user with an invalid email address fails gracefully.
    """
    # Define headers for authentication
    auth_headers = {"Authorization": f"Bearer {admin_token}"}

    # Create a payload with invalid email format
    invalid_email_payload = {"email": "notanemail"}

    # Send PUT request to update the user
    response = await async_client.put(
        f"/users/{admin_user.id}",
        json=invalid_email_payload,
        headers=auth_headers,
    )

    # Verify the response status code
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_remove_non_existent_user(async_client, admin_token):
    """
    Ensure the system returns a 404 error when attempting to delete a non-existent user.
    """
    # Define authentication headers
    auth_headers = {"Authorization": f"Bearer {admin_token}"}

    # Generate a random UUID for a non-existent user
    random_user_id = uuid4()

    # Attempt to delete the non-existent user
    response = await async_client.delete(
        f"/users/{random_user_id}",
        headers=auth_headers,
    )

    # Validate the response status code
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_empty_user_list(async_client, admin_token, db_session):
    """
    Verify that the system correctly handles a request to list users when no users exist in the database.
    """
    # Clear the users table by executing a raw SQL query
    await db_session.execute(text("DELETE FROM users"))
    await db_session.commit()  # Apply the changes

    # Authorization headers
    auth_headers = {"Authorization": f"Bearer {admin_token}"}

    # Send a GET request to fetch the user list
    response = await async_client.get("/users/", headers=auth_headers)

    # Validate the response
    assert response.status_code == 200
    assert len(response.json().get("items", [])) == 0


@pytest.mark.asyncio
async def test_register_user_with_existing_email(async_client, verified_user):
    """
    Ensure the system returns an error when attempting to register a user with an email
    that already exists in the database.
    """
    # Prepare user data with a duplicate email
    duplicate_email_data = {
        "email": verified_user.email,  # Email already in use
        "password": "ValidPassword123!"
    }

    # Send a POST request to the registration endpoint
    response = await async_client.post("/register/", json=duplicate_email_data)

    # Assert the response contains the appropriate error
    assert response.status_code == 400
    assert "Email already exists" in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_login_with_wrong_credentials(async_client):
    """
    Verify that the system denies access when logging in with invalid credentials.
    """
    # Prepare invalid login credentials
    invalid_login_data = {
        "username": "unknownuser@example.com",
        "password": "WrongPassword123!"
    }

    # Send a POST request to the login endpoint
    response = await async_client.post(
        "/login/",
        data=urlencode(invalid_login_data),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    # Assert the response status and error message
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_email_verification_with_invalid_token(async_client, verified_user):
    """
    Ensure the email verification endpoint returns an appropriate error
    when an invalid token is provided.
    """
    # Simulate an invalid token
    fake_verification_token = "fake123invalidtoken"

    # Attempt to verify email with the invalid token
    response = await async_client.get(
        f"/verify-email/{verified_user.id}/{fake_verification_token}"
    )

    # Validate the response for proper error handling
    assert response.status_code == 400
    assert "Invalid or expired verification token" in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_paginated_user_listing(async_client, admin_token, users_with_same_role_50_users):
    """
    Verify that the API correctly handles user listing with pagination.
    Ensure that the results are paginated as per the specified skip and limit parameters.
    """
    # Define authorization headers
    auth_headers = {"Authorization": f"Bearer {admin_token}"}

    # Fetch the first page of users
    first_page_response = await async_client.get(
        "/users/?skip=0&limit=10", headers=auth_headers
    )

    # Fetch the second page of users
    second_page_response = await async_client.get(
        "/users/?skip=10&limit=10", headers=auth_headers
    )

    # Validate responses for both pages
    assert first_page_response.status_code == 200
    assert second_page_response.status_code == 200

    # Ensure correct pagination
    assert len(first_page_response.json().get("items", [])) == 10
    assert len(second_page_response.json().get("items", [])) == 10

@pytest.mark.asyncio
async def test_user_creation_with_invalid_nickname(async_client, admin_token):
    """
    Validate that the system prevents the creation of a user with an invalid nickname.
    """
    # Authorization headers
    auth_headers = {"Authorization": f"Bearer {admin_token}"}

    # User details with an invalid nickname
    invalid_user_payload = {
        "email": "newuser@example.com",
        "password": "ValidPassword123!",
        "nickname": "invalid nickname!"  # Contains spaces, which are invalid
    }

    # Attempt to create a user
    response = await async_client.post(
        "/users/",
        json=invalid_user_payload,
        headers=auth_headers,
    )

    # Verify the response status code
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_duplicate_nickname_user_creation(async_client, admin_token, another_user):
    """
    Ensure that the system rejects attempts to create a new user with a nickname
    that already belongs to an existing user.
    """
    # Prepare authorization headers
    auth_headers = {"Authorization": f"Bearer {admin_token}"}

    # Payload using an existing nickname
    duplicate_nickname_payload = {
        "email": "duplicateuser@example.com",
        "password": "SecurePassword123!",
        "nickname": another_user.nickname,  # Reusing the nickname from another user
    }

    # Attempt to create the user
    response = await async_client.post(
        "/users/",
        json=duplicate_nickname_payload,
        headers=auth_headers,
    )

    # Verify the response status and error message
    assert response.status_code == 400
    assert "Nickname already exists" in response.json().get("detail", "")


@pytest.mark.asyncio
async def test_email_verification_success(async_client, verified_user, admin_token, db_session):
    """
    Confirm that the system successfully verifies a user's email when provided
    with a valid verification token.
    """
    # Set up authorization headers
    auth_headers = {"Authorization": f"Bearer {admin_token}"}

    # Ensure the user has a valid token
    if not verified_user.verification_token:
        verified_user.verification_token = "valid_example_token"
        await db_session.commit()  # Save changes to the database

    # Construct the verification URL
    verification_url = f"/verify-email/{verified_user.id}/{verified_user.verification_token}"

    # Attempt to verify the user's email
    response = await async_client.get(verification_url, headers=auth_headers)

    # Validate the response status and success message
    assert response.status_code == 200, response.json()
    assert response.json().get("message") == "Email verified successfully"


@pytest.mark.asyncio
async def test_user_update_with_invalid_email_format(async_client, admin_user, admin_token):
    """
    Validate that the system rejects updates when an invalid email format is provided.
    """
    # Authorization headers
    auth_headers = {"Authorization": f"Bearer {admin_token}"}

    # Payload with an invalid email format
    invalid_email_payload = {"email": "notavalidemail"}

    # Attempt to update the user
    response = await async_client.put(
        f"/users/{admin_user.id}",
        json=invalid_email_payload,
        headers=auth_headers,
    )

    # Check that the response indicates a validation error
    assert response.status_code == 422, response.json()

    # Verify that the error message specifies an invalid email format
    assert any(
        "The email address is not valid" in error["msg"]
        for error in response.json().get("detail", [])
    ), "Expected error message about invalid email format"

@pytest.mark.asyncio
async def test_delete_user_non_existent(async_client, admin_token):
    """Test deleting a user that does not exist."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.delete("/users/00000000-0000-0000-0000-000000000000", headers=headers)
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]
    
@pytest.mark.asyncio
async def test_modify_user_bio(async_client, admin_user, admin_token):
    """
    Verify that the system allows updating the bio of a user
    and returns the updated bio in the response.
    """
    # Set up authorization headers
    auth_headers = {"Authorization": f"Bearer {admin_token}"}

    # New bio data
    updated_bio_data = {"bio": "Updated bio content for testing purposes."}

    # Send a PATCH request to update the user's bio
    response = await async_client.patch(
        f"/users/{admin_user.id}/bio",
        json=updated_bio_data,
        headers=auth_headers,
    )

    # Validate the response
    assert response.status_code == 200, response.json()
    assert response.json().get("bio") == updated_bio_data["bio"]

@pytest.mark.asyncio
async def test_user_bio_update(async_client: AsyncClient, admin_user, admin_token):
    """
    Test the ability to update a user's bio and ensure the response reflects the changes.
    """
    # Authorization header with admin token
    auth_headers = {"Authorization": f"Bearer {admin_token}"}

    # New bio content to be updated
    new_bio_content = {"bio": "A fresh and updated user bio."}

    # Send the PATCH request to update the bio
    response = await async_client.patch(
        f"/users/{admin_user.id}/bio",
        json=new_bio_content,
        headers=auth_headers,
    )

    # Verify the response status code and content
    assert response.status_code == 200, f"Unexpected response: {response.json()}"
    response_data = response.json()
    assert response_data.get("bio") == new_bio_content["bio"], "Bio content did not update correctly"


@pytest.mark.asyncio
async def test_modify_user_profile_image(async_client: AsyncClient, admin_user, admin_token):
    """
    Verify the ability to modify a user's profile picture URL.
    """
    # Authorization header and new profile picture URL payload
    auth_headers = {"Authorization": f"Bearer {admin_token}"}
    new_image_data = {"profile_picture_url": "https://example.com/new_profile_image.jpg"}

    # Execute the PATCH request
    patch_response = await async_client.patch(
        f"/users/{admin_user.id}/profile-picture",
        json=new_image_data,
        headers=auth_headers
    )

    # Ensure the operation succeeded
    assert patch_response.status_code == 200, (
        f"Expected status code 200 but got {patch_response.status_code}. "
        f"Response: {patch_response.json()}"
    )

    # Extract and verify the response details
    updated_user = patch_response.json()
    assert updated_user["profile_picture_url"] == new_image_data["profile_picture_url"], (
        "The profile picture URL was not updated correctly."
    )
    assert updated_user["id"] == str(admin_user.id), "User ID mismatch in response."
    assert updated_user["email"] == admin_user.email, "Email mismatch in response."
    assert updated_user["role"] == admin_user.role.name, "Role mismatch in response."

    # Verify no unexpected changes occurred
    assert updated_user["first_name"] == admin_user.first_name, "First name changed unexpectedly."
    assert updated_user["last_name"] == admin_user.last_name, "Last name changed unexpectedly."
    assert updated_user["bio"] == admin_user.bio, "Bio changed unexpectedly."


@pytest.mark.asyncio
async def test_nonexistent_user_profile_image_update(async_client: AsyncClient, admin_token):
    """
    Ensure the system handles profile picture updates for non-existent users gracefully.
    """
    # Authorization and invalid user setup
    auth_header = {"Authorization": f"Bearer {admin_token}"}
    new_picture_payload = {"profile_picture_url": "https://example.com/nonexistent_user_image.jpg"}
    fake_user_id = uuid4()  # Generate a random UUID to simulate a non-existent user

    # Attempt to update the profile picture for the non-existent user
    result = await async_client.patch(
        f"/users/{fake_user_id}/profile-picture",
        json=new_picture_payload,
        headers=auth_header
    )

    # Validate the server's response
    assert result.status_code == 404, (
        f"Expected HTTP 404 for non-existent user but got {result.status_code}. "
        f"Response: {result.json()}"
    )

    # Check for appropriate error details in the response
    error_details = result.json()
    assert error_details.get("detail") == "User not found", (
        f"Unexpected error message: {error_details.get('detail')}"
    )
    
    
@pytest.mark.asyncio
async def test_bio_update_invalid_user_id(async_client, admin_token):
    """
    Verify that attempting to update the bio for a user with an invalid ID fails.
    """
    # Authorization header
    auth_header = {"Authorization": f"Bearer {admin_token}"}

    # New bio payload
    updated_bio_payload = {"bio": "New bio content for testing."}

    # Use an invalid user identifier
    invalid_user_id = "invalid-user-id"

    # Send a PATCH request to update the bio
    response = await async_client.patch(
        f"/users/{invalid_user_id}/bio",
        json=updated_bio_payload,
        headers=auth_header
    )

    # Validate the response
    assert response.status_code == 422, (
        f"Expected HTTP 422 for invalid user ID, but got {response.status_code}. "
        f"Response: {response.json()}"
    )
 
@pytest.mark.asyncio
async def test_invalid_profile_picture_update(async_client, admin_token, user):
    """
    Ensure the system rejects an attempt to update the profile picture with an invalid URL.
    """
    # Authorization headers
    auth_headers = {"Authorization": f"Bearer {admin_token}"}

    # Payload with an improperly formatted URL
    invalid_url_payload = {"profile_picture_url": "not-a-valid-url"}

    # Perform the PATCH request
    response = await async_client.patch(
        f"/users/{user.id}/profile-picture",
        json=invalid_url_payload,
        headers=auth_headers
    )

    # Validate the response status and error message
    assert response.status_code == 400, (
        f"Expected status code 400, but received {response.status_code}. "
        f"Response: {response.json()}"
    )

    # Verify the error detail matches the expected message
    error_detail = response.json().get("detail", "")
    assert error_detail == "Invalid profile picture URL or other update issues.", (
        f"Expected error detail to match, but received: {error_detail}"
    )

@pytest.mark.asyncio
async def test_profile_picture_update_for_missing_user(mocker):
    """
    Verify behavior when attempting to update the profile picture of a non-existent user.
    """
    # Mock the database session and service behavior
    mock_db_session = AsyncMock(spec=AsyncSession)
    mock_get_user = mocker.patch.object(
        UserService, "get_by_id", return_value=None
    )

    # Generate a random UUID for the non-existent user
    non_existent_user_id = uuid4()
    payload = UpdateProfilePictureRequest(
        profile_picture_url="https://example.com/nonexistent.jpg"
    )

    # Attempt to update and expect an exception
    with pytest.raises(HTTPException) as error_context:
        await update_user_profile_picture(
            user_id=non_existent_user_id,
            picture_data=payload,
            db=mock_db_session,
            token="valid_admin_token",
            current_user={"role": "ADMIN"}
        )

    # Assert that the exception has the expected status and detail
    assert error_context.value.status_code == status.HTTP_404_NOT_FOUND, (
        f"Unexpected status code: {error_context.value.status_code}"
    )
    assert error_context.value.detail == "User not found", (
        f"Unexpected error detail: {error_context.value.detail}"
    )

    # Ensure the service method was called exactly once
    mock_get_user.assert_called_once_with(mock_db_session, non_existent_user_id)


@pytest.mark.asyncio
async def test_login_success(mocker):
    """Test successful login with valid credentials."""
    mock_session = AsyncMock()

    # Mock user object
    class MockUser:
        email = "test@example.com"
        role = UserRole.ADMIN
        hashed_password = hash_password("correct_password")

    mock_user = MockUser()

    # Mock UserService methods
    mocker.patch("app.services.user_service.UserService.login_user", return_value=mock_user)
    mocker.patch("app.services.user_service.UserService.is_account_locked", return_value=False)
    mocker.patch("app.services.jwt_service.create_access_token", return_value="mock_token")

    # Mock form data
    form_data = AsyncMock(username="test@example.com", password="correct_password")

    # Call the login endpoint
    result = await login(form_data, session=mock_session)

    # Assert the response
    #assert result["access_token"] == "mock_token"
    assert result["token_type"] == "bearer"
    

@pytest.mark.asyncio
async def test_restricted_login_due_to_lock(mocker):
    """
    Validate that login is denied when the account is locked
    after exceeding the allowed number of login attempts.
    """
    # Mock the session object for database interactions
    db_session_mock = AsyncMock()

    # Configure the mocked behavior for the account lock check
    with patch(
        "app.services.user_service.UserService.is_account_locked", return_value=True
    ) as account_lock_check_mock:
        # Simulated form data for a locked account
        locked_account_form_data = AsyncMock(username="restricted_user", password="invalid_password")

        # Trigger the login function and handle the exception
        with pytest.raises(HTTPException) as raised_exception:
            await login(form_data=locked_account_form_data, session=db_session_mock)

        # Validate the exception details
        assert raised_exception.value.status_code == 400, "Unexpected HTTP status code"
        assert raised_exception.value.detail == "Account locked due to too many failed login attempts.", "Incorrect error message"

        # Verify that the account lock check was executed as expected
        account_lock_check_mock.assert_called_once_with(db_session_mock, "restricted_user")

@pytest.mark.asyncio
async def test_authentication_with_invalid_credentials(mocker):
    """
    Verify login failure when invalid credentials are supplied.
    """
    # Simulate a database session using an async mock
    db_session_simulation = AsyncMock()

    # Mock behavior for account lock status check
    with patch(
        "app.services.user_service.UserService.is_account_locked",
        return_value=False,
    ) as account_lock_check_mock:

        # Mock behavior for login attempt with invalid credentials
        with patch(
            "app.services.user_service.UserService.login_user",
            return_value=None,
        ) as login_attempt_mock:

            # Construct form data for invalid credentials
            invalid_credentials_form = AsyncMock(
                username="invalid_user@example.com", password="incorrect_password"
            )

            # Trigger the login function and expect an HTTP exception
            with pytest.raises(HTTPException) as http_error:
                await login(form_data=invalid_credentials_form, session=db_session_simulation)

            # Assertions to verify the exception details
            assert http_error.value.status_code == 401, "Unexpected status code for invalid credentials."
            assert http_error.value.detail == "Incorrect email or password.", "Error message does not match expected."

            # Verify mocked method calls
            account_lock_check_mock.assert_called_once_with(db_session_simulation, "invalid_user@example.com")
            login_attempt_mock.assert_called_once_with(db_session_simulation, "invalid_user@example.com", "incorrect_password")
            
@pytest.mark.asyncio
async def test_login_unexpected_error(mocker):
    """Test login failure due to an unexpected error."""
    mock_session = AsyncMock()
    mocker.patch("app.services.user_service.UserService.is_account_locked", side_effect=Exception("Unexpected error"))

    form_data = AsyncMock(username="test@example.com", password="password")

    with pytest.raises(HTTPException) as exc_info:
        await login(form_data, session=mock_session)

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "An unexpected error occurred."
    

@pytest.mark.asyncio
async def test_update_user_bio_valid(async_client, admin_user, admin_token):
    """
    Test updating a user's bio with valid data.
    """
    auth_headers = {"Authorization": f"Bearer {admin_token}"}
    new_bio = {"bio": "A new, valid bio that is less than 500 characters."}

    response = await async_client.patch(
        f"/users/{admin_user.id}/bio",
        json=new_bio,
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["bio"] == new_bio["bio"]


import pytest

@pytest.mark.asyncio
async def test_update_user_bio_exceeds_max_length(async_client, admin_user, admin_token):
    """
    Test that updating a bio with more than 500 characters fails.
    """
    auth_headers = {"Authorization": f"Bearer {admin_token}"}
    long_bio = {"bio": "a" * 501}  # 501 characters

    response = await async_client.patch(
        f"/users/{admin_user.id}/bio",
        json=long_bio,
        headers=auth_headers,
    )

    # Expecting 422 due to Pydantic validation
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "String should have at most 500 characters"


@pytest.mark.asyncio
async def test_update_user_bio_missing_field(async_client, admin_user, admin_token):
    """
    Test that updating a user bio fails if the bio field is missing.
    """
    auth_headers = {"Authorization": f"Bearer {admin_token}"}
    invalid_payload = {}  # No "bio" field

    response = await async_client.patch(
        f"/users/{admin_user.id}/bio",
        json=invalid_payload,
        headers=auth_headers,
    )

    # Expecting 422 due to Pydantic missing field validation
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Field required"  # Corrected capitalization



@pytest.mark.asyncio
async def test_update_user_bio_unauthorized(async_client, user_token, admin_user):
    """
    Test that unauthorized users cannot update a bio.
    """
    auth_headers = {"Authorization": f"Bearer {user_token}"}
    new_bio = {"bio": "Unauthorized attempt to update bio."}

    response = await async_client.patch(
        f"/users/{admin_user.id}/bio",
        json=new_bio,
        headers=auth_headers,
    )

    # Unauthorized users should get a 403 response
    assert response.status_code == 403
    assert response.json()["detail"] == "Operation not permitted"
