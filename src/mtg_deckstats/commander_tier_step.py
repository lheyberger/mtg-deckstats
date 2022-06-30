#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mtg_parser
from mtg_deckstats.utils import cleanup_name
from mtg_deckstats.base_step import BaseStep


__all__ = ['CommanderTierStep']


class CommanderTierStep(BaseStep):

    def __call__(self, deck):
        cmdrs, tiers, default = self.data or self.load_data()

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
    def load_data(cls):
        cmdrs = mtg_parser.parse_deck(
            'https://tappedout.net/'
            'mtg-decks/best-commanders-in-edh-tier-list/'
        )

        cmdrs = dict(map(lambda c: (c.name, ' '.join(c.tags)), cmdrs))
        tiers = sorted(set(value for value in cmdrs.values() if value))
        default = tiers[-1]

        return cmdrs, tiers, default
