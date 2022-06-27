#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mtg_parser
from mtg_deckstats.utils import cleanup_name


__all__ = ['CommanderTierStep']


class CommanderTierStep:

    def __init__(self, data=None):
        self.data = data or {}

    def __call__(self, deck):
        cmdrs, tiers, default = self.data or self.pre_cache()

        power = deck.get('cards', [])
        power = filter(lambda c: 'commander' in c.get('tags', ()), power)
        power = map(lambda c: cleanup_name(c.get('name')), power)
        power = map(lambda name: cmdrs.get(name, default), power)
        power = map(lambda t: max(9 - tiers.index(t), 0), power)
        power = max(power)

        return {
            'commander_power_tier': power,
        }

    @classmethod
    def pre_cache(cls):
        cmdrs = mtg_parser.parse_deck(
            'https://tappedout.net/'
            'mtg-decks/best-commanders-in-edh-tier-list/'
        )

        cmdrs = dict(map(lambda c: (c.name, ' '.join(c.tags)), cmdrs))
        tiers = sorted(set(cmdrs.values()))
        default = tiers[-1]

        return cmdrs, tiers, default
