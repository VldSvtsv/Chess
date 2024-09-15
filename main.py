import functools
import tkinter as tk
from PIL import Image, ImageTk

window = tk.Tk()
from tkinter import messagebox as mb

F = False
inFlip = False  #Если фигура ходит только в одну сторону, лучше использовать это
last_place = [-1, -1]
check_wh_king = 1
check_bl_king = 1
image_files = {
    'bBi': 'chess_samara/bB.png',
    'bKi': 'chess_samara/bK.png',
    'bKn': 'chess_samara/bN.png',
    'bPa': 'chess_samara/bP.png',
    'bQu': 'chess_samara/bQ.png',
    'bRo': 'chess_samara/bR.png',
    'wBi': 'chess_samara/wB.png',
    'wKi': 'chess_samara/wK.png',
    'wKn': 'chess_samara/wN.png',
    'wPa': 'chess_samara/wP.png',
    'wQu': 'chess_samara/wQ.png',
    'wRo': 'chess_samara/wR.png',
    'wLo': 'symmetric/wP.png',
    'bLo': 'symmetric/bP.png',
    'bSn': 'adventurer/bB.png',
    'wSn': 'adventurer/wB.png',
    'wFa': 'berlin/wB.png',
    'bFa': 'berlin/bB.png',
    'wPf': 'chess7/wP.png',
    'bPf': 'chess7/bP.png',
    'wDe': './pixel/wP.png',
    'bDe': './pixel/bP.png'
}
images = dict()
blank = Image.new('RGBA', (45, 45), (0, 0, 0, 0))
images['blank'] = ImageTk.PhotoImage(blank)
images['blank']
for figure, filename in image_files.items():
    im = Image.open(filename)
    im = im.resize((45, 45))
    im_ph = ImageTk.PhotoImage(im)
    images[figure] = im_ph

buttons = []
for i in range(8):
    buttons += [[[], [], [], [], [], [], [], []]]
for i in range(8):
    for j in range(8):
        buttons[i][j] = [
            i, j, 0, 0, 0, 0, 0, 0, 0, 'blank'
        ]  #0 - столбец; 1 - строка; 2 - фигура; 3 - цвет клетки; 4 - для изменения кнопки;


        #5 - нажата ли кнопка; 6 - отмечина ли кнопка; 7 - цвет фигуры; 8 - ключ для рисунка
        #9 ключ для рисунка; 10 - цвет
def Save():
    save_chess = open("test.txt", "w")

    for i in range(8):
        for j in range(8):
            for n in range(9):
                save_chess.write(str(buttons[i][j][n]))
                save_chess.write('@@@')
            save_chess.write('\n')

    save_chess.write(str(Turn))
    save_chess.close()


def change_turn():
    global Turn, F
    cleaning()
    mb.showinfo('Смена хода', 'Готов?')
    F = False
    if Turn:
        Turn = False
        info.config(text='Ход чёрных')
    else:
        Turn = True
        info.config(text='Ход былых')
    Flip()
    b = ThisPlacement()
    View(b)
    for i in b:
        Draw(i[0], i[1], False)


def cleaning():
    for i in range(8):
        for j in range(8):
            buttons[i][j][4].config(bg='#383838')
            buttons[i][j][5] = 0
            buttons[i][j][6] = 0
            buttons[i][j][4].config(image=images['blank'])


def ForViewAndPR(a, b):
    watisee = []
    if buttons[a][b][2] == 'Factory':
        watisee += factory(a, b)
    elif buttons[a][b][2] == 'Lobo':
        watisee += lobo(a, b)
    elif buttons[a][b][2] == 'Knight':
        watisee += horse_king(a, b)
    if buttons[a][b][2] == 'Rook':
        watisee += rook(a, b)
    elif buttons[a][b][2] == 'Bishop':
        watisee += bishop(a, b)
    elif buttons[a][b][2] == 'Pawn':
        watisee += pawn(a, b)
    elif buttons[a][b][2] == 'Queen':
        watisee += bishop(a, b)
        watisee += rook(a, b)
    elif buttons[a][b][2] == 'King':
        watisee += horse_king(a, b)
    elif buttons[a][b][2] == 'Sniper':
        watisee += sniper(a, b)
    elif buttons[a][b][2] == 'Pfactory':
        watisee += pfactory(a, b)
    elif buttons[a][b][2] == 'Desant':
        watisee += desant(a, b)
    return watisee


def placement(a, b, c, d):
    if c == 'black' or c == 2:
        c1 = 2
        n = 'b' + d[0] + d[1]
    else:
        c1 = 1
        n = 'w' + d[0] + d[1]
    buttons[a][b][2] = d
    buttons[a][b][7] = c1
    buttons[a][b][9] = n


def View(this_placement):
    print(1)
    print(Turn)
    watisee = []
    for i in this_placement:
        if Turn and buttons[i[0]][i[1]][7] == 1:
            print(1)
            watisee.append([i[0], i[1], 'C'])
            watisee += ForViewAndPR(i[0], i[1])
        elif not (Turn) and buttons[i[0]][i[1]][7] == 2:
            print(2)
            watisee.append([i[0], i[1], 'C'])
            watisee += ForViewAndPR(i[0], i[1])
    for i in watisee:
        buttons[i[0]][i[1]][4].config(bg=buttons[i[0]][i[1]][3])
        if i[2] == 'F':
            Draw(i[0], i[1], True)


def Flip():
    global inFlip
    cleaning()
    this_placement = ThisPlacement()
    for i in this_placement:

        buttons[i[0]][i[1]][2] = 0
        buttons[i[0]][i[1]][7] = 0
        buttons[i[0]][i[1]][9] = 'blank'
        buttons[i[0]][i[1]][4].config(image=images['blank'])
    for i in this_placement:
        placement(7 - i[0], 7 - i[1], i[2], i[3])
    inFlip = not (inFlip)


def ThisPlacement():
    this_placement = []
    for a in range(8):
        for b in range(8):
            if buttons[a][b][2] != 0:
                this_placement.append(
                    [a, b, buttons[a][b][7], buttons[a][b][2]])
    return this_placement


def turn(a, b):
    global Turn
    if Turn:
        if buttons[a][b][7] == 1 or buttons[a][b][6] == 1:
            PR(a, b)
            #View(ThisPlacement())
    else:
        if buttons[a][b][7] == 2 or buttons[a][b][6] == 1:
            PR(a, b)


def Draw(a, b, lemesee):
    if lemesee:
        buttons[a][b][4].config(image=images[buttons[a][b][9]])
    elif Turn and buttons[a][b][7] == 1:
        buttons[a][b][4].config(image=images[buttons[a][b][9]])
    elif not (Turn) and buttons[a][b][7] == 2:
        buttons[a][b][4].config(image=images[buttons[a][b][9]])


def rook(a, b):
    watisee = []
    arm1 = a + 1
    while arm1 <= 7 and (buttons[arm1][b][2] == 0 or
                         (buttons[arm1][b][7] + buttons[a][b][7]) == 3):
        if buttons[arm1][b][7] + buttons[a][b][7] == 3:
            watisee.append([arm1, b, 'F'])
            arm1 = 8
        elif buttons[arm1][b][2] == 0:
            watisee.append([arm1, b, 'C'])
        arm1 += 1
    arm1 = a - 1
    while arm1 >= 0 and (buttons[arm1][b][2] == 0
                         or buttons[arm1][b][7] + buttons[a][b][7] == 3):
        if buttons[arm1][b][7] + buttons[a][b][7] == 3:
            watisee.append([arm1, b, 'F'])
            arm1 = -1
        elif buttons[arm1][b][2] == 0:
            watisee.append([arm1, b, 'C'])
        arm1 -= 1
    brm1 = b + 1
    while brm1 <= 7 and (buttons[a][brm1][2] == 0 or
                         (buttons[a][brm1][7] + buttons[a][b][7]) == 3):
        if buttons[a][brm1][7] + buttons[a][b][7] == 3:
            watisee.append([a, brm1, 'F'])
            brm1 = 8
        elif buttons[a][brm1][2] == 0:
            watisee.append([a, brm1, 'C'])
        brm1 += 1
    brm1 = b - 1
    while brm1 >= 0 and (buttons[a][brm1][2] == 0 or
                         (buttons[a][brm1][7] + buttons[a][b][7]) == 3):
        if buttons[a][brm1][7] + buttons[a][b][7] == 3:
            watisee.append([a, brm1, 'F'])
            brm2 = -1
        elif buttons[a][brm1][2] == 0:
            watisee.append([a, brm1, 'C'])
        brm1 -= 1
    return watisee


def bishop(a, b):
    watisee = []
    abm = a + 1
    bbm = b + 1
    while (abm <= 7
           and bbm <= 7) and (buttons[abm][bbm][2] == 0 or
                              (buttons[abm][bbm][7] + buttons[a][b][7]) == 3):
        if buttons[abm][bbm][7] + buttons[a][b][7] == 3:
            watisee.append([abm, bbm, 'F'])
            abm = 8
            bbm = 8
        else:
            watisee.append([abm, bbm, 'C'])
        abm += 1
        bbm += 1
    abm = a + 1
    bbm = b - 1
    while (abm <= 7
           and bbm >= 0) and (buttons[abm][bbm][2] == 0 or
                              (buttons[abm][bbm][7] + buttons[a][b][7]) == 3):
        if buttons[abm][bbm][7] + buttons[a][b][7] == 3:
            watisee.append([abm, bbm, 'F'])
            abm = 8
            bbm = -1
        else:
            watisee.append([abm, bbm, 'C'])
        abm += 1
        bbm -= 1
    abm = a - 1
    bbm = b + 1
    while (abm >= 0
           and bbm <= 7) and (buttons[abm][bbm][2] == 0 or
                              (buttons[abm][bbm][7] + buttons[a][b][7]) == 3):
        if buttons[abm][bbm][7] + buttons[a][b][7] == 3:
            watisee.append([abm, bbm, 'F'])
            abm = -1
            bbm = 8
        else:
            watisee.append([abm, bbm, 'C'])
        abm -= 1
        bbm += 1
    abm = a - 1
    bbm = b - 1
    while (abm >= 0
           and bbm >= 0) and (buttons[abm][bbm][2] == 0 or
                              (buttons[abm][bbm][7] + buttons[a][b][7]) == 3):
        if buttons[abm][bbm][7] + buttons[a][b][7] == 3:
            watisee.append([abm, bbm, 'F'])
            abm = -1
            bbm = -1
        else:
            watisee.append([abm, bbm, 'C'])
        abm -= 1
        bbm -= 1
    return watisee


def horse_king(a, b):
    watisee = []
    if buttons[a][b][2] == 'Knight':
        a_offsets = [-2, -2, -1, 1, 1, -1, 2, 2]
        b_offsets = [-1, 1, -2, 2, -2, 2, -1, 1]
    elif buttons[a][b][2] == 'King':
        a_offsets = [-1, -1, -1, 0, 0, 1, 1, 1]
        b_offsets = [-1, 0, 1, -1, 1, -1, 0, 1]
    for i in range(8):
        aok = a + a_offsets[i]
        bok = b + b_offsets[i]
        if aok < 8 and bok < 8:
            if aok >= 0 and bok >= 0:
                if buttons[aok][bok][2] == 0:
                    watisee.append([aok, bok, 'C'])
                elif buttons[aok][bok][7] + buttons[a][b][7] == 3:
                    watisee.append([aok, bok, 'F'])
    return watisee


def pawn(a, b):
    watisee = []
    if (not (inFlip) and buttons[a][b][7] == 1) or (inFlip
                                                    and buttons[a][b][7] == 2):
        if buttons[a - 1][b][2] == 0:
            watisee.append([a - 1, b, 'C'])
            if a == 6 and buttons[a - 2][b][2] == 0:
                watisee.append([a - 2, b, 'C'])
        if b + 1 <= 7 and a - 1 >= 0:
            if buttons[a][b][7] + buttons[a - 1][b + 1][7] == 3:
                watisee.append([a - 1, b + 1, 'F'])
            elif buttons[a - 1][b + 1][2] == 0:
                watisee.append([a - 1, b + 1, 'E'])
        if b - 1 >= 0 and a - 1 >= 0:
            if buttons[a][b][7] + buttons[a - 1][b - 1][7] == 3:
                watisee.append([a - 1, b - 1, 'F'])
            elif buttons[a - 1][b - 1][2] == 0:
                watisee.append([a - 1, b - 1, 'E'])
    return watisee


def pfactory(a, b):
    watisee = []
    if (not (inFlip) and buttons[a][b][7] == 1) or (inFlip
                                                    and buttons[a][b][7] == 2):
        if a - 1 >= 0 and buttons[a + 1][b][2] == 0:
            watisee.append([a - 1, b, 'C'])
        elif a - 1 >= 0 and buttons[a][b][7] + buttons[a - 1][b][7] == 3:
            watisee.append([a - 1, b, 'F'])
    return watisee


def lobo(a, b):
    watisee = []
    if (not (inFlip) and buttons[a][b][7] == 1) or (inFlip
                                                    and buttons[a][b][7] == 2):
        if buttons[a - 1][b][2] == 0 and a - 1 >= 0:
            watisee.append([a - 1, b, 'C'])
            if buttons[a - 2][b][2] == 0 and a - 2 >= 0:
                watisee.append([a - 2, b, 'C'])
            elif buttons[a - 2][b][7] + buttons[a][b][7] == 3 and a - 2 >= 0:
                watisee.append([a - 1, b, 'F'])
        elif buttons[a - 1][b][7] + buttons[a][b][7] == 3 and a - 1 >= 0:
            watisee.append([a - 2, b, 'F'])
        if b + 1 < 8 and a - 1 >= 0:
            if buttons[a][b][7] + buttons[a - 1][b + 1][7] == 3:
                watisee.append([a - 1, b + 1, 'F'])
            elif buttons[a - 1][b + 1][2] == 0:
                watisee.append([a - 1, b + 1, 'C'])
        if b - 1 >= 0 and a - 1 >= 0:
            if buttons[a][b][7] + buttons[a - 1][b - 1][7] == 3:
                watisee.append([a - 1, b - 1, 'F'])
            elif buttons[a - 1][b - 1][2] == 0:
                watisee.append([a - 1, b - 1, 'C'])
    return watisee


def sniper(a, b):
    watisee = []
    if a + 1 <= 7 and buttons[a + 1][b][2] == 0:
        watisee.append([a + 1, b, 'C'])
        if a + 2 <= 7 and buttons[a + 2][b][2] == 0:
            watisee.append([a + 2, b, 'C'])
            arm1 = a + 3
            while arm1 <= 7 and (buttons[arm1][b][2] == 0 or
                                 (buttons[arm1][b][7] + buttons[a][b][7])
                                 == 3):
                if buttons[arm1][b][7] + buttons[a][b][7] == 3:
                    watisee.append([arm1, b, 'F'])
                    arm1 = 8
                elif buttons[arm1][b][2] == 0:
                    watisee.append([arm1, b, 'E'])
                arm1 += 1
        elif a + 2 <= 7 and buttons[a][b][7] + buttons[a + 2][b][7] == 3:
            watisee.append([a + 2, b, 'E'])
    elif a + 1 <= 7 and buttons[a][b][7] + buttons[a + 1][b][7] == 3:
        watisee.append([a + 1, b, 'E'])

    if a - 1 >= 0 and buttons[a - 1][b][2] == 0:
        if buttons[a - 1][b][2] == 0:
            watisee.append([a - 1, b, 'C'])
            if a - 2 >= 0 and buttons[a - 2][b][2] == 0:
                watisee.append([a - 2, b, 'C'])
                arm1 = a - 3
                while arm1 >= 0 and (buttons[arm1][b][2] == 0
                                     or buttons[arm1][b][7] + buttons[a][b][7]
                                     == 3):
                    if buttons[arm1][b][7] + buttons[a][b][7] == 3:
                        watisee.append([arm1, b, 'F'])
                        arm1 = -1
                    elif buttons[arm1][b][2] == 0:
                        watisee.append([arm1, b, 'E'])
                    arm1 -= 1
            elif a - 2 >= 0 and buttons[a][b][7] + buttons[a - 2][b][7] == 3:
                watisee.append([a - 2, b, 'E'])
        elif a - 1 >= 0 and buttons[a][b][7] + buttons[a - 1][b][7] == 3:
            watisee.append([a - 1, b, 'E'])

    if b + 1 <= 7 and buttons[a][b + 1][2] == 0:
        watisee.append([a, b + 1, 'C'])
        if b + 2 <= 7 and buttons[a][b + 2][2] == 0:
            watisee.append([a, b + 2, 'C'])
            brm1 = b + 3
            while brm1 <= 7 and (buttons[a][brm1][2] == 0 or
                                 (buttons[a][brm1][7] + buttons[a][b][7])
                                 == 3):
                if buttons[a][brm1][7] + buttons[a][b][7] == 3:
                    watisee.append([a, brm1, 'F'])
                    brm1 = 8
                elif buttons[a][brm1][2] == 0:
                    watisee.append([a, brm1, 'E'])
                brm1 += 1
        elif b + 2 <= 7 and buttons[a][b][7] + buttons[a][b + 2][7] == 3:
            watisee.append([a, b + 2, 'E'])
    elif b + 1 <= 7 and buttons[a][b][7] + buttons[a][b + 1][7] == 3:
        watisee.append([a, b + 1, 'E'])

    if b - 1 >= 0 and buttons[a][b - 1][2] == 0:
        watisee.append([a, b - 1, 'C'])
        if b + 2 >= 0 and buttons[a][b - 2][2] == 0:
            watisee.append([a, b - 2, 'C'])
            brm1 = b - 3
            while brm1 >= 0 and (buttons[a][brm1][2] == 0 or
                                 (buttons[a][brm1][7] + buttons[a][b][7])
                                 == 3):
                if buttons[a][brm1][7] + buttons[a][b][7] == 3:
                    watisee.append([a, brm1, 'F'])
                    brm1 = -1
                elif buttons[a][brm1][2] == 0:
                    watisee.append([a, brm1, 'E'])
                brm1 -= 1
        elif b + 2 >= 0 and buttons[a][b][7] + buttons[a][b - 2][7] == 3:
            watisee.append([a, b - 2, 'E'])
    elif b - 1 >= 0 and buttons[a][b][7] + buttons[a][b - 1][7] == 3:
        watisee.append([a, b - 1, 'E'])
    return watisee


def factory(a, b):
    watisee = []
    if a + 1 <= 7 and buttons[a + 1][b][2] == 0:
        watisee.append([a + 1, b, 'C'])
    elif a + 1 <= 7 and buttons[a][b][7] + buttons[a + 1][b][7] == 3:
        watisee.append([a + 1, b, 'F'])
    if a - 1 <= 7 and buttons[a - 1][b][2] == 0:
        watisee.append([a - 1, b, 'C'])
    elif a - 1 <= 7 and buttons[a][b][7] + buttons[a - 1][b][7] == 3:
        watisee.append([a - 1, b, 'F'])
    if b + 1 <= 7 and buttons[a][b + 1][2] == 0:
        watisee.append([a, b + 1, 'C'])
    elif b + 1 <= 7 and buttons[a][b][7] + buttons[a][b + 1][7] == 3:
        watisee.append([a, b + 1, 'F'])
    if b - 1 <= 7 and buttons[a][b - 1][2] == 0:
        watisee.append([a, b - 1, 'C'])
    elif b - 1 <= 7 and buttons[a][b][7] + buttons[a][b - 1][7] == 3:
        watisee.append([a, b - 1, 'F'])
    return watisee


def desant(a, b):

    watisee = pawn(a, b)  # Прямо как пешка
    # Но еще умеет десантироваться на зеркально отраженную поверхность
    if buttons[7 - a][b][2] == 0:
        watisee.append([7 - a, b, 'C'])

    return watisee


def PR(a, b):
    global Turn, F, last_place, check_bl_king, check_wh_king
    Ts = True  #Выполнять ли ход для снайпера
    a_offsets_king = [-1, -1, -1, 0, 0, 1, 1, 1]
    b_offsets_king = [-1, 0, 1, -1, 1, -1, 0, 1]
    if buttons[a][b][5] == 0 and buttons[a][b][6] == 0 and not F:
        last_place = [a, b]
        buttons[a][b][5] = 1
        buttons[a][b][4].config(bg='#CACACA')
        watisee = ForViewAndPR(a, b)
        for i in watisee:
            if i[2] == 'C':
                buttons[i[0]][i[1]][6] = 1
                buttons[i[0]][i[1]][4].config(bg='#CACACA')
            elif i[2] == 'F':
                buttons[i[0]][i[1]][6] = 1
                buttons[i[0]][i[1]][4].config(bg='#FF6060')
        F = True
    elif buttons[a][b][6] == 1:  #Ход
        # для пешки
        if (buttons[last_place[0]][last_place[1]][2]
                in ('Pawn', 'Pfactory', 'Desant')) and buttons[last_place[0]][
                    last_place[1]][7] == 2 and ((a == 7 and not (inFlip)) or
                                                (a == 0 and inFlip)):
            placement(last_place[0], last_place[1], 'black', 'Queen')
        elif (buttons[last_place[0]][last_place[1]][2]
              in ('Pawn', 'Pfactory', 'Desant')) and buttons[last_place[0]][
                  last_place[1]][7] == 1 and ((a == 0 and not (inFlip)) or
                                              (a == 7 and inFlip)):
            placement(last_place[0], last_place[1], 'white', 'Queen')
        #Для оборотня
        if buttons[last_place[0]][last_place[1]][2] == 'Lobo' and buttons[
                last_place[0]][last_place[1]][7] == 2 and buttons[
                    last_place[0]][last_place[1]][7] + buttons[a][b][7] == 3:
            placement(last_place[0], last_place[1], 'black', buttons[a][b][2])
        elif buttons[last_place[0]][last_place[1]][2] == 'Lobo' and buttons[
                last_place[0]][last_place[1]][7] == 1 and buttons[
                    last_place[0]][last_place[1]][7] + buttons[a][b][7] == 3:
            placement(last_place[0], last_place[1], 'white', buttons[a][b][2])
        if buttons[last_place[0]][last_place[1]][2] == 'Sniper' and (
                abs(a - last_place[0]) >= 3 or abs(b - last_place[1]) >= 3):
            Ts = False
        if Ts:
            buttons[a][b][2] = buttons[last_place[0]][last_place[1]][2]
            buttons[a][b][7] = buttons[last_place[0]][last_place[1]][7]
            buttons[a][b][9] = buttons[last_place[0]][last_place[1]][9]
            last_button = buttons[last_place[0]][last_place[1]]
            buttons[a][b][4].config(image=images[last_button[9]])
            if buttons[a][b][2] == 'Factory':
                if buttons[a][b][7] == 1:
                    placement(last_place[0], last_place[1], 'white',
                              'Pfactory')
                else:
                    placement(last_place[0], last_place[1], 'black',
                              'Pfactory')
            else:
                buttons[last_place[0]][last_place[1]][2] = 0
                #buttons[last_place[0]][last_place[1]][4].config(text='')
                buttons[last_place[0]][last_place[1]][7] = 0
                buttons[last_place[0]][last_place[1]][9] = 'blank'
                buttons[last_place[0]][last_place[1]][4].config(
                    image=images['blank'])
        else:
            buttons[a][b][2] = 0
            buttons[a][b][4].config(text='')
            buttons[a][b][7] = 0
            buttons[a][b][9] = 'blank'
            buttons[a][b][4].config(image=images['blank'])

        for i in range(8):  #ищет короля на доске
            for j in range(8):
                if buttons[i][j][2] == 'King':
                    if buttons[i][j][7] == 1:
                        check_wh_king = 1
                    if buttons[i][j][7] == 2:
                        check_bl_king = 1
        if check_wh_king == 0:
            print('black wins')
            mb.showinfo('Победа', 'Победил ' + 'черные')
        if check_bl_king == 0:
            print('white wins')
            mb.showinfo('Победа', 'Победил ' + 'белые')
        check_wh_king = 0
        check_bl_king = 0

        cleaning()
        change_turn()

        F = False
    elif buttons[a][b][6] == 0:

        a = ForViewAndPR(last_place[0], last_place[1])
        print()
        a.append([last_place[0], last_place[1]])
        for i in a:
            buttons[i[0]][i[1]][4].config(bg=buttons[i[0]][i[1]][3])
            buttons[i[0]][i[1]][5] = 0
            buttons[i[0]][i[1]][6] = 0
        F = False


for i in range(8):
    for j in range(8):
        if (i + j) % 2 == 0:
            a = '#7971F1'
        else:
            a = '#FFFFFF'
        frame = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
        frame.grid(row=i, column=j)
        button = tk.Button(master=frame,
                           bg='#383838',
                           image=images['blank'],
                           command=functools.partial(turn, i, j))
        buttons[i][j][3] = a
        buttons[i][j][4] = button
        button.pack()

frame = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
frame.grid(column=8, row=0, columnspan=4, rowspan=4)
save = tk.Button(master=frame,
                 height=10,
                 width=10,
                 text='Сохранить',
                 command=functools.partial(Save))
save.pack()

frame = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
frame.grid(column=8, row=4, columnspan=4, rowspan=4)
info = tk.Button(master=frame,
                 text='ход белых',
                 height=10,
                 width=10,
                 command=functools.partial(change_turn))
info.pack()

answer = mb.askyesno(title="Вопрос", message="начать новаю игру?")
if answer:
    placement(7, 2, 'white', 'Lobo')
    placement(7, 5, 'white', 'Lobo')
    placement(7, 1, 'white', 'Knight')
    placement(7, 6, 'white', 'Knight')
    placement(7, 7, 'white', 'Sniper')
    placement(7, 0, 'white', 'Sniper')

    placement(0, 2, 'black', 'Bishop')
    placement(0, 5, 'black', 'Bishop')
    placement(0, 1, 'black', 'Knight')
    placement(0, 6, 'black', 'Knight')
    placement(0, 0, 'black', 'Rook')
    placement(0, 7, 'black', 'Rook')

    placement(6, 0, 'white', 'Pawn')
    placement(6, 1, 'white', 'Desant')
    placement(6, 2, 'white', 'Pawn')
    placement(6, 3, 'white', 'Pawn')
    placement(6, 4, 'white', 'Pawn')
    placement(6, 5, 'white', 'Pawn')
    placement(6, 6, 'white', 'Desant')
    placement(6, 7, 'white', 'Pawn')

    placement(1, 0, 'black', 'Pawn')
    placement(1, 1, 'black', 'Pawn')
    placement(1, 2, 'black', 'Pawn')
    placement(1, 3, 'black', 'Pawn')
    placement(1, 4, 'black', 'Pawn')
    placement(1, 5, 'black', 'Pawn')
    placement(1, 6, 'black', 'Pawn')
    placement(1, 7, 'black', 'Pawn')

    placement(7, 4, 'white', 'Factory')
    placement(0, 4, 'black', 'Queen')

    placement(7, 3, 'white', 'King')
    placement(0, 3, 'black', 'King')

    Turn = True
    d = ThisPlacement()
    for i in d:
        print(i[0])
        Draw(i[0], i[1], False)
    View(d)

else:
    File = open("test.txt", "r")
    for s in File:
        N = s.split('@@@')
        if len(N) > 1:
            if N[2] != '0':
                placement(int(N[0]), int(N[1]), int(N[7]), N[2])
        else:
            if N[0] == 'True':
                Turn = True
                info.config(text='Ход белых')
            elif N[0] == 'False':
                Turn = False
                info.config(text='Ход чёрных')
    File.close()
window.mainloop()

