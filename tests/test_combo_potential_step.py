#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from mtg_deckstats.combo_potential_step import ComboPotentialStep
from .utils import mock_response


def _mock_combos(requests_mock):
    mock_response(
        requests_mock,
        'https://docs.google.com',
        'combo_spreadsheet'
    )


@pytest.mark.parametrize('combos', [[
    ('ub', 'Demonic Consultation', "Thassa's Oracle"),
    ('ru', 'Deadeye Navigator', 'Dockside Extortionist'),
]])
def test_load_data(requests_mock, combos):

    _mock_combos(requests_mock)

    result = ComboPotentialStep.load_data()

    for combo in combos:
        combo_list = result
        combo_list = (c for c in combo_list if set(c['ci']) == set(combo[0]))
        combo_list = (c for c in combo_list if c['cards'] == set(combo[1:]))
        combo_list = list(combo_list)
        assert len(combo_list) == 1


@pytest.mark.parametrize('cards, combo_density', [[
    [
        {'name': "Thassa's Oracle", 'cmc': 2, 'color_identity': 'u'},
        {'name': "Demonic Consultation", 'cmc': 1, 'color_identity': 'b'},
        {'name': "Dockside Extortionist", 'cmc': 2, 'color_identity': 'r'},
        {'name': "Deadeye Navigator", 'cmc': 6, 'color_identity': 'b'},
    ],
    2
]])
def test_call_no_cache(requests_mock, cards, combo_density):

    _mock_combos(requests_mock)

    step = ComboPotentialStep()

    result = step({'cards': cards})

    assert result['combos_density'] == combo_density
    assert result['combos_level'] >= 0 and result['combos_level'] <= 9


@pytest.mark.slow
@pytest.mark.parametrize('combos', [[
    ('ub', 'Demonic Consultation', "Thassa's Oracle"),
    ('ru', 'Deadeye Navigator', 'Dockside Extortionist'),
]])
def test_slow_load_data(combos):

    result = ComboPotentialStep.load_data()

    for combo in combos:
        combo_list = result
        combo_list = (c for c in combo_list if set(c['ci']) == set(combo[0]))
        combo_list = (c for c in combo_list if c['cards'] == set(combo[1:]))
        combo_list = list(combo_list)
        assert len(combo_list) == 1

    return result
