# Description: Split a message into all possible combinations of words
import itertools
def split_message(message):
    words = message.split()
    n = len(words)
    result = []
    for i in range(1, n+1):
        combinations = list(itertools.combinations(words, i))
        for c in combinations:
            result.append(" ".join(c))

    return result
