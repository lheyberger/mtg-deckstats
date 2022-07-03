#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint
import time
import pytest
import mtg_deckstats
from .utils import assert_objects_are_equal


sources = [
    (
        'https://aetherhub.com'
        '/Deck/mtg-parser-3-amigos'
    ),
    (
        'https://www.archidekt.com'
        '/decks/1365846/'
    ),
    (
        'https://deckstats.net'
        '/decks/30198/2034245--mtg-parser-3-amigos'
    ),
    (
        'https://www.moxfield.com'
        '/decks/Agzx8zsi5UezWBUX5hMJPQ'
    ),
    (
        'https://www.mtggoldfish.com'
        '/deck/3935836'
    ),
    (
        'https://scryfall.com'
        '/@gorila/decks/e7aceb4c-29d5-49f5-9a49-c24f64da264b'
    ),
    (
        'https://tappedout.net'
        '/mtg-decks/mtg-parser-3-amigos/'
    ),
    (
        'https://decks.tcgplayer.com'
        '/magic/commander/gorila/mtg-parser--3-amigos/1384198'
    ),
]


@pytest.mark.slow
@pytest.fixture(name='cache', scope='module')
def fixture_cache():
    return mtg_deckstats.report.pre_cache()


@pytest.mark.slow
@pytest.mark.parametrize('src', sources)
def test_slow_report_no_cache(src):

    start = time.time()
    result = mtg_deckstats.report.compute(src)
    end = time.time()

    assert result
    pprint(f'Finished test in {round(end - start, 2)}')
    pprint(result)


@pytest.mark.slow
@pytest.mark.parametrize('src', sources)
def test_slow_report_cached(src, cache):

    start = time.time()
    result = mtg_deckstats.report.compute(src, data=cache)
    end = time.time()

    assert result
    pprint(f'Finished test (w/ cache) in {round(end - start, 2)}')
    pprint(result)


@pytest.mark.parametrize('src', sources)
def test_report(monkeypatch, src):

    mock_result = {'test_step': 42}

    def mock_run_graph(*args, **kwargs):
        del args
        del kwargs
        return {'create_report': mock_result}

    monkeypatch.setattr(
        mtg_deckstats.report, 'run_graph',
        mock_run_graph,
    )

    result = mtg_deckstats.report.compute(src)

    assert_objects_are_equal(
        {'src': src, **mock_result},
        {'src': src, **result}
    )


def test_pre_cache(monkeypatch):

    steps = [
        'canadian_highlander_step.CanadianHighlanderStep',
        'salt_step.SaltStep',
        'commander_tier_step.CommanderTierStep',
        'deck_composition_step.DeckCompositionStep',
        'combo_potential_step.ComboPotentialStep'
    ]
    for step in steps:
        monkeypatch.setattr(
            f'mtg_deckstats.{step}.load_data',
            lambda step=step: step
        )

    result = mtg_deckstats.report.pre_cache()

    assert set(steps) == set(result.values())
