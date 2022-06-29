#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from mtg_deckstats.rarity_step import RarityStep
from .utils import assert_objects_are_equal


@pytest.mark.parametrize('cards, expected', [
    [
        [
            {'rarity': 'common'},
            {'rarity': 'common'},
            {'rarity': 'common'},
            {'rarity': 'rare'},
            {'rarity': 'rare'},
            {'rarity': 'mythic'},
        ],
        {
            'rarity_common': 3,
            'rarity_rare': 2,
            'rarity_mythic': 1,
        }
    ]
])
def test_rarity_step_call(cards, expected):

    step = RarityStep()

    result = step({'cards': cards})

    assert_objects_are_equal(result, expected)
