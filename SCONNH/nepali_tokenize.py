import re

def nepali_tokenize(text):
    colon_lexicon = ['अंशत:', 'मूलत:', 'सर्वत:', 'प्रथमत:', 'सम्भवत:', 'सामान्यत:', 'विशेषत:', 'प्रत्यक्षत:',
        				'मुख्यत:', 'स्वरुपत:', 'अन्तत:', 'पूर्णत:', 'फलत:', 'क्रमश:', 'अक्षरश:', 'प्रायश:',
        				'कोटिश:', 'शतश:', 'शब्दश:','अत:']

        # Handling punctuations: , " ' ) ( { } [ ] ! ‘ ’ “ ” :- ? । / —
    text = re.sub('\,|\"|\'| \)|\(|\)| \{| \}| \[| \]|!|‘|’|“|”| \:-|\?|।|/|\—', ' ', text)
    words_original = text.split()

    words = []
    for word in words_original:
            if word[len(word) - 1:] == '-':
                if not word == '-':
                    words.append(word[:len(word) - 1])
            else:
                if word[len(word) - 1:] == ':' and word not in colon_lexicon:
                    words.append(word[:len(word) - 1])
                else:
                    words.append(word)

    return words
