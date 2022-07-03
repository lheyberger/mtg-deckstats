#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mtg_deckstats.graph import run_graph
from mtg_deckstats.canadian_highlander_step import CanadianHighlanderStep
from mtg_deckstats.combo_potential_step import ComboPotentialStep
from mtg_deckstats.commander_tier_step import CommanderTierStep
from mtg_deckstats.create_report_step import CreateReportStep
from mtg_deckstats.deck_composition_step import DeckCompositionStep
from mtg_deckstats.mana_producers_step import ManaProducersStep
from mtg_deckstats.mana_value_step import ManaValueStep
from mtg_deckstats.parse_deck_step import ParseDeckStep
from mtg_deckstats.rarity_step import RarityStep
from mtg_deckstats.salt_step import SaltStep


__all__ = ['compute', 'pre_cache']


def compute(src: str, data: dict = None) -> dict:
    functions = {
        'parse_deck': ParseDeckStep(src),
        'mana_value': ManaValueStep(),
        'rarity': RarityStep(),
        'canadian_highlander': CanadianHighlanderStep(data=data),
        'salt': SaltStep(data=data),
        'commander_tier': CommanderTierStep(data=data),
        'deck_composition': DeckCompositionStep(data=data),
        'combo_potential': ComboPotentialStep(data=data),
        'mana_producers': ManaProducersStep(),
        'create_report': CreateReportStep(),
    }
    dependencies = {
        'parse_deck': [],
        'mana_value': ['parse_deck'],
        'rarity': ['parse_deck'],
        'canadian_highlander': ['parse_deck'],
        'salt': ['parse_deck'],
        'commander_tier': ['parse_deck'],
        'deck_composition': ['parse_deck'],
        'combo_potential': ['parse_deck'],
        'mana_producers': ['parse_deck'],
        'create_report': [
            'mana_value',
            'rarity',
            'canadian_highlander',
            'salt',
            'commander_tier',
            'deck_composition',
            'combo_potential',
            'mana_producers',
        ],
    }

    results = run_graph(functions, dependencies)
    result = results.get('create_report', {})

    return {'src': src, **result}


def pre_cache():
    steps = [
        CanadianHighlanderStep,
        SaltStep,
        CommanderTierStep,
        DeckCompositionStep,
        ComboPotentialStep,
    ]

    cache = {step.__name__: step.load_data() for step in steps}
    return cache
