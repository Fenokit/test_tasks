import random
class CityGrid:
    def __init__(self, N, M, coverage=0.3):
        self.rows = N
        self.columns = M
        self.grid = [[False for _ in range(M)] for _ in range(N)]
        self.coverage = coverage
        self._block_random_blocks()

    def _block_random_blocks(self):
        total_blocks = self.rows * self.columns
        blocked_blocks = int(total_blocks * self.coverage)

        # Генерируем список со всеми ячейками
        all_blocks = [(row, col) for row in range(self.rows) for col in range(self.columns)]

        # Размещаем заблокированные блоки случайным образом, учитывая охват
        blocked_positions = random.sample(all_blocks, blocked_blocks)
        for position in blocked_positions:
            row, col = position
            self.grid[row][col] = True

    def print_grid(self):
        for row in self.grid:
            row_str = ""
            for block in row:
                if block:
                    row_str += "X "  # Занятый блок
                else:
                    row_str += "O "  # Свободный блок
            print(row_str)


a = CityGrid(1, 10, 0.3)
print(a.print_grid())


