from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("spritely")
except PackageNotFoundError:
    pass


def hello_world():
    return "hello world"
