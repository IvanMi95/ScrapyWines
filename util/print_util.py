from datetime import datetime
import traceback


GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"


def custom_print(arg: str) -> None:
    print(GREEN + "=*=" * 35 + RESET)
    print(arg)
    print(GREEN + "=*=" * 35 + RESET)


def print_exception(exception: Exception) -> None:
    now = datetime.now()
    date_string = now.strftime("%d/%m/%Y, %H:%M:%S")

    print(RED + "=*=" * 35 + RESET)
    print(RED + date_string + RESET)
    print(RED + f"Exception: {str(exception)}\n" + RESET)
    print(RED + f"Exception: {traceback.format_exc()}\n" + RESET)
    print(RED + "=*=" * 35 + RESET)
