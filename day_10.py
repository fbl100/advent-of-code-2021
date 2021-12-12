import numpy as np

error_scores = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

completion_scores = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

opens = set([c for c in "([{<"])
closes = set([c for c in ")]}>"])
open_matches = {
    ')': '(',
    '}': '{',
    ']': '[',
    '>': '<'
}

close_matches = {v: k for k, v in open_matches.items()}


def calculate_error_score(c):
    '''
    >>> calculate_error_score(')')
    3
    >>> calculate_error_score('d')
    0
    '''
    return error_scores[c] if c in error_scores else 0


def calculate_corruption_score(s):
    '''
    >>> calculate_corruption_score('}}]])})]')
    288957
    '''
    completion_sum = 0
    for c in s:
        completion_sum = (completion_sum * 5) + completion_scores[c]
    return completion_sum


def process_line(line):
    """
    >>> process_line("[({(<(())[]>[[{[]{<()<>>")
    {'error_score': 0, 'corruption_score': 288957}
    >>> process_line("{([(<{}[<>[]}>{[]{[(<()>")
    {'error_score': 1197, 'corruption_score': 0}
    >>> process_line("[(()[<>])]({[<{<<[]>>(")
    {'error_score': 0, 'corruption_score': 5566}
    """

    stack = list()
    for c in line:
        # print(f"{c} ** {stack}")
        if c in opens:
            # print(f"push {c}")
            stack.append(c)
        elif c in closes:
            last_item = stack[-1]
            expected = close_matches[last_item]
            if c == expected:
                # print(f"pop  {c}")
                stack.pop()
            else:
                return {
                    'error_score': calculate_error_score(c),
                    'corruption_score': 0
                }
                # return c, remaining, f"Expected {expected}, but found {c} instead."

    return {
        'error_score': 0,
        'corruption_score': calculate_corruption_score("".join([close_matches[x] for x in reversed(stack)]))
    }


def process_file(file_name):
    """
    >>> process_file("day_10_test.txt")
    (26397, 288957)
    """
    with open(file_name) as f:
        lines = f.readlines()

    error_sum = 0
    completion_scores = list()

    for line in lines:
        result = process_line(line)

        error_sum += result['error_score']
        if result['corruption_score'] > 0:
            completion_scores.append(result['corruption_score'])

    median = int(np.median(completion_scores))
    # print(f"sum = {sum}")
    return (error_sum, median)


process_file("day_10_test.txt")
(a,b) = process_file("day_10_input.txt")
print(a)
print(b)