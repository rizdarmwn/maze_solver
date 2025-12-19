from graphics import Window
from maze import Maze


def main():
    win = Window(800, 600)
    seed = 100
    maze = Maze(10, 10, 25, 18, 20, 20, win, seed)
    maze.solve(algo="dfs")

    win.wait_for_close()


if __name__ == "__main__":
    main()
