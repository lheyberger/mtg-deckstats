#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mtg_parser
from more_itertools import flatten
from mtg_deckstats.utils import cleanup_name
from mtg_deckstats.base_step import BaseStep


__all__ = []


class CommanderTierStep(BaseStep):

    def __call__(self, deck):
        cmdrs = self.data or self.load_data()

        cards = deck.get('cards', [])
        commanders = filter(lambda c: 'commander' in c.get('tags', ()), cards)
        names = map(lambda c: cleanup_name(c.get('name')), commanders)
        powers = map(lambda name: cmdrs.get(name, 0), names)
        power = max(powers)

        return {
            'commander_power_tier': power,
        }

    @classmethod
    def load_data(cls):
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
        decks = map(mtg_parser.parse_deck, sources)
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
