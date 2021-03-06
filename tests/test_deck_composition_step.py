#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from mtg_deckstats.deck_composition_step import DeckCompositionStep
from .utils import assert_objects_are_equal, mock_response


categories = [
    {
        'name': 'board_wipes',
        'pattern': 'mh-mass-answers',
        'response': 'tappedout_board_wipes',
        'cards': [
            'Austere Command',
            'Wrath of God',
        ]
    },
    {
        'name': 'target_answers',
        'pattern': 'mh-targeted-answers',
        'response': 'tappedout_target_answers',
        'cards': [
            'Path to Exile',
            'Swords to Plowshares',
        ]
    },
    {
        'name': 'steady_draw',
        'pattern': 'mh-draw-s',
        'response': 'tappedout_steady_draw',
        'cards': [
            'Rhystic Study',
            'Sylvan Library',
        ]
    },
    {
        'name': 'burst_draw',
        'pattern': 'mh-draw-b',
        'response': 'tappedout_burst_draw',
        'cards': [
            'Harmonize',
            "Jeska's Will",
        ]
    },
    {
        'name': 'tutors',
        'pattern': 'mh-tutors',
        'response': 'tappedout_tutors',
        'cards': [
            'Demonic Tutor',
            'Vampiric Tutor',
        ]
    },
]


@pytest.fixture(scope='module')
def mock_categories(requests_mock):
    for category in categories:
        mock_response(requests_mock, category['pattern'], category['response'])


def test_load_data():
    result = DeckCompositionStep.load_data()

    for category in categories:
        for card in category['cards']:
            assert card in result[category['name']]


@pytest.mark.parametrize('cards, expected', [[
    [
        {'name': 'Austere Command'},
        {'name': 'Wrath of God'},
        {'name': 'Path to Exile'},
        {'name': 'Sylvan Library'},
        {'name': "Jeska's Will"},
        {'name': 'Demonic Tutor'},
    ],
    {
        'board_wipes': 2,
        'target_answers': 1,
        'steady_draw': 1,
        'burst_draw': 1,
        'tutors': 1,
    }
]])
def test_call_no_cache(cards, expected):

    step = DeckCompositionStep()

    result = step({'cards': cards})

    assert_objects_are_equal(result, expected)
