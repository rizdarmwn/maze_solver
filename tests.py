import unittest

from maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
        )

    def test_maze_create_cells_with_x1_y1(self):
        num_cols = 5
        num_rows = 5
        m1 = Maze(10, 10, num_rows, num_cols, 50, 50)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
        )

    def test_maze_create_cells_with_different_cols_rows(self):
        num_cols = 10
        num_rows = 5
        m1 = Maze(10, 10, num_rows, num_cols, 40, 60)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
        )

    def test_maze_break_entrance_and_exit(self):
        num_cols = 10
        num_rows = 5
        m1 = Maze(10, 10, num_rows, num_cols, 50, 50)
        self.assertEqual(m1._Maze__cells[0][0].has_top_wall, False)
        self.assertEqual(m1._Maze__cells[-1][-1].has_bottom_wall, False)

    def test_reset_cells_visited(self):
        num_cols = 10
        num_rows = 5
        m1 = Maze(10, 10, num_rows, num_cols, 50, 50)
        for i in range(m1._Maze__num_cols):
            for j in range(m1._Maze__num_rows):
                self.assertEqual(m1._Maze__cells[i][j].visited, False)


if __name__ == "__main__":
    unittest.main()
