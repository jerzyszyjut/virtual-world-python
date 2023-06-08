class Position:
    __x: int
    __y: int

    def __init__(self, x: int, y: int) -> None:
        self.__x = x
        self.__y = y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Position):
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

    def set(self, position: "Position") -> None:
        self.__x = position.get_x()
        self.__y = position.get_y()
