n_tests = int(input())


def move(string: str, step: int) -> str:
    return string[step:] + string[:step]


for test in range(n_tests):
    binary_string = input()
    table = tuple(tuple(int(i) for i in move(binary_string, step)) for step in range(len(binary_string)))
    max_ones = 0
    ones = 0
    for i in binary_string:
        if i == '1':
            ones += 1
        else:
            max_ones = max(max_ones, ones)
            ones = 0
    # 0 - max_ones, 1 - (max_ones - 1) * 2




