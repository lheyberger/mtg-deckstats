#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing.pool import ThreadPool as Pool

import requests

from mtg_deckstats.__version__ import __version__
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


def compute(src: str, data: dict = None, session=None) -> dict:
    session = session or requests
    context = {
        'data': data,
        'session': session,
    }
    functions = {
        'parse_deck': ParseDeckStep(src, session=session),
        'mana_value': ManaValueStep(),
        'rarity': RarityStep(),
        'canadian_highlander': CanadianHighlanderStep(**context),
        'salt': SaltStep(**context),
        'commander_tier': CommanderTierStep(**context),
        'deck_composition': DeckCompositionStep(**context),
        'combo_potential': ComboPotentialStep(**context),
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


def pre_cache(session=None):
    session = session or requests
    steps = [
        CanadianHighlanderStep,
        SaltStep,
        CommanderTierStep,
        DeckCompositionStep,
        ComboPotentialStep,
    ]

    def load_data(step):
        return step.__name__, step.load_data(session)

    with Pool(processes=max(len(steps), 5)) as pool:
        results = pool.map(load_data, steps)

    cache = dict(results)
    cache['version'] = __version__
    return cache
