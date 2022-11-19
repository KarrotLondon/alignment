from pathlib import Path
from typing import List


def get_kinks() -> List[str]:
    with open(Path(__file__).with_name("kink-list.txt"), newline="") as f:
        return [k.rstrip("\n") for k in f.readlines()]
