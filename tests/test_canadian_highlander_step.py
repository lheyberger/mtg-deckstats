#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from jinja2 import Template
from mtg_deckstats.canadian_highlander_step import CanadianHighlanderStep


def _mock_api_call(requests_mock, cards):
    template = Template(r"""
    <table>
        <tbody>
            {% for card in cards %}
            <tr><td>{{card.name}}</td><td>{{card.score}}</td></tr>
            {% endfor %}
        </tbody>
    <table>
    """)
    html = template.render(cards=cards)

    requests_mock.get(
        'https://www.canadianhighlander.ca/points-list/',
        text=html
    )


@pytest.mark.parametrize('cards', [
    [
        {'name': 'Sol Ring', 'score': 1},
        {'name': 'Mana Crypt', 'score': 2},
        {'name': 'Vampiric Tutor', 'score': 3},
    ],
])
def test_load_data(requests_mock, cards):

    _mock_api_call(requests_mock, cards)

    result = CanadianHighlanderStep.load_data()

    assert result
    for card in cards:
        assert result[card.get('name')] == card.get('score')


@pytest.mark.parametrize('cards, score', [
    [
        [
            {'name': 'Sol Ring', 'score': 1},
            {'name': 'Mana Crypt', 'score': 2},
            {'name': 'Vampiric Tutor', 'score': 3},
        ],
        6,
    ],
])
def test_call_no_cache(requests_mock, cards, score):

    _mock_api_call(requests_mock, cards)

    step = CanadianHighlanderStep()
    result = step({'cards': cards})

    assert result['canadian_highlander_score'] == score



@pytest.mark.slow
@pytest.mark.parametrize('cards', [
    [
        {'name': 'Sol Ring'},
        {'name': 'Mana Crypt'},
        {'name': 'Vampiric Tutor'},
    ],
])
def test_slow_load_data(cards):

    result = CanadianHighlanderStep.load_data()

    assert result
    for card in cards:
        assert result[card.get('name')] > 0
