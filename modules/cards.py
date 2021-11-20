from modules.constants import *


class Dealer:
    def __init__(self):
        self.hand = []
        self.card_down_img = pygame.transform.scale(cardback, (125, 200))

    def take_card(self, card_type):
        hand_value = sum([card.card_value for card in self.hand])
        card = Card(card_type, 0)
        if card.card_value == 11:
            card.ace_check_value(hand_value)
        self.hand.append(card)


class Card:
    def __init__(self, card_type, y):
        self.card_highlighted = False
        self.card_rect = pygame.Rect(WIDTH // 2 - 150 // 2, y, 125, 200)
        self.card_img = pygame.transform.scale(card_type[0], (self.card_rect.width, self.card_rect.height))
        self.card_value = card_type[1]
        self.x_position = 0

    def ace_check_value(self, hand_value):
        if hand_value + self.card_value > 21:
            self.card_value = 1

    def raise_height(self):
        if self.card_rect.y - 10 != HEIGHT - 220:
            self.card_rect.y -= 10

    def lower_height(self):
        if not (self.card_rect.y + self.card_rect.height) + 10 > HEIGHT + 50:
            self.card_rect.y += 10

    def draw(self):
        WINDOW.blit(self.card_img, (self.card_rect.x, self.card_rect.y))
