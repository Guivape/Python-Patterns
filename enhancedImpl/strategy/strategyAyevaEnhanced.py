import time

def pairs(seq):
    n = len(seq)
    for i in range(n):
        yield seq[i], seq[(i + 1) % n]

SLOW = 3
LIMIT = 5
WARNING = 'too bad, you picked the slow algorithm :('

def all_unique_sort(s):
    # Slows down if string is longer than LIMIT
    if len(s) > LIMIT:
        print(WARNING)
        time.sleep(SLOW)
    srt = sorted(s)
    for c1, c2 in pairs(srt):
        if c1 == c2:
            return False
    return True

def all_unique_set(s):
    # Slows down if string is shorter than LIMIT
    if len(s) < LIMIT:
        print(WARNING)
        time.sleep(SLOW)
    return len(set(s)) == len(s)

def main():
    strategies = {
        '1': all_unique_set,
        '2': all_unique_sort
    }

    while True:
        word = input("Enter a word (type 'quit' to exit): ")
        if word == 'quit':
            print("bye")
            break

        strategy_choice = input("Choose strategy: [1] Use a set, [2] Sort and pair: ")
        strategy = strategies.get(strategy_choice)
        if strategy:
            print(f"allUnique({word}): {strategy(word)}")
        else:
            print(f"Unknown strategy choice: {strategy_choice}")

if __name__ == "__main__":
    main()
