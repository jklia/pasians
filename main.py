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
                        active = cards.index(card)

        if e.type == MOUSEMOTION:
            xm, ym = e.pos
            if active is not None:
                for i in range(7):
                    if cards[active] in field[i]:
                        line = field[i].index(cards[active])
                        if field[i][line].posi(check_posi) or field[i][line].extr_posi(extra_car, check):
                            if field[i][line].numb != 13:
                                z = 1
                                m_field = field[i][line:].copy()
                                del_i = i
                                del_active_f = line
                                for j in range(len(m_field)):
                                    m_field[j].rect.centerx = xm
                                    m_field[j].rect.centery = ym + j*40
                                break
                            else:
                                for s in range(7):
                                    if len(field[s]) == 1:
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
                            if column[cur].numb != 13:
                                cards[active].rect.centerx = xm
                                cards[active].rect.centery = ym
                                m_field = [0]
                                m_field[0] = column[cur]
                                z = 2
                            else:
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
                    z = 0
                    for card in cards:
                        if card.rect.colliderect(m_field[0]) and card not in m_field and card not in column and card.numb - 1 == m_field[0].numb and card.numb != 14 and card.coloring != m_field[0].coloring:
                            for i in range(7):
                                if card in field[i]:
                                    m_field[0].rect.x = field[i][-1].rect.x
                                    m_field[0].rect.y = field[i][-1].rect.y + 40
                                    for j in range(1, len(m_field)):
                                        m_field[j].rect.x = m_field[j-1].rect.x
                                        m_field[j].rect.y = m_field[j-1].rect.y + 40
                                    field[i] = field[i] + m_field
                                    cards[active - 1].change(1)
                                    possible[i] = m_field[-1]
                                    possible[del_i] = field[del_i][del_active_f - 1]
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
                                    possible[del_i] = field[del_i][-1]
                                else:
                                    possible[del_i] = card1

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
                    for i in range(7):
                        if field[i][-1].numb == 1:  #len(field[i]) == 1
                            if field[i][0].inside(m_field[0]):
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
