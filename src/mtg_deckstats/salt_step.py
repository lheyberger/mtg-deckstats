#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import itertools
import requests
import more_itertools
from mtg_deckstats.utils import yield_cards


__all__ = []


class SaltStep():

    def __init__(self, data: dict = None, session=None):
        self._data = (data or {}).get(self.__class__.__name__)
        self._session = session

    def __call__(self, deck):
        salt_score = self._data or self.load_data(self._session)
        card_names = [card.get('name') for card in yield_cards(deck)]
        score = sum(v for k, v in salt_score.items() if k in card_names)
        return {
            'salt_score': round(score, 2),
        }

    @classmethod
    def load_data(cls, session=None):
        session = session or requests
        cardlists = (
            session
            .get('https://json.edhrec.com/pages/top/salt-2021.json')
            .json()
            .get('container', {})
            .get('json_dict', {})
            .get('cardlists', [])
        )
        cardviews = (c.get('cardviews', {}) for c in cardlists)
        cards = itertools.chain.from_iterable(cardviews)

        salt_score = {}
        for card in cards:
            salt = card.get('salt')
            if not salt:
                salt = re.findall(r'\d+\.\d+', card.get('label'))
                salt = more_itertools.first(salt)
                salt = float(salt)
            salt_score[card.get('name')] = salt

        return salt_score
