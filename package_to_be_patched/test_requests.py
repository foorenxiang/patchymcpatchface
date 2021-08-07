import patchymcpatchface as pf


def test_requests():
    def request_inner():
        print("I am the patched request!")
        return {
            "title": "I",
            "body": "am",
            "userId": 42,
        }

    pf.patch_apply(
        "package_to_be_patched.requests_library_patch_example.Session.request",
        lambda: request_inner(),
    )
    from package_to_be_patched.requests_library_patch_example import requests_function

    response = requests_function()
    print(response)

    assert isinstance(response, dict)


if __name__ == "__main__":
    test_requests()
