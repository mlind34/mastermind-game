import sys
import random
import pygame
# from setup import *
from pygame.locals import *

# window dimensions
WINDOWWIDTH = 700
WINDOWHEIGHT = 800

# board tile size
TILELOC = 80

TILESIZE = 60

# feedback tile size and margin
FBSIZE = 25

# board margins
TOPMARGIN = 50
LEFTMARGIN = 150
FBLEFTMARGIN = 475
FBTOPMARGIN = 70

# Screen Surface
SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

# board dimensions
ROWS = 9
COLUMNS = 4

# Tile Colors (R, G, B)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 220, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 100, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game Colors (R, G, B)
GRAY = (169, 169, 169)
BOARD = (71, 41, 6)
BGCOLOR = (71, 41, 6)


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


# SCREENS
def start_screen():
    # fonts
    font_lg = pygame.font.Font('GamePlayed-vYL7.ttf', 70)
    font_md = pygame.font.Font('GamePlayed-vYL7.ttf', 25)
    font_sm = pygame.font.Font('GamePlayed-vYL7.ttf', 14)

    # display title
    title = font_lg.render('MASTERMIND', True, WHITE)
    title_rect = title.get_rect(center=(WINDOWWIDTH / 2, WINDOWHEIGHT / 14))
    SCREEN.blit(title, title_rect)

    # text buffers
    y_buffer = 40
    x_buffer = 40

    # rules title
    font_md.set_underline(True)
    rule_title = font_md.render('Rules:', True, WHITE)
    rule_title_rect = rule_title.get_rect(center=(title_rect.bottomleft[0] - x_buffer,
                                                  title_rect.bottomleft[1] + y_buffer))
    SCREEN.blit(rule_title, rule_title_rect)

    # rule 1
    rule_1 = font_sm.render('- Objective of the game is to guess the 4 color solution '
                            'generated by the CPU', True, WHITE)

    rule_1_rect = rule_1.get_rect(topleft=(rule_title_rect.center[0] - x_buffer,
                                           rule_title_rect.center[1] + y_buffer))
    SCREEN.blit(rule_1, rule_1_rect)

    # rule 2
    rule_2 = font_sm.render('- Select from 6 color tiles to guess the correct solution', True, WHITE)
    rule_2_rect = rule_2.get_rect(topleft=(rule_1_rect.bottomleft[0],
                                           rule_1_rect.bottomleft[1] + y_buffer))
    SCREEN.blit(rule_2, rule_2_rect)

    # rule 3
    rule_3 = font_sm.render('- If guess is correct color in correct position, a black tile will '
                            'be displayed', True, WHITE)

    rule_3_rect = rule_3.get_rect(topleft=(rule_2_rect.bottomleft[0],
                                           rule_2_rect.bottomleft[1] + y_buffer))
    SCREEN.blit(rule_3, rule_3_rect)

    # rule 4
    rule_4 = font_sm.render('- If guess is correct color in incorrect position, a white tile will '
                            'be displayed', True, WHITE)
    rule_4_rect = rule_4.get_rect(topleft=(rule_3_rect.bottomleft[0],
                                           rule_3_rect.bottomleft[1] + y_buffer))
    SCREEN.blit(rule_4, rule_4_rect)

    # rule 5
    rule_5 = font_sm.render('- Use up and down arrow keys to select color and right and left to'
                            'select column', True, WHITE)
    rule_5_rect = rule_5.get_rect(topleft=(rule_4_rect.bottomleft[0],
                                           rule_4_rect.bottomleft[1] + y_buffer))
    SCREEN.blit(rule_5, rule_5_rect)

    # rule 6
    rule_6 = font_sm.render('- Press [ENTER] to submit guessed row', True, WHITE)
    rule_6_rect = rule_6.get_rect(topleft=(rule_5_rect.bottomleft[0],
                                           rule_5_rect.bottomleft[1] + y_buffer))
    SCREEN.blit(rule_6, rule_6_rect)

    # begin
    begin = font_md.render('PRESS [SPACE] TO BEGIN', True, WHITE)
    begin_rect = begin.get_rect(topleft=(rule_6_rect.bottomleft[0],
                                         rule_6_rect.bottomleft[1] + y_buffer))

    SCREEN.blit(begin, begin_rect)


def finish_screen(outcome):
    # fonts
    font_lg = pygame.font.Font('GamePlayed-vYL7.ttf', 70)
    font_md = pygame.font.Font('GamePlayed-vYL7.ttf', 25)

    # player win
    if outcome == 'p':
        congrats = font_lg.render('CONGRATULATIONS!!', True, BLACK)
        congrats_rect = congrats.get_rect(center=(WINDOWWIDTH/2, WINDOWHEIGHT/5))
        SCREEN.blit(congrats, congrats_rect)

        you_won = font_lg.render('YOU WON!!', True, BLACK)
        you_won_rect = you_won.get_rect(center=(WINDOWWIDTH / 2, (WINDOWHEIGHT / 5) + 150))
        SCREEN.blit(you_won, you_won_rect)

    # cpu win
    if outcome == 'c':
        sorry = font_lg.render('SORRY :(', True, BLACK)
        sorry_rect = sorry.get_rect(center=(WINDOWWIDTH / 2, WINDOWHEIGHT / 5))
        SCREEN.blit(sorry, sorry_rect)

        you_lost = font_lg.render('YOU LOST', True, BLACK)
        you_lost_rect = you_lost.get_rect(center=(WINDOWWIDTH / 2, (WINDOWHEIGHT / 5) + 150))
        SCREEN.blit(you_lost, you_lost_rect)

    play_again = font_md.render('PLAY AGAIN??', True, BLACK)
    play_again_rect = play_again.get_rect(center=(WINDOWWIDTH / 2, (WINDOWHEIGHT / 5) + 250))
    SCREEN.blit(play_again, play_again_rect)

    press_enter = font_md.render('Press [SPACE] to play again', True, BLACK)
    press_enter_rect = press_enter.get_rect(center=(WINDOWWIDTH / 2, (WINDOWHEIGHT / 5) + 350))
    SCREEN.blit(press_enter, press_enter_rect)


if __name__ == '__main__':
    main()
