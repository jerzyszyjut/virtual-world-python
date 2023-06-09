class Position:
    pass


class PositionSquare:
    __x: int
    __y: int

    def __init__(self, x: int, y: int) -> None:
        self.__x = x
        self.__y = y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PositionSquare):
            return NotImplemented
        return self.__x == other.__x and self.__y == other.__y

    def __str__(self) -> str:
        return f"Position({self.__x}, {self.__y})"

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash((self.__x, self.__y))

    def __getitem__(self, item: int) -> int:
        return (self.__x, self.__y)[item]

    def __setitem__(self, key: int, value: int) -> None:
        if key == 0:
            self.__x = value
        elif key == 1:
            self.__y = value
        else:
            raise IndexError("Position has only 2 coordinates")

    def get_x(self) -> int:
        return self.__x

    def get_y(self) -> int:
        return self.__y

    def set_x(self, x: int) -> None:
        self.__x = x

    def set_y(self, y: int) -> None:
        self.__y = y

    def get(self) -> tuple[int, int]:
        return self.__x, self.__y

    def set(self, position: "PositionSquare") -> None:
        self.__x = position.get_x()
        self.__y = position.get_y()


class PositionHexagon:
    __q: int
    __r: int
    __s: int

    def __init__(self, q: int, r: int, s: int) -> None:
        self.__q = q
        self.__s = s
        self.__r = r

        self.validate()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PositionHexagon):
            return NotImplemented
        return self.__q == other.__q and self.__r == other.__r and self.__s == other.__s

    def __str__(self) -> str:
        return f"Position({self.__q}, {self.__r}, {self.__s})"

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash((self.__q, self.__r, self.__s))

    def __getitem__(self, item: int) -> int:
        return (self.__q, self.__r, self.__s)[item]

    def __setitem__(self, key: int, value: int) -> None:
        if key == 0:
            self.__q = value
        elif key == 1:
            self.__r = value
        elif key == 2:
            self.__s = value
        else:
            raise IndexError("Position has only 3 coordinates")

        self.validate()

    def validate(self) -> None:
        if self.__q + self.__r + self.__s != 0:
            raise ValueError("q + r + s must be 0")

    def get_q(self) -> int:
        return self.__q

    def get_r(self) -> int:
        return self.__r

    def get_s(self) -> int:
        return self.__s

    def set_q(self, q: int) -> None:
        self.__q = q
        self.validate()

    def set_r(self, r: int) -> None:
        self.__r = r
        self.validate()

    def set_s(self, s: int) -> None:
        self.__s = s
        self.validate()

    def get(self) -> tuple[int, int, int]:
        return self.__q, self.__r, self.__s

    def set(self, position: "PositionHexagon") -> None:
        self.__q = position.get_q()
        self.__r = position.get_r()
        self.__s = position.get_s()
        self.validate()

    def get_cube(self) -> tuple[int, int, int]:
        return self.__q, self.__r, self.__s

    def get_axial(self) -> tuple[int, int]:
        return self.__q, self.__r
