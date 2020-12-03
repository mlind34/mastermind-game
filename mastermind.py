import sys
import random
import pygame
from setup import *
from pygame.locals import *


# GAME FUNCTIONS
def game_board():
    """Initializes main game board matrix structure"""
    # create game solution
    game_colors = [RED, YELLOW, BLUE, GREEN, ORANGE, WHITE]
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
                square = GameTile(j, i, GRAY, TILELOC, TILESIZE, LEFTMARGIN, TOPMARGIN, 1)

                columns.append(square)

        board.append(columns)

    return board


def fb_board():
    """Creates feedback matrix structure"""
    feedback = []
    for i in range(1, ROWS):
        columns = []
        for j in range(COLUMNS):
            fb_square = GameTile(j, i, GRAY, TILELOC, FBSIZE, FBLEFTMARGIN, FBTOPMARGIN, .5)
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
        self.draw()


# MAIN GAME
def main():
    # game initialization/setup
    pygame.init()
    pygame.display.set_caption('Mastermind')
    clock = pygame.time.Clock()

    # game states
    game_over = False
    intro = True
    complete_row = False

    # initialize game and feedback board
    board = game_board()
    feedback = fb_board()

    # set turn counter to last row
    turn_counter = ROWS - 1

    # tile color options
    game_colors = [RED, BLUE, YELLOW, GREEN, ORANGE, WHITE]

    # fresh screen
    SCREEN.fill(BGCOLOR)

    if intro:
        start_screen()

    # tracks left-right and up-down to select color and column
    key_pos = 0
    color_track = 0

    # main game loop
    while True:

        events = pygame.event.get()
        for event in events:
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    intro = False

            keys = pygame.key.get_pressed()

            if not intro and not game_over:
                # fresh screen
                SCREEN.fill(BOARD)

                # draw boards to screen
                draw_board(board)
                draw_feedback(feedback)

                # colors first column
                board[turn_counter][key_pos].update(game_colors[color_track])

                # left-right keys change column, up-down changes color
                if event.type == KEYDOWN and not game_over:
                    if keys[K_LEFT] and key_pos > 0:
                        key_pos -= 1
                    if keys[K_RIGHT] and key_pos < 3:
                        key_pos += 1
                        color_track = 0
                        if key_pos == 3:
                            complete_row = True
                    if keys[K_UP] and color_track < 5:
                        color_track += 1
                    if keys[K_DOWN] and color_track > 0:
                        color_track -= 1

                    # updates board according to input
                    board[turn_counter][key_pos].update(game_colors[color_track])

                    # If Enter pressed, assign feedback, decrement turn_counter
                    if keys[K_RETURN] and turn_counter >= 1 and complete_row:
                        color_track = 0
                        if assign_feedback(board, feedback, turn_counter):
                            game_over = True
                            reveal_solution(board)
                            finish_screen('p')

                        else:
                            complete_row = False
                            turn_counter -= 1
                            key_pos = 0

                    if turn_counter < 1:
                        reveal_solution(board)
                        game_over = True
                        finish_screen('c')
                        turn_counter += 1

            if keys[K_SPACE] and game_over:
                main()

            pygame.display.update()
            clock.tick(30)


if __name__ == '__main__':
    main()
