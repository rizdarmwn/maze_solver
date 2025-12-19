from graphics import Line, Point, Window


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
