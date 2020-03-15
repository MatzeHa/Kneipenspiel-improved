import pygame

pygame.init()

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


def controls_game(player, pause_menue, setup):
    _run = True

    player.m ove_h = 0
    player.move_v = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            _run = False

        if event.type == pygame.KEYDOWN:
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
