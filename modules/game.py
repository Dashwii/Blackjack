from modules.constants import *
from modules.cards import Card, Dealer
from modules.constants import chip_1, chip_10, chip_100, chip_500, background
import random
import time

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
    images = {1: chip_1, 10: chip_10, 100: chip_100, 500: chip_500}
    chip_position = {1: [50, HEIGHT - 325], 10: [225, HEIGHT - 325], 100: [75, HEIGHT - 150], 500: [250, HEIGHT - 150]}

    def __init__(self, value):
        self.value = value
        self.image = pygame.transform.scale(Chip.images[self.value], (150, 150))
        self.x = Chip.chip_position[value][0]
        self.y = Chip.chip_position[value][1]
        self.chip_rect = pygame.Rect(self.x, self.y, 150, 150)

    def draw(self):
        WINDOW.blit(self.image, (self.x, self.y))


class PlacedChip(Chip):
    def __init__(self, value):
        super().__init__(value)
        self.x = 75 + random.randint(-10, 10)
        self.y = 150 + random.randint(-10, 10)
        self.chip_rect = pygame.Rect(self.x, self.y, 150, 150)


class MainMenu:
    def __init__(self):
        self.playing = True
        self.game_toggle = False
        self.clock = pygame.time.Clock()
        self.blackjack_title = DrawText(text_font, "Blackjack", (WIDTH // 2, -100), WHITE)
        self.play_title = DrawText(text_font, "Play", (WIDTH // 2, HEIGHT // 2), WHITE)

    def game_loop(self):
        title_pos_update = pygame.USEREVENT
        pygame.time.set_timer(title_pos_update, 7)

        while self.playing:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                mouse = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    self.playing = False
                    pygame.display.quit()
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.play_title.text_rect.collidepoint(mouse):
                        self.game_toggle = True
                        self.playing = False
                if event.type == title_pos_update:
                    if self.blackjack_title.text_rect.y + 1 < 150:
                        self.blackjack_title.text_rect.y += 1
            self.blit_to_screen()

    def blit_to_screen(self):
        WINDOW.blit(title_background, (0, 0))
        self.blackjack_title.draw()
        self.play_title.draw()
        pygame.display.update()


class Game:
    def __init__(self):
        self.playing = True
        self.clock = pygame.time.Clock()
        self.keys_pressed = {"Mouse_1": False}
        self.money = 2500
        self.bet_amount = 0
        self.last_bet_amount = 0
        self.money_text = DrawText(chip_text_font, f"Money: ${self.money}", (129, 25), WHITE)
        self.bet_text = DrawText(chip_text_font, f"Bet: ${self.bet_amount}", (72, 75), WHITE)
        self.deal_text = DrawText(chip_text_font, "Deal", (WIDTH - 100, 700), WHITE)
        self.hit_text = DrawText(chip_text_font, "Hit", (WIDTH - 100, 700), WHITE)
        self.stay_text = DrawText(chip_text_font, "Stay", (WIDTH - 100, 775), WHITE)
        self.double_text = DrawText(chip_text_font, "Double", (150, 325), WHITE)
        self.all_in_text = DrawText(chip_text_font, "All in", (150, 150), WHITE)
        self.clear_bet_text = DrawText(chip_text_font, "Clear bet", (350, 205), WHITE)
        self.player_hand_value = 0
        self.dealer_hand_value = 0
        self.player_hand_value_text = DrawText(chip_text_font, f"{self.player_hand_value}", (WIDTH // 2, HEIGHT - 250), WHITE)
        self.dealer_hand_value_text = DrawText(chip_text_font, f"{self.dealer_hand_value}", (WIDTH // 2, 250), WHITE)
        self.chips = [Chip(1), Chip(10), Chip(100), Chip(500)]
        self.unused_cards = [clover_a, clover2, clover3, clover4, clover5, clover6, clover7, clover8, clover9, clover10, clover_j, clover_k, clover_q,
                             diamond_a, diamond_2, diamond_3, diamond_4, diamond_5, diamond_6, diamond_7, diamond_8, diamond_9, diamond_10, diamond_j, diamond_k, diamond_q,
                             heart_a, heart_2, heart_3, heart_4, heart_5, heart_6, heart_7, heart_8, heart_9, heart_10, heart_j, heart_k, heart_q,
                             spade_a, spade_2, spade_3, spade_4, spade_5, spade_6, spade_7, spade_8, spade_9, spade_10, spade_j, spade_k, spade_q]
        self.used_cards = []
        self.placed_chips = []
        self.player_hand = []
        self.dealer = Dealer()

        self.update_cards_y = pygame.USEREVENT
        self.update_cards_x = pygame.USEREVENT + 1
        self.card_dealing_interval = pygame.USEREVENT + 2
        self.time_since_win = 0

        self.double_available = False
        self.dealing_cards = False
        self.round_playing = False
        self.player_stay = False
        self.dealer_playing = False

        self.end_of_round = False
        self.player_won = False
        self.dealer_won = False
        self.push = False
        self.blackjack = False

    def game_loop(self):
        pygame.time.set_timer(self.update_cards_y, 20)
        pygame.time.set_timer(self.update_cards_x, 1)
        pygame.time.set_timer(self.card_dealing_interval, 500)
        random.shuffle(self.unused_cards)
        while self.playing:
            self.clock.tick(FPS)
            self.process_events()
            self.render()
            self.reset_input()

    def process_events(self):
        def update_card_x_position(cards):
            for ix, card in enumerate(cards[::-1]):
                if card.x_position > card.card_rect.x:
                    if not card.card_rect.x + 1 > card.x_position:
                        card.card_rect.x += 1
                elif card.x_position < card.card_rect.x:
                    if not card.card_rect.x - 1 < card.x_position:
                        card.card_rect.x -= 1

        def check_value_of_hand(hand):
            return sum([card.card_value for card in hand])

        def pop_card():
            card = self.unused_cards.pop()
            self.used_cards.append(card)
            return card

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                self.playing = False
                pygame.display.quit()
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.keys_pressed["Mouse_1"] = True
            if event.type == pygame.KEYDOWN:
                if keys[pygame.K_ESCAPE]:
                    self.playing = False
            if event.type == self.update_cards_y:
                for card in self.player_hand:
                    if card.card_rect.collidepoint(mouse_pos):
                        card.raise_height()
                    else:
                        card.lower_height()

            if event.type == self.update_cards_x:
                update_card_x_position(self.player_hand)
                update_card_x_position(self.dealer.hand)

            if event.type == self.card_dealing_interval and self.dealing_cards:
                card_type_1, card_type_2 = pop_card(), pop_card()
                card = Card(card_type_1, HEIGHT - 150)
                card_2 = Card(card_type_2, 0)

                if card.card_value == 11:
                    card.ace_check_value(sum([card.card_value for card in self.player_hand]))

                if card_2.card_value == 11:
                    card_2.ace_check_value(sum([card.card_value for card in self.dealer.hand]))

                if len(self.player_hand) <= len(self.dealer.hand):
                    self.player_hand.append(card)
                elif len(self.dealer.hand) <= len(self.player_hand):
                    self.dealer.hand.append(card_2)
                if len(self.player_hand) == 2 and len(self.dealer.hand) == 2:
                    self.dealing_cards = False
                    self.round_playing = True
                    if check_value_of_hand(self.player_hand) in [9, 10, 11]:
                        self.double_available = True

                elif check_value_of_hand(self.player_hand) == 21:
                    self.player_won = True
                    self.blackjack = True
                    self.time_since_win = time.time()
                elif check_value_of_hand(self.dealer.hand) == 21:
                    self.dealer_won = True
                    self.time_since_win = time.time()

            if event.type == self.card_dealing_interval and self.dealer_playing:
                if sum([card.card_value for card in self.dealer.hand]) >= 17:
                    self.dealer_playing = False
                    self.end_of_round = True
                else:
                    card_type = pop_card()
                    self.dealer.take_card(card_type)

        if self.keys_pressed["Mouse_1"]:
            for chip in self.chips:
                if chip.chip_rect.collidepoint(mouse_pos) and self.money >= chip.value and not self.dealing_cards and not self.round_playing:  # Add chips to bet
                    self.placed_chips.append(PlacedChip(chip.value))
                    self.money -= chip.value
                    self.money_text.update_text(f"Money: ${self.money}")
                    self.bet_amount += chip.value
                    self.bet_text.update_text(f"Bet: ${self.bet_amount}")

            if len(self.placed_chips) > 0 and self.placed_chips[-1].chip_rect.collidepoint(mouse_pos) and not self.round_playing and not self.dealing_cards:  # Remove chips used in bet if clicked.
                self.money += self.placed_chips[-1].value
                self.money_text.update_text(f"Money: ${self.money}")
                self.bet_amount -= self.placed_chips[-1].value
                self.bet_text.update_text(f"Bet: ${self.bet_amount}")
                self.placed_chips.pop()

            if len(self.placed_chips) > 0 and self.deal_text.text_rect.collidepoint(mouse_pos) and not self.round_playing:  # Deal cards
                self.dealing_cards = True

            if self.hit_text.text_rect.collidepoint(mouse_pos) and self.round_playing and not self.player_stay and not self.player_hand_value >= 21:  # Add card to player hand
                card_type = pop_card()
                card = Card(card_type, HEIGHT - 150)
                if card.card_value == 11:
                    card.ace_check_value(sum([card.card_value for card in self.player_hand]))
                self.player_hand.append(card)
                if self.double_available:
                    self.double_available = False
                if check_value_of_hand(self.player_hand) == 21 and not self.player_won:
                    self.player_won = True
                    self.time_since_win = time.time()

            if self.stay_text.text_rect.collidepoint(mouse_pos) and self.round_playing and not self.player_stay and not check_value_of_hand(self.player_hand) >= 21:  # Player stays
                self.dealer_playing = True
                self.player_stay = True

            if self.double_text.text_rect.collidepoint(mouse_pos) and self.double_available:
                self.bet_amount *= 2
                self.bet_text.update_text(f"Bet: ${self.bet_amount}")
                self.double_available = False

            if self.all_in_text.text_rect.collidepoint(mouse_pos) and not self.round_playing:
                self.insert_all_chips()

            if self.clear_bet_text.text_rect.collidepoint(mouse_pos) and not self.round_playing:
                self.placed_chips = []
                self.money += self.bet_amount
                self.bet_amount = 0
                self.money_text.update_text(f"Money: ${self.money}")
                self.bet_text.update_text(f"Bet: ${self.bet_amount}")

        player_hand_width_of_cards = len(self.player_hand) * 125
        dealer_hand_width_of_cards = len(self.dealer.hand) * 125

        # Based on how many cards there are multiply the x offset of the card based on its index in the list
        for index, card in enumerate(self.player_hand[::-1]):
            card.x_position = player_hand_width_of_cards // 2 + (WIDTH // 2 - card.card_rect.width) - index * 125
        for index, card in enumerate(self.dealer.hand[::-1]):
            card.x_position = dealer_hand_width_of_cards // 2 + (WIDTH // 2 - card.card_rect.width) - index * 125

        self.player_hand_value = sum([card.card_value for card in self.player_hand])
        if not self.player_stay:
            self.dealer_hand_value = sum([card.card_value for card in self.dealer.hand[1:]])
        else:
            self.dealer_hand_value = sum([card.card_value for card in self.dealer.hand])

        if not self.player_stay and not self.dealer_won:
            if self.player_hand_value > 21:
                self.dealer_won = True
                self.time_since_win = time.time()

        if self.end_of_round and not self.player_won and not self.dealer_won and not self.push:
            if self.dealer_hand_value > 21:
                self.player_won = True
                self.time_since_win = time.time()
            elif self.player_hand_value == 21:
                self.player_won = True
                self.time_since_win = time.time()
            elif self.dealer_hand_value == 21:
                self.dealer_won = True
                self.time_since_win = time.time()
            elif self.player_hand_value == self.dealer_hand_value:
                self.push = True
                self.time_since_win = time.time()
            elif self.player_hand_value > self.dealer_hand_value and self.player_stay and not self.dealer_playing:
                self.player_won = True
                self.time_since_win = time.time()
            elif self.dealer_hand_value > self.player_hand_value and self.player_stay and not self.dealer_playing:
                self.dealer_won = True
                self.time_since_win = time.time()

        if self.blackjack and not self.dealing_cards and time.time() - self.time_since_win > 1.5:
            # Fix win screen to display correct amount of money won
            initial_cash = self.money
            cash_won = self.bet_amount * 2
            self.money += cash_won
            self.win_screen(f"You won ${abs(self.money - initial_cash) // 2}")
            self.shuffle_cards()
        elif self.push and not self.dealing_cards and time.time() - self.time_since_win > 1.5:
            self.money += self.bet_amount
            self.win_screen("Push!")
            self.shuffle_cards()
        elif self.player_won and not self.dealing_cards and time.time() - self.time_since_win > 1.5:
            initial_cash = self.money
            cash_won = self.bet_amount * 2
            self.money += cash_won
            self.win_screen(f"You won ${abs(self.money - initial_cash) // 2}")
            self.shuffle_cards()
        elif self.dealer_won and not self.dealing_cards and time.time() - self.time_since_win > 1.5:
            if self.money == 0:
                self.win_screen("Dealer wins!")
                self.lost_game()
                return
            self.win_screen("Dealer wins!")
            self.shuffle_cards()

        self.player_hand_value_text.update_text(f"{self.player_hand_value}")
        self.dealer_hand_value_text.update_text(f"{self.dealer_hand_value}")

    @staticmethod
    def draw_transparent_background():
        s = pygame.Surface((WIDTH, HEIGHT))
        s.set_alpha(200)
        s.fill(BLACK)
        WINDOW.blit(s, (0, 0))

    def insert_last_bet(self, last_bet):
        for chip in self.chips[::-1]:
            chips_in = last_bet // chip.value
            chips_sum_value = chips_in * chip.value
            if self.money - chips_sum_value < 0:
                return
            last_bet -= chips_sum_value
            self.money -= chips_sum_value
            self.bet_amount += chips_sum_value
            self.money_text.update_text(f"Money: ${self.money}")
            self.bet_text.update_text(f"Bet: ${self.bet_amount}")
            [self.placed_chips.append(PlacedChip(chip.value)) for _ in range(chips_in)]

    def insert_all_chips(self):
        for chip in self.chips[::-1]:
            chips_in = self.money // chip.value
            self.money -= chip.value * chips_in
            self.bet_amount += chip.value * chips_in
            self.money_text.update_text(f"Money: ${self.money}")
            self.bet_text.update_text(f"Bet: ${self.bet_amount}")
            [self.placed_chips.append(PlacedChip(chip.value)) for _ in range(chips_in)]

    def win_screen(self, text):
        self.last_bet_amount = self.bet_amount
        self.reset_round()
        self.insert_last_bet(self.last_bet_amount)
        self.draw_transparent_background()
        while True:
            win_text = DrawText(text_font, f"{text}", (WIDTH // 2, HEIGHT // 2), WHITE)
            win_text.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    pygame.display.quit()
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return
            pygame.display.update()

    def shuffle_cards(self):
        if not len(self.unused_cards) < 14:
            return
        if len(self.unused_cards) < 8:
            pass
        elif not random.randint(1, 5) == 1:
            return
        self.unused_cards += self.used_cards
        self.used_cards = []
        random.shuffle(self.unused_cards)
        while True:
            WINDOW.fill(BLACK)
            shuffling_cards_text = DrawText(text_font, f"Shuffling cards...", (WIDTH // 2, HEIGHT // 2), WHITE)
            shuffling_cards_text.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    pygame.display.quit()
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return
            pygame.display.update()

    def lost_game(self):
        while True:
            WINDOW.fill(BLACK)
            lose_text = DrawText(chip_text_font, "You ran out of money! Go home!", (WIDTH // 2, HEIGHT // 2), WHITE)
            lose_text.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    pygame.display.quit()
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.playing = False
                    return
            pygame.display.update()

    def reset_round(self):
        self.time_since_win = 0
        self.bet_amount = 0
        self.player_hand_value = 0
        self.dealer_hand_value = 0
        self.placed_chips = []
        self.player_hand = []
        self.dealer = Dealer()
        self.dealing_cards = False
        self.round_playing = False
        self.player_stay = False
        self.dealer_playing = False
        self.player_won = False
        self.dealer_won = False
        self.push = False
        self.end_of_round = False
        self.double_available = False
        self.blackjack = False

        self.money_text.update_text(f"Money: ${self.money}")
        self.bet_text.update_text(f"Bet: ${self.bet_amount}")

    def reset_input(self):
        for key in self.keys_pressed.keys():
            self.keys_pressed[key] = False

    def render(self):
        WINDOW.blit(pygame.transform.scale(background, (WIDTH, HEIGHT)), (0, 0))
        for chip in self.chips:
            if chip.value <= self.money:
                chip.draw()
        for chip in self.placed_chips:
            chip.draw()

        for player_card in self.player_hand:
            player_card.draw()
        if not self.player_stay and len(self.dealer.hand) > 0:
            WINDOW.blit(self.dealer.card_down_img, (self.dealer.hand[0].card_rect.x, self.dealer.hand[0].card_rect.y))  # Draw card back image where card index 0 should be
            for index, dealer_card in enumerate(self.dealer.hand[1:]):
                dealer_card.draw()
        else:
            for index, dealer_card in enumerate(self.dealer.hand):
                dealer_card.draw()

        if len(self.placed_chips) > 0 and not self.round_playing and not self.dealing_cards:
            self.deal_text.draw()
            self.clear_bet_text.draw()

        if len(self.placed_chips) == 0:
            self.all_in_text.draw()
        if self.round_playing and not self.player_stay:
            self.hit_text.draw()
            self.stay_text.draw()
        if self.double_available:
            self.double_text.draw()
        if self.round_playing:
            self.player_hand_value_text.draw()
            self.dealer_hand_value_text.draw()

        self.money_text.draw()
        self.bet_text.draw()
        pygame.display.update()
