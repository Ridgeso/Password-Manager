from cProfile import run
from terminal import Terminal

def main():
    run = True

    with Terminal() as manager:
        while run:
            manager.print_setup()
            command = input()

            if command == "1":
                manager.get_password(input())
            elif command == "2":
                manager.store_password()
            elif command == "3":
                manager.delete_password(input())
            elif command == "4":
                manager.update_password()
            elif command == "5":
                run = False


if __name__ == '__main__':
    main()
