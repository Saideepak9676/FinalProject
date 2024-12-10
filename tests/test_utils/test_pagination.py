import pytest
from starlette.requests import Request
from starlette.datastructures import URL, QueryParams
from app.utils.pagination import generate_pagination_links


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
