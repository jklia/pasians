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

extra_pig = ['ace_of_hearts (1).png', 'ace_of_clubs (1).png', 'ace_of_diamonds (1).png', 'ace_of_spades (2).png']
extra_kids = ['ch', 'kr', 'bu', 'pi']

check = [[15, 14], [14, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10], [10, 11], [11, 12], [12, 13]]

possible = []

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

    def posi(self, g):
        a = 0
        for card in g:
            if self.numb + 1 == card.numb and self.coloring != card.coloring or self.numb == 13 and card.numb == 1:
                a += 1
        return a >= 1

    def extr_posi(self, g, o):
        a = 0
        for card in g:
            if [card[-1].numb, self.numb] in o and self.kind == card[-1].kind:
                a += 1
        return a >= 1


class Layer(sprite.Sprite):
    def __init__(self, x_co, y_co, width, height, numb, col):
        super().__init__()
        self.numb = numb
        self.width = width
        self.height = height
        self.rect = Rect(x_co, y_co, width, height)
        self.fill_color = col
        self.rect.x = x_co
        self.rect.y = y_co

    def reset(self):
        draw.rect(window, self.fill_color, (self.rect.x, self.rect.y, self.width, self.height))

    def inside(self, c):
        return self.rect.colliderect(c)

win_width = 1300
win_height = 700
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load("poker.png"), (win_width, win_height + 600))

image1 = transform.scale(image.load('card_back.png'), (90, 120))
window.blit(image1, (800, 200))


extra_car = [
    [],
    [],
    [],
    [],
]

for i in range(4):
    if i % 2 == 0:
        card = Card(800 + i*100, 50, 90, 120, 1, extra_pig[i], 'card_back.png', extra_kids[i], 15, 'R')
    else:
        card = Card(800 + i * 100, 50, 90, 120, 1, extra_pig[i], 'card_back.png', extra_kids[i], 15, 'B')
    card.change(1)
    extra_car[i].append(card)

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

random.shuffle(cards)
column = cards.copy()
column1 = []

k = 0
for i in range(7):
    card1 = Layer(i*100, 0, 90, 120, 1, (235, 14, 47))
    field[i].append(card1)
    for j in range(i + 1):
        cards[k].rect.x = i * 100
        cards[k].rect.y = j * 40
        if j == i:
            cards[k].change(1)
            possible.append(cards[k])
        field[i].append(cards[k])
        column.pop(0)
        k += 1

game = True
finish = False
clock = time.Clock()
FPS = 60


cur = 0
z = 0
m = 0
m_field = []
del_i = None
del_active_f = None
started = False
active = None
check_posi = possible.copy()


while game:

    # window.blit(background, (0, -300))
    # for i in extra_car:
    #     for card in i:
    #         card.reset()
    #
    # column[cur].change(1)
    # for card in column:
    #     card.reset()
    #
    # for i in range(7):
    #     for card in (field[i]):
    #         card.reset()

    for e in event.get():

        if e.type == QUIT:
            game = False

        if e.type == MOUSEBUTTONDOWN:

            if e.button == 1:
                xm, ym = e.pos
                if 800 < xm < 890 and 200 < ym < 320:
                    if cur < len(column) - 1:
                        cur += 1
                    elif cur == len(column) - 1:
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
                        print('aaaa')
                        active = cards.index(card)

        if e.type == MOUSEMOTION:
            xm, ym = e.pos
            if active is not None:
                print('cccc')
                for i in range(7):
                    if cards[active] in field[i]:
                        print('ffff')
                        line = field[i].index(cards[active])
                        print(field[i][line].numb)
                        if field[i][line].posi(check_posi) or field[i][line].extr_posi(extra_car, check):
                            if field[i][line].numb != 13:
                                print('tttt')
                                z = 1
                                m_field = field[i][line:].copy()
                                del_i = i
                                del_active_f = line
                                for j in range(len(m_field)):
                                    m_field[j].rect.centerx = xm
                                    m_field[j].rect.centery = ym + j*40
                                break
                            else:
                                print('ooo')
                                for s in range(7):
                                    if len(field[s]) == 1:
                                        print('ne cto')
                                        z = 3
                                        m_field = field[i][line:].copy()
                                        del_i = i
                                        del_active_f = line
                                        for j in range(len(m_field)):
                                            m_field[j].rect.centerx = xm
                                            m_field[j].rect.centery = ym + j*40
                                        break

                else:
                    if cards[active] == column[cur]:
                        if column[cur].posi(check_posi) or column[cur].extr_posi(extra_car, check):
                            print('pppp')
                            if column[cur].numb != 13:
                                print('wwww')
                                cards[active].rect.centerx = xm
                                cards[active].rect.centery = ym
                                m_field = [0]
                                m_field[0] = column[cur]
                                z = 2
                            else:
                                print('llll')
                                for s in range(7):
                                    if len(field[s]) == 1:
                                        z = 2
                                        m = 1
                                        cards[active].rect.centerx = xm
                                        cards[active].rect.centery = ym
                                        m_field = [0]
                                        m_field[0] = column[cur]

        if e.type == MOUSEBUTTONUP:
            if e.button == 3:
                if z == 1:
                    #cards[active - 1].change(1)
                    z = 0
                    for card in cards:
                        if card.rect.colliderect(m_field[0]) and card not in m_field and card not in column and card.numb - 1 == m_field[0].numb and card.numb != 14 and card.coloring != m_field[0].coloring:
                            for i in range(7):
                                if card in field[i]:
                                    print('mmm')
                                    m_field[0].rect.x = field[i][-1].rect.x
                                    m_field[0].rect.y = field[i][-1].rect.y + 40
                                    for j in range(1, len(m_field)):
                                        m_field[j].rect.x = m_field[j-1].rect.x
                                        m_field[j].rect.y = m_field[j-1].rect.y + 40
                                    field[i] = field[i] + m_field
                                    cards[active - 1].change(1)
                                    print(possible[i].numb)
                                    possible[i] = m_field[-1]
                                    print(possible[i].numb)
                                    print(possible[del_i].numb)
                                    possible[del_i] = field[del_i][del_active_f - 1]
                                    print(possible[del_i].numb)
                                    del field[del_i][del_active_f:]
                                    break
                            break
                    for i in range(4):
                        if len(m_field) == 1:
                            if extra_car[i][-1].rect.colliderect(m_field[0]) and extra_car[i][-1].kind == m_field[0].kind and [extra_car[i][-1].numb,  m_field[0].numb] in check:
                                m_field[0].rect.x = extra_car[i][-1].rect.x
                                m_field[0].rect.y = extra_car[i][-1].rect.y
                                extra_car[i].append(m_field.pop(0))
                                cards[active - 1].change(1)
                                del field[del_i][del_active_f:]
                                if len(field[del_i]) > 0:
                                    print(possible[del_i].numb)
                                    possible[del_i] = field[del_i][-1]
                                    print(possible[del_i].numb)
                                else:
                                    possible[del_i] = card1

                                #possible[del_i] = field[del_i][-1]
                elif z == 2:
                    z = 0
                    if m != 1:
                        for card in cards:
                            if card.rect.colliderect(m_field[0]) and card not in column and card.numb - 1 == m_field[0].numb and card.numb != 14 and card.coloring != m_field[0].coloring:
                                for i in range(7):
                                    if card in field[i]:
                                        m_field[0].rect.x = field[i][-1].rect.x
                                        m_field[0].rect.y = field[i][-1].rect.y + 40
                                        field[i].append(m_field[0])
                                        possible[i] = m_field[-1]
                                        del column[cur]
                                        cur -= 1
                                        #del field[del_i][del_active_f]
                                        break
                                break

                    if m == 1:
                        for i in range(7):
                            if len(field[i]) == 1:
                                if field[i][0].inside(m_field[0]):
                                    m = 0
                                    m_field[0].rect.x = field[i][-1].rect.x
                                    m_field[0].rect.y = field[i][-1].rect.y
                                    field[i].append(m_field[0])
                                    possible[i] = m_field[-1]
                                    del column[cur]
                                    cur -= 1
                    for i in range(4):
                        if len(m_field) == 1:
                            if extra_car[i][-1].rect.colliderect(m_field[0]) and extra_car[i][-1].kind == m_field[0].kind and [extra_car[i][-1].numb,  m_field[0].numb] in check:
                                m_field[0].rect.x = extra_car[i][-1].rect.x
                                m_field[0].rect.y = extra_car[i][-1].rect.y
                                extra_car[i].append(m_field.pop(0))
                                del column[cur]
                                cur -= 1
                elif z == 3:
                    print('eeee')
                    #cards[active - 1].change(1)
                    for i in range(7):
                        if field[i][-1].numb == 1:  #len(field[i]) == 1
                            print('yyyyy')
                            if field[i][0].inside(m_field[0]):
                                print("uuuuu")
                                m_field[0].rect.x = field[i][0].rect.x
                                m_field[0].rect.y = field[i][0].rect.y
                                for j in range(1, len(m_field)):
                                    m_field[j].rect.x = m_field[j - 1].rect.x
                                    m_field[j].rect.y = m_field[j - 1].rect.y + 40
                                field[i] = field[i] + m_field
                                cards[active - 1].change(1)
                                possible[i] = m_field[-1]
                                possible[del_i] = field[del_i][del_active_f - 1]
                                del field[del_i][del_active_f:]
                                z = 0
                        break

                    # for card in extra_car:
                    #     if len(m_field) == 1:
                    #         print('какиш2')
                    #         if card.rect.colliderect(m_field[0]) and card.numb - 1 == m_field[0].numb and card.kind == m_field[0].kind:
                    #             print('какиш3')
                    #             m_field[0].rect.x = card.rect.x
                    #             m_field[0].rect.y = card.rect.y
                    #             card = m_field.pop(0)
                    #             del column[cur]
                    #             card.reset()

            active = None

    window.blit(background, (0, -300))
    for i in extra_car:
        for card in i:
            card.reset()

    column[cur].change(1)
    for card in column:
        card.reset()

    for i in range(7):
        for card in (field[i]):
            card.reset()
    check_posi = possible.copy()
    window.blit(image1, (800, 200))

    display.update()
    clock.tick(FPS)
