with open("tetrisScrabble/palabrasEspañolArreglado.txt", "r", encoding="utf-8") as f:
    firsto = True
    WORDS = []
    ENNE = []
    for word in f:
        if word.startswith("ñ"):
            ENNE.append(word)
        else:
            if firsto and word.startswith("o"):
                firsto = False
                WORDS += ENNE
            WORDS.append(word)
with open("tetrisScrabble/palabrasEspañolOrdenado.txt", "w", encoding="utf-8") as f:
    f.writelines(word for word in WORDS)
