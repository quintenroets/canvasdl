from . import announ, assignment, files, videos


def get_checkers():
    return (
        announ,
        assignment,
        files,
        videos,
    )
