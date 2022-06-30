#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from mtg_deckstats.mana_value_step import ManaValueStep
from .utils import assert_objects_are_equal


@pytest.mark.parametrize('cards, expected', [[
    [
        {'cmc': 0, 'type_line': 'Land'},
        {'cmc': 0, 'type_line': 'Land'},
        {'cmc': 1},
        {'cmc': 1},
        {'cmc': 2},
        {'cmc': 2},
        {'cmc': 3},
        {'cmc': 3},
    ],
    {
        'cmc_sum': 12,
        'cmc_avg': 1.5,
        'cmc_avg_no_lands': 2,
    }
]])
def test_step_call(cards, expected):

    step = ManaValueStep()

    result = step({'cards': cards})

    assert_objects_are_equal(result, expected)
