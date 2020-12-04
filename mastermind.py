import sys
import random
from setup import *
from pygame.locals import *


# GAME FUNCTIONS
def game_board():
    """Initializes main game board matrix structure"""
    # create game solution
    game_colors = [RED, YELLOW, BLUE, GREEN, ORANGE, PURPLE]
    solution = random.sample(game_colors, 4)

    # add GameTile sprite for each row and column
    board = []
    for i in range(ROWS):
        columns = []
        for j in range(COLUMNS):
            # make top row the solution row
            if i == 0:

                # fill color black to hide solution
                square = GameTile(j, i, BLACK, TILELOC, TILESIZE, LEFTMARGIN, TOPMARGIN, 1)

                # reassign color to actual solution color
                square.color = solution[j]

                columns.append(square)
            else:
                square = GameTile(j, i, TILE, TILELOC, TILESIZE, LEFTMARGIN, TOPMARGIN, 1)

                columns.append(square)

        board.append(columns)

    return board


def fb_board():
    """Creates feedback matrix structure"""
    feedback = []
    for i in range(1, ROWS):
        columns = []
        for j in range(COLUMNS):

            if j > 1:
                fb_square = GameTile(j, i, TILE, TILELOC, FBSIZE, FBLEFTMARGIN - 80, FBTOPMARGIN - 30, .5)
            else:
                fb_square = GameTile(j, i, TILE, TILELOC, FBSIZE, FBLEFTMARGIN, FBTOPMARGIN, .5)
            columns.append(fb_square)

        feedback.append(columns)

    return feedback


def draw_board(board):
    """draws main board data structure to the screen"""
    for i in range(len(board)):
        for j in range(len(board[i])):
            square = board[i][j]
            square.draw()


def draw_feedback(feedback):
    """draws feedback data structure to the screen"""
    for i in range(len(feedback)):
        for j in range(len(feedback[i])):
            fb_square = feedback[i][j]
            fb_square.draw()


def assign_feedback(board, feedback, row):
    """colors feedback tiles based on user input"""
    # get game arrays
    sol = [tile.color for tile in board[0]]
    guess = [tile.color for tile in board[row]]
    result = feedback[row - 1]

    # array of indices to randomize black and white tiles
    choices = [0, 1, 2, 3]
    for i in range(len(sol)):
        if sol[i] == guess[i]:
            choice = random.choice(choices)
            result[choice].update(BLACK)
            choices.remove(choice)

        elif sol[i] in guess:
            choice = random.choice(choices)
            result[choice].update(WHITE)
            choices.remove(choice)

    # if all tiles match
    result = [tile.color for tile in result]
    if result == [BLACK, BLACK, BLACK, BLACK]:
        return True


def reveal_solution(board):
    """reveals solution when game has ended"""
    sol_row = board[0]
    for i in range(len(sol_row)):
        sol_row[i].update(sol_row[i].color)


def check_complete(board, row):
    """Checks if a row is incomplete"""
    for tile in board[row]:
        if tile.color == TILE:
            return False
    return True


# TILE SPRITE CLASSES
class GameTile(pygame.sprite.Sprite):
    """Represents game tile in main board matrix"""

    def __init__(self, x, y, color, loc, size, xm, ym, buff):
        pygame.sprite.Sprite.__init__(self)
        self.loc = loc
        self.size = size
        self.xm = xm
        self.ym = ym
        self.buff = buff
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(color)
        self.color = color
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        """draws tile to screen"""
        rect = ((self.loc * self.rect.x * self.buff) + self.xm, (self.loc * self.rect.y) + self.ym,
                self.size, self.size)
        SCREEN.blit(self.image, rect)

    def update(self, color):
        """updates tile"""
        self.image.fill(color)
        self.color = color
        pygame.draw.rect(SCREEN, BLACK, ((self.loc * self.rect.x * self.buff) + self.xm,
                                         (self.loc * self.rect.y) + self.ym, self.size, self.size), 10)
        self.draw()
        return self.color

    def get_color(self):
        return self.color


# MAIN GAME
def main():
    # game initialization/setup
    pygame.init()
    pygame.display.set_caption('Mastermind')
    clock = pygame.time.Clock()

    # game states
    game_over = False
    intro = True

    # initialize game and feedback board
    board = game_board()
    feedback = fb_board()

    # set turn counter to last row
    turn_counter = ROWS - 1

    # fresh screen
    SCREEN.fill(BGCOLOR)

    if intro:
        start_screen()

    # tile color options
    tile_colors = [TILE, RED, BLUE, YELLOW, GREEN, ORANGE, PURPLE]

    # tracks left-right and up-down to select color and column
    key_pos = 0
    color_index = 0

    # main game loop
    while True:

        events = pygame.event.get()
        for event in events:
            # exit game
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # Start game
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    intro = False

            keys = pygame.key.get_pressed()

            if not intro and not game_over:
                # fresh screen with legend
                SCREEN.fill(BGCOLOR)
                main_legend()

                # draw boards to screen
                draw_board(board)
                draw_feedback(feedback)

                # borders first tile
                board[turn_counter][key_pos].update(tile_colors[color_index])

                # left-right keys change column, up-down changes color
                if event.type == KEYDOWN and not game_over:
                    if keys[K_LEFT] and key_pos > 0:

                        left_color = board[turn_counter][key_pos - 1].get_color()
                        color_index = tile_colors.index(left_color)
                        key_pos -= 1

                    if keys[K_RIGHT] and key_pos < 3:

                        right_color = board[turn_counter][key_pos + 1].get_color()
                        color_index = tile_colors.index(right_color)
                        key_pos += 1

                    if keys[K_UP] and color_index < 6:
                        color_index += 1
                        
                    if keys[K_DOWN] and color_index > 1:
                        color_index -= 1

                    # updates board according to input
                    board[turn_counter][key_pos].update(tile_colors[color_index])

                    # If Enter pressed, assign feedback, decrement turn_counter
                    if keys[K_RETURN] and turn_counter >= 1 and check_complete(board, turn_counter):

                        color_index = 0

                        # if player wins
                        if assign_feedback(board, feedback, turn_counter):
                            game_over = True
                            reveal_solution(board)
                            finish_screen('p')
                        else:
                            turn_counter -= 1
                            key_pos = 0

                    # if cpu wins
                    if turn_counter < 1:
                        reveal_solution(board)
                        game_over = True
                        finish_screen('c')
                        turn_counter += 1

            # Reset Game
            if keys[K_n]:
                main()

            # New Game
            if keys[K_SPACE] and game_over:
                main()

            pygame.display.update()
            clock.tick(30)


if __name__ == '__main__':
    main()
