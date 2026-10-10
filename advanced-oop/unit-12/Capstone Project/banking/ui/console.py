from __future__ import annotations
import getpass
import os


class Console:
    #Central terminal presentation service

    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    WHITE = "\033[97m"

    WIDTH = 78

    #Initialise this component with its required dependencies and local state
    def __init__(self) -> None:
        if os.name == "nt":
            # Enable ANSI escape sequences in modern Windows terminals
            os.system("")

        self.colour_enabled = True

    #Perform the internal paint step used by this workflow
    def _paint(
        self,
        text: str,
        colour: str,
    ) -> str:
        if not self.colour_enabled:
            return text

        return f"{colour}{text}{self.RESET}"

    #Clear the current screen state in a controlled way
    def clear_screen(self) -> None:
        print("\033[2J\033[H", end="", flush=True)

    #Display the standard navigation option for returning to the role menu
    def back_to_main_menu(self) -> None:
        while True:
            value = input(
                self._paint(
                    "\n0. Back to Main Menu: ",
                    self.YELLOW,
                )
            ).strip()

            if value == "0":
                return

            self.error(
                "Invalid option. Enter 0 to return to the main menu."
            )

    #Render a consistent terminal separator used by BankSecure screens
    def separator(self) -> None:
        print(
            self._paint(
                "=" * self.WIDTH,
                self.WHITE,
            )
        )

    #Write standard terminal text without role-specific emphasis
    def normal(self, text: str = "") -> None:
        print(
            self._paint(
                text,
                self.WHITE,
            )
        )

    #Write terminal text using the configured bold presentation
    def bold(self, text: str) -> None:
        print(
            self._paint(
                text,
                self.BOLD + self.WHITE,
            )
        )

    #Write CUSTOMER information using the CUSTOMER presentation style
    def user_info(self, text: str) -> None:
        print(
            self._paint(
                text,
                self.CYAN,
            )
        )

    #Write BANK_STAFF information using the BANK_STAFF presentation style
    def staff_info(self, text: str) -> None:
        print(
            self._paint(
                text,
                self.BLUE,
            )
        )

    #Write ADMINISTRATOR information using the ADMINISTRATOR presentation style
    def admin_info(self, text: str) -> None:
        print(
            self._paint(
                text,
                self.MAGENTA,
            )
        )

    #Write a successful operation message using the success presentation style
    def success(self, text: str) -> None:
        print(
            self._paint(
                text,
                self.GREEN,
            )
        )

    #Write a controlled error message using the error presentation style
    def error(self, text: str) -> None:
        print(
            self._paint(
                text,
                self.RED,
            )
        )

    #Write a warning message using the warning presentation style
    def warning(self, text: str) -> None:
        print(
            self._paint(
                text,
                self.YELLOW,
            )
        )

    def heading(
        self,
        text: str,
        clear: bool = True,
    ) -> None:
        if clear:
            self.clear_screen()

        self.separator()
        self.bold(text)
        self.separator()

    def prompt(
        self,
        text: str,
    ) -> str:
        return input(
            self._paint(
                text,
                self.WHITE,
            )
        )

    def secret_prompt(
        self,
        text: str,
    ) -> str:
        return getpass.getpass(
            self._paint(
                text,
                self.WHITE,
            )
        )
