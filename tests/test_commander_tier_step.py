#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from mtg_deckstats.commander_tier_step import CommanderTierStep
from .utils import mock_responses


def _mock_api_call(requests_mock):
    mock_responses(
        requests_mock,
        'GET',
        r'https://tappedout.net/',
        [
            'tappedout_commander_tiers_1',
            'tappedout_commander_tiers_2',
        ],
    )


@pytest.mark.parametrize('commanders', [[
    "Najeela, the Blade-Blossom",
    "Thrasios, Triton Hero",
    "Tymna the Weaver",
    "Barktooth Warbeard",
]])
def test_load_data(requests_mock, commanders):

    _mock_api_call(requests_mock)

    cmdrs, tiers, default = CommanderTierStep.load_data()

    cmdr_tiers = set(cmdrs.values())
    assert default in tiers
    for tier in tiers:
        assert tier in cmdr_tiers
    for commander in commanders:
        assert commander in cmdrs


@pytest.mark.parametrize('cards', [
    [{'tags': ['commander'], 'name': "Najeela, the Blade-Blossom"}],
    [{'tags': ['commander'], 'name': "Thrasios, Triton Hero"}],
    [{'tags': ['commander'], 'name': "Tymna the Weaver"}],
    [{'tags': ['commander'], 'name': "Barktooth Warbeard"}],
])
def test_call_no_cache_one_commander(requests_mock, cards):

    _mock_api_call(requests_mock)

    step = CommanderTierStep()
    result = step({'cards': cards})

    assert result['commander_power_tier'] >= 0


@pytest.mark.parametrize('cards', [
    [
        {'tags': ['commander'], 'name': "Najeela, the Blade-Blossom"},
        {'tags': ['commander'], 'name': "Barktooth Warbeard"},
    ],
])
def test_call_no_cache_two_commanders(requests_mock, cards):

    _mock_api_call(requests_mock)

    step = CommanderTierStep()
    result = step({'cards': cards})

    assert result['commander_power_tier'] >= 0


@pytest.mark.slow
@pytest.mark.parametrize('commanders', [[
    "Najeela, the Blade-Blossom",
    "Thrasios, Triton Hero",
    "Tymna the Weaver",
    "Barktooth Warbeard",
]])
def test_slow_load_data(commanders):

    cmdrs, tiers, default = CommanderTierStep.load_data()

    cmdr_tiers = set(cmdrs.values())
    assert default in tiers
    for tier in tiers:
        assert tier in cmdr_tiers
    for commander in commanders:
        assert commander in cmdrs
