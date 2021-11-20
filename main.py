from modules.game import MainMenu, Game


def main():
    main_menu = MainMenu()
    while True:
        if main_menu.playing:
            main_menu.game_loop()
        if main_menu.game_toggle:
            game = Game()
            while game.playing:
                game.game_loop()
            print("i")
            main_menu.game_toggle = False
            main_menu.playing = True
            del game


if __name__ == "__main__":
    main()