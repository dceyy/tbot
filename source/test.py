karaliste = []
with open('karalistekelimeler.txt', 'r', encoding='utf-8') as f:
    for line in f:
        karaliste.append(line.strip())
print(karaliste)