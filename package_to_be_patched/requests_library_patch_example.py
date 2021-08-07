from requests import Session, adapters


def requests_function():
    session = Session()
    adapter = adapters.HTTPAdapter(max_retries=3)
    URL = "https://jsonplaceholder.typicode.com/posts"
    session.mount(URL, adapter)

    body_request = {
        "title": "foo",
        "body": "bar",
        "userId": 1,
    }

    response = session.request("GET", URL, json=body_request)
    print(type(response))
    print(dir(response))
    from icecream import ic

    ic(response)
    return response


if __name__ == "__main__":
    print(requests_function())
