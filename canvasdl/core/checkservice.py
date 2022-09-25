import time

from . import starter


def main():
    hours = 2
    seconds = hours * 60**2
    while True:
        time.sleep(seconds)
        starter.check_changes()


if __name__ == "__main__":
    main()
