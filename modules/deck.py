from modules.constants import *


class Card:
    def __init__(self, card_type):
        self.card_highlighted = False
        self.card_colors = {"Darker Green": DARKER_GREEN, "Red": RED, "Black": BLACK, "White": WHITE, "Green": GREEN}  # Represent different types of cards as colors for now
        self.card_type = card_type
        self.card_color = self.card_colors[self.card_type]
        self.card_rect = pygame.Rect(WIDTH // 2 - 150 // 2, HEIGHT - 150, 125, 200)
        self.x_position = 0

    def raise_height(self):
        if self.card_rect.y - 10 != HEIGHT - 220:
            self.card_rect.y -= 10

    def lower_height(self):
        if not (self.card_rect.y + self.card_rect.height) + 10 > HEIGHT + 50:
            self.card_rect.y += 10

    def draw(self):
        pygame.draw.rect(WINDOW, self.card_color, self.card_rect, 0)
