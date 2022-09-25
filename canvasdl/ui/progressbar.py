try:
    from .popup import Popup as ProgressBar

except ImportError:
    # no progress
    class ProgressBar:
        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            pass

        def __exit__(self, *_):
            pass

        def __getattr__(self, name):
            return self.empty

        def empty(self, *args, **kwargs):
            pass
