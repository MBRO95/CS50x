i = "-1"
while (int(i) <= 0 or int(i) > 8):
    try:
        i = int(input("Please enter a positive height value between 0-8: "))
    except ValueError:
        continue

# print("Height: " + str(i))


def brick_builder(height: int):
    for i in range(1, height + 1):
        print_space(height - i)
        print_brick(int(i))
        print("  ", end='')
        print_brick(int(i))
        print()


def print_space(spaces: int):
    for i in range(spaces):
        print(" ", end='')


def print_brick(bricks: int):
    for i in range(bricks):
        print("#", end='')


brick_builder(int(i))
