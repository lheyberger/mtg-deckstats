#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from mtg_deckstats.mana_producers_step import ManaProducersStep
from .utils import assert_objects_are_equal


@pytest.mark.parametrize('cards, expected', [
    [
        [],
        {'mana_producers': 0}
    ],
    [
        [{}],
        {'mana_producers': 0}
    ],
    [
        [{'produced_mana': 'w'}],
        {'mana_producers': 1}
    ],
    [
        [{'produced_mana': 'w', 'type_line': 'Basic Land'}],
        {'mana_producers': 0}
    ],
    [
        [
            {'produced_mana': 'w', 'type_line': 'Basic Land'},
            {'produced_mana': 'w'},
        ],
        {'mana_producers': 1}
    ],
    [
        [
            {'produced_mana': 'g', 'type_line': 'Basic Land'},
            {'produced_mana': 'w', 'type_line': 'Basic Land'},
            {'produced_mana': 'g'},
            {'produced_mana': 'w'},
        ],
        {'mana_producers': 2}
    ],
])
def test_mana_producers_step_call(cards, expected):

    step = ManaProducersStep()

    result = step({'cards': cards})

    assert_objects_are_equal(result, expected)
