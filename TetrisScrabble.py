import pygame
import random
import sys
from bs4 import BeautifulSoup
import requests
sys.path.append("/Users/artai/OneDrive/Desktop/Artai/Programacion")
#from floatingMenuLibrary import floatingMenu, Option

pygame.init()
pygame.font.init()

SIZE = 40

COLS = 10; ROWS = 20

WIDTH, HEIGHT = 1200, 1000

screen = pygame.display.set_mode((WIDTH, HEIGHT))

font = pygame.font.SysFont("Arial", 20, True)
font40 = pygame.font.SysFont("Arial", 40, True)

LETTERS = {"A": 12.53, "B": 1.42, "C": 4.68, "D": 5.86, "E": 13.68, "F": 0.69, "G": 1.01, "H": 0.70, "I": 6.25, 
           "J":  0.44, "K": 0.01, "L": 4.97, "M": 3.15, "N":  6.71, "Ñ": 0.31, "O": 8.68, "P": 2.51, "Q": 0.88, 
           "R":  6.87, "S": 7.98, "T": 4.63, "U": 3.93, "V":  0.90, "W": 0.02, "X": 0.22, "Y": 0.90, "Z": 0.52}
LET = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "ñ", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
TYPES = ["L", "J", "T", "I", "S", "Z", "O"]

PIECES = {"L": [[0, 1, 0,],
                [0, 1, 0],
                [0, 1, 1]], 
          "J": [[0, 2, 0],
                [0, 2, 0],
                [2, 2, 0]], 
          "T": [[0, 0, 0],
                [3, 3, 3],
                [0, 3, 0]], 
          "I": [[0, 0, 0, 0],
                [4, 4, 4, 4],
                [0, 0, 0, 0],
                [0, 0, 0, 0]], 
          "S": [[0, 0, 0],
                [0, 5, 5],
                [5, 5, 0]], 
          "Z": [[0, 0, 0],
                [6, 6, 0],
                [0, 6, 6]],
          "O": [[7, 7],
                [7, 7]]}

COLORS = {"L": "blue", "J": "orange", "T": "violet", "I": "lightblue", "S": "green", "Z": "red", "O": "yellow"}

WORDS = []
for i in LETTERS:
    with open(f"tetrisScrabble/dicts/wordsScrabble1{i}.txt", "r", encoding='utf-8') as f:
        WORDS += [f.read().splitlines()]

def chooseLetter():
    r = random.random()*100
    s = 0
    for i in LETTERS:
        s += LETTERS[i]
        if r <= s:
            return i

def getArticles(word):
    baseUrl = 'https://dle.rae.es'
    r = requests.get(f'{baseUrl}/{word}')
    soup = BeautifulSoup(r.text, 'lxml')
    definitions = []
    title = ''
    for article in soup.select('article.o-main__article'):
        title = ' '.join(article.select_one('h1.c-page-header__title').stripped_strings) if article.select_one('h1.c-page-header__title') else None
        definitions = []
        for li in article.select('li.j'):
            item = li.select_one('div.c-definitions__item')
            if item:
                definitions.append(' '.join(item.stripped_strings))
        else:
            for li in article.select('li.m'):
                item = li.select_one('div.c-definitions__item')
                if item:
                    definitions.append(' '.join(item.stripped_strings))
        if title == '':
            break
        return (title, definitions)
    
    for div in soup.select('div.o-main__content'):
        for item in div.select('article'):
            if item:
                entry = ' '.join(item.stripped_strings).split()
                goodLine = ""
    
                for i in entry[1].lower()[1:-1]:
                    if i == "á":
                        goodLine += "a"
                    elif i == "é" or i == "è": 
                        goodLine += "e"
                    elif i == "í":
                        goodLine += "i"
                    elif i == "ó":
                        goodLine += "o"
                    elif i == "ú" or i == "ü":
                        goodLine += "u"
                    else:
                        goodLine += i
                if goodLine == word:
                    title, definitions = getArticles(' '.join(item.stripped_strings).split()[0])
                    return (title, definitions)
    for div in soup.select('div.o-container'):
        for item in div.select('article'):
            if item:
                title, definitions = getArticles(' '.join(item.stripped_strings).split()[0])
                return (title, definitions)
    return (title, definitions)

class Piece():
    def __init__(self):
        self.type = random.choice(TYPES)
        self.piece = PIECES[self.type]
        self.letters = [[chooseLetter() if self.piece[i][j] != 0 else 0 for j in range(len(self.piece))] for i in range(len(self.piece))]
        self.x = 3
        self.y = -1

    def draw(self):
        for j in range(len(self.piece)):
            for i in range(len(self.piece)):
                if self.piece[i][j] != 0:
                    pygame.draw.rect(screen, COLORS[self.type], ((self.x+i)*SIZE, (self.y+j)*SIZE, SIZE-1, SIZE-1), border_radius=4)
                    text = font.render(self.letters[i][j], True, "black")
                    screen.blit(text, ((self.x+i)*SIZE+21*SIZE/64, (self.y+j)*SIZE+3*SIZE/16))

    
    def update(self, board):        
        self.y += 1
        if self.checkCollision(board):
            self.y -= 1
            return True

    def move(self, dir, board):
        if dir == "right":
            self.x += 1
            if self.checkCollision(board):
                self.x -= 1

        elif dir == "left":
            self.x -= 1
            if self.checkCollision(board):
                self.x += 1

        elif dir == "down":
            self.y += 1
            if self.checkCollision(board):
                self.y -= 1
        
        elif dir == "drop":
            while not self.checkCollision(board):
                self.y += 1
            self.y -= 1
            return True
            

    def rotate(self, spin, board):
        if spin == "CCW":
            oldPiece = self.piece.copy()
            self.piece = [[0 for _ in range(len(oldPiece))] for _ in range(len(oldPiece))]
            oldLetters = self.letters.copy()
            self.letters = [[0 for _ in range(len(oldPiece))] for _ in range(len(oldPiece))]
            for i in range(len(oldPiece)):
                for j in range(len(oldPiece)):
                    self.piece[i][j] = oldPiece[len(oldPiece)-1-j][i]
                    self.letters[i][j] = oldLetters[len(oldPiece)-1-j][i]
            if self.checkCollision(board):
                self.x -= 1
                if self.checkCollision(board):
                    self.x += 2
                    if self.checkCollision(board):
                        self.x -= 1
                        self.y += 1
                        if self.checkCollision(board):
                            self.piece = oldPiece
                            self.letters = oldLetters
                            self.y -= 1
                

        elif spin == "CW":
            oldPiece = self.piece.copy()
            self.piece = [[0 for _ in range(len(oldPiece))] for _ in range(len(oldPiece))]
            oldLetters = self.letters.copy()
            self.letters = [[0 for _ in range(len(oldPiece))] for _ in range(len(oldPiece))]
            for i in range(len(oldPiece)):
                for j in range(len(oldPiece)):
                    self.piece[i][j] = oldPiece[j][len(oldPiece)-1-i]
                    self.letters[i][j] = oldLetters[j][len(oldPiece)-1-i]
            if self.checkCollision(board):
                self.x -= 1
                if self.checkCollision(board):
                    self.x += 2
                    if self.checkCollision(board):
                        self.x -= 1
                        self.y += 1
                        if self.checkCollision(board):
                            self.piece = oldPiece
                            self.letters = oldLetters
                            self.y -= 1
                    

    def checkCollision(self, board):
        for j in range(len(self.piece)):
            for i in range(len(self.piece)):
                if self.piece[i][j] != 0:
                    if 0 <= i+self.x < COLS and 0 <= j+self.y < ROWS:
                        if board.board[i+self.x][j+self.y] != 0:
                            return True
                    else:
                        if j+self.y < 0:
                            continue
                        else:
                            return True
        return False

        

class Board():
    def __init__(self):
        self.board = [[0 for _ in range(ROWS)] for _ in range(COLS)]
        self.letters = [[0 for _ in range(ROWS)] for _ in range(COLS)]
        
    def draw(self):
        for i in range(COLS):
            for j in range(ROWS):
                if self.board[i][j] == 0:
                    color = "grey"
                else:
                    color = COLORS[TYPES[self.board[i][j]-1]]
                pygame.draw.rect(screen, color, (i * SIZE, j * SIZE, SIZE-1, SIZE-1), border_radius=4)
                if self.letters[i][j] != 0:
                    text = font.render(self.letters[i][j], True, "black")
                    screen.blit(text, (i*SIZE+21*SIZE/64, j*SIZE+3*SIZE/16))

    
    def appendPiece(self, piecex):
        for j in range(len(piecex.piece)):
            for i in range(len(piecex.piece)):
                if piecex.piece[i][j] != 0:
                    self.board[i+piecex.x][j+piecex.y] = piecex.piece[i][j]
                    self.letters[i+piecex.x][j+piecex.y] = piecex.letters[i][j]

    def checkWords(self, piece, score):
        found = None
        # for j in range(piece.y, piece.y+len(piece.piece)):
        #     for i in range(piece.x, piece.x+len(piece.piece)):   
        for j in range(0, piece.y+len(piece.piece)):
            for i in range(0, piece.x+len(piece.piece)):  
                if j >= ROWS or i >= COLS or j < 0 or i < 0:
                    continue
                if self.letters[i][j] != 0:
                    word = ""
                    for k in range(COLS-i):
                        if self.letters[i+k][j] == 0:
                            break
                        word += self.letters[i+k][j]
                        if len(word) > 2:
                            if word.lower() in WORDS[LET.index(word[0].lower())]:
                                if found == None:
                                    found = [i, j, k, "h", word]
                                elif k > found[2]:
                                    found = [i, j, k, "h", word]

                                #found = True
                                #break
                if found != None: break
            if found != None: break
        
        # for j in range(piece.y, piece.y+len(piece.piece)):
        #     for i in range(piece.x, piece.x+len(piece.piece)):  
        for j in range(0, piece.y+len(piece.piece)):
            for i in range(0, piece.x+len(piece.piece)):
                if j >= ROWS or i >= COLS or j < 0 or i < 0:
                    continue
                if self.letters[i][j] != 0:
                    word = ""
                    for k in range(ROWS-j):
                        if self.letters[i][j+k] == 0:
                            break
                        word += self.letters[i][j+k]
                        if len(word) > 2:
                            if word.lower() in WORDS[LET.index(word[0].lower())]:
                                
                                if found == None:
                                    found = [i, j, k, "v", word]
                                elif k > found[2]:
                                    found = [i, j, k, "v", word]
                                
                                #found = True
                                #break
                if found != None: break
            if found != None: break

        if found != None: 
            #print(found[4])
            score.add(found[4])
            self.cleanWord(found)
        return found != None
    
    def cleanWord(self, found):
        if found[3] == "h":
            for j2 in range(found[1], 0, -1):
                for i2 in range(found[0], found[0]+found[2]+1):
                    self.board[i2][j2] = self.board[i2][j2-1]
                    self.letters[i2][j2] = self.letters[i2][j2-1]
        else:
            for _ in range(found[2]+1):
                for j2 in range(found[1]+found[2], 0, -1):
                    self.board[found[0]][j2] = self.board[found[0]][j2-1]
                    self.letters[found[0]][j2] = self.letters[found[0]][j2-1]

class UI():
    def __init__(self):
        self.x = 450
        self.y = 70
        self.n = 0
        self.words = []
        self.articles = ['', []]

    def add(self, word):
        f = lambda x: pow(x, 2)-2*x-2
        self.n += f(len(word))*100

        self.words.append(word)

        self.articles = getArticles(word.lower())
    
    def draw(self):
        t = font40.render("Puntuación: " + str(self.n), True, "white")
        screen.blit(t, (self.x, self.y))

        for i, word in enumerate(self.words[::-1]):
            t = font40.render(word.lower().title(), True, 'white')
            screen.blit(t, (self.x, self.y+50*(i+1)))
        if self.articles[0] != '':
            title = font40.render(self.articles[0].split()[0].removesuffix(','), True, 'blue')
            screen.blit(title, ((self.x+font40.render(self.words[-1], True, 'white').width)+10, self.y+50))

            h = 65
            for i, article in enumerate(self.articles[1]):
                t = font.render(article, True, 'white', wraplength=WIDTH-(self.x+100)-font40.render(self.words[-1], True, 'white').width-title.width)
                screen.blit(t, (self.x+100+title.width+font40.render(self.words[-1], True, 'white').width, self.y+h))
                h += t.height + 20

def main():
    
    run = True
    clock = pygame.time.Clock()
    board = Board()
    piece = Piece()
    ui = UI()

    t = 1

    dropped = False

    gameOver = False

    #f = floatingMenu("Board", [Option("board", str(board.letters).replace("], [", "\n")), Option("piece", str(piece.letters).replace("], [", "\n"))], 600, 150, 300, 100)
    while run:

        pygame.display.set_caption("FPS: " + str(clock.get_fps()))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    run = False
                if e.key == pygame.K_d or e.key == pygame.K_RIGHT:
                    piece.move("right", board)
                if e.key == pygame.K_a or e.key == pygame.K_LEFT:
                    piece.move("left", board)
                if e.key == pygame.K_s or e.key == pygame.K_DOWN:
                    piece.move("down", board)
                if e.key == pygame.K_SPACE:
                    piece.move("drop", board)
                    dropped = True
                if e.key == pygame.K_w or e.key == pygame.K_UP:
                    piece.rotate("CW", board)
                if e.key == pygame.K_z:
                    piece.rotate("CCW", board)

        screen.fill('black')

        if dropped:
            board.appendPiece(piece)
            
            while board.checkWords(piece, ui):
                ...
            
            piece = Piece()
            if piece.checkCollision(board):
                gameOver = True
            dropped = False
            t = 1
        elif t%max(10, (30-(ui.n//1000))) == 0:
            t = 0
            if piece.update(board):
                
                board.appendPiece(piece)
                while board.checkWords(piece, ui):
                    ...
                piece = Piece()
                if piece.checkCollision(board):
                    gameOver = True

        if gameOver:
            print("Has perdido")
            print("Puntuación final: " + str(ui.n))
            run = False
            main()       
        
        board.draw()
        piece.draw()
        ui.draw()

        # f.options[0].variable = str(board.letters).replace("], [", "\n")
        # f.options[1].variable = str(piece.letters).replace("], [", "\n")
        #f.update(screen)
        
        t += 1
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()