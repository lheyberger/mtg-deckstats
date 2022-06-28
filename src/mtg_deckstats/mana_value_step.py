#!/usr/bin/env python
# -*- coding: utf-8 -*-

import statistics
from mtg_deckstats.utils import yield_cards


__all__ = ['ManaValueStep']


class ManaValueStep():

    def __call__(self, deck):
        cmcs = []
        cmcs_no_lands = []

        for card in yield_cards(deck):
            cmc = card.get('cmc', 0)
            if 'Land' not in card.get('type_line', ''):
                cmcs_no_lands.append(cmc)
            cmcs.append(cmc)

        return {
            'cmc_sum': sum(cmcs),
            'cmc_avg': round(statistics.mean(cmcs), 2),
            'cmc_avg_no_lands': round(statistics.mean(cmcs_no_lands), 2),
        }
