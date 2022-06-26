#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mtg_deckstats.run_graph import run_graph
from mtg_deckstats.create_report_step import CreateReportStep
from mtg_deckstats.mana_value_step import ManaValueStep
from mtg_deckstats.parse_deck_step import ParseDeckStep
from mtg_deckstats.rarity_step import RarityStep


__all__ = ['report']


def report(src: str) -> dict:
    functions = {
        'parse_deck': ParseDeckStep(src),
        'mana_value': ManaValueStep(),
        'rarity': RarityStep(),
        # 'canadian_highlander': CanadianHighlanderStep(),
        # 'salt': SaltStep(),
        # 'commander_tier': CommanderTierStep(),
        # 'deck_composition': DeckCompositionStep(),
        # 'combo_potential': ComboPotentialStep(),
        # 'mana_producers': ManaProducersStep(),
        'create_report': CreateReportStep(),
    }
    dependencies = {
        'parse_deck': [],
        'mana_value': ['parse_deck'],
        'rarity': ['parse_deck'],
        # 'canadian_highlander': ['parse_deck'],
        # 'salt': ['parse_deck'],
        # 'commander_tier': ['parse_deck'],
        # 'deck_composition': ['parse_deck'],
        # 'combo_potential': ['parse_deck'],
        # 'mana_producers': ['parse_deck'],
        'create_report': [
            'mana_value',
            'rarity',
            # 'canadian_highlander',
            # 'salt',
            # 'commander_tier',
            # 'deck_composition',
            # 'combo_potential',
            # 'mana_producers',
        ],
    }

    results = run_graph(functions, dependencies)
    result = results.get('create_report', {})

    return {'src': src, **result}
