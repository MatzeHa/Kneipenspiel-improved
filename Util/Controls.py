import pygame
import sys

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
                g.guy.end_game = True
                # game_maxle_control(self.game_maxle, keys, g.guy, g.drinks) # TODO: umbaun


            # Bestellen
            elif g.guy.orderAction == 5 or g.guy.orderAction == 6:
                keys = pygame.key.get_pressed()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                        pygame.quit()
                        run = False
                        sys.exit()
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
                keys = pygame.key.get_pressed()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                        sys.exit()

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

                dirtyrects = []

            # Laufen
            else:
                keys = pygame.key.get_pressed()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                        sys.exit()
                if keys[pygame.K_UP]:
                    g.guy.dir = 0
                elif keys[pygame.K_RIGHT]:
                    g.guy.dir = 1
                elif keys[pygame.K_DOWN]:
                    g.guy.dir = 2
                elif keys[pygame.K_LEFT]:
                    g.guy.dir = 3

                g.guy.walk(g.waiter + g.guests, g.obstacles, g.interactables, setup)


        #        run, game_maxle, inventory_active, kitchen = laufen(g, self.sv["win_w"], self.sv["win_h"],
        #                                                            self.sv["wall_w"], self.sv["wall_h"])
        #        if game_maxle:
        #            self.game_maxle = game_maxle
    return run, kitchen


def run_lvl(self, win, g):
    run = True
    while run:
        _dirtyrects, run, kitchen = self.redraw_game_window(g)
        g.timer_clock.tick(30)
        pygame.display.update(_dirtyrects)

    if kitchen:
        #            if lvl_kitchen not in locals():
        from Level.CreateKitchen import LVLKitchen
        lvl_kitchen = LVLKitchen(win)
        g.guy.x = lvl_kitchen.sv["coord"]["w"][7]
        g.guy.y = lvl_kitchen.sv["coord"]["h"][0]
        g.guy.facing = 2
        self.g = g
        lvl_kitchen.run_lvl(win, g, self)

    win.blit(self.sv["images"].game_over, (win_w / 2 - 400, win_h / 2 - 232))
    pygame.display.update()
    pygame.quit()

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

