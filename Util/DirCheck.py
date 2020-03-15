def dir_check(in_the_way, char):
    active_itw = 0

    for itw in in_the_way:
        # oben
        if char.dir == 0:
            if itw.x < char.x + char.width / 2 < itw.x + itw.width and \
                    itw.y <= char.y - char.height < itw.y + itw.height:
                active_itw = itw
                break
        # rechts
        elif char.dir == 1:
            if itw.y < char.y + char.height / 2 < itw.y + itw.height and \
                    itw.x <= char.x + char.width * 2 - char.vel < itw.x + itw.width:
                active_itw = itw
                break
        # unten
        elif char.dir == 2:
            if itw.x < char.x + char.width / 2 < itw.x + itw.width and \
                    itw.y <= char.y + char.height * 2 - char.vel < itw.y + itw.height:
                active_itw = itw
                break
        # links
        elif char.dir == 3:
            if itw.y < char.y + char.height / 2 < itw.y + itw.height and \
                    itw.x <= char.x - char.width < itw.x + itw.width:
                active_itw = itw
                break
    return active_itw
