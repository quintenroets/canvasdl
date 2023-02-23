import threading


class Threads:
    def __init__(self, target, args=(), kwargs=None):
        if callable(target):
            self.threads = [
                threading.Thread(target=target, args=arg, kwargs=kwargs or {})
                for arg in zip(*args)
            ]
        else:
            self.threads = [
                threading.Thread(target=t, args=args, kwargs=kwargs or {})
                for t in target
            ]

    def start(self):
        for t in self.threads:
            t.start()
        return self

    def join(self):
        for t in self.threads:
            t.join()
