#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import pytest
import mtg_deckstats
from .utils import assert_objects_are_equal, mock_response, mock_responses


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


@pytest.fixture(name='slow_cache', scope='module')
def slow_cache_fixture():
    return mtg_deckstats.pre_cache()


@pytest.fixture(name='fast_cache', scope='module')
def fast_cache_fixture():
    try:
        with open('tests/mocks/pre_cache.pkl', 'rb') as cache_file:
            return pickle.load(cache_file)
    except:
        pytest.fail(reason='Please follow instructions in CONTRIBUTING.md')
        return None


@pytest.mark.slow
@pytest.mark.parametrize('src', sources)
def test_slow_report_cached(src, slow_cache):

    result = mtg_deckstats.compute(src, data=slow_cache)

    assert result


def test_patched_pre_cache(monkeypatch):

    def mock_load_data(step):
        def inner_load_data(cls, session=None):
            return step
        return inner_load_data

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
            mock_load_data(step),
        )

    result = mtg_deckstats.pre_cache()

    assert set(steps) <= set(result.values())


@pytest.mark.parametrize('src', sources)
def test_patched_report(monkeypatch, src):

    mock_result = {'test_step': 42}

    def mock_run_graph(*args, **kwargs):
        del args
        del kwargs
        return {'create_report': mock_result}

    monkeypatch.setattr(
        mtg_deckstats.report, 'run_graph',
        mock_run_graph,
    )

    result = mtg_deckstats.compute(src)

    assert_objects_are_equal(
        {'src': src, **mock_result},
        {'src': src, **result}
    )


@pytest.mark.parametrize('deck', [
    {
        'url': 'https://www.moxfield.com/decks/Agzx8zsi5UezWBUX5hMJPQ',
        'pattern': r'https://.*?moxfield.com',
        'mock': 'mock_moxfield_Agzx8zsi5UezWBUX5hMJPQ',
        'scryfall_pattern': r'https://api.scryfall.com/cards/collection',
        'scryfall_mocks': [
            'scryfall_moxfield_Agzx8zsi5UezWBUX5hMJPQ_1',
            'scryfall_moxfield_Agzx8zsi5UezWBUX5hMJPQ_2'
        ],
    },
])
def test_pre_cached_compute(requests_mock, fast_cache, deck):
    mock_response(
        requests_mock,
        deck['pattern'],
        deck['mock']
    )
    mock_responses(
        requests_mock,
        'POST',
        deck['scryfall_pattern'],
        deck['scryfall_mocks']
    )

    result = mtg_deckstats.compute(deck['url'], data=fast_cache)
    assert result
