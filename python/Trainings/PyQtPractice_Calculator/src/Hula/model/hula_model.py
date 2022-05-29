import random


class HulaModel:
    def __init__(self):
        self.taken = []

    def clear_taken(self):
        self.taken = []

    def add_taken(self, item):
        self.taken.append(item)

    def remove_taken(self, item):
        self.taken.remove(item)

    def generate(self, start, stop):
        if len(list(range(start, stop + 1))) == len(self.taken):
            rand_guessed = "Nothing To Guess"
        else:
            guessed = []
            while True:
                rand_guessed = random.randint(start, stop)
                if rand_guessed not in self.taken:
                    guessed.append(rand_guessed)
                    if guessed.count(rand_guessed) == 3:
                        break
        return rand_guessed
