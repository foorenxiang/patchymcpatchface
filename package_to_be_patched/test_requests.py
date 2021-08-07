import sys
import os

sys.path.append(os.getcwd())
import patchymcpatchface as pf


def test_requests():
    class Session:
        def request(self, *args, **kwargs):
            print("I am the patched request!")
            return {
                "title": "foo",
                "body": "bar",
                "userId": 1,
            }

        mount = lambda *args, **kwargs: None

    pf.patch_apply(
        "package_to_be_patched.requests_library_patch_example.Session", Session
    )
    from package_to_be_patched.requests_library_patch_example import requests_function

    response = requests_function()
    print(response)

    assert isinstance(response, dict)


if __name__ == "__main__":
    test_requests()
