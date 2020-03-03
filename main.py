"""main"""

from substitute import Substitute
SUB = Substitute()


def main():
    """entry point"""
    while True:
        try:
            print("1: Quel aliment souhaitez-vous remplacer ?")
            print("2: Retrouver mes aliments substitués.")
            entry = int(input())
            if entry == 1:
                SUB.remplace()
            elif entry == 2:
                SUB.get_client_data()
            else:
                print("entrer une valeur entre 1 et 2")
        except ValueError:
            print("entrer une valeur entre 1 et 2")


if __name__ == "__main__":
    main()
