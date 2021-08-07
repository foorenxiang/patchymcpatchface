class Session:
    def request(self, *args, **kwargs):
        print("I am the patched request!")
        return {
            "title": "foo",
            "body": "bar",
            "userId": 1,
        }
