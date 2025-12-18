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
    def __init__(self, win: Window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.__win = win

    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

        if self.has_left_wall:
            p1 = Point(x1, y1)
            p2 = Point(x1, y2)
            line = Line(p1, p2)
            self.__win.draw_line(line)
        if self.has_top_wall:
            p1 = Point(x1, y1)
            p2 = Point(x2, y1)
            line = Line(p1, p2)
            self.__win.draw_line(line)
        if self.has_right_wall:
            p1 = Point(x2, y1)
            p2 = Point(x2, y2)
            line = Line(p1, p2)
            self.__win.draw_line(line)
        if self.has_bottom_wall:
            p1 = Point(x2, y2)
            p2 = Point(x1, y2)
            line = Line(p1, p2)
            self.__win.draw_line(line)

    def draw_move(self, to_cell, undo=False):
        fill_color = "gray" if undo else "red"
        x1 = ((self.__x2 - self.__x1) / 2) + self.__x1
        y1 = ((self.__y2 - self.__y1) / 2) + self.__y1
        x2 = ((to_cell.__x2 - to_cell.__x1) / 2) + to_cell.__x1
        y2 = ((to_cell.__y2 - to_cell.__y1) / 2) + to_cell.__y1
        p1 = Point(x1, y1)
        p2 = Point(x2, y2)
        line = Line(p1, p2)
        self.__win.draw_line(line, fill_color)


def main():
    win = Window(800, 600)
    cell1 = Cell(win)
    cell2 = Cell(win)
    cell1.draw(100, 200, 200, 300)
    cell2.draw(200, 300, 300, 400)
    cell1.draw_move(cell2)

    win.wait_for_close()


if __name__ == "__main__":
    main()
