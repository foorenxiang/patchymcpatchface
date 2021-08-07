"""Module to be patched"""
from requests import Session, adapters


def requests_function():
    """Request function to be patched"""
    session = Session()
    adapter = adapters.HTTPAdapter(max_retries=3)
    url = "https://jsonplaceholder.typicode.com/posts"
    session.mount(url, adapter)

    body_request = {
        "title": "foo",
        "body": "bar",
        "userId": 1,
    }

    response = session.request("GET", url, json=body_request)
    return response


if __name__ == "__main__":
    print(requests_function())
