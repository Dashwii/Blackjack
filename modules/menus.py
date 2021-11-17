from modules.constants import *
from modules.deck import Card
import random

color_list = ["Red", "Green", "Black", "Darker Green"]

class MainMenu:
    def __init__(self):
        self.playing = True
        self.game_toggle = False
        self.clock = pygame.time.Clock()

        self.comicsans = pygame.font.SysFont("comcisans", 100)
        self.blackjack_title = self.comicsans.render("Blackjack", True, WHITE)
        self.title_rect = pygame.Rect(WIDTH // 2 - self.blackjack_title.get_width() // 2, -100, self.blackjack_title.get_width(), self.blackjack_title.get_height())


    def game_loop(self):
        title_pos_update = pygame.USEREVENT
        pygame.time.set_timer(title_pos_update, 25)

        while self.playing:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    self.playing = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if keys[pygame.K_g]:
                        self.game_toggle = True
                        self.playing = False
                if event.type == title_pos_update:
                    if self.title_rect.y + 1 != 100:
                        self.title_rect.y += 1
            self.draw()

    def draw(self):
        WINDOW.fill(DARKER_GREEN)
        WINDOW.blit(self.blackjack_title, self.title_rect)
        pygame.display.update()


class GameMenu:
    def __init__(self):
        self.playing = True
        self.clock = pygame.time.Clock()
        self.cards = []
        # half of deck width = 375
        self.mid_width = 750

    def game_loop(self):
        card_animation_interval = pygame.USEREVENT
        pygame.time.set_timer(card_animation_interval, 5)
        [self.cards.append(Card(random.choice(color_list))) for i in range(5)]
        while self.playing:
            self.clock.tick(FPS)
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    self.playing = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if keys[pygame.K_ESCAPE]:
                        self.playing = False
                if event.type == card_animation_interval:
                    self.change_height_of_cards()
                    self.update_x_position_of_cards()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for index, card in enumerate(self.cards):
                        if card.card_rect.collidepoint(mouse):
                            del self.cards[index]

            self.calculate_x_position_of_cards()
            self.check_mouse_over_card(mouse)
            self.draw()

    def check_mouse_over_card(self, mouse_pos):
        for card in self.cards:
            if card.card_rect.collidepoint(mouse_pos):
                card.card_highlighted = True
            else:
                card.card_highlighted = False

    def change_height_of_cards(self):
        for card in self.cards:
            if card.card_highlighted:
                card.raise_height()
            else:
                card.lower_height()

    def calculate_x_position_of_cards(self):
        total_width_of_cards = len(self.cards) * 125
        # Based on how many cards there are multiply the x offset of the card based on its index in the list
        for ix, card in enumerate(self.cards[::-1]):
            card.x_position = total_width_of_cards // 2 + (self.mid_width - card.card_rect.width) - ix * 125

    def update_x_position_of_cards(self):
        for ix, card in enumerate(self.cards[::-1]):
            if card.x_position > card.card_rect.x:
                if not card.card_rect.x + 5 > card.x_position:
                    card.card_rect.x += 5
            elif card.x_position < card.card_rect.x:
                if not card.card_rect.x - 5 < card.x_position:
                    card.card_rect.x -= 5

    def blit_cards(self):
        for card in self.cards:
            card.draw()

    def draw(self):
        WINDOW.fill(BLUE)
        self.blit_cards()
        pygame.display.update()
