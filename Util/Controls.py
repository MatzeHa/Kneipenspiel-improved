import pygame
import sys

#nötig??
from Scripts.Util.QuitGame import quit_game
from Scripts.Util.DirCheck import dir_check
from Scripts.Util.Obstacles import Radio

pygame.init()
pygame.key.set_repeat()


def controls_pause(pause_menu):
    run = True

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            quit_game()
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            pause_menu.do_action_mouse(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit_game()

            elif event.key == pygame.K_UP:
                pygame.key.set_repeat(500, 100)

                pause_menu.selected = pause_menu.selected[1:] + pause_menu.selected[:1]
                while pause_menu.nr_selectables[pause_menu.selected.index(1)] == 0:
                    pause_menu.selected = pause_menu.selected[1:] + pause_menu.selected[:1]

            elif event.key == pygame.K_DOWN:
                pygame.key.set_repeat(500, 100)

                pause_menu.selected = pause_menu.selected[-1:] + pause_menu.selected[:-1]
                while pause_menu.nr_selectables[pause_menu.selected.index(1)] == 0:
                    pause_menu.selected = pause_menu.selected[-1:] + pause_menu.selected[:-1]

            elif event.key == pygame.K_RETURN:
                pause_menu.do_action("return")

            elif event.key == pygame.K_LEFT:
                inst = pause_menu.clickables[pause_menu.screen][pause_menu.selected.index(1)]
                if isinstance(inst, pause_menu.Slider):
                    if inst.val >= 1:
                        inst.val = inst.val - 1

            elif event.key == pygame.K_RIGHT:
                inst = pause_menu.clickables[pause_menu.screen][pause_menu.selected.index(1)]
                if isinstance(inst, pause_menu.Slider):
                    if inst.val < 255:
                        inst.val = inst.val + 1
    return run

def check_location_change():

    pass

def controls_game(setup, g, lvl):
    check_location_change()

    run = True
    walk = True
    if not g.guy.ingame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_game()
                elif event.key == pygame.K_p:
                    setup.pause_menu.active = True
                    setup.pause_menu.start_pause = True
                    walk = False
                # Bestellen

                elif event.key == pygame.K_e:
                    walk = False
                    active_inter = dir_check(g.interactables, g.guy)
                    if active_inter != 0:
                        if active_inter.art == "door":
                            active_inter.activated = True
                            g.guy.travel = active_inter.goto


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

                elif event.key == pygame.K_d:
                    walk = False
                    # wenn noch was im glas ist  und  die animation des letzten schlucks beendet ist
                    if g.guy.sips > 0 and g.guy.sipCount == 8:
                        g.guy.drink_a_sip(g.drinks[g.guy.drink][2])

                elif event.key == pygame.K_g:
                    walk = False
                    if g.guy.drink:
                        active_guest = dir_check(g.guests, g.guy)
                        if not active_guest.drink:
                            g.guy.drink = False  # JESUS-MODUS: diese Zeile weglassen...
                            active_guest.drink = g.guy.drink
                            active_guest.sips = g.guy.sips
                            active_guest.text = 'Oha! Danke?'
                            active_guest.text_count = 0

                elif event.key == pygame.K_i:
                    walk = False
                    inventory_active = not inventory_active

                elif event.key == pygame.K_l:
                    walk = False
                    g.guy.drunkenness -= 10
                    if g.guy.drunkenness < 0:
                        g.guy.drunkenness = 0

                elif event.key == pygame.K_t:
                    walk = False
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

                elif event.key == pygame.K_o:
                    walk = False
                    if g.guy not in g.waiter[0].orders_open.keys():
                        if g.guy.sit:
                            g.waiter[0].orders_open.update({g.guy: [0, 0, 0]})
                            g.guy.orderActive = True
                            g.guy.orderAction = 0
                        else:
                            g.guy.text = 'Ich sollte mich besser erstmal setzen.'
                            g.guy.text_count = -1

                elif event.key == pygame.K_m:
                    walk = False
                    if not g.guy.ingame:
                        players = []
                        if g.guy.sit:
                            players = [guest for guest in g.guests if guest.sit and guest.chair.nr == g.guy.table]
                        if players:
                            from Scripts.Minigames.GameMaxle import GameMaxle

                            g.guy.ingame = True
                            g.guy.game = "maxle"
                            g.guy.start_game = True
                            setup.game_maxle = GameMaxle(g.guy, players, g.drinks)
        # Laufen
        if walk:
            run, game_maxle, inventory_active = controls_walking(setup, g)

            #        if game_maxle:
            #            self.game_maxle = game_maxle
    return run

def controls_order(g):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()
        if event.type == pygame.KEYDOWN:
#            if event.key == pygame.K_ESCAPE:
#                g.dialog_menu.quit = True

            if g.guy.orderAction == 5 or g.guy.orderAction == 6:
                if event.key == pygame.K_DOWN:
                    if g.order_menue.choice < len(g.order_menue.drinks) - 1:
                        g.order_menue.choice += 1
                elif event.key == pygame.K_UP:
                    if g.order_menue.choice > 0:
                        g.order_menue.choice -= 1
                elif event.key == pygame.K_e:
                    g.waiter[0].orders_open[g.guy][1] = g.order_menue.choice + 1
                    g.guy.orderAction = 7
    return g

def controls_dialog(dialog_menu):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                dialog_menu.quit = True
            # Talken
            if event.key == pygame.K_UP:
                if dialog_menu.choice > 0:
                    dialog_menu.choice -= 1
            elif event.key == pygame.K_DOWN:
                if dialog_menu.choice < len(dialog_menu.dlst[dialog_menu.Line][1]) - 1:
                    dialog_menu.choice += 1
            elif event.key == pygame.K_q:
                dialog_menu.Line = 0
            elif event.key == pygame.K_e:
                if isinstance(dialog_menu.dlst[dialog_menu.Line][1], tuple):
                    dialog_menu.Line = dialog_menu.dlst[dialog_menu.Line][2][dialog_menu.choice]
                    dialog_menu.choice = 0
    return dialog_menu

def controls_walking(setup, g):
    game_maxle = False
    inventory_active = False
    run = True
#    pygame.key.set_repeat(100, 10)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        g.guy.sit = False
        g.guy.facing = 0
        g.guy.dir = 0
        g.guy.walk(g.waiter + g.guests, g.obstacles, g.interactables, setup)
    elif keys[pygame.K_DOWN]:
        g.guy.sit = False
        g.guy.facing = 2
        g.guy.dir = 2
        g.guy.walk(g.waiter + g.guests, g.obstacles, g.interactables, setup)
    if keys[pygame.K_RIGHT]:
        g.guy.sit = False
        g.guy.facing = 1
        g.guy.dir = 1
        g.guy.walk(g.waiter + g.guests, g.obstacles, g.interactables, setup)
    elif keys[pygame.K_LEFT]:
        g.guy.sit = False
        g.guy.facing = 3
        g.guy.dir = 3
        g.guy.walk(g.waiter + g.guests, g.obstacles, g.interactables, setup)

    else:
        g.guy.walking = False
        g.guy.walkCount = 0
    if g.guy.dead:
        run = False

    return run, game_maxle, inventory_active


def controls_maxle(game, guy, drinks):
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            quit_game()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.quit = True
            if event.key == pygame.K_w:
                if game.p_on_turn == 0 and game.do_action != "thrown" and game.do_action != "doubt":
                    game.do_action = "dice"
            if event.key == pygame.K_a:
                if game.p_on_turn == 0 and not game.first_round and game.do_action != "thrown" and \
                        game.do_action != "dice" and game.do_action != "doubt":
                    game.do_action = "doubt"
            if game.do_action == "thrown":
                if event.key == pygame.K_UP:
                    game.incr_dice()
                if event.key == pygame.K_DOWN:
                    game.decr_dice()
                if event.key == pygame.K_RIGHT:
                    game.dice_chose = 1
                if event.key == pygame.K_LEFT:
                    game.dice_chose = 0
                if event.key == pygame.K_e:
                    if not game.first_round:
                        game.player_called = True
    return game

''''

def controls_game(player, pause_menu, setup):
    _run = True

    player.move_h = 0
    player.move_v = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            _run = False

        if event.type == pygameKEYDOWN:
            pygame.key.set_repeat(200, 100)
            if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                if pause_menu.active:
                    pause_menu.end_pause_fun(setup)
                else:
                    pause_menu.active = True

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


def controls_pause(pause_menu):
    _run = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            _run = False
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            pause_menu.do_action_mouse(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
        if event.type == pygame.KEYDOWN:
            # pygame.key.set_repeat(0, 0)

            if event.key == pygame.K_UP:
                pause_menu.selected = pause_menu.selected[1:] + pause_menu.selected[:1]
                while pause_menu.nr_selectables[pause_menu.selected.index(1)] == 0:
                    pause_menu.selected = pause_menu.selected[1:] + pause_menu.selected[:1]

            elif event.key == pygame.K_DOWN:
                pause_menu.selected = pause_menu.selected[-1:] + pause_menu.selected[:-1]
                while pause_menu.nr_selectables[pause_menu.selected.index(1)] == 0:
                    pause_menu.selected = pause_menu.selected[-1:] + pause_menu.selected[:-1]

            elif event.key == pygame.K_RETURN:
                pause_menu.do_action("return")

            elif event.key == pygame.K_LEFT:
                inst = pause_menu.clickables[pause_menu.screen][pause_menu.selected.index(1)]
                if isinstance(inst, pause_menu.Slider):
                    if inst.val >= 1:
                        inst.val = inst.val - 1

            elif event.key == pygame.K_RIGHT:
                inst = pause_menu.clickables[pause_menu.screen][pause_menu.selected.index(1)]
                if isinstance(inst, pause_menu.Slider):
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

