import numpy as np
import random
import pygame
from pygame.locals import *
from const import TEST_GRID, CP

n = 4


class GridOFGame():
    def __init__(self):
        self.grid = np.zeros((n, n))
        self.score = 0
        self.high_score = 0
        self.height = 800
        self.width = 600 
        self.REPEATE = True
        pygame.init()
        pygame.display.set_caption("2048")

        pygame.font.init()
        self.myfont = pygame.font.SysFont("Comic Sans MS", 30)

        self.screen = pygame.display.set_mode((self.width, self.height))

        try:
            with open('high_score.txt', 'r') as file:
                self.high_score = int(file.read())
        except FileNotFoundError:
            pass

    def new_num(self, n):
        poss = list(zip(*np.where(self.grid == 0)))

        for pos in random.sample(poss, k = n):
            if random.random() < 0.1:
                self.grid[pos] = 4
            else:
                self.grid[pos] = 2

    def check_for_sum(self, rc):
        rc = rc[rc != 0]
        new_rc = list()
        flg = 0
        for i in range(len(rc)):
            if flg:
                flg = 0
                continue
            if i != len(rc) - 1 and rc[i] == rc[i + 1]:
                self.score += rc[i] * 2
                new_element = rc[i] * 2
                flg = 1
            else:
                new_element = rc[i]
            new_rc.append(new_element)
        return new_rc
 
    def move(self, way):
        if way == 'L':
            for i in range(n):
                row = self.grid[i]
                new_row = np.zeros(n)
                just_number = row[row != 0]
                just_number = self.check_for_sum(just_number)
                new_row[0 : len(just_number)] = just_number
                self.grid[i] = new_row
        elif way == 'R':
            for i in range(n):
                row = self.grid[i]
                new_row = np.zeros(n)
                just_number = row[row != 0]
                just_number = self.check_for_sum(just_number[::-1])[::-1]
                new_row[n - len(just_number) : n] = just_number
                self.grid[i] = new_row
        elif way == 'U':
            for i in range(n):
                col = self.grid[:, i]
                new_col = np.zeros(n)
                just_number = col[col != 0]
                just_number = self.check_for_sum(just_number)
                new_col[0 : len(just_number)] = just_number
                self.grid[:, i] = new_col
        elif way == 'D':
            for i in range(n):
                col = self.grid[:, i]
                new_col = np.zeros(n)
                just_number = col[col != 0]
                just_number = self.check_for_sum(just_number[::-1])[::-1]
                new_col[n - len(just_number) : n] = just_number
                self.grid[:, i] = new_col
    
    def score_board(self):
        pygame.draw.rect(self.screen,
                    CP[0],
                    pygame.Rect(350, 20, 175, 150),
                    border_radius=8)
        
        pygame.draw.rect(self.screen,
                    CP[0],
                    pygame.Rect(100, 20, 175, 150),
                    border_radius=8)

        text_high_score = self.myfont.render(f"High Score", True, (0, 0, 0))
        trhs = text_high_score.get_rect(center=(437, 60))
        self.screen.blit(text_high_score, trhs)

        text_high_score = self.myfont.render(f"{int(max(self.score, self.high_score))}", True, (0, 0, 0))
        trhs = text_high_score.get_rect(center=(437, 120))
        self.screen.blit(text_high_score, trhs)
        
        text_score = self.myfont.render(f"Score", True, (0, 0, 0))
        trs = text_score.get_rect(center=(187, 60))
        self.screen.blit(text_score, trs)

        text_score_number = self.myfont.render(f"{int(self.score)}", True, (0, 0, 0))
        trsn = text_score.get_rect(center=(210, 120))
        self.screen.blit(text_score_number, trsn)

    def game_page(self):
        self.screen.fill(CP['back'])
        self.score_board()

        for i in range(4):
            for j in range(4):
                m = self.grid[i][j]
                x = j * self.width // n + 10
                y = i * (self.height - 200) // n + 10
                w = self.width // n - 2 * 10
                h = (self.height - 200) // n - 2 * 10
                y += 180
                pygame.draw.rect(self.screen, 
                                CP[m],
                                pygame.Rect(x, y, w, h),
                                border_radius=8)
                if m == 0:
                    continue
                text = self.myfont.render(f"{int(m)}", True, (0, 0, 0))
                tr = text.get_rect(center=(x + w/2, y + h/2))
                self.screen.blit(text, tr)

    def wait_for_key(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 'Q'
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        return 'U'
                    elif event.key == K_RIGHT:
                        return 'R'
                    elif event.key == K_LEFT:
                        return 'L'
                    elif event.key == K_DOWN:
                        return 'D'
                    elif event.key == K_q or event.key == K_ESCAPE:
                        return 'Q'
                    elif event.key == K_SPACE:
                        return 'S'

    def game_over_page(self):
        self.screen.fill(CP['back'])

        self.score_board()

        game_over_text = self.myfont.render(f"GAME OVER!", True, (0, 0, 0))
        got = game_over_text.get_rect(center=(300, 400))
        self.screen.blit(game_over_text, got)

        resume_text = self.myfont.render(f"For Try Again Press Space", True, (0, 0, 0))
        rt = resume_text.get_rect(center=(300, 450))
        self.screen.blit(resume_text, rt)

        quit_text = self.myfont.render(f"For Quit Press Q Or esc", True, (0, 0, 0))
        qt = quit_text.get_rect(center=(300, 500))
        self.screen.blit(quit_text, qt)

        move = ''
        pygame.display.update()
        while True:
            move = self.wait_for_key()
            if move == 'Q':
                self.REPEATE = False
                break
            elif move == 'S':
                self.REPEATE = True
                break

    def game_over(self):
        tmp = self.grid.copy()
        for i in 'LRUD':
            self.move(i)
            if not all((self.grid == tmp).flatten()):
                self.grid = tmp
                return False
        return True

    def play(self):
        self.new_num(2)
        while True:
            self.game_page()
            pygame.display.flip()
            move = self.wait_for_key()
            if move == 'Q':
                self.REPEATE = False
                return self.score
            old_one = self.grid.copy()
            self.move(move)
            if self.game_over():
                if self.high_score < self.score:
                    self.high_score = self.score
                    with open('high_score.txt', 'w') as file:
                        file.write(f"{int(self.high_score)}")

                self.game_over_page()
                break

            if not all((self.grid == old_one).flatten()):
                self.new_num(1)


if __name__ == '__main__':
    while True:
        gameGrid = GridOFGame()
        gameGrid.play()
        if not gameGrid.REPEATE:
            break
