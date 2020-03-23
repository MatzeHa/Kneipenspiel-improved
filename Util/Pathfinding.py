def pathfinding(char, coords, win_sizex, win_sizey, wall_sizex, wall_sizey, obstacles, interactables,
                pos_goals, cell_size):
    # Wenn Ober kein Ziel hat, läuft er zu zufälligem Ziel
    if char.goal == ():
        char.goal = (coords["w"][pos_goals[0]], coords["h"][pos_goals[1]])

    # erstelle dictionary, in der die Wegkosten gespeichert werden
    costs = {}
    invest = []
    for i in coords["w"][slice(0, int((win_sizex - wall_sizex * 2) / cell_size))]:
        for j in coords["h"][slice(0, int((win_sizey - wall_sizey * 2) / cell_size))]:
            # Die Wegkosten aller Felder werden auf -10 gesetzt
            costs.update({(i, j): -10})
    # Liste mit Startwert
    s = [(char.x,  char.y)]
    # Startpunkt wird auf Kosten 0 gesetzt
    costs[s[0]] = 0
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]             # up right down left

    # Berechnung der kostenwerte für alle felder
    run = 1
    # solange die Kosten des Zielfeldes -10 sind,
    while costs[char.goal[0], char.goal[1]] == -10:
        # soll die Funktion vom Startpunkt s für die 4 angrenzenden Felder
        for _s in s:
            for i in directions:
                # überprüfen ob es ein Wand-'Feld' ist und
                if wall_sizex <= _s[0] + i[0] * cell_size < win_sizex - wall_sizex and \
                        wall_sizey <= _s[1] + i[1] * cell_size < win_sizey - wall_sizey:
                    # ob das Feld bereits geprüft wurde
                    if costs[(_s[0] + i[0] * cell_size, _s[1] + i[1] * cell_size)] == -10:
                        if not (_s[0] + i[0] * cell_size, _s[1] + i[1] * cell_size) in invest:
                            # hänge Tupel mit coords der Zelle an die Liste an
                            invest.append((_s[0] + i[0] * cell_size, _s[1] + i[1] * cell_size))
        s = []
        # Wenn Obstacle auf Feld: Kosten = -1
        for i in invest:
            obst_collide = False
            for obst in obstacles + interactables:
                if not obst.walkable:
                    if obst.x + obst.width > i[0] >= obst.x and \
                            obst.y + obst.height > i[1] >= obst.y:
                        if char.chair != obst:
                            obst_collide = True
                            costs[i] = -1
                            break

            # Wenn Feld frei: Kosten des Felds = um eins höher als das Vorherige
            if not obst_collide:
                s.append(i)
                costs[i] = run

        run += 1

        invest = []

    # Zielfeld
    z = (char.goal[0], char.goal[1])

    i = ()
    for step in range(0, costs[(z[0], z[1])]):
        for i in directions:
            if wall_sizex <= z[0] + i[0] * cell_size < win_sizex - wall_sizex and \
                    wall_sizey <= z[1] + i[1] * cell_size < win_sizey - wall_sizey:
                # wenn kosten am günstigsten sind
                if costs[(z[0] + i[0] * cell_size, z[1] + i[1] * cell_size)] == costs[(z[0], z[1])] - 1:
                    # je nach geschwindigkeit muss step mehrmals gegangen werden
                    for j in range(0, int(cell_size / char.vel)):
                        char.steps.append((i[0], i[1]))
                    break
        z = (z[0] + i[0] * cell_size, z[1] + i[1] * cell_size)
    char.goal = ()
