class SilentUIHandle:
    def __getattr__(self, name):
        def method(*args, **kwargs):
            pass

        return method
