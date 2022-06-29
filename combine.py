from requests_cache import CachedSession
from bs4 import BeautifulSoup
from dataclasses import dataclass

# session.cache.clear()
session = CachedSession(expire_after=-1)

CARD_CALCULATOR_URL = 'http://astcardcalc.herokuapp.com/'
dataset = {
    'VRahCN3t6B7QHmTJ': [6, 17, 20, 21, 33, 42, 44, 45, 31],
    'cJ3AX8mhWKBTwPyC': [4, 12, 15,19, 26, 29, 38, 40, 19, 34]
}

@dataclass
class Cards:
    ast: str
    card: str
    target: str
    time: str
    optimal: str

    def __str__(self):
        correct = u'\u2713' if self.wasOptimal() else ' '
        return f'{correct} [{self.time}]: {self.target} => {self.optimal}.'

    def __repr__(self):
        return self.__str__()

    def wasOptimal(self):
        return self.target == self.optimal

class CardList:
    def __init__(self, cards):
        self.cards = cards


def get_cards(log, fight):
    print(f'{CARD_CALCULATOR_URL}{log}/{fight}')
    html_text = session.get(f'{CARD_CALCULATOR_URL}{log}/{fight}').text;
    soup = BeautifulSoup(html_text, 'html.parser');

    card_plays = []

    cards = []
    for h2 in soup.find_all('h2'):
        if h2.text == 'Card Play':
            section = h2.parent.contents[3].contents[1]
            if len(section.contents) > 1:
                card_plays.append(section.contents[1])

    # card_plays = card_plays[0:1]

    for play in card_plays:
        details = play.contents[1].find_all('span');
        ast = details[0].text
        card = details[1].actionfetch['name']
        target = details[2].text
        time = details[3].text
        optimal = play.contents[3].span.text
        cards.append(Cards(ast, card, target, time, optimal))


    return cards

def process():
    total_cards = []

    for log, fights in dataset.items():
        for fight in fights:
            cards = get_cards(log, fight)
            total_cards = total_cards + cards

    total_cards.sort(key=lambda x: x.time)

    with  open('output.txt', 'w') as f:
        for card in total_cards:
            f.write(str(card))


