import sys
import os

sys.path.append(os.getcwd())

import patchymcpatchface as pf


def test_requests_target_ancestor():
    def request_inner():
        print("I am the patched request!")
        return {
            "title": "I",
            "body": "am",
            "userId": 42,
        }

    pf.patch_apply(
        "package_to_be_patched.request_call.Session.request",
        lambda *args, **kwargs: request_inner(),
    )
    from package_to_be_patched.request_call import requests_function

    response = requests_function()
    print(response)

    assert isinstance(response, dict)


def test_requests_target_object():
    def request_inner():
        print("I am the patched request!")
        return {
            "title": "I",
            "body": "am",
            "userId": 42,
        }

    from package_to_be_patched.request_call import requests_function, Session

    pf.patch_apply(
        (Session, "request"),
        lambda *args, **kwargs: request_inner(),
    )

    response = requests_function()
    print(response)

    assert isinstance(response, dict)
