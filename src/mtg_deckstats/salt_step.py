#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import itertools
import requests
import more_itertools
from mtg_deckstats.utils import yield_cards
from mtg_deckstats.base_step import BaseStep


__all__ = ['SaltStep']


class SaltStep(BaseStep):

    def __call__(self, deck):
        salt_score = self.data or self.load_data()
        card_names = [card.get('name') for card in yield_cards(deck)]
        score = sum(v for k, v in salt_score.items() if k in card_names)
        return {
            'salt_score': round(score, 2),
        }

    @classmethod
    def load_data(cls):
        cardlists = (
            requests
            .get('https://json.edhrec.com/top/salt.json')
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
