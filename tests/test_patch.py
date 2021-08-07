"""Tests for patchymcpatchface"""
from patching_example import patching_example


def test_main():
    """Run sample as test, as it is inherently self testing"""

    patching_example.main()


def test_requests_target_ancestor():
    """Test patch on requests by targeting ancestry"""
    import patchymcpatchface as pf

    def request_inner():
        print("I am the patched request!")
        return {
            "title": "I",
            "body": "am",
            "userId": 42,
        }

    pf.patch_apply(
        "patching_example.mypackage.request_call.Session.request",
        lambda *args, **kwargs: request_inner(),
    )
    from patching_example.mypackage.request_call import requests_function

    response = requests_function()
    print(response)

    assert isinstance(response, dict)


def test_requests_target_object():
    """Test patch on requests by targeting imported object"""
    import patchymcpatchface as pf

    def request_inner():
        print("I am the patched request!")
        return {
            "title": "I",
            "body": "am",
            "userId": 42,
        }

    from patching_example.mypackage.request_call import requests_function, Session

    pf.patch_apply(
        (Session, "request"),
        lambda *args, **kwargs: request_inner(),
    )

    response = requests_function()
    print(response)

    assert isinstance(response, dict)
