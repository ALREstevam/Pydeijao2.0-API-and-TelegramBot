word2emoji = {
    ('maçã',) : '🍏',
    ('maçã verde',) :'🍎',
    ('pêra',) : '🍐',
    ('laranja', 'pokan', 'pocã', 'poncã', 'poncãn', 'tangerina', 'mexerica',) : '🍊',
    ('melancia',) : '🍉',
    ('uva',) : '🍇',
    ('morango',) : '🍓',
    ('melão',) : '🍈',
    ('pêssego',) : '🍑',
    ('abacaxi',) : '🍍',
    ('kiwi',) : '🥝',
    ('abacate',) : '🥑',
    ('tomate',) : '🍅',
    ('berinjela', 'beringela',) : '🍆',
    ('pepino', 'pipino',) : '🥒',
    ('cenoura',) : '🥕',
    ('milho',) : '🌽',
    ('batata',) : '🥔',
    ('queijo',) : '🧀',
    ('pão',) : '🍞',
    ('pé de moleque', 'pé-de-moleque', 'pé-de-moça', 'pé de moça',) : '🥜',
    ('ovo',) : '🥚',
    ('bacon', 'bisteca', 'suína',) : '🥓',
    ('frango', 'franguinho',) : '🍗',
    ('kebab', 'kebabe',) : '🥙',
    ('carne', 'bife',) : '🍖',
    ('salada',) : '🥗',
    ('sopa',) : '🥘',
    ('macarrão', 'macarronada', 'espaguete', 'spaghetti' , 'bolonhesa',) : '🍝',
    ('arroz e feijão', 'arroz integral e feijão', 'arroz e feijão preto', 'arroz integral e feijão preto', 'arroz', 'feijão',) : '🍛',
    ('pudim', 'pudin',) : '🍮',
    ('doce',) : '🍬',
    ('biscoito', 'bolacha',) : '🍪',
    ('café',) : '☕',
    ('prato',) : '🍽',
    ('almoço', ) : '☀',
    ('jantar', '') : '🌙',
}

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

def emojisFor(text):
    splitted = str(text)\
        .lower()\
        .replace('.', '')\
        .replace(',', '')\
        .replace(':', '')\
        .replace('\n', '')\
        .replace('\t', '')\
        .replace('\r', '')\
        .replace('•', '')\
        .split(' ')
    emojis = []
    stopword = False
    splitted = remove_values_from_list(splitted, '')
    splitted = remove_values_from_list(splitted, ' ')
    splitted = remove_values_from_list(splitted, 'e')
    splitted = remove_values_from_list(splitted, 'com')
    splitted = remove_values_from_list(splitted, '•')

    # for each sended word
    for word in splitted:
        #for each collection words -> emoji
        for wordsEmoji, emoji in word2emoji.items():

            if stopword:
                #break
                pass

            #foe each word -> emoji
            for wordEmoji in wordsEmoji:

                if word in wordEmoji:
                    if emoji not in emojis:
                        emojis.append(emoji)
                    stopword = True
                    break

    return emojis

def emojisAtEnd(text):
    return text + ' ' + ''.join(emojisFor(text))

def emojisAtBegin(text):
    return  ''.join(emojisFor(text)) +  ' ' + text