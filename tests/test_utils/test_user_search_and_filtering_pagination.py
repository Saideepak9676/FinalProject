import pytest
from starlette.requests import Request
from starlette.datastructures import URL, QueryParams
from app.utils.pagination import generate_pagination_links
from urllib.parse import urlencode  # Importing urlencode for encoding query parameters


@pytest.mark.asyncio
async def test_generate_pagination_links():
    # Mock request object
    class MockRequest:
        def __init__(self, base_url):
            self.url = URL(base_url)
            self.query_params = QueryParams()  # Mimic the query_params attribute

        def url_for(self, *args, **kwargs):
            return str(self.url)

    request = MockRequest("http://localhost:8000/users")

    # Define input parameters
    skip = 0
    limit = 10
    total_users = 45  # Total number of users for testing

    # Generate pagination links
    links = generate_pagination_links(request, skip, limit, total_users)

    # Assert the structure and values of the links
    assert "next" in links
    assert "prev" in links
    assert "first" in links
    assert "last" in links

    # Assert correct link values
    assert links["next"] == "http://localhost:8000/users?skip=10&limit=10"
    assert links["prev"] is None  # No previous page at the start
    assert links["first"] == "http://localhost:8000/users?skip=0&limit=10"
    assert links["last"] == "http://localhost:8000/users?skip=40&limit=10"

    # Test a middle page
    skip = 20
    links = generate_pagination_links(request, skip, limit, total_users)
    assert links["prev"] == "http://localhost:8000/users?skip=10&limit=10"
    assert links["next"] == "http://localhost:8000/users?skip=30&limit=10"
    assert links["first"] == "http://localhost:8000/users?skip=0&limit=10"
    assert links["last"] == "http://localhost:8000/users?skip=40&limit=10"


@pytest.mark.asyncio
async def test_pagination_edge_cases():
    """
    Test edge cases for pagination utility.
    """
    class MockRequest:
        def __init__(self, base_url):
            self.url = URL(base_url)
            self.query_params = QueryParams()

    request = MockRequest("http://localhost:8000/users")
    
    # Case 1: Total items less than limit
    links = generate_pagination_links(request, skip=0, limit=10, total_items=5)
    assert links["next"] is None, "Next link should not exist"
    assert links["prev"] is None, "Previous link should not exist"

    # Case 2: Total items exactly a multiple of limit
    links = generate_pagination_links(request, skip=0, limit=10, total_items=20)
    assert links["last"] == "http://localhost:8000/users?skip=10&limit=10", "Last link is incorrect"


@pytest.mark.asyncio
async def test_pagination_boundary(async_client, admin_token):
    """
    Test the `/users` endpoint pagination boundaries.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}

    # Test with skip set to a very large number (beyond the total user count)
    query_params = {"skip": 10000, "limit": 10}
    response = await async_client.get(f"/users?{urlencode(query_params)}", headers=headers)
    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
    data = response.json()
    assert len(data["items"]) == 0, "Pagination with out-of-bound skip should return an empty list"

    # Test with skip set to 0 and limit set to 1 (minimum valid values)
    query_params = {"skip": 0, "limit": 1}
    response = await async_client.get(f"/users?{urlencode(query_params)}", headers=headers)
    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
    data = response.json()
    assert len(data["items"]) <= 1, "Pagination with minimal values should return up to 1 result"
