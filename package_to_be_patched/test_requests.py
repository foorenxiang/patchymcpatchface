import sys
import os

sys.path.append(os.getcwd())
# import patchymcpatchface as pf

# import patch_package.request_patch

# pf.invoke_patch_hooks([patch_package.request_patch])


def test_requests(mocker):
    from requests.sessions import Session

    patch_request = lambda *args, **kwargs: {
        "title": "foo",
        "body": "bar",
        "userId": 1,
    }
    mocker.patch.object(Session, "request", patch_request)
    from package_to_be_patched.requests_library_patch_example import requests_function

    response = requests_function()
    # assert isinstance(response, dict)
    print(response)


if __name__ == "__main__":
    test_requests()
