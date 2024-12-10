from typing import Any, Dict
from urllib.parse import urlencode
from starlette.datastructures import URL


def generate_pagination_links(
    request: Any, skip: int, limit: int, total_items: int
) -> Dict[str, str]:
    """
    Generate pagination links for API responses.

    :param request: The request object to extract the base URL.
    :param skip: The current skip (offset) value.
    :param limit: The current limit (number of items per page).
    :param total_items: Total number of items available.
    :return: A dictionary containing 'next', 'prev', 'first', and 'last' links.
    """
    base_url = str(request.url).split("?")[0]
    query_params = dict(request.query_params)  # Convert to mutable dictionary

    # Calculate the next page link
    if skip + limit < total_items:
        query_params["skip"] = skip + limit
        query_params["limit"] = limit
        next_link = f"{base_url}?{urlencode(query_params)}"
    else:
        next_link = None

    # Calculate the previous page link
    if skip - limit >= 0:
        query_params["skip"] = max(skip - limit, 0)
        query_params["limit"] = limit
        prev_link = f"{base_url}?{urlencode(query_params)}"
    else:
        prev_link = None

    # Calculate the first page link
    query_params["skip"] = 0
    query_params["limit"] = limit
    first_link = f"{base_url}?{urlencode(query_params)}"

    # Calculate the last page link
    last_page_skip = (total_items - 1) // limit * limit
    query_params["skip"] = last_page_skip
    query_params["limit"] = limit
    last_link = f"{base_url}?{urlencode(query_params)}"

    return {
        "next": next_link,
        "prev": prev_link,
        "first": first_link,
        "last": last_link,
    }
