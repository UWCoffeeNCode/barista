from typing import Union, List


def parse_bool(s: Union[str, None]) -> Union[bool, None]:
    if s is None:
        return None

    test = s.lower()
    if (test == "true") or (test == "t") or (test == "yes") or (test == "y"):
        return True
    if (test == "false") or (test == "f") or (test == "no") or (test == "n"):
        return False

    return None


def parse_list(s: Union[str, None]) -> Union[List[str], None]:
    if s is None:
        return None
    return s.split(",")
