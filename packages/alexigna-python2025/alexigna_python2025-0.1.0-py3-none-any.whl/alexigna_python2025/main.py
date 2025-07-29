from io import StringIO
from typing import Any

import yaml


def dict_to_yaml(data: dict[str, Any]) -> str:
    s = StringIO()
    yaml.safe_dump(data, s)
    s.seek(0)
    return s.read()


if __name__ == "__main__":
    print(
        dict_to_yaml(
            {
                "a": 1,
                "b": 2,
                "c": [3, 4],
            }
        )
    )
