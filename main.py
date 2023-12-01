import copy
import random
import time

import matplotlib.pyplot as plt


class CityGrid:
    def __init__(self, num_rows: int, num_columns: int, radius: int = 1, coverage: float = 0.3):
        self.rows = num_rows
        self.columns = num_columns
        self.radius = radius
        self.grid = [[False for _ in range(num_columns)] for _ in range(num_rows)]
        self.grid_copy = []
        self.coverage = coverage

        self.tower_coord = []  # Установленные башни
        self.covered_blocks = []  # Зоны покрытия
        self.blocked_blocks = []  # Блоки в которых нельзя ставить башню (условия задачи)
        self.blocks_not_for_tower = copy.deepcopy(self.blocked_blocks)  # Блоки в которых не стоит ставить башню (ранее
        # установленные башни и общие зоны башен)
        self._block_random_blocks()

    def _block_random_blocks(self):
        """
        Randomly blocks a portion of the grid cells based on the coverage.
        """
        total_blocks = self.rows * self.columns
        num_blocked_blocks = int(total_blocks * self.coverage)

        # Generate a list with all cells
        all_blocks = [(row, col) for row in range(self.rows) for col in range(self.columns)]

        # Place blocked blocks randomly, considering the coverage
        self.blocked_blocks = random.sample(all_blocks, num_blocked_blocks)
        for position in self.blocked_blocks:
            row, col = position
            self.grid[row][col] = 'X'
        self.grid_copy = copy.deepcopy(self.grid)

    def print_grid(self):
        """
        Prints the grid representation.
        """
        for row in self.grid:
            row_str = ""
            for block in row:
                if block == 'X':
                    row_str += "X "  # Occupied block
                elif block == 1:
                    row_str += "# "  # Block covered by tower
                elif block in ['1', '2', '3']:  # Different types of towers
                    row_str += f"{block} "  # Towers
                else:
                    row_str += "O "  # Free block
            print(row_str)

    def get_free_block_coordinates(self):
        """
        Returns the coordinates of the free blocks in the grid.
        """
        block_coordinates = []
        for index_row, row in enumerate(self.grid):
            for index_col, block in enumerate(row):
                if not block:
                    block_coordinates.append([index_row, index_col])
        return block_coordinates

    def get_tower_coverage_bounds(self, row_index: int, col_index: int):
        """
        Returns the boundaries of the tower's coverage area based on its index.
        """
        start_row = max(0, row_index - self.radius)
        end_row = min(self.rows, row_index + self.radius + 1)
        start_col = max(0, col_index - self.radius)
        end_col = min(self.columns, col_index + self.radius + 1)

        return start_row, end_row, start_col, end_col

    def find_tower_coverage(self, block_coordinates: list, mode='bigger'):
        """
        Determines the coordinates of the tower that provides maximum coverage.
        """
        max_coverage = 0
        grid_center = [self.rows // 2, self.columns // 2]
        # print(f'grid_center {grid_center}')
        check_mode = [grid_center] if mode == 'center' else block_coordinates
        print(f'check_mode - {check_mode}')
        coverage_coordinates = []
        selected_tower_coord = []
        for coord in check_mode:
            row_index, col_index = coord[0], coord[1]
            total_coverage = 0
            coord = []
            # print(f'row_index, col_index - {row_index}-{col_index}')
            start_row, end_row, start_col, end_col = self.get_tower_coverage_bounds(row_index, col_index)
            # print(f'{start_row, end_row, start_col, end_col}')
            for covered_row in range(start_row, end_row):
                for covered_col in range(start_col, end_col):
                    # print([covered_row,covered_col])
                    # print(f'{[covered_row, covered_col]} - {self.grid[covered_row][covered_col]}')

                    # if self.grid[covered_row][covered_col] == False or self.grid[covered_row][covered_col] == 1:
                    if not self.grid[covered_row][covered_col]:
                        total_coverage += 1
                        # if [covered_row, covered_col] in self.covered_blocks:
                        #     continue
                        # else:
                        coord.append([covered_row, covered_col])
                        # print(coord)
                    elif self.grid[covered_row][covered_col]:
                        coord.append([covered_row, covered_col])


            if mode == 'bigger':
                if total_coverage > max_coverage:
                    max_coverage = total_coverage
                    selected_tower_coord = [[row_index, col_index]]
                    coverage_coordinates = coord
                elif total_coverage == max_coverage:
                    coverage_coordinates += coord
                    selected_tower_coord += [[row_index, col_index]]
            elif mode == 'smaller':
                if total_coverage < max_coverage or max_coverage == 0:
                    max_coverage = total_coverage
                    selected_tower_coord = [[row_index, col_index]]
                    coverage_coordinates = coord
                elif total_coverage == max_coverage:
                    coverage_coordinates += coord
                    selected_tower_coord += [[row_index, col_index]]
            elif mode == 'center':
                selected_tower_coord = [[row_index, col_index]]
                coverage_coordinates = coord
        print(f'{selected_tower_coord} - {coverage_coordinates}\n')

        if len(selected_tower_coord) > 1:

            closest_tower_coord = min(selected_tower_coord,
                                      key=lambda x: abs(x[0] - grid_center[0]) + abs(x[1] - grid_center[1]))
            index_center = selected_tower_coord.index(closest_tower_coord)
            coverage_coordinates = coverage_coordinates[index_center * max_coverage:(index_center + 1) * max_coverage]
            selected_tower_coord = [closest_tower_coord]
        if selected_tower_coord[0] in coverage_coordinates:
            coverage_coordinates.remove(selected_tower_coord[0])
        print(f'{selected_tower_coord} - {coverage_coordinates}\n')
        # self.print_grid()
        # print()

        print(f' ДО self.covered_blocks - {self.covered_blocks}\n')

        # print(f'self.covered_blocks - {self.covered_blocks}\ncoverage_coordinates - {coverage_coordinates}')
        for el in coverage_coordinates:
            if el in self.covered_blocks:
                print(f'Ecть {el}')
                self.covered_blocks.remove(el)
                self.blocks_not_for_tower.append(el)
            else:
                self.covered_blocks += [el]
        print(self.blocks_not_for_tower)
        self.tower_coord += selected_tower_coord
        # print(f' ПОСЛЕ self.covered_blocks - {self.covered_blocks}')

    def place_tower(self, tower_coord):
        """
        Places a tower on the grid and marks the covered blocks.
        """
        print(tower_coord)
        start_row, end_row, start_col, end_col = self.get_tower_coverage_bounds(tower_coord[0], tower_coord[1])
        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                if not self.grid[row][col]:
                    self.grid[row][col] = True
        self.grid[tower_coord[0]][tower_coord[1]] = str(2)

    def optimize_grid(self):
        """
        Optimizes the grid by placing towers in strategic locations.
        """

        check = 100
        block_coordinates = self.get_free_block_coordinates()
        num_repeats = 0

        while check != len(self.covered_blocks):
            check = len(self.covered_blocks)

            self.find_tower_coverage(block_coordinates)
            self.place_tower(self.tower_coord)
            self.print_grid()
            # print(self.blocks_not_for_tower)
            # print(self.covered_blocks)
            print()

            num_repeats += 1
        self.visualize_city_grid()
        num_towers = []
        for el in self.tower_coord:
            if el not in num_towers:
                num_towers.append([el])
        num_towers.clear()

    def visualize_city_grid(self):
        """
        Visualizes a grid, including blocked blocks, towers, coverage areas, and data paths.
        """
        # Creating a graph
        fig, axes = plt.subplots(1, 2, figsize=(10, 10))

        ax1 = axes[0]  # First subplot for "before" visualization
        ax2 = axes[1]  # Second subplot for "after" visualization

        # Formation of blocked grid blocks
        blocked_blocks = a.blocked_blocks

        # Building blocked blocks
        for block in blocked_blocks:
            ax1.add_patch(plt.Rectangle((block[0], block[1]), 1, 1, facecolor='black', edgecolor='black'))
            ax2.add_patch(plt.Rectangle((block[0], block[1]), 1, 1, facecolor='black', edgecolor='black'))

        # Forming a list with towers
        towers = a.tower_coord

        # Building towers
        for tower in towers:
            ax2.add_patch(plt.Rectangle((tower[0], tower[1]), 1, 1, facecolor='red', edgecolor='black'))

        # Formation of the coverage area
        coverage_zones = []
        for tower in a.tower_coord:
            x = tower[0] - a.radius
            y = tower[1] - a.radius
            coverage_zones.append([x, y, a.radius * 2 + 1, a.radius * 2 + 1])

        # Building coverage areas
        for zone in coverage_zones:
            ax2.add_patch(plt.Rectangle((zone[0], zone[1]), zone[2], zone[3], hatch='///////', linewidth=1,
                                        edgecolor='black', facecolor='none', alpha=0.3))

        # Formation of data transmission paths
        data_paths = []

        for index_tower, tower in enumerate(towers):
            start_row, end_row, start_col, end_col = a.get_tower_coverage_bounds(tower[0], tower[1])
            for row in range(start_row, end_row):
                for col in range(start_col, end_col):
                    if [row, col] in towers and [row, col] != tower:
                        data_paths += [
                            [[float(tower[0] + 0.5), float(tower[1] + 0.5)], [float(row + 0.5), float(col + 0.5)]]]

        # Building data transmission paths
        for index_path, path in enumerate(data_paths):
            ax2.arrow(path[0][0], path[0][1], path[1][0] - path[0][0], path[1][1] - path[0][1], color='green',
                      width=0.1)

        # Setting up the plots
        ax1.set_xlim(0, self.columns)
        ax1.set_ylim(0, self.rows)
        ax1.set_aspect('equal', adjustable='box')
        ax1.set_title('Before')

        ax2.set_xlim(0, self.columns)
        ax2.set_ylim(0, self.rows)
        ax2.set_aspect('equal', adjustable='box')
        ax2.set_title('After')

        # Adding text with the application results
        results = """
        Result 1: ...
        Result 2: ...
        Result 3: ...
        """
        fig.text(0.5, 0.05, results, ha='center', fontsize=12, va='bottom')

        # Displaying the plots
        plt.tight_layout()
        plt.show()


# coverage = float(input())
# num_rows = int(input())
# num_columns = int(input())

if __name__ == '__main__':
    a = CityGrid(10, 10)
    a.optimize_grid()
