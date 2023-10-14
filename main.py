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


class Card(sprite.Sprite):
    def __init__(self, x_co, y_co, width, height, opened, front, back, kind, numb, coloring):
        super().__init__()
        self.coloring = coloring
        self.opened = opened
        self.kind = kind
        self.numb = numb
        self.front = front
        self.back = back
        self.width = width
        self.height = height
        self.image = transform.scale(image.load(back), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x_co
        self.rect.y = y_co

    def change(self, opened):       #переворот карты
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
background = transform.scale(image.load("poker.png"), (win_width, win_height + 600))

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
        if i < 2:
            card = Card(800, 200, 90, 120, 2, pictures[i][j], 'card_back.png', kinds[i], j+2, 'R')
            cards.append(card)
        else:
            card = Card(800, 200, 90, 120, 2, pictures[i][j], 'card_back.png', kinds[i], j+2, 'B')
            cards.append(card)

for card in cards:
    print(card.numb)

random.shuffle(cards)
column = cards.copy()
column1 = []

k = 0
for i in range(7):
    for j in range(i + 1):
        cards[k].rect.x = i * 100
        cards[k].rect.y = j * 70
        if j == i:
            cards[k].change(1)
        field[i].append(cards[k])
        column.pop(0)
        k += 1

game = True
finish = False
clock = time.Clock()
FPS = 60

cur = 0
z = 0
m_field = []
del_i = None
del_active_f = None
started = False
active = None

while game:

    window.blit(background, (0, -300))

    column[cur].change(1)
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
                xm, ym = e.pos
                if 800 < xm < 890 and 200 < ym < 320:
                    if cur < 23:
                        cur += 1
                    elif cur == 23:
                        cur = 0
                if column[cur].rect.x < 900:
                    column[cur].rect.x = column[cur].rect.x + 100
                else:
                    for card in column:
                        card.rect.x = 800
                        card.rect.y = 200
                    column[cur].rect.x = column[cur].rect.x + 100

            if e.button == 3:
                xm, ym = e.pos
                for card in cards:
                    if card.inside(xm, ym):
                        active = cards.index(card)

        if e.type == MOUSEMOTION:
            xm, ym = e.pos
            if active is not None:
                for i in range(7):
                    if cards[active] in field[i]:
                        z = 1
                        active_f = field[i].index(cards[active])
                        m_field = field[i][active_f:].copy()
                        del_i = i
                        del_active_f = active_f
                        for j in range(len(m_field)):
                            m_field[j].rect.centerx = xm
                            m_field[j].rect.centery = ym + j*70
                        break
                else:
                    if cards[active] == column[cur]:
                        cards[active].rect.centerx = xm
                        cards[active].rect.centery = ym
                        m_field = column[cur]
                        z = 2

        if e.type == MOUSEBUTTONUP:
            if e.button == 3:
                if z == 1:
                    print("a")
                    cards[active - 1].change(1)
                    z = 0
                    for card in cards:
                        if card.rect.colliderect(m_field[0]) and card not in m_field and card not in column and card.numb - 1 == m_field[0].numb and card.numb != 14 and card.coloring != m_field[0].coloring:
                            for i in range(7):
                                if card in field[i]:
                                    print('b')
                                    m_field[0].rect.x = field[i][-1].rect.x
                                    m_field[0].rect.y = field[i][-1].rect.y + 70
                                    for j in range(1, len(m_field)):
                                        m_field[j].rect.x = m_field[j-1].rect.x
                                        m_field[j].rect.y = m_field[j-1].rect.y + 70
                                        field[i] = field[i] + m_field
                                        del field[del_i][del_active_f:]
                                    break
                            break
                elif z == 2:
                    z = 0
                    for card in cards:
                        if card.rect.colliderect(m_field) and card not in column and card.numb - 1 == m_field.numb and card.numb != 14 and card.coloring != m_field.coloring:
                            for i in range(7):
                                if card in field[i]:
                                    m_field.rect.x = field[i][-1].rect.x
                                    m_field.rect.y = field[i][-1].rect.y + 70
                                    field[i].append(m_field)
                                    del field[del_i][del_active_f]
                                    break
                            break
            active = None


    window.blit(image1, (800, 200))
    display.update()
    clock.tick(FPS)







