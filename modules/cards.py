from modules.constants import *
import random

cardback = pygame.image.load("./assets/cards/ac.png")
clover_a = (pygame.image.load("./assets/cards/ac.png"), 11)
clover2 = (pygame.image.load("./assets/cards/2c.png"), 2)
clover3 = (pygame.image.load("./assets/cards/3c.png"), 3)
clover4 = (pygame.image.load("./assets/cards/4c.png"), 4)
clover5 = (pygame.image.load("./assets/cards/5c.png"), 5)
clover6 = (pygame.image.load("./assets/cards/6c.png"), 6)
clover7 = (pygame.image.load("./assets/cards/7c.png"), 7)
clover8 = (pygame.image.load("./assets/cards/8c.png"), 8)
clover9 = (pygame.image.load("./assets/cards/9c.png"), 9)
clover10 = (pygame.image.load("./assets/cards/10c.png"), 9)
clover_j = (pygame.image.load("./assets/cards/jc.png"), 10)
clover_k = (pygame.image.load("./assets/cards/kc.png"), 10)
clover_q = (pygame.image.load("./assets/cards/qc.png"), 10)
diamond_a = (pygame.image.load("./assets/cards/ad.png"), 11)
diamond_2 = (pygame.image.load("./assets/cards/2d.png"), 2)
diamond_3 = (pygame.image.load("./assets/cards/3d.png"), 3)
diamond_4 = (pygame.image.load("./assets/cards/4d.png"), 4)
diamond_5 = (pygame.image.load("./assets/cards/5d.png"), 5)
diamond_6 = (pygame.image.load("./assets/cards/6d.png"), 6)
diamond_7 = (pygame.image.load("./assets/cards/7d.png"), 7)
diamond_8 = (pygame.image.load("./assets/cards/8d.png"), 8)
diamond_9 = (pygame.image.load("./assets/cards/9d.png"), 9)
diamond_10 = (pygame.image.load("./assets/cards/10d.png"), 10)
diamond_j = (pygame.image.load("./assets/cards/jd.png"), 10)
diamond_k = (pygame.image.load("./assets/cards/kd.png"), 10)
diamond_q = (pygame.image.load("./assets/cards/qd.png"), 10)
heart_a = (pygame.image.load("./assets/cards/ah.png"), 11)
heart_2 = (pygame.image.load("./assets/cards/2h.png"), 2)
heart_3 = (pygame.image.load("./assets/cards/3h.png"), 3)
heart_4 = (pygame.image.load("./assets/cards/4h.png"), 4)
heart_5 = (pygame.image.load("./assets/cards/5h.png"), 5)
heart_6 = (pygame.image.load("./assets/cards/6h.png"), 6)
heart_7 = (pygame.image.load("./assets/cards/7h.png"), 7)
heart_8 = (pygame.image.load("./assets/cards/8h.png"), 8)
heart_9 = (pygame.image.load("./assets/cards/9h.png"), 9)
heart_10 = (pygame.image.load("./assets/cards/10h.png"), 10)
heart_j = (pygame.image.load("./assets/cards/jh.png"), 10)
heart_k = (pygame.image.load("./assets/cards/kh.png"), 10)
heart_q = (pygame.image.load("./assets/cards/qh.png"), 10)
spade_a = (pygame.image.load("./assets/cards/as.png"), 11)
spade_2 = (pygame.image.load("./assets/cards/2s.png"), 2)
spade_3 = (pygame.image.load("./assets/cards/3s.png"), 3)
spade_4 = (pygame.image.load("./assets/cards/4s.png"), 4)
spade_5 = (pygame.image.load("./assets/cards/5s.png"), 5)
spade_6 = (pygame.image.load("./assets/cards/6s.png"), 6)
spade_7 = (pygame.image.load("./assets/cards/7s.png"), 7)
spade_8 = (pygame.image.load("./assets/cards/8s.png"), 8)
spade_9 = (pygame.image.load("./assets/cards/9s.png"), 9)
spade_10 = (pygame.image.load("./assets/cards/10s.png"), 10)
spade_j = (pygame.image.load("./assets/cards/js.png"), 10)
spade_k = (pygame.image.load("./assets/cards/ks.png"), 10)
spade_q = (pygame.image.load("./assets/cards/qs.png"), 10)

cards = [clover_a, clover2, clover3, clover4, clover5, clover6, clover7, clover8, clover9, clover10, clover_j, clover_k, clover_q,
         diamond_a, diamond_2, diamond_3, diamond_4, diamond_5, diamond_6, diamond_7, diamond_8, diamond_9, diamond_10, diamond_j, diamond_k, diamond_q,
         heart_a, heart_2, heart_3, heart_4, heart_5, heart_6, heart_7, heart_8, heart_9, heart_10, heart_j, heart_k, heart_q,
         spade_a, spade_2, spade_3, spade_4, spade_5, spade_6, spade_7, spade_8, spade_9, spade_10, spade_j, spade_k, spade_q,]


class Player:
    def __init__(self):
        self.hand = []

    def calclulate_card_values(self):
        total = 0
        for card in self.hand:
            total += card.card_value


class Dealer:
    def __init__(self):
        self.hand = [Card(), Card()]
        self.card_down_img = cardback


# PROGRAM ABILITY FOR ACE TO BE 1 OR 11
class Card:
    def __init__(self):
        self.card_highlighted = False
        self.card_rect = pygame.Rect(WIDTH // 2 - 150 // 2, HEIGHT - 150, 125, 200)
        self.card_type = random.choice(cards)
        self.card_value = self.card_type[1]
        self.card_img = pygame.transform.scale(self.card_type[0], (self.card_rect.width, self.card_rect.height))
        self.x_position = 0

    def raise_height(self):
        if self.card_rect.y - 10 != HEIGHT - 220:
            self.card_rect.y -= 10

    def lower_height(self):
        if not (self.card_rect.y + self.card_rect.height) + 10 > HEIGHT + 50:
            self.card_rect.y += 10

    def draw(self):
        WINDOW.blit(self.card_img, (self.card_rect.x, self.card_rect.y))


