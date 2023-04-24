#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import mtg_parser
from more_itertools import flatten
from mtg_deckstats.utils import cleanup_name


__all__ = []


class CommanderTierStep():

    def __init__(self, data: dict = None, session=None):
        self._data = (data or {}).get(self.__class__.__name__)
        self._session = session

    def __call__(self, deck):
        cmdrs = self._data or self.load_data(self._session)
        cards = deck.get('cards', [])
        commanders = filter(lambda c: 'commander' in c.get('tags', ()), cards)
        names = map(lambda c: cleanup_name(c.get('name')), commanders)
        powers = map(lambda name: cmdrs.get(name, 0), names)
        power = max(powers)
        return {
            'commander_power_tier': power,
        }

    @classmethod
    def load_data(cls, session=None):
        session = session or requests
        sources = [
            (
                'https://tappedout.net/'
                'mtg-decks/best-commanders-in-edh-tier-list-part-1/'
            ),
            (
                'https://tappedout.net/'
                'mtg-decks/best-commanders-in-edh-tier-list-part-2/'
            ),
        ]

        decks = (mtg_parser.parse_deck(src, session) for src in sources)
        cards = flatten(decks)

        cmdrs = {}
        tiers = set()
        for card in cards:
            name = cleanup_name(card.name)
            tier = ''.join(card.tags)
            cmdrs[name] = tier
            tiers.add(tier)

        tiers = sorted(tiers)

        return {k: max(9 - tiers.index(v), 0) for k, v in cmdrs.items()}
