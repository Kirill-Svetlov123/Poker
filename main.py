import random
import pygame

pygame.init()

display_width = 800
display_height = 600

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Poker')

icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

bank = 0
Max_points = 0
Player1_points = 0
Player2_points = 0

clock = pygame.time.Clock()
current_time = 0

need_input = False
input_text = '|'
input_tick = 30

player_name = ''

class Card:
    def __init__(self, val, suit, image, x, y, points, set):
        self.val = val
        self.suit = suit
        self.image = image
        self.x = x
        self.y = y
        self.points = points
        self.set = set

    def __repr__(self):
        return repr(self.val + ' ' + self.suit)

class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (142, 142, 142)
        self.active_color = (195, 195, 195)
        self.active = False

    def draw(self, x, y, message, action, font_color=(0, 0, 0), font_size=30, h=0, w=0):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed(3)

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(display, self.active_color, (x, y, self.width, self.height))

            if click[0] == 1:
                if action is not None:
                    self.active = True
                    if action == quit:
                        pygame.quit()
                        quit()
                    else:
                        action()
                        self.active = False

        else:
            pygame.draw.rect(display, self.inactive_color, (x, y, self.width, self.height))

        output_text(message=message, x=x + w, y=y + h, font_color=font_color, font_size = font_size)




Card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
Card_suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
Cards_img = pygame.image.load('Cards.png')
Combination = {'High card': 1, 'Pair': 2, 'Two pair': 3, 'Three of a Kind': 4, 'Straight': 5, 'Flush': 6, 'Full House': 7, 'Four of a Kind': 8, 'Straight-flush': 9, 'Royal Flush': 10}
results = {'p1': 0, 'p1 points': 0, 'p2': 0, 'p2 points': 0}


def show_menu():
    menu_background = pygame.image.load('Menu_background.png')

    settings_btn = Button(190, 80)
    quit_btn = Button(190, 80)

    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.blit(menu_background, (0, 0))
        settings_btn.draw(display_width/2 - 190/2, display_height/2 - 65, 'Играть', settings, (0, 0, 0), 50, 10, 20)
        quit_btn.draw(display_width/2 - 190/2, display_height/2 + 40, 'Выход', quit, (0, 0, 0), 50, 10, 20)

        pygame.display.update()
        clock.tick(60)

def start_game():
    if Max_points > 0:
        while game_cycle():
            pass

def game_cycle():

    global Player1_cards
    global Player2_cards
    global Table_cards
    global Cards
    global Player1_points
    Cards = []

    run = True
    background = pygame.image.load('Table.png')

    for i in range(len(Card_values)):
        for j in range(len(Card_suits)):
            rect = (80 * i, 120 * j, 80, 120)
            img = Cards_img.subsurface(rect)
            Cards.append(Card(Card_values[i], Card_suits[j], img, 0, 0, i + 2, ''))

    Player1_cards = create_set('p1')
    Player2_cards = create_set('p2')
    Table_cards = create_set('t')

    output(Player1_cards, Player2_cards, Table_cards)

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.blit(background, (0, 0))
        draw_players_cards()
        draw_table_cards()

        output_text(str(Player1_points), 10, 560, (0, 0, 0))
        output_text(str(Player2_points), 10, 10, (0, 0, 0))
        output_text('Банк: ' + str(bank), 10, 275, (0, 0, 0))
        output_text(player_name, 55, 480, (255, 255, 255), font_size=35)

        auction()

        pygame.display.update()

        if len(Table_cards) == 5:
            pygame.time.wait(10000)
            if Player1_points == 0 or Player2_points == 0:
                run = False
            else:
                start_game()

    return end_game()

def settings():

    bckgrnd = pygame.image.load('settings_bg.png')
    settings = True

    global plus_100_btn
    global plus_200_btn
    global plus_500_btn
    global plus_1000_btn
    global  plus_2000_btn

    global minus_100_btn
    global minus_200_btn
    global minus_500_btn
    global minus_1000_btn
    global minus_2000_btn

    global equally_0_btn

    plus_100_btn = Button(90, 40)
    plus_200_btn = Button(90, 40)
    plus_500_btn = Button(90, 40)
    plus_1000_btn = Button(90, 40)
    plus_2000_btn = Button(90, 40)

    minus_100_btn = Button(90, 40)
    minus_200_btn = Button(90, 40)
    minus_500_btn = Button(90, 40)
    minus_1000_btn = Button(90, 40)
    minus_2000_btn = Button(90, 40)

    equally_0_btn = Button(60, 40)
    start_btn = Button(130, 50)

    while settings:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.blit(bckgrnd, (0, 0))

        output_text('Введите ваше имя и нажмите Enter', 175, 300, (50, 50, 50), font_size=30)
        output_text('Ваше имя: ' + player_name, 175, 430, (50, 50, 50), font_size=30)
        output_text('Количество очков у игрока: ' + str(Max_points), 150, 30, (0, 0, 0), font_size=40)

        plus_100_btn.draw(90, 100, '+ 100', setting, (0, 0, 0), 20, 10, 20)
        plus_200_btn.draw(200, 100, '+ 200', setting, (0, 0, 0), 20, 10, 20)
        plus_500_btn.draw(310, 100, '+ 500', setting, (0, 0, 0), 20, 10, 20)
        plus_1000_btn.draw(420, 100, '+ 1000', setting, (0, 0, 0), 20, 10, 20)
        plus_2000_btn.draw(530, 100, '+ 2000', setting, (0, 0, 0), 20, 10, 20)

        minus_100_btn.draw(90, 170, '- 100', setting, (0, 0, 0), 20, 10, 20)
        minus_200_btn.draw(200, 170, '- 200', setting, (0, 0, 0), 20, 10, 20)
        minus_500_btn.draw(310, 170, '- 500', setting, (0, 0, 0), 20, 10, 20)
        minus_1000_btn.draw(420, 170, '- 1000', setting, (0, 0, 0), 20, 10, 20)
        minus_2000_btn.draw(530, 170, '- 2000', setting, (0, 0, 0), 20, 10, 20)

        equally_0_btn.draw(660, 135, '= 0', setting, (0, 0, 0), 20, 10, 20)

        start_btn.draw(660, 540, 'Начать', start_game, (0, 0, 0), h=10, w=20)


        get_input()

        pygame.display.update()

def auction():

    pygame.time.wait(1000)

    global run_auction
    global bet
    global plus_10_btn
    global minus_10_btn
    global all_in_btn
    global time

    run_auction = True

    bet = 0

    create_bet = Button(90, 35)
    plus_10_btn = Button(40, 40)
    minus_10_btn = Button(40, 40)
    all_in_btn = Button(80, 35)
    check_btn = Button(80, 35)

    while run_auction:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.draw.rect(display, (255, 255, 255), (670, 430, 70, 40))

        output_text(str(bet), 675, 435, (0, 0, 0))


        if Player1_points > 0:
            create_bet.draw(660, 480, 'сделать', end_auction, (0, 0, 0), 15, w=20)
            output_text('ставку', 683, 495, (0, 0, 0), font_size=15)
            minus_10_btn.draw(620, 430, '-10', calculate, font_size=20, h=10, w=5)
            plus_10_btn.draw(750, 430, '+10', calculate, font_size=20, h=10, w=5)
            all_in_btn.draw(620, 550, 'Ва-банк', calculate, (0, 0, 0), 15, h=10, w=12)
        else:
            create_bet.draw(660, 480, 'сделать', None, (0, 0, 0), 15, w=20)
            output_text('ставку', 683, 495, (0, 0, 0), font_size=15)
            minus_10_btn.draw(620, 430, '-10', None, font_size=20, h=10, w=5)
            plus_10_btn.draw(750, 430, '+10', None, font_size=20, h=10, w=5)
            all_in_btn.draw(620, 550, 'Ва-банк', None, (0, 0, 0), 15, h=10, w=12)

        check_btn.draw(710, 550, 'Чек', end_auction, (0, 0, 0), 15, h=10, w=25)

        pygame.display.update()

def calculate():

    global bet

    if plus_10_btn.active and bet < Player1_points:
        bet += 10

    if minus_10_btn.active and bet > 0:
        bet -= 10

    if all_in_btn.active:
        bet = Player1_points
        end_auction()

    pygame.time.wait(300)


def end_auction():

    global run_auction
    global bank
    global Player1_points

    bank += bet
    Player1_points -= bet

    if bet > 0:
        output_text('-' + str(bet), 80, 560, (0, 0, 0))

    run_auction = False
    pygame.time.wait(5000)
    new_card()

def setting():

    global Max_points
    global Player1_points
    global Player2_points

    if plus_100_btn.active == True:
        Max_points += 100

    elif plus_200_btn.active == True:
        Max_points += 200

    elif plus_500_btn.active == True:
        Max_points += 500

    elif plus_1000_btn.active == True:
        Max_points += 1000

    elif plus_2000_btn.active == True:
        Max_points += 2000

    elif minus_100_btn.active == True and Max_points - 100 >= 0:
        Max_points -= 100

    elif minus_200_btn.active == True and Max_points - 200 >= 0:
        Max_points -= 200

    elif minus_500_btn.active == True and Max_points - 500 >= 0:
        Max_points -= 500

    elif minus_1000_btn.active == True and Max_points - 1000 >= 0:
        Max_points -= 1000

    elif minus_2000_btn.active == True and Max_points - 2000 >= 0:
        Max_points -= 2000

    elif equally_0_btn.active == True:
        Max_points = 0

    Player1_points = Max_points
    Player2_points = Max_points

    pygame.time.wait(300)

def get_input():
    global input_text, need_input, player_name, input_tick

    input_rect = pygame.Rect(225, 350, 350, 60)

    pygame.draw.rect(display, (255, 255, 255), input_rect)

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed(3)

    if input_rect.collidepoint(mouse[0], mouse[1]) and click[0]:
        need_input = True

    if need_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if need_input and event.type == pygame.KEYDOWN:
                input_text = input_text.replace('|', '')
                input_tick = 30


                if event.key == pygame.K_RETURN:
                    need_input = False
                    player_name = input_text
                    input_text = ''
                    print(player_name)
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 10:
                        input_text += event.unicode

                input_text += '|'

    if len(input_text):
        output_text(input_text, input_rect.x + 10, input_rect.y + 10, (0, 0, 0), font_size=40)

    input_tick -= 1

    if input_tick == 0:
        input_text = input_text[:-1]
    if input_tick == -30:
        input_text += '|'
        input_tick = 30


def rand_card():
    choice = random.randrange(0, len(Cards))
    card = Cards[choice]
    del Cards[choice]
    return card

def create_set(a):
    mass = []
    for i in range(2):
        card = rand_card()
        card.set = a
        mass.append(card)
    return mass

def new_card():
    card = rand_card()
    card.set = 't'
    Table_cards.append(card)
    print(repr(Table_cards[-1]))
    display.blit(Table_cards[-1].image,(Table_cards[-2].x - 100, Table_cards[-2].y))


def output(Player1_cards, Player2_cards, Table_cards):
    print('Player1: ', end="")
    for i in range(0, len(Player1_cards)):
        print('|' + repr(Player1_cards[i]) + '| ', end="")

    print('\n', 'Table: ', end="", sep="")
    for i in range(0, len(Table_cards)):
        print('|' + repr(Table_cards[i]) + '| ', end="")

    print('\n', 'Player2: ', end="", sep="")
    for i in range(0, len(Player2_cards)):
        print('|' + repr(Player2_cards[i]) + '| ', end="")

    print('\n')

def draw_players_cards():
    for i in range(2):
        display.blit(Player1_cards[i].image, ((display_width/2)-90+100*i, 470))
        Player1_cards[i].x = (display_width/2)-90+100*i
        Player1_cards[i].y = 470
        display.blit(Player2_cards[i].image, ((display_width/2)-90+100*i, 10))
        Player2_cards[i].x = (display_width/2)-90+100*i
        Player2_cards[i].y = 10

def draw_table_cards():
    for i in range(len(Table_cards)):
        display.blit(Table_cards[i].image, ((display_width / 2) + 160 - 100 * i, (display_height / 2) - 60))
        Table_cards[i].x = (display_width / 2) + 160 - 100 * i
        Table_cards[i].y = (display_height / 2) - 60

def new_mass(mass1, mass2):
    Mass = []
    for i in range(len(mass1)):
        Mass.append(mass1[i])

    for i in range(len(mass2)):
        Mass.append(mass2[i])

    sorted_mass = sort_mass(Mass)
    return sorted_mass

def sort_mass(Tab_and_p):
    for i in range(len(Tab_and_p) - 1):
        for j in range(len(Tab_and_p) - i - 1):
            if Tab_and_p[j].points > Tab_and_p[j + 1].points:
                Tab_and_p[j], Tab_and_p[j + 1] = Tab_and_p[j + 1], Tab_and_p[j]

    print('\n')
    for i in range(len(Tab_and_p)):
        print(repr(Tab_and_p[i]) + ' ')

    return Tab_and_p

def check(Player_cards, Table_cards):

    global results
    Tab_and_p = new_mass(Player_cards, Table_cards)

#Алгоритм поиска Старшей карты
    for i in range(-1, -1*len(Tab_and_p), -1):
        if (Tab_and_p[i].set != 't'):
            if (Player_cards == Player1_cards):
                results['p1'] = Combination['High card']
                results['p1 points'] = Tab_and_p[i].points
            elif (Player_cards == Player2_cards):
                results['p2'] = Combination['High card']
                results['p2 points'] = Tab_and_p[i].points
            print('Старшая карта')
            break

#Алгоритм поиска Пары карт
    for i in range(1, len(Tab_and_p)):
        if (Tab_and_p[i].val == Tab_and_p[i-1].val and Tab_and_p[i].set != Tab_and_p[i-1].set):
            if (Player_cards == Player1_cards):
                results['p1'] = Combination['Pair']
                results['p1 points'] = (Tab_and_p[i].points + Tab_and_p[i-1].points)
            elif (Player_cards == Player2_cards):
                results['p2'] = Combination['Pair']
                results['p2 points'] = (Tab_and_p[i].points + Tab_and_p[i-1].points)
            print('Пара')
            break

#Алгоритм поиска Двух Пар карт
    for i in range(1, len(Tab_and_p)):
        if (Tab_and_p[i].val == Tab_and_p[i-1].val and Tab_and_p[i].set != Tab_and_p[i-1].set):
            for j in range(i+2, len(Tab_and_p)):
                if (Tab_and_p[j].val == Tab_and_p[j - 1].val and Tab_and_p[j].set != Tab_and_p[j - 1].set):
                    if (Player_cards == Player1_cards):
                        results['p1'] = Combination['Two pair']
                        results['p1 points'] = Tab_and_p[j].points + Tab_and_p[j-1].points + Tab_and_p[i].points + Tab_and_p[i-1].points
                    elif (Player_cards == Player2_cards):
                        results['p2'] = Combination['Two pair']
                        results['p2 points'] += Tab_and_p[j].points + Tab_and_p[j-1].points + Tab_and_p[i].points + Tab_and_p[i-1].points
                print('Две Пары')
            break

#Алгоритм поиска Тройки(Сета)
    for i in range(2, len(Tab_and_p)):
        if ((Tab_and_p[i].val == Tab_and_p[i - 1].val and Tab_and_p[i].val == Tab_and_p[i - 2].val) and (Tab_and_p[i].set != 't' or Tab_and_p[i-1].set != 't' or Tab_and_p[i-2].set != 't')):
            if (Player_cards == Player1_cards):
                results['p1'] = Combination['Three of a Kind']
                results['p1 points'] = Tab_and_p[i].points + Tab_and_p[i-1].points + Tab_and_p[i-2].points
            elif (Player_cards == Player2_cards):
                results['p2'] = Combination['Three of a Kind']
                results['p2 points'] = Tab_and_p[i].points + Tab_and_p[i-1].points + Tab_and_p[i-2].points
            print('Тройка')

#Алгоритм поиска Стрита
    for i in range(4, len(Tab_and_p)):
        if ((Tab_and_p[i].points == Tab_and_p[i-1].points + 1) and (Tab_and_p[i].points == Tab_and_p[i-2].points + 2) and (Tab_and_p[i].points == Tab_and_p[i-3].points + 3) and (Tab_and_p[i].points == Tab_and_p[i-4].points + 4) and (Tab_and_p[i].set != 't' or Tab_and_p[i-1].set != 't' or Tab_and_p[i-2].set != 't' or Tab_and_p[i-3].set != 't' or Tab_and_p[i-4].set != 't')):
            if (Player_cards == Player1_cards):
                results['p1'] = Combination['Straight']
                results['p1 points'] = Tab_and_p[i].points + Tab_and_p[i-1].points + Tab_and_p[i-2].points + Tab_and_p[i-3].points + Tab_and_p[i-4].points
            elif (Player_cards == Player2_cards):
                results['p2'] = Combination['Straight']
                results['p2 points'] = Tab_and_p[i].points + Tab_and_p[i-1].points + Tab_and_p[i-2].points + Tab_and_p[i-3].points + Tab_and_p[i-4].points
            print('Стрит')

#Алгоритм поиска Флэша
    for i in range(4, len(Tab_and_p)):
        if ((Tab_and_p[i].suit == Tab_and_p[i-1].suit) and (Tab_and_p[i].suit == Tab_and_p[i-2].suit) and (Tab_and_p[i].suit == Tab_and_p[i-3].suit) and (Tab_and_p[i].suit == Tab_and_p[i-4].suit) and (Tab_and_p[i].set != 't' or Tab_and_p[i-1].set != 't' or Tab_and_p[i-2].set != 't' or Tab_and_p[i-3].set != 't' or Tab_and_p[i-4].set != 't')):
            if (Player_cards == Player1_cards):
                results['p1'] = Combination['Flush']
                results['p1 points'] = Tab_and_p[i].points + Tab_and_p[i-1].points + Tab_and_p[i-2].points + Tab_and_p[i-3].points + Tab_and_p[i-4].points
            elif (Player_cards == Player2_cards):
                results['p2'] = Combination['Flush']
                results['p2 points'] = Tab_and_p[i].points + Tab_and_p[i-1].points + Tab_and_p[i-2].points + Tab_and_p[i-3].points + Tab_and_p[i-4].points
            print('Флэш')

#Алгоритм поиска Фулл Хауса, начиная с Пары
    for i in range(1, len(Tab_and_p)):
        if (Tab_and_p[i].val == Tab_and_p[i-1].val and Tab_and_p[i].set != Tab_and_p[i-1].set):
            if (len(Tab_and_p) - 1 - i > 2):
                for j in range(i+3, len(Tab_and_p)):
                    if ((Tab_and_p[j].val == Tab_and_p[j - 1].val and Tab_and_p[j].val == Tab_and_p[j - 2].val) and (Tab_and_p[j].set != 't' or Tab_and_p[j-1].set != 't' or Tab_and_p[j-2].set != 't')):
                        if (Player_cards == Player1_cards):
                            results['p1'] = Combination['Full House']
                            results['p1 points'] = Tab_and_p[i].points + Tab_and_p[i - 1].points + Tab_and_p[j].points + Tab_and_p[j - 1].points + Tab_and_p[j - 2].points
                        elif (Player_cards == Player2_cards):
                            results['p2'] = Combination['Full House']
                            results['p2 points'] = Tab_and_p[i].points + Tab_and_p[i - 1].points + Tab_and_p[j].points + Tab_and_p[j - 1].points + Tab_and_p[j - 2].points
                        print('Фулл Хаус')

#Алгоритм поиска Фулл Хауса, начиная с Тройки(Сета)
    for i in range(2, len(Tab_and_p)):
        if ((Tab_and_p[i].val == Tab_and_p[i - 1].val and Tab_and_p[i].val == Tab_and_p[i - 2].val) and (Tab_and_p[i].set != 't' or Tab_and_p[i-1].set != 't' or Tab_and_p[i-2].set != 't')):

            if (len(Tab_and_p) - 1 - i > 1):
                for j in range(i+2, len(Tab_and_p)):
                    if (Tab_and_p[j].val == Tab_and_p[j - 1].val and Tab_and_p[j].set != Tab_and_p[j - 1].set):
                        if (Player_cards == Player1_cards):
                            results['p1'] = Combination['Full House']
                            results['p1 points'] = Tab_and_p[j].points + Tab_and_p[j - 1].points + Tab_and_p[i].points + Tab_and_p[i - 1].points + Tab_and_p[i - 2].points
                        elif (Player_cards == Player2_cards):
                            results['p2'] = Combination['Full House']
                            results['p2 points'] = Tab_and_p[j].points + Tab_and_p[j - 1].points + Tab_and_p[i].points + Tab_and_p[i - 1].points + Tab_and_p[i - 2].points
                        print('Фулл Хаус')

#Алгоритм поиска Каре
    for i in range(3, len(Tab_and_p)):
        if ((Tab_and_p[i].val == Tab_and_p[i-1].val and Tab_and_p[i].val == Tab_and_p[i-2].val and Tab_and_p[i].val == Tab_and_p[i-3].val) and (Tab_and_p[i] != 't' or Tab_and_p[i-1] != 't' or Tab_and_p[i-2] != 't' or Tab_and_p[i-3] != 't')):
            if (Player_cards == Player1_cards):
                results['p1'] = Combination['Four of a Kind']
                results['p1 points'] = Tab_and_p[i].points + Tab_and_p[i - 1].points + Tab_and_p[i-2].points + Tab_and_p[i - 3].points
            elif (Player_cards == Player2_cards):
                results['p2'] = Combination['Four of a Kind']
                results['p2 points'] = Tab_and_p[i].points + Tab_and_p[i - 1].points + Tab_and_p[i-2].points + Tab_and_p[i - 3].points
            print('Каре')

#Алгоритм поиска Стрит-Флэша
    for i in range(4, len(Tab_and_p)):
        if ((Tab_and_p[i].points == Tab_and_p[i-1].points - 1 and Tab_and_p[i].points == Tab_and_p[i-2].points - 2 and Tab_and_p[i].points == Tab_and_p[i-3].points - 3 and Tab_and_p[i].points == Tab_and_p[i-4].points - 4) and (Tab_and_p[i].suit == Tab_and_p[i-1].suit and Tab_and_p[i].suit == Tab_and_p[i-2].suit and Tab_and_p[i].suit == Tab_and_p[i-3].suit and Tab_and_p[i].suit == Tab_and_p[i-4].suit)):
            if (Player_cards == Player1_cards):
                results['p1'] = Combination['Straight-flush']
                results['p1 points'] = Tab_and_p[i].points + Tab_and_p[i-1].points + Tab_and_p[i-2].points + Tab_and_p[i-3].points + Tab_and_p[i-4].points
            elif (Player_cards == Player2_cards):
                results['p2'] = Combination['Straight-flush']
                results['p2 points'] = Tab_and_p[i].points + Tab_and_p[i-1].points + Tab_and_p[i-2].points + Tab_and_p[i-3].points + Tab_and_p[i-4].points
            print('Стрит-Флэш')

#Алгоритм поиска Флэш-Рояля
    for i in range(4, len(Tab_and_p)):
        if (Tab_and_p[i].val == 'Ace' and (Tab_and_p[i].points == Tab_and_p[i-1].points - 1 and Tab_and_p[i].points == Tab_and_p[i-2].points - 2 and Tab_and_p[i].points == Tab_and_p[i-3].points - 3 and Tab_and_p[i].points == Tab_and_p[i-4].points - 4) and (Tab_and_p[i].suit == Tab_and_p[i-1].suit and Tab_and_p[i].suit == Tab_and_p[i-2].suit and Tab_and_p[i].suit == Tab_and_p[i-3].suit and Tab_and_p[i].suit == Tab_and_p[i-4].suit)):
            if (Player_cards == Player1_cards):
                results['p1'] = Combination['Straight-flush']
                results['p1 points'] = Tab_and_p[i].points + Tab_and_p[i-1].points + Tab_and_p[i-2].points + Tab_and_p[i-3].points + Tab_and_p[i-4].points
            elif (Player_cards == Player2_cards):
                results['p2'] = Combination['Straight-flush']
                results['p2 points'] = Tab_and_p[i].points + Tab_and_p[i-1].points + Tab_and_p[i-2].points + Tab_and_p[i-3].points + Tab_and_p[i-4].points
            print('Флэш-Рояль')


def end_game():

    bckgrnd = pygame.image.load('end_game_background.png')

    global results
    check(Player1_cards, Table_cards)
    check(Player2_cards, Table_cards)

    restart_btn = Button(280, 70)
    back_to_menu_btn = Button(290, 70)

    end = True
    while end:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.blit(bckgrnd, (0, 0))
        restart_btn.draw(display_width / 2 - 150, display_height / 2 - 65, 'Играть заново', settings, (0, 0, 0), 40, 10, 15)
        back_to_menu_btn.draw(display_width / 2 - 155, display_height / 2 + 50, 'Выйти из игры', show_menu, (0, 0, 0), 40, 10, 15)

        output_text('КОНЕЦ ИГРЫ', display_width / 2 - 200, display_height / 2 - 210, (0, 0, 0), font_size = 60)

        if results['p1'] == results['p2']:
            if results['p1 points'] == results['p2 points']:
                output_text('Ничья', display_width / 2 - 100, display_height / 2 - 130, (0, 0, 0))
            elif results['p1 points'] > results['p2 points']:
                output_text('Первый игрок выиграл', display_width / 2 - 150, display_height / 2 - 130, (0, 0, 0))
            elif results['p1 points'] < results['p2 points']:
                output_text('Второй игрок выиграл', display_width / 2 - 150, display_height / 2 - 130, (0, 0, 0))
        elif results['p1'] > results['p2']:
            output_text('Первый игрок выиграл', display_width/2 - 150, display_height/2 - 130, (0, 0, 0))
        elif results['p1'] < results['p2']:
            output_text('Второй игрок выиграл', display_width/2 - 150, display_height/2 - 130, (0, 0, 0))

        pygame.display.update()


def output_text(message, x, y, font_color, font_type = 'times-new-roman.ttf', font_size = 30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))

show_menu()

pygame.quit()
quit()