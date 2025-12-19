import random
from time import sleep
from tkinter import BOTH, Canvas, Tk


class Window:
    def __init__(self, width: int, height: int):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(height=height, width=width)
        self.__canvas.pack()
        self.running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, line, fill_color: str = "black"):
        line.draw(self.__canvas, fill_color)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1: Point, p2: Point):
        self.__p1 = p1
        self.__p2 = p2

    def draw(self, canvas: Canvas, fill_color: str):
        x1, y1 = self.__p1.x, self.__p1.y
        x2, y2 = self.__p2.x, self.__p2.y

        canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=2)


class Cell:
    def __init__(self, win: Window | None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.__win = win
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

        if self.__win is None:
            return

        if self.has_left_wall:
            p1 = Point(x1, y1)
            p2 = Point(x1, y2)
            line = Line(p1, p2)
            self.__win.draw_line(line)
        else:
            p1 = Point(x1, y1)
            p2 = Point(x1, y2)
            line = Line(p1, p2)
            self.__win.draw_line(line, "#d9d9d9")
        if self.has_top_wall:
            p1 = Point(x1, y1)
            p2 = Point(x2, y1)
            line = Line(p1, p2)
            self.__win.draw_line(line)
        else:
            p1 = Point(x1, y1)
            p2 = Point(x2, y1)
            line = Line(p1, p2)
            self.__win.draw_line(line, "#d9d9d9")
        if self.has_right_wall:
            p1 = Point(x2, y1)
            p2 = Point(x2, y2)
            line = Line(p1, p2)
            self.__win.draw_line(line)
        else:
            p1 = Point(x2, y1)
            p2 = Point(x2, y2)
            line = Line(p1, p2)
            self.__win.draw_line(line, "#d9d9d9")
        if self.has_bottom_wall:
            p1 = Point(x2, y2)
            p2 = Point(x1, y2)
            line = Line(p1, p2)
            self.__win.draw_line(line)
        else:
            p1 = Point(x2, y2)
            p2 = Point(x1, y2)
            line = Line(p1, p2)
            self.__win.draw_line(line, "#d9d9d9")

    def draw_move(self, to_cell, undo=False):
        if self.__win is None:
            return
        fill_color = "gray" if undo else "red"
        x1 = ((self.__x2 - self.__x1) / 2) + self.__x1
        y1 = ((self.__y2 - self.__y1) / 2) + self.__y1
        x2 = ((to_cell.__x2 - to_cell.__x1) / 2) + to_cell.__x1
        y2 = ((to_cell.__y2 - to_cell.__y1) / 2) + to_cell.__y1
        p1 = Point(x1, y1)
        p2 = Point(x2, y2)
        line = Line(p1, p2)
        self.__win.draw_line(line, fill_color)


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win: Window | None = None,
        seed=None,
    ):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells: list[list[Cell]] = []
        if seed is not None:
            random.seed(seed)
        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()

    def __create_cells(self):
        for _ in range(self.__num_cols):
            col: list[Cell] = []
            for _ in range(self.__num_rows):
                col.append(Cell(self.__win))
            self.__cells.append(col)
        if self.__win is not None:
            for i in range(self.__num_cols):
                for j in range(self.__num_rows):
                    self.__draw_cell(i, j)

    def __draw_cell(self, i, j):
        if self.__win is None:
            return
        x1 = self.__x1 + i * self.__cell_size_x
        y1 = self.__y1 + j * self.__cell_size_y
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y
        self.__cells[i][j].draw(x1, y1, x2, y2)
        self.__animate()

    def __animate(self):
        if self.__win is None:
            return
        self.__win.redraw()
        sleep(0.02)

    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0, 0)
        self.__cells[-1][-1].has_bottom_wall = False
        self.__draw_cell(len(self.__cells) - 1, len(self.__cells[0]) - 1)

    def __break_walls_r(self, i, j):
        self.__cells[i][j].visited = True
        while True:
            unvisited = []
            if i + 1 < self.__num_cols:
                if not self.__cells[i + 1][j].visited:
                    unvisited.append((i + 1, j))
            if j + 1 < self.__num_rows:
                if not self.__cells[i][j + 1].visited:
                    unvisited.append((i, j + 1))
            if i - 1 >= 0:
                if not self.__cells[i - 1][j].visited:
                    unvisited.append((i - 1, j))
            if j - 1 >= 0:
                if not self.__cells[i][j - 1].visited:
                    unvisited.append((i, j - 1))

            if len(unvisited) == 0:
                self.__draw_cell(i, j)
                return

            idx = random.randint(0, len(unvisited) - 1)
            x, y = unvisited[idx]

            if x == i + 1:
                self.__cells[i][j].has_right_wall = False
                self.__cells[x][y].has_left_wall = False
            elif y == j + 1:
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[x][y].has_top_wall = False
            elif x == i - 1:
                self.__cells[i][j].has_left_wall = False
                self.__cells[x][y].has_right_wall = False
            elif y == j - 1:
                self.__cells[i][j].has_top_wall = False
                self.__cells[x][y].has_bottom_wall = False

            self.__break_walls_r(x, y)

    def __reset_cells_visited(self):
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__cells[i][j].visited = False

    def solve(self, algo="dfs") -> bool:
        return self.__solve_r(algo=algo)

    def __solve_r(self, i=0, j=0, algo="dfs") -> bool:
        self.__animate()
        self.__cells[i][j].visited = True
        if i == len(self.__cells) - 1 and j == len(self.__cells[0]) - 1:
            return True

        unvisited = []
        while True:
            if (
                i + 1 < self.__num_cols
                and not self.__cells[i + 1][j].visited
                and not self.__cells[i + 1][j].has_left_wall
                and not self.__cells[i][j].has_right_wall
            ):
                unvisited.append((i + 1, j))
            if (
                j + 1 < self.__num_rows
                and not self.__cells[i][j + 1].visited
                and not self.__cells[i][j + 1].has_top_wall
                and not self.__cells[i][j].has_bottom_wall
            ):
                unvisited.append((i, j + 1))
            if (
                i - 1 >= 0
                and not self.__cells[i - 1][j].visited
                and not self.__cells[i - 1][j].has_right_wall
                and not self.__cells[i][j].has_left_wall
            ):
                unvisited.append((i - 1, j))
            if (
                j - 1 >= 0
                and not self.__cells[i][j - 1].visited
                and not self.__cells[i][j - 1].has_bottom_wall
                and not self.__cells[i][j].has_top_wall
            ):
                unvisited.append((i, j - 1))

            if len(unvisited) == 0:
                return False
            if algo == "dfs":
                x, y = unvisited.pop()
            else:
                x, y = unvisited.pop(0)
            self.__cells[i][j].draw_move(self.__cells[x][y])
            if self.__solve_r(x, y):
                return True
            else:
                self.__cells[x][y].draw_move(self.__cells[i][j], True)


def main():
    win = Window(800, 600)
    seed = 100
    maze = Maze(10, 10, 25, 18, 20, 20, win, seed)
    maze.solve(algo="dfs")

    win.wait_for_close()


if __name__ == "__main__":
    main()
