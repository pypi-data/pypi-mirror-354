from pathlib import Path
from typing import Any
import platform
import json
import sys
import os


def stringToList(string: str, content_type):
    string = string[1:-1]
    array = []
    for i in string.split(","):
        if i == "":
            continue
        else:
            array.append(content_type(i))
    return array


def getDataPath() -> str:
    if platform.system() == "Windows":
        return os.path.join(os.getenv("APPDATA"), "JakobDev", "jdNBTExplorer")
    elif platform.system() == "Darwin":
        return os.path.join(str(Path.home()),"Library", "Application Support", "JakobDev", "jdNBTExplorer")
    elif platform.system() == "Haiku":
        return os.path.join(str(Path.home()),"config", "settings", "JakobDev", "jdNBTExplorer")
    else:
        if os.getenv("XDG_DATA_HOME"):
            return os.path.join(os.getenv("XDG_DATA_HOME"), "JakobDev", "jdNBTExplorer")
        else:
            return os.path.join(str(Path.home()), ".local", "share", "JakobDev", "jdNBTExplorer")


def readJsonFile(path: str,default: Any) -> Any:
    """
    Tries to parse the given JSON file and prints a error if the file couldn't be parsed
    Returns default if the file is not found or couldn't be parsed
    """
    if os.path.isfile(path):
        try:
            with open(path,"r",encoding="utf-8") as f:
                data = json.load(f)
                return data
        except json.decoder.JSONDecodeError as e:
            print(f"Can't parse {os.path.basename(path)}: {e.msg}: line {e.lineno} column {e.colno} (char {e.pos})",file=sys.stderr)
            return default
        except Exception:
            print("Can't read " + os.path.basename(path),file=sys.stderr)
            return default
    else:
        return default
