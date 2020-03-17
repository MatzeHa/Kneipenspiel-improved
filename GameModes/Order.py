import pygame

pygame.init()

font = pygame.font.SysFont('Courier', 30, True)
talk_font = pygame.font.SysFont('Courier', 20, True)
order_font = pygame.font.SysFont('Courier', 30, True)
order_choose_font = pygame.font.SysFont('Courier', 33, True)
order_choose_font.set_underline(True)

Order_pic = pygame.image.load('../Graph/GUI/order.png')

textcount_max = 51


class OrderMenue:
    def __init__(self, drinks):
        self.drinks = drinks
        self.choice = 0
        self.choice_name = ''
        self.x = 500
        self.y = 100
        self.AC = 20  # = AnimationCounter

    def draw(self, win, setup, g, lvl):
        # Karten-Animation
        if self.AC > 3:
            self.AC -= 1
            self.y = setup.win_h - setup.win_h * 0.9 * (3 / self.AC)
            print(self.y)
        # Darstellung der Karte
        # win.blit(lvl.win_copy, (0, 0))
        win.blit(Order_pic, (self.x, self.y))
        dirtyrect = pygame.Rect(self.x, self.y, Order_pic.get_width(), Order_pic.get_height())
        j = 0
        # Darstellung des Texte
        for k in self.drinks.keys():
            print(k)
            if k != 0:
                i = self.drinks[k][0]
                if self.choice == j:
                    text = order_choose_font.render(str(i), 1, (0, 0, 0))
                    win.blit(text, (self.x + 100, self.y + 300 + 100 * j))
                    preis = order_choose_font.render(str(self.drinks[k][1]), 1, (0, 0, 0))
                    win.blit(preis, (self.x + 700, self.y + 300 + 100 * j))
                    self.choice_name = str(i)
                else:
                    text = order_font.render(str(i), 1, (0, 0, 0))
                    win.blit(text, (self.x + 100, self.y + 300 + 100 * j))
                    preis = order_font.render(str(self.drinks[k][1]), 1, (0, 0, 0))
                    win.blit(preis, (self.x + 700, self.y + 300 + 100 * j))
                j += 1
        return dirtyrect

#    def del_order(self, win, win_copy):
#        dirtyrect = pygame.Rect(self.x, self.y, Order_pic.get_width(), Order_pic.get_height())
#        win.blit(win_copy, (dirtyrect.x, dirtyrect.y), dirtyrect)
#        return(dirtyrect)
