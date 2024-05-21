def win(a, b):
    if a == b:
        return None
    if (a == "Rock" and b == "Scissors") or \
       (a == "Scissors" and b == "Paper") or \
       (a == "Paper" and b == "Rock"):
        return 1
    return 2