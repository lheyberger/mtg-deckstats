#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
from mtg_deckstats.utils import yield_cards


__all__ = ['RarityStep']


class RarityStep():

    def __call__(self, deck):

        counter = Counter(card.get('rarity') for card in yield_cards(deck))

        return dict(('rarity_' + k, v) for k, v in counter.most_common())
