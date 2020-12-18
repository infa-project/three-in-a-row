from random import choice


LIST_OF_COLORS = ['r', 'g', 'b', 'y', 'p']
N = 10


def is_there_three_in_a_row(arr):
    for i in range(N):
        for j in range(N - 2):
            if arr[i][j] == arr[i][j + 1] == arr[i][j + 2] or \
                    arr[j][i] == arr[j + 1][i] == arr[j + 2][i]:
                return True
    return False


def generate_field_list():
    field_list = [[choice(LIST_OF_COLORS) for _ in range(N)] for _ in range(N)]
    while is_there_three_in_a_row(field_list):
        field_list = [[choice(LIST_OF_COLORS) for _ in range(N)] for _ in range(N)]
    return field_list

if __name__ == "__main__":
    print("This module is not for direct call!")
