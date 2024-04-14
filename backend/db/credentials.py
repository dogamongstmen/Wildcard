from io import TextIOWrapper
from os import getcwd


def get_db_credentials() -> str:
    handle: TextIOWrapper = open(f"{getcwd()}/db/db_cred.txt", "r")
    line = handle.readline()
    handle.close()
    return line
