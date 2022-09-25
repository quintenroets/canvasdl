from . import canvas, drive, edstem, gradescope, piazza, website


def get_checkers():
    return (
        *canvas.get_checkers(),
        drive,
        edstem,
        gradescope,
        piazza,
        website,
    )
