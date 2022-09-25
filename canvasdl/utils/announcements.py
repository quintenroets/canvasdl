from .path import Path


def get(course: str):
    root = Path.content_assets / "canvas" / "announ"
    course = course.replace("_", " ")
    for subfolder in root.iterdir():
        if subfolder.name.lower() == course:
            return load_announs(subfolder)


def load_announs(folder: Path):
    announs = [path.yaml for path in folder.iterdir()]
    announs = "<br><hr>".join(
        f"<h2><strong>{announ['title']}</strong><small>&ensp;&ensp;"
        f"{announ['created_at']}"
        f"</small></h2>{announ['message']}" for announ in announs
    )
    return announs
