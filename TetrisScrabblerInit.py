LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
WORDS = []

with open("tetrisScrabble/palabrasEspañolOrdenado.txt", "r", encoding="utf-8") as archive:
    for line in archive:
        goodLine = ""
        
        for i in line.lower():
            if i == "á":
                goodLine += "a"
            elif i == "é" or i == "è": 
                goodLine += "e"
            elif i == "í":
                goodLine += "i"
            elif i == "ó":
                goodLine += "o"
            elif i == "ú" or i == "ü":
                goodLine += "u"
            else:
                goodLine += i
        if len(goodLine.lower()[:-1]) <= 10:
            WORDS.append(goodLine.lower()[:-1])
    for i in LETTERS:
        for j in LETTERS:
            if i.lower() in WORDS:
                WORDS.remove(i.lower())
            if (i+j).lower() in WORDS:
                WORDS.remove((i+j).lower())

for i, word in enumerate(WORDS):
    if i == 0: pass
    if word == WORDS[i-1]:
        WORDS.remove(word)

previousStartingLetter = 0
CWORDS = []
for word in WORDS:
    if word.startswith(LETTERS[previousStartingLetter].lower()):
        CWORDS.append(word)
    else:
        print(previousStartingLetter)
        print(CWORDS[0])
        with open(f"tetrisScrabble/dicts/wordsScrabble1{LETTERS[previousStartingLetter]}.txt", "w", encoding='utf-8') as f:
            f.writelines(word+"\n" for word in CWORDS)
        previousStartingLetter += 1
        CWORDS = []
with open(f"tetrisScrabble/dicts/wordsScrabble1{LETTERS[previousStartingLetter]}.txt", "w", encoding='utf-8') as f:
    f.writelines(word+"\n" for word in CWORDS)

# with open(f"tetrisScrabble/dicts/wordsScrabble.txt", "w", encoding='utf-8') as f:
#     f.writelines(word+"\n" for word in WORDS)
