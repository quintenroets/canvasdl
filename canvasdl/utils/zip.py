from zipfile import ZipFile

from . import Path


def unzip(zip_path: Path):
    extract_folder = zip_path.with_suffix("")
    extract_folder.rmtree()
    with ZipFile(zip_path) as zip_file:
        zip_file.extractall(path=extract_folder)

    macosx_folder = extract_folder / "__MACOSX"
    if macosx_folder.exists():
        macosx_folder.rmtree()

    if len(list(extract_folder.iterdir())) == 1:
        subfolder: Path = next(extract_folder.iterdir())
        if subfolder.name == extract_folder.name:
            extract_folder_temp = extract_folder.with_suffix(".tmp")
            subfolder.rename(extract_folder_temp)
            extract_folder.rmdir()
            extract_folder_temp.rename(extract_folder)

    for path in extract_folder.find():
        path.tag = zip_path.tag
        path.mtime = zip_path.mtime

    zip_path.unlink()
