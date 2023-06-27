def get_file_contents(filepath: str, defaultValue = ""):
    contents = defaultValue
    file = open(filepath, "r")
    try:
        contents = file.read()
    finally:
        file.close()

    return contents