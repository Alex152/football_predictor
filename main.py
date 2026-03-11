#from src.core.request_manager import init_request_table
#init_request_table()

from src.system.init_system import initialize_system
from src.core.request_manager import print_request_status


def main():

    initialize_system()

    print_request_status()

    print("Sistema listo")


if __name__ == "__main__":
    main()