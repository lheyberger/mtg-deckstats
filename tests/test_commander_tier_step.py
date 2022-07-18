#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from mtg_deckstats.commander_tier_step import CommanderTierStep
from .utils import mock_responses


@pytest.mark.parametrize('commanders', [[
    "Codie, Vociferous Codex",
    "Kenrith, the Returned King",
    "Kraum, Ludevic's Opus",
    "Najeela, the Blade-Blossom",
    "Thrasios, Triton Hero",
    "Tymna the Weaver",
]])
def test_load_data(requests_mock, commanders):

    mock_responses(
        requests_mock,
        'GET',
        r'https://tappedout.net/',
        [
            'tappedout_commander_tiers_1',
            'tappedout_commander_tiers_2',
        ],
    )

    cmdrs, tiers, default = CommanderTierStep.load_data()

    cmdr_tiers = cmdrs.values()
    assert default in tiers
    for tier in tiers:
        assert tier in cmdr_tiers
    for commander in commanders:
        assert commander in cmdrs


@pytest.mark.parametrize('cards', [
    [{'tags': ['commander'], 'name': "Codie, Vociferous Codex"}],
    [{'tags': ['commander'], 'name': "Kenrith, the Returned King"}],
    [{'tags': ['commander'], 'name': "Kraum, Ludevic's Opus"}],
    [{'tags': ['commander'], 'name': "Najeela, the Blade-Blossom"}],
    [{'tags': ['commander'], 'name': "Thrasios, Triton Hero"}],
    [{'tags': ['commander'], 'name': "Tymna the Weaver"}],
])
def test_call_no_cache(requests_mock, cards):

    mock_responses(
        requests_mock,
        'GET',
        r'https://tappedout.net/',
        [
            'tappedout_commander_tiers_1',
            'tappedout_commander_tiers_2',
        ],
    )

    step = CommanderTierStep()
    result = step({'cards': cards})

    assert result['commander_power_tier'] >= 0
