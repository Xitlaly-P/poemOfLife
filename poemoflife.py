import pygame
import random

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Poem of Life')

clock = pygame.time.Clock()

# some Variables
crashed = False
pause = True
size = 25
roll = False
DONE1 = False

# colors used
back = (246, 249, 229)
forg = (250, 227, 227)
darkback = (136, 57, 85)
boardclr = (217, 166, 183)
boardclr2 = (194, 112, 139)
pla1clr = (4, 150, 255)
pla2clr = (216, 17, 89)

def generate_poem(words_list):
    # Define the number of words for each line
    lines_lengths = [4, 5, 6]
    
    # Initialize an index to keep track of the current position in the words_list
    index = 0
    
    # Create a list to hold the poem's lines
    poem_lines = []
    
    # Iterate over the desired lengths for each line
    for length in lines_lengths:
        # Check if there are enough words remaining in the words_list
        if index + length <= len(words_list):
            # Select the words for the current line and join them
            line = " ".join(words_list[index:index+length])
            
            # Add the line to the poem_lines list
            poem_lines.append(line)
            
            # Update the index to skip the words already used
            index += length
        else:
            # If there are not enough words left, break the loop
            break
    
    # Join the poem_lines to form the complete poem
    poem = "\n".join(poem_lines)
    
    return poem

# after Win
def WINNER():
    global pla1_poem, pla2_poem
    
    # Generate poems for both players
    pla1_poem = generate_poem(pla1.collected_words)
    pla2_poem = generate_poem(pla2.collected_words)

    # Determine the winner based on the turn
    if turn == 1:
        winner_name = "Player 2"
        winner_poem = pla2_poem
        winner_clr = pla2.clr
    elif turn == 2:
        winner_name = "Player 1"
        winner_poem = pla1_poem
        winner_clr = pla1.clr

    # Display the winner and their poem on the screen
    pygame.draw.rect(gameDisplay, (back), (95, 95, 610, 410))
    pygame.draw.rect(gameDisplay, (darkback), (100, 100, 600, 400))
    pygame.draw.rect(gameDisplay, (back), (105, 105, 590, 390))
    
    smallText = pygame.font.SysFont("comicsansms", 90)
    textSurf, textRect = text_objects("GAME OVER", smallText, darkback)
    textRect.center = ((display_width // 2), (display_height // 2 - 100))
    gameDisplay.blit(textSurf, textRect)

    smallText = pygame.font.SysFont("comicsansms", 50)
    textSurf, textRect = text_objects(f"WINNER: {winner_name}", smallText, darkback)
    textRect.center = ((display_width // 2), (display_height // 2))
    gameDisplay.blit(textSurf, textRect)

    # Display the winner's poem
    smallText = pygame.font.SysFont("comicsansms", 20)
    lines = winner_poem.split('\n')
    for i, line in enumerate(lines):
        textSurf, textRect = text_objects(line, smallText, winner_clr)
        textRect.center = ((display_width // 2), (display_height // 2 + i * 30 + 50))
        gameDisplay.blit(textSurf, textRect)

    smallText1 = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects("Hit Space to Play Again", smallText1, darkback)
    textRect.center = ((700), (580))
    gameDisplay.blit(textSurf, textRect)

    temp = True
    while temp:
        global crashed, DONE1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
                temp = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameDisplay.fill(back)
                    b.__init__()
                    pla1.__init__(b, pla1clr)
                    pla2.__init__(b, pla2clr)
                    temp = False
                    DONE1 = False
        pygame.display.update()


# game Board Class
class board:
    def __init__(self):
        # board List
        self.boardarr = []
        count = 1
        self.words = self.load_words()  # Load words from the text file

        # generate 2D Board 10 X 10
        for i in range(0, 10):
            temp = []
            for j in range(0, 10):
                x = j * 60
                y = i * 60
                word = random.choice(self.words)  # Select a random word from the list
                temp.append((x, y, count, word))  # Include word in tile info
                count += 1
            self.boardarr.append(temp)


    def load_words(self):
        with open('words.txt', 'r') as f:
            words = f.readlines()
        return [word.strip() for word in words]

    def draw(self):
        #stufff
        for i in self.boardarr:
            for j in i:
                if int(j[2]) % 2 == 0:
                    colorb = boardclr
                else:
                    colorb = boardclr2

                pygame.draw.rect(gameDisplay, (colorb), (j[0], j[1], 59, 59))

                # Adjust font size based on word length
                if len(j[3]) > 8:  # You can adjust this threshold as needed
                    smallText = pygame.font.SysFont("comicsansms", 8)  # Decrease font size
                    truncated_word = j[3][:7] + "..."  # Truncate word and add "..."
                else:
                    smallText = pygame.font.SysFont("comicsansms", 10)  # Default font size
                    truncated_word = j[3]

                textSurf, textRect = text_objects(truncated_word, smallText, darkback)
                textRect.center = ((j[0] + (60 // 2)), (j[1] + (60 // 2)))
                gameDisplay.blit(textSurf, textRect)



# player class
class player:
    def __init__(self, B, clr):
        self.val = 100
        self.xpos = None
        self.ypos = None
        self.barr = B.boardarr
        self.clr = clr
        self.size = random.randint(15, 25)
        self.collected_words = []  # Initialize an empty list to store collected words
        for x in self.barr:
            for y in x:
                if self.val == y[2]:
                    self.xpos = y[0]
                    self.ypos = y[1]

    def move(self, no):
        if self.val - no > 0:
            self.val -= no
        else:
            print("You can not move")
        for x in self.barr:
            for y in x:
                if self.val == y[2]:
                    self.xpos = y[0]
                    self.ypos = y[1]
                    self.collected_words.append(y[3])  # Add the word of the current tile to collected_words
                    print(f"Appended word: {y[3]}")
        if self.val == 1:
            print("+=+" * 10 + " YOU WIN " + "+=+" * 10)
            global DONE1
            DONE1 = True

    def draw(self):
        pygame.draw.circle(gameDisplay, (self.clr), (self.xpos + 30, self.ypos + 30), self.size)


def text_objects(text, font, clr, *kward):
    if len(kward) > 0:
        textSurface = font.render(text, True, clr, kward[0])
    else:
        textSurface = font.render(text, True, clr)
    return textSurface, textSurface.get_rect()

# functions for dice
def one():
    x, y, w, h = 605, 50, 190, 190
    pygame.draw.rect(gameDisplay, darkback, (x, y, w, h))
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 2)), (y + (h // 2))), size)

def two():
    x, y, w, h = 605, 50, 190, 190
    pygame.draw.rect(gameDisplay, darkback, (x, y, w, h))
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 4)), (y + (h // 2))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (3 * w // 4)), (y + (h // 2))), size)

def three():
    x, y, w, h = 605, 50, 190, 190
    pygame.draw.rect(gameDisplay, darkback, (x, y, w, h))
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 4)), (y + (3 * h // 4))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 2)), (y + (h // 2))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (3 * w // 4)), (y + (h // 4))), size)

def four():
    x, y, w, h = 605, 50, 190, 190
    pygame.draw.rect(gameDisplay, darkback, (x, y, w, h))
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 4)), (y + (h // 4))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 4)), (y + (3 * h // 4))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (3 * w // 4)), (y + (h // 4))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (3 * w // 4)), (y + (3 * h // 4))), size)

def five():
    x, y, w, h = 605, 50, 190, 190
    pygame.draw.rect(gameDisplay, darkback, (x, y, w, h))
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 2)), (y + (h // 2))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 4)), (y + (h // 4))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 4)), (y + (3 * h // 4))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (3 * w // 4)), (y + (h // 4))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (3 * w // 4)), (y + (3 * h // 4))), size)

def six():
    x, y, w, h = 605, 50, 190, 190
    pygame.draw.rect(gameDisplay, darkback, (x, y, w, h))
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 4)), (y + (h // 2))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (3 * w // 4)), (y + (h // 2))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 4)), (y + (h // 4)) - 10), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 4)), (y + (3 * h // 4)) + 10), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (3 * w // 4)), (y + (h // 4)) - 10), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (3 * w // 4)), (y + (3 * h // 4)) + 10), size)

# pygame Start
pygame.init()

b = board()
pla1 = player(b, (4, 150, 255))
pla2 = player(b, (216, 17, 89))
turn = 1
gameDisplay.fill(back)

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if roll == True:
                    roll = False
                else:
                    roll = True

    if not DONE1:
        b.draw()
        pla1.draw()
        pla2.draw()
        smallText = pygame.font.SysFont("comicsansms", 40)
        textSurf, textRect = text_objects(str("Turn"), smallText, darkback, back)
        textRect.center = ((700), (300))
        gameDisplay.blit(textSurf, textRect)
        smallText1 = pygame.font.SysFont("comicsansms", 20)
        textSurf, textRect = text_objects("Hit Space to Play", smallText1, darkback, back)
        textRect.center = ((700), (500))
        gameDisplay.blit(textSurf, textRect)
        if roll:
            time = random.randint(5, 25)
            for i in range(time):
                no = random.randint(1, 6)
                if no == 1:
                    one()
                elif no == 2:
                    two()
                elif no == 3:
                    three()
                elif no == 4:
                    four()
                elif no == 5:
                    five()
                elif no == 6:
                    six()
                pygame.time.wait(100)
                pygame.display.update()

            roll = False
            if turn == 1:
                pla1.move(no)
                turn = 2
                pygame.draw.circle(gameDisplay, pla2.clr, (700, 400), 50)
            elif turn == 2:
                pla2.move(no)
                turn = 1
                pygame.draw.circle(gameDisplay, pla1.clr, (700, 400), 50)
    else:
        WINNER()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
