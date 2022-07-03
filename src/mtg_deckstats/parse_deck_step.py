#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import mtg_parser
from mtg_deckstats.utils import cleanup_name


__all__ = ['ParseDeckStep']


class ParseDeckStep():

    _endpoint_ = 'https://api.scryfall.com/cards/collection'
    _fields_ = [
        'name',
        'type_line',
        'cmc',
        'color_identity',
        'produced_mana',
        'rarity',
    ]

    def __init__(self, deck_url):
        self._deck_url_ = deck_url

    def __call__(self):
        cards = mtg_parser.parse_deck(self._deck_url_)
        cards = list(cards)
        half = int(len(cards)/2)

        new_cardlist = []

        for batch in (cards[:half], cards[half:]):
            identifiers = [{'name': cleanup_name(card.name)} for card in batch]
            payload = {'identifiers': identifiers}
            response = requests.post(self._endpoint_, json=payload)
            j = response.json()
            new_cardlist.extend(map(
                lambda c: {k: v for (k, v) in c.items() if k in self._fields_},
                j.get('data', [])
            ))

        for card in cards:
            new_card = next(c for c in new_cardlist if card.name in c['name'])
            new_card['quantity'] = card.quantity
            new_card['tags'] = card.tags

        return {
            'cards': new_cardlist,
        }
