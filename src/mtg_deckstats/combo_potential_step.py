#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import reduce
from operator import itemgetter
import csv
import requests


__all__ = ['ComboPotentialStep']


class ComboPotentialStep:

    def __init__(self, data=None):
        self.data = data or {}

    def __call__(self, deck):
        combos = self.data or self.pre_cache()

        cards = deck.get('cards', [])
        card_names = set(card.get('name') for card in cards)

        color_identities = (
            set(card.get('color_identity', ()))
            for card in cards
        )
        color_identity = ''.join(
            reduce(lambda x, y: x | y, color_identities)
        ).lower()
        color_identity_filter = set('wubrg') - set(color_identity)

        combos = (
            c for c in combos
            if not color_identity_filter & set(c['ci'])
        )
        combos = (
            c for c in combos
            if c['cards'] <= card_names
        )
        combos = list(combos)

        for combo in combos:
            combo_cards = list(
                c for c in cards
                if c.get('name') in combo.get('cards')
            )
            combo['cards'] = combo_cards
            combo['cmc'] = sum(c.get('cmc', 0) for c in combo_cards)
            combo['nb'] = len(combo_cards)
            combo['cmdr'] = any(
                c for c in combo_cards
                if 'commander' in c.get('tags', ())
            )

        combos = sorted(combos, key=itemgetter('cmc'))
        combos = sorted(combos, key=itemgetter('cmdr'), reverse=True)
        combos = sorted(combos, key=itemgetter('nb'))

        return {
            'combos_level': self._get_power_level(combos),
            'combos_density': len(combos),
        }

    @classmethod
    def _get_power_level(cls, combos):
        levels = [
            (9, lambda c: c['nb'] <= 2 and c['cmc'] <= 4 and c['cmdr']),
            (8, lambda c: c['nb'] <= 2 and c['cmc'] > 4 and c['cmdr']),

            (7, lambda c: c['nb'] <= 2 and c['cmc'] <= 4),
            (6, lambda c: c['nb'] <= 2 and c['cmc'] > 4),

            (5, lambda c: c['nb'] == 3 and c['cmc'] <= 6 and c['cmdr']),
            (4, lambda c: c['nb'] == 3 and c['cmc'] > 6 and c['cmdr']),

            (3, lambda c: c['nb'] == 3 and c['cmc'] <= 6),
            (2, lambda c: c['nb'] == 3 and c['cmc'] > 6),

            (1, lambda c: True),
        ]

        combo_levels = map(
            lambda c: next((level for level, f in levels if f(c)), 0),
            combos
        )
        return max(combo_levels, default=0)

    @classmethod
    def pre_cache(cls):
        url = (
            'https://docs.google.com/spreadsheets/d/'
            '1KqyDRZRCgy8YgMFnY0tHSw_3jC99Z0zFvJrPbfm66vA/export'
            '?format=tsv&id=1KqyDRZRCgy8YgMFnY0tHSw_3jC99Z0zFvJrPbfm66vA&gid=0'
        )
        lines = (
            requests
            .get(url)
            .content
            .decode('utf-8')
            .splitlines()
        )
        tsv_file = csv.reader(lines, delimiter='\t')
        lines = list(tsv_file)

        combos = []
        for line in lines[1:]:
            if not line[17] or not line[11]:
                continue

            cards = set(line[1:10])
            cards.discard('')

            combos.append({
                'cards': cards,
                'ci': ''.join(set('wubrg') & set(line[11])),
            })

        return combos
