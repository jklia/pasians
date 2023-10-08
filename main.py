import random

from pygame import *


pages = ()
kinds = ['ch', 'bu', 'kr', 'pi']
pictures = [
    ['2_of_hearts.png', '3_of_hearts.png', '4_of_hearts.png', '5_of_hearts.png', '6_of_hearts.png', '7_of_hearts.png', '8_of_hearts.png', '9_of_hearts.png', '10_of_hearts.png', 'jack_of_hearts.png', 'queen_of_hearts.png', 'king_of_hearts.png', 'ace_of_hearts.png'],
    ['2_of_diamonds.png', '3_of_diamonds.png', '4_of_diamonds.png', '5_of_diamonds.png', '6_of_diamonds.png', '7_of_diamonds.png', '8_of_diamonds.png', '9_of_diamonds.png', '10_of_diamonds.png', 'jack_of_diamonds.png', 'queen_of_diamonds.png', 'king_of_diamonds.png', 'ace_of_diamonds.png'],
    ['2_of_clubs.png', '3_of_clubs.png', '4_of_clubs.png', '5_of_clubs.png', '6_of_clubs.png', '7_of_clubs.png', '8_of_clubs.png', '9_of_clubs.png', '10_of_clubs.png', 'jack_of_clubs.png', 'queen_of_clubs.png', 'king_of_clubs.png', 'ace_of_clubs.png'],
    ['2_of_spades.png', '3_of_spades.png', '4_of_spades.png', '5_of_spades.png', '6_of_spades.png', '7_of_spades.png', '8_of_spades.png', '9_of_spades.png', '10_of_spades.png', 'jack_of_spades.png', 'queen_of_spades.png', 'king_of_spades.png', 'ace_of_spades.png']
    ]


# класс-родитель для спрайтов
class Card(sprite.Sprite):
    # конструктор класса
    def __init__(self, x_co, y_co, width, height, opened, front, back, kind, numb):
        super().__init__()
        # каждый спрайт должен хранить свойство image - изображение
        self.kind = kind
        self.numb = numb
        self.front = front
        self.back = back
        self.width = width
        self.height = height
        self.image = transform.scale(image.load(back), (width, height))
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = x_co
        self.rect.y = y_co
    def change (self, opened):
        if opened == 1:
            self.image = transform.scale(image.load(self.front), (self.width, self.height))
        elif opened == 2:
            self.image = transform.scale(image.load(self.back), (self.width, self.height))
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def inside(self, x, y):
        return self.rect.collidepoint(x, y)


win_width = 1300
win_height = 700
window = display.set_mode((win_width, win_height))
# display.set_caption("Maze")
# background = transform.scale(image.load("bosh.png"), (win_width, win_height))
window.fill((200, 255, 255))

image1 = transform.scale(image.load('card_back.png'), (90, 120))
window.blit(image1, (800, 200))

field = [
    [],
    [],
    [],
    [],
    [],
    [],
    []
]

cards = []
for i in range(4):
    for j in range(13):
        card = Card(800, 200, 90, 120, 2, pictures[i][j], 'card_back.png', kinds[i], j+1)
        cards.append(card)

random.shuffle(cards)
column = cards.copy()
column1 = []
#lying_cards = []
k = 0
for i in range(7):
    for j in range(i + 1):
        print(k)
        cards[k].rect.x = i * 100
        cards[k].rect.y = j * 70
        cards[k].change(1)
        field[i].append(cards[k])
        #lying_cards.append(cards[j])
        column.pop(0)
        k += 1
for card in cards:
    print(card.rect.x, card.rect.y)
game = True
finish = False
clock = time.Clock()
FPS = 60

# font.init()
# font = font.SysFont("Arial", 70)
# lose_1 = font.render('PLAYER1 LOSE!', True, (180, 0, 0))
# lose_2 = font.render('PLAYER2 LOSE!', True, (180, 0, 0))

k = 0
started = False
active = None
while game:

    window.fill((200, 255, 255))
    column[k].change(1)
    for card in column:
        card.reset()
    for i in range(7):
        for card in (field[i]):
            card.reset()
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                print("eeeee")
                xm, ym = e.pos
                if 800 < xm < 890 and 200 < ym < 320:
                    if k < 23:
                        k += 1
                    elif k == 23:
                        k = 0
                if column[k].rect.x < 900:
                    column[k].rect.x = column[k].rect.x + 100
                else:
                    for card in column:
                        card.rect.x = 800

            if e.button == 3:
                print("sssssss")
                xm, ym = e.pos
                for card in cards:
                    if card.inside(xm, ym):
                        print("vvvvvv")
                        active = cards.index(card)

        if e.type == MOUSEMOTION:
            xm, ym = e.pos
            if active is not None:
                print("aaaaaa")
                cards[active].rect.centerx = xm
                cards[active].rect.centery = ym

        if e.type == MOUSEBUTTONUP:
            if e.button == 3:
                active = None
    #window.fill((200, 255, 255))
    # column[k].reset()
    # for i in range(7):
    #     for card in (field[i]):
    #         card.reset()
    window.blit(image1, (800, 200))
    display.update()
    clock.tick(FPS)
