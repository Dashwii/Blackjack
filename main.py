from modules.menus import MainMenu, GameMenu


def main():
    main_menu = MainMenu()
    while True:
        if main_menu.playing:
            main_menu.game_loop()
        if main_menu.game_toggle:
            game = GameMenu()
            while game.playing:  # If game.playing not true assume user wants to return to menu for now
                game.game_loop()
            main_menu.game_toggle = False
            main_menu.playing = True

main()















# if __name__ == "__main__":
#     main()




"""
CHECKLIST
- Create main menu, Create card and deck system
"""