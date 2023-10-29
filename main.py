import pygame
import sys
import time
import random


class Sudoku:
    def __init__(self, board):
        self.board = board  # Change 'grid' to 'board'

    def print_board(self):
        for row in self.board:
            print(" ".join(map(str, row)))

    def find_empty_space(self, position):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    position[0] = i
                    position[1] = j
                    return True  # if empty space found
        return False

    def used_in_row(self, row_index, num):
        return num in self.board[row_index]

    def used_in_column(self, col_index, num):
        for i in range(9):
            if self.board[i][col_index] == num:
                return True
        return False

    def used_in_3x3(self, row_index, col_index, num):
        for i in range(3):
            for j in range(3):
                if self.board[i + row_index][j + col_index] == num:
                    return True
        return False

    def check_location_is_safe(self, row_index, col_index, num):
        return (not self.used_in_row(row_index, num)) and not (self.used_in_column(col_index, num)) and not (
            self.used_in_3x3(row_index - row_index % 3, col_index - col_index % 3, num))

    def generate_sudoku_board(self, difficulty=12):
        # Initialize an empty 9x9 board
        self.board = [[0 for i in range(9)] for i in range(9)]

        # Generate a random Sudoku board
        for i in range(difficulty):  # Adjust the number of iterations for difficulty
            row, col, num = random.randint(0, 8), random.randint(0, 8), random.randint(1, 9)
            while not self.check_location_is_safe(row, col, num):
                row, col, num = random.randint(0, 8), random.randint(0, 8), random.randint(1, 9)
            self.board[row][col] = num


pygame.init()


class SudokuSolverGUI(Sudoku):
    def __init__(self, board):
        super().__init__(board)  # Call the parent class (Sudoku) constructor

        self.window_size = 540
        self.grid_size = self.window_size // 9
        self.colors = {
            "white": (255, 255, 255),
            "black": (0, 0, 0),
        }
        self.font = pygame.font.Font(None, 36)
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption("Sudoku GUI")

    def solve_sudoku(self):

        position = [0, 0]

        if not self.find_empty_space(position):
            return True

        row = position[0]
        column = position[1]

        for num in range(1, 10):
            if self.check_location_is_safe(row, column, num):
                self.handle_gui_close_if_x_clicked()

                self.board[row][column] = num
                self.draw_entire_board()

                if self.solve_sudoku():
                    return True

                self.board[row][column] = 0  # reset, this will also go recursively back and reset all values
                self.draw_entire_board()

        return False

    def handle_gui_close_if_x_clicked(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def draw_grid(self):
        line_color = self.colors["black"]

        for i in range(10):
            if i % 3 == 0:
                line_width = 2  # Make the lines around the 3x3 boxes bolder
            else:
                line_width = 1  # Keep the smaller lines within the boxes thinner

            # draw horizontal line
            pygame.draw.line(self.screen, line_color, (i * self.grid_size, 0), (i * self.grid_size, self.window_size), line_width)


            pygame.draw.line(self.screen, line_color, (0, i * self.grid_size), (self.window_size, i * self.grid_size), line_width)


    def draw_numbers(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] != 0:
                    text = self.font.render(str(self.board[row][col]), True, self.colors["black"])
                    text_rect = text.get_rect(center=(col * self.grid_size + self.grid_size // 2, row * self.grid_size + self.grid_size // 2))
                    pygame.draw.rect(self.screen, self.colors["white"], (col * self.grid_size, row * self.grid_size, self.grid_size, self.grid_size))
                    self.screen.blit(text, text_rect)

    def draw_entire_board(self):
        self.screen.fill(self.colors["white"])
        self.draw_numbers()
        self.draw_grid()

        pygame.display.update()


if __name__ == "__main__":
    sudoku_board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    gui = SudokuSolverGUI(sudoku_board)

    difficulty = 10
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    gui.solve_sudoku()

                if event.key == pygame.K_r:
                    gui.generate_sudoku_board(difficulty)

                if event.key == pygame.K_UP:
                    difficulty += 1
                    print(f"Difficulty: {difficulty}")

                if event.key == pygame.K_DOWN:
                    if difficulty > 1:
                        difficulty -= 1
                        print(f"Difficulty: {difficulty}")

        gui.draw_entire_board()

    pygame.quit()
    sys.exit()
