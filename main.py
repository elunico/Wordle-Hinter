# put green letters in their position here
pos_correct_letter = {
    0: '',
    1: '',
    2: '',
    3: '',
    4: '',
}

# put *all* yellow letters in each position into each string
pos_misplaced_letters = {
    0: '',
    1: '',
    2: '',
    3: '',
    4: '',
}

# put all the grey letters into this string
bad_letters = ''


def find_words(pos_correct_letter, pos_misplaced_letters, bad_letters, words=None):
    if words is None: 
        with open("/usr/share/dict/words", "r") as f:
            words = [i.lower() for i in f.read().splitlines() if len(i) == 5 and "'" not in i]

    for word in (i for i in words if all(x not in i for x in bad_letters)):
        for index in range(5):
            # letter belongs at this space
            if pos_correct_letter[index] and pos_correct_letter[index] != word[index]:
                break

            # letter is in word but not in this place
            if word[index] in pos_misplaced_letters[index]:
                break

            if not all(j in word for x in pos_misplaced_letters.values() for j in x):
                break
        else:
            yield word


if __name__ == "__main__":
    find_words(pos_correct_letter, pos_misplaced_letters, bad_letters)
