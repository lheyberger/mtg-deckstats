#!/usr/bin/env python
# -*- coding: utf-8 -*-

import more_itertools


__all__ = ['ManaProducersStep']


class ManaProducersStep():

    def __call__(self, deck):
        producers = deck.get('cards', [])
        producers = filter(
            lambda c: 'Land' not in c.get('type_line', ''),
            producers
        )
        producers = filter(
            lambda c: c.get('produced_mana'),
            producers
        )
        return {
            'mana_producers': more_itertools.ilen(producers),
        }
