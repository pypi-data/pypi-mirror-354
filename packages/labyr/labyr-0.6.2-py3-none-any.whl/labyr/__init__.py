from typing import Any, Callable, Union

from icecream import ic as _ic

from .utils import color, getchar
from .utils.transform import get_map, transform

__all__ = ["labyr", "LabyrGame"]


def genlvls(
    chars: dict,
    lvlSizes: dict[int, tuple[int, int]],
):
    out = {}

    def init(dimen: tuple[int, int]) -> list[list[str]]:
        space = getchar(chars, "space")[0]
        x, y = dimen
        grid = [[space] * x for _ in range(y)]

        for i in range(x):
            for j in range(y):
                if i == 0 or i == x - 1 or j == 0 or j == y - 1:
                    grid[j][i] = "#"

        return grid

    for lvl, dimen in lvlSizes.items():
        out[lvl] = init(dimen)

    # lvl configs
    # out[lvl][y][x]

    # lvl 0 conf
    out[0][1][1] = getchar(chars, "player")[0]
    out[0][1][5] = getchar(chars, "exit")[0]

    return out


def cout_labyr(map: list[list[str]], chars: dict):
    chmap = get_map(chars)
    # dict(transform(["player", "exit", "wall", "space"], lambda arg: getch(chars, arg)))

    print("\n\n")
    for i in range(len(map)):
        for j in range(len(map[0])):
            cell = map[i][j]
            ch = cell[0]
            if ch != "$" and ch in chmap:
                print(chmap[ch](ch), end="")
            elif cell.startswith("$M"):  # e.g. str: "$M1" means monster #1
                print(chmap["M"]("M"), end="")
        print()


class LabyrGame:
    def __init__(self) -> None:
        c = color.C()
        self.clvl = 0
        self.chars = {
            "DEFAULTS": {
                "space": (".", c.dark_gray),
                "wall": ("#", c.dark_gray),
                "player": ("@", c.blue),
                "exit": ("E", c.green),
                "monster": ("M", c.red),
            },
            "space": (".", c.dark_gray),
            "wall": ("#", c.dark_gray),
            "player": ("@", c.blue),
            "exit": ("E", c.green),
            "monster": ("M", c.red),
        }
        lvlSizes = {0: (7, 3)}
        self.levels = genlvls(self.chars, lvlSizes)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        cout_labyr(self.levels[self.clvl], self.chars)


labyr = LabyrGame()
