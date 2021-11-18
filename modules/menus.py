from modules.constants import *
from modules.cards import Card, Player

text_font = pygame.font.SysFont("comcisans", 100)
chip_text_font = pygame.font.SysFont("comcisans", 50)


class DrawText:
    def __init__(self, font, text, position, color):
        self.font = font
        self.text = text
        self.color = color
        self.text_render = self.font.render(self.text, True, color)
        self.x = position[0] - self.text_render.get_width() // 2
        self.y = position[1]
        self.text_rect = pygame.Rect(self.x, self.y, self.text_render.get_width(), self.text_render.get_height())

    def update_text(self, text):
        self.text = text
        self.text_render = self.font.render(self.text, True, self.color)

    def draw(self):
        WINDOW.blit(self.text_render, self.text_rect)


class Chip:
    colors = {1: WHITE, 10: BLUE, 100: GREEN, 500: RED}
    chip_position = {1: [50, HEIGHT - 325], 10: [225, HEIGHT - 325], 100: [75, HEIGHT - 150], 500: [250, HEIGHT - 150]}

    def __init__(self, value):
        self.value = value
        self.color = Chip.colors[self.value]
        self.x = Chip.chip_position[value][0]
        self.y = Chip.chip_position[value][1]
        self.circle_rect = pygame.Rect(self.x, self.y, 150, 150)
        self.text_number = DrawText(chip_text_font, f"{self.value}", (self.x + (self.circle_rect.width // 2), self.y + (self.circle_rect.height // 2) - 10), BLACK)

    def draw(self):
        pygame.draw.circle(WINDOW, self.color, (self.x + (self.circle_rect.width // 2), self.y + (self.circle_rect.height // 2)), 75)
        self.text_number.draw()


class PlacedChip(Chip):
    def __init__(self, value):
        super().__init__(value)
        self.x = 75
        self.y = 150
        self.circle_rect = pygame.Rect(self.x, self.y, 150, 150)
        self.text_number = DrawText(chip_text_font, f"{self.value}", (self.x + (self.circle_rect.width // 2), self.y + (self.circle_rect.height // 2) - 10), BLACK)


class MainMenu:
    def __init__(self):
        self.playing = True
        self.game_toggle = False
        self.clock = pygame.time.Clock()
        self.blackjack_title = DrawText(text_font, "Blackjack", (WIDTH // 2, -100), WHITE)
        self.play_title = DrawText(text_font, "Play", (WIDTH // 2, HEIGHT // 2), WHITE)

    def game_loop(self):
        title_pos_update = pygame.USEREVENT
        pygame.time.set_timer(title_pos_update, 25)

        while self.playing:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                mouse = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    self.playing = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.play_title.text_rect.collidepoint(mouse):
                        self.game_toggle = True
                        self.playing = False
                if event.type == title_pos_update:
                    if self.blackjack_title.text_rect.y + 1 < 100:
                        self.blackjack_title.text_rect.y += 1
            self.draw()

    def draw(self):
        WINDOW.fill(DARKER_GREEN)
        self.blackjack_title.draw()
        self.play_title.draw()
        pygame.display.update()


class GameMenu:
    def __init__(self):
        self.playing = True
        self.clock = pygame.time.Clock()
        self.bet_amount = 0
        self.money = 2500
        self.money_text = DrawText(chip_text_font, f"Money: ${self.money}", (129, 25), WHITE)
        self.bet_text = DrawText(chip_text_font, f"Bet: ${self.bet_amount}", (72, 75), WHITE)
        self.player = Player()
        self.mid_width = 750
        self.chips = [Chip(1), Chip(10), Chip(100), Chip(500)]
        self.placed_bets = []

    def game_loop(self):
        card_highlight_interval = pygame.USEREVENT
        card_x_pos_update_interval = pygame.USEREVENT + 1
        pygame.time.set_timer(card_highlight_interval, 20)
        pygame.time.set_timer(card_x_pos_update_interval, 1)
        while self.playing:
            self.clock.tick(FPS)
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.playing = False

                if event.type == pygame.KEYDOWN:
                    if keys[pygame.K_ESCAPE]:
                        self.playing = False
                    if keys[pygame.K_SPACE]:
                        self.player.hand.append(Card())

                if event.type == card_highlight_interval:
                    self.change_height_of_cards()

                if event.type == card_x_pos_update_interval:
                    self.update_x_position_of_cards()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for index, card in enumerate(self.player.hand):
                            if card.card_rect.collidepoint(mouse):
                                del self.player.hand[index]
                        for index, chip in enumerate(self.chips):
                            if chip.circle_rect.collidepoint(mouse):
                                placed_chip = Chip(chip.value)
                                placed_chip.circle_rect.y -= 500
                                self.placed_bets.append(PlacedChip(chip.value))
                                self.bet_amount += chip.value
                                self.bet_text.update_text(f"Bet: ${self.bet_amount}")
                                self.money -= chip.value
                                self.money_text.update_text(f"Money: ${self.money}")

                        if len(self.placed_bets) > 0 and self.placed_bets[-1].circle_rect.collidepoint(mouse):
                            placed_chip = self.placed_bets.pop()
                            self.bet_amount -= placed_chip.value
                            self.bet_text.update_text(f"Bet: ${self.bet_amount}")
                            self.money += placed_chip.value
                            self.money_text.update_text(f"Money: ${self.money}")

            self.player.calclulate_card_values()
            self.calculate_x_position_of_cards()
            self.check_mouse_over_card(mouse)
            self.draw()

    def draw_last_placed_chip(self):
        if len(self.placed_bets) > 0:
            self.placed_bets[-1].draw()

    def check_mouse_over_card(self, mouse_pos):
        for card in self.player.hand:
            if card.card_rect.collidepoint(mouse_pos):
                card.card_highlighted = True
            else:
                card.card_highlighted = False

    def change_height_of_cards(self):
        for card in self.player.hand:
            if card.card_highlighted:
                card.raise_height()
            else:
                card.lower_height()

    def calculate_x_position_of_cards(self):
        total_width_of_cards = len(self.player.hand) * 125
        # Based on how many cards there are multiply the x offset of the card based on its index in the list
        for ix, card in enumerate(self.player.hand[::-1]):
            card.x_position = total_width_of_cards // 2 + (self.mid_width - card.card_rect.width) - ix * 125

    def update_x_position_of_cards(self):
        for ix, card in enumerate(self.player.hand[::-1]):
            if card.x_position > card.card_rect.x:
                if not card.card_rect.x + 1 > card.x_position:
                    card.card_rect.x += 1
            elif card.x_position < card.card_rect.x:
                if not card.card_rect.x - 1 < card.x_position:
                    card.card_rect.x -= 1

    def blit_chips(self):
        for chip in self.chips:
            chip.draw()

    def blit_cards(self):
        for card in self.player.hand:
            card.draw()

    def draw(self):
        WINDOW.fill(DARKER_GREEN)
        self.blit_cards()
        self.blit_chips()
        self.bet_text.draw()
        self.money_text.draw()
        self.draw_last_placed_chip()
        pygame.display.update()
