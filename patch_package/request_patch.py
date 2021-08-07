from patchymcpatchface import patch_apply


patch_request = lambda: {
    "title": "foo",
    "body": "bar",
    "userId": 1,
}


def patch_hook():  #  define this patch_hook (reserved function name) for patcher to pick up
    """Patch hook to be called by patchymcpatchface"""
    patch_apply(
        "requests.sessions.Session.request", patch_request
    )  #  put in the full module ancestry and the patch function as parameters
    print("patch_object invoked")
