import pygame
import sys

from Util.QuitGame import quit_game
from Util.DirCheck import dir_check
from Util.Obstacles import Radio
from Minigames.GameMaxle import GameMaxle

pygame.init()


def controls_pause(pause_menu):
    print("controls Pause")
    pass


def controls_game(setup, g):
    run = True
    kitchen = False
    if g.guy.ingame:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                quit_game()
                # game_maxle_control(self.game_maxle, keys, g.guy, g.drinks) # TODO: umbaun
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            # Bestellen
            if g.guy.orderAction == 5 or g.guy.orderAction == 6:
                if keys[pygame.K_DOWN]:
                    if g.order_menue.choice < len(g.order_menue.drinks) - 1:
                        g.order_menue.choice += 1
                if keys[pygame.K_UP]:
                    if g.order_menue.choice > 0:
                        g.order_menue.choice -= 1
                if keys[pygame.K_e]:
                    g.waiter[0].orders_open[g.guy][1] = g.order_menue.choice + 1
                    g.guy.orderAction = 7

            # Talken
            elif g.guy.talk_action == 2:
                if keys[pygame.K_UP]:
                    if g.dialog_menue.choice > 0:
                        g.dialog_menue.choice -= 1
                if keys[pygame.K_DOWN]:
                    if g.dialog_menue.choice < len(g.dialog_menue.dlst[g.dialog_menue.Line][1]) - 1:
                        g.dialog_menue.choice += 1
                if keys[pygame.K_q]:
                    g.dialog_menue.Line = 0
                if keys[pygame.K_e]:
                    if isinstance(g.dialog_menue.dlst[g.dialog_menue.Line][1], tuple):
                        g.dialog_menue.Line = g.dialog_menue.dlst[g.dialog_menue.Line][2][g.dialog_menue.choice]
                        g.dialog_menue.choice = 0

            # Laufen
            else:
                run, game_maxle, inventory_active, kitchen = controls_walking(setup, g)


        #        if game_maxle:
        #            self.game_maxle = game_maxle
    return run, kitchen


def controls_walking(setup, g):
    kitchen = False
    game_maxle = False
    inventory_active = False
    run = True
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            quit_game()
    pygame.event.pump()

    if keys[pygame.K_UP]:
        g.guy.sit = False
        g.guy.facing = 0
        g.guy.dir = 0
        g.guy.walk(g.waiter + g.guests, g.obstacles, g.interactables, setup)
    elif keys[pygame.K_RIGHT]:
        g.guy.sit = False
        g.guy.facing = 1
        g.guy.dir = 1
        g.guy.walk(g.waiter + g.guests, g.obstacles, g.interactables, setup)
    elif keys[pygame.K_DOWN]:
        g.guy.sit = False
        g.guy.facing = 2
        g.guy.dir = 2
        g.guy.walk(g.waiter + g.guests, g.obstacles, g.interactables, setup)
    elif keys[pygame.K_LEFT]:
        g.guy.sit = False
        g.guy.facing = 3
        g.guy.dir = 3
        g.guy.walk(g.waiter + g.guests, g.obstacles, g.interactables, setup)
    elif keys[pygame.K_e]:
        active_inter = dir_check(g.interactables, g.guy)
        print(active_inter)
        if active_inter != 0:

            if active_inter.art == "door":
                if active_inter.goto == "kitchen":
                    kitchen = True
                    run = False

                active_inter.active = True
                active_inter.openClose = True
            elif active_inter.art == "chair":
                if not g.guy.sit and not active_inter.active:
                    g.guy.sit_down(active_inter)
            #                            for i in dirtyrect:
            #                                dirtyrects.append(i)

            # active_inter.active = True
            #                        else:
            #                            textwin.text_count = 0
            #                            textwin.talker = active_inter.sit
            #                            textwin.text = 'Hey, schubs nicht so!'

            elif isinstance(active_inter, Radio):
                active_inter.active = not active_inter.active
                if active_inter.active:
                    pygame.mixer.music.play(-1)
                else:
                    pygame.mixer.music.stop()
            elif active_inter.art == "chalkboard":
                g.guy.text = 'Angebot der Woche: Willi!'
                g.guy.text_count = 0
    elif keys[pygame.K_d]:
        # wenn noch was im glas ist  und  die animation des letzten schlucks beendet ist
        if g.guy.sips > 0 and g.guy.sipCount == 8:
            g.guy.drink_a_sip(g.drinks[g.guy.drink][2])

    elif keys[pygame.K_g]:
        if g.guy.drink:
            active_guest = dir_check(g.guests, g.guy)
            if not active_guest.drink:
                g.guy.drink = False  # JESUS-MODUS: diese Zeile weglassen...
                active_guest.drink = g.guy.drink
                active_guest.sips = g.guy.sips
                active_guest.text = 'Oha! Danke?'
                active_guest.text_count = 0

    elif keys[pygame.K_i]:
        inventory_active = not inventory_active

    elif keys[pygame.K_l]:
        g.guy.drunkenness -= 10
        if g.guy.drunkenness < 0:
            g.guy.drunkenness = 0

    elif keys[pygame.K_t]:  # talk
        active_guest = dir_check(g.guests, g.guy)
        if active_guest != 0:
            g.guy.talk_action = 1
            g.dialog_menue.chars[1] = active_guest
        if g.guy.sit:
            talkers = [guest for guest in g.guests if guest.sit and guest.chair.nr == g.guy.table]
            if len(talkers) == 1:
                g.guy.talk_action = 1
                g.dialog_menue.chars[1] = talkers[0]
            if len(talkers) > 1:
                g.guy.talk_action = 1
                g.dialog_menue.chars[1] = talkers[0]
                g.dialog_menue.chars[2] = talkers[1]
    elif keys[pygame.K_o]:  # bestellen
        if g.guy not in g.waiter[0].orders_open.keys():
            if g.guy.sit:
                g.waiter[0].orders_open.update({g.guy: [0, 0, 0]})
                g.guy.orderActive = True
                g.guy.orderAction = 0
            else:
                g.guy.text = 'Ich sollte mich besser erstmal setzen.'
                g.guy.text_count = -1
    elif keys[pygame.K_p]:
        if not g.guy.ingame:
            players = []
            if g.guy.sit:
                players = [guest for guest in g.guests if guest.sit and guest.chair.nr == g.guy.table]
            if players:
                game_maxle = GameMaxle(g.guy, players, g.drinks)
                g.guy.ingame = True
                g.guy.start_game = True
    else:
        g.guy.walking = False
        g.guy.walkCount = 0
    if g.guy.dead:
        run = False
    return run, game_maxle, inventory_active, kitchen


def game_maxle_control(game, keys, guy, drinks):
    if keys[pygame.K_w]:
        if game.p_on_turn == 0 and game.do_action != "thrown" and game.do_action != "doubt":
            game.do_action = "dice"
    if keys[pygame.K_a]:
        if game.p_on_turn == 0 and not game.first_round and game.do_action != "thrown" and \
                game.do_action != "dice" and game.do_action != "doubt":
            game.do_action = "doubt"
    if game.do_action == "thrown":
        if keys[pygame.K_UP]:
            game.incr_dice()
        if keys[pygame.K_DOWN]:
            game.decr_dice()
        if keys[pygame.K_RIGHT]:
            game.dice_chose = 1
        if keys[pygame.K_LEFT]:
            game.dice_chose = 0
        if keys[pygame.K_e]:
            if not game.first_round:
                game.player_called = True


''''

def controls_game(player, pause_menue, setup):
    _run = True

    player.move_h = 0
    player.move_v = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            _run = False

        if event.type == pygameKEYDOWN:
            pygame.key.set_repeat(200, 100)
            if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                if pause_menue.active:
                    pause_menue.end_pause_fun(setup)
                else:
                    pause_menue.active = True

    pygame.event.pump()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.move_v = -player.vel
    if keys[pygame.K_DOWN]:
        player.move_v = player.vel
    if keys[pygame.K_RIGHT]:
        player.move_h = player.vel
    if keys[pygame.K_LEFT]:
        player.move_h = -player.vel
    return _run     


def controls_pause(pause_menue):
    _run = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            _run = False
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            pause_menue.do_action_mouse(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
        if event.type == pygame.KEYDOWN:
            # pygame.key.set_repeat(0, 0)

            if event.key == pygame.K_UP:
                pause_menue.selected = pause_menue.selected[1:] + pause_menue.selected[:1]
                while pause_menue.nr_selectables[pause_menue.selected.index(1)] == 0:
                    pause_menue.selected = pause_menue.selected[1:] + pause_menue.selected[:1]

            elif event.key == pygame.K_DOWN:
                pause_menue.selected = pause_menue.selected[-1:] + pause_menue.selected[:-1]
                while pause_menue.nr_selectables[pause_menue.selected.index(1)] == 0:
                    pause_menue.selected = pause_menue.selected[-1:] + pause_menue.selected[:-1]

            elif event.key == pygame.K_RETURN:
                pause_menue.do_action("return")

            elif event.key == pygame.K_LEFT:
                inst = pause_menue.clickables[pause_menue.screen][pause_menue.selected.index(1)]
                if isinstance(inst, pause_menue.Slider):
                    if inst.val >= 1:
                        inst.val = inst.val - 1

            elif event.key == pygame.K_RIGHT:
                inst = pause_menue.clickables[pause_menue.screen][pause_menue.selected.index(1)]
                if isinstance(inst, pause_menue.Slider):
                    if inst.val < 255:
                        inst.val = inst.val + 1
    pygame.event.pump()
    return _run


'''
'''
# Inventar
elif inventory_active:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            pygame.quit()
            run = False
            sys.exit()
    if keys[pygame.K_i]:
        inventory_active = not inventory_active
    redraw_game_window(clock, dirtyrects)
    dirtyrects = []
'''

