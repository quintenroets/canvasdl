from canvasdl.ui.progressmanager import ProgressManager


def main():
    with ProgressManager():
        from . import starter  # noqa: autoimport

        starter.check_changes()


if __name__ == "__main__":
    main()
