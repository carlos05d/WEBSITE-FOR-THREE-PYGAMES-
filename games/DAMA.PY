import pygame
import sys

# Define constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
SQUARE_SIZE = 80
BOARD_SIZE = 8
FPS = 30

class DamaGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SQUARE_SIZE * BOARD_SIZE, SQUARE_SIZE * BOARD_SIZE))
        pygame.display.set_caption("Dama (Checkers)")
        self.clock = pygame.time.Clock()
        self.board = self.create_board()
        self.current_player = 'X'  # Player 'X' starts
        self.selected_piece = None
        self.valid_moves = []
        self.game_over = False

    def create_board(self):
        # Create an empty board
        board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        # Place pieces for 'X' (bottom player)
        for row in range(5, 8):
            for col in range(0, BOARD_SIZE, 2):
                board[row][col if row % 2 == 0 else col + 1] = 'X'
        
        # Place pieces for 'O' (top player)
        for row in range(0, 3):
            for col in range(0, BOARD_SIZE, 2):
                board[row][col if row % 2 == 0 else col + 1] = 'O'
        
        return board

    def draw_board(self):
        # Draw the checkerboard
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                pygame.draw.rect(self.screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

                # Draw pieces
                piece = self.board[row][col]
                if piece == 'X':
                    pygame.draw.circle(self.screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3)
                elif piece == 'O':
                    pygame.draw.circle(self.screen, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3)

    def draw_valid_moves(self):
        for move in self.valid_moves:
            row, col = move
            pygame.draw.circle(self.screen, GREEN, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 4)

    def is_valid_move(self, start_row, start_col, end_row, end_col, player):
        # Ensure the move is within the bounds
        if not (0 <= end_row < BOARD_SIZE and 0 <= end_col < BOARD_SIZE):
            return False

        # Check if the target square is empty
        if self.board[end_row][end_col] is not None:
            return False

        # Basic movement logic: only move diagonally, 1 square for normal moves
        if abs(end_row - start_row) == 1 and abs(end_col - start_col) == 1:
            return True

        # Capture logic: move 2 squares, the middle square must contain an opponent's piece
        if abs(end_row - start_row) == 2 and abs(end_col - start_col) == 2:
            middle_row = (start_row + end_row) // 2
            middle_col = (start_col + end_col) // 2
            if self.board[middle_row][middle_col] is not None and self.board[middle_row][middle_col] != player:
                return True

        return False

    def get_valid_moves(self, row, col, player):
        # Get all valid moves for a piece at (row, col)
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # 4 diagonal directions

        for dr, dc in directions:
            for i in range(1, 3):  # Look up to 2 squares away
                new_row = row + dr * i
                new_col = col + dc * i
                if self.is_valid_move(row, col, new_row, new_col, player):
                    moves.append((new_row, new_col))
                if abs(new_row - row) == 2 and abs(new_col - col) == 2:  # If it's a capture move, stop checking further
                    break
        return moves

    def make_move(self, start_row, start_col, end_row, end_col):
        self.board[end_row][end_col] = self.board[start_row][start_col]
        self.board[start_row][start_col] = None

        # Capture a piece if necessary
        if abs(end_row - start_row) == 2 and abs(end_col - start_col) == 2:
            middle_row = (start_row + end_row) // 2
            middle_col = (start_col + end_col) // 2
            self.board[middle_row][middle_col] = None

        # Check for promotion to king (optional rule, not implemented here)
        # Example: self.promote_to_king(end_row, end_col)

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def handle_click(self, pos):
        if self.game_over:
            return

        col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
        piece = self.board[row][col]

        if self.selected_piece is None:
            # If the clicked square has the current player's piece, select it
            if piece == self.current_player:
                self.selected_piece = (row, col)
                self.valid_moves = self.get_valid_moves(row, col, self.current_player)
        else:
            start_row, start_col = self.selected_piece
            if (row, col) in self.valid_moves:
                # Make the move if it's valid
                self.make_move(start_row, start_col, row, col)
                self.switch_player()
                self.selected_piece = None
                self.valid_moves = []
                self.check_game_over()
            else:
                self.selected_piece = None
                self.valid_moves = []

    def check_game_over(self):
        # Check if the current player has no valid moves or pieces left
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece == self.current_player:
                    if self.get_valid_moves(row, col, self.current_player):
                        return
        self.game_over = True

    def draw_game_over(self):
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, RED)
        self.screen.blit(text, (SQUARE_SIZE * 2, SQUARE_SIZE * 3))
        font = pygame.font.Font(None, 36)
        text = font.render("Press R to Restart or Q to Quit", True, RED)
        self.screen.blit(text, (SQUARE_SIZE * 1.5, SQUARE_SIZE * 4))

    def reset_game(self):
        self.board = self.create_board()
        self.current_player = 'X'
        self.selected_piece = None
        self.valid_moves = []
        self.game_over = False

    def play(self):
        while True:
            self.screen.fill(WHITE)
            self.draw_board()

            # Draw the selected piece and its valid moves
            if self.selected_piece is not None:
                self.draw_valid_moves()

            if self.game_over:
                self.draw_game_over()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self.handle_click(mouse_pos)

                if self.game_over and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = DamaGame()
    game.play()

