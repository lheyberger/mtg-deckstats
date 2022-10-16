#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import pytest
from mtg_deckstats.salt_step import SaltStep


@pytest.mark.parametrize('card_name, salt_score', [
    ['Sol Ring', 42],
    ['Mana Crypt', 42.42],
])
def test_salt_step_load_data_with_salt(requests_mock, card_name, salt_score):

    cards = [{
        'name': card_name,
        'salt': salt_score,
    }]

    requests_mock.get(
        re.compile('https://json.edhrec.com/'),
        json={
            'container': {
                'json_dict': {
                    'cardlists': [{
                        'cardviews': cards
                    }]
                }
            }
        }
    )

    result = SaltStep.load_data()

    assert result[card_name] == salt_score


@pytest.mark.parametrize('card_name, salt_score', [
    ['Sol Ring', 1.4242424242],
    ['Mana Crypt', 42.42],
])
def test_salt_step_load_data_with_label(requests_mock, card_name, salt_score):

    cards = [{
        'name': card_name,
        'label': f'salt score {salt_score}',
    }]

    requests_mock.get(
        re.compile('https://json.edhrec.com/'),
        json={
            'container': {
                'json_dict': {
                    'cardlists': [{
                        'cardviews': cards
                    }]
                }
            }
        }
    )

    result = SaltStep.load_data()

    assert result[card_name] == salt_score


@pytest.mark.parametrize('cards, salt_score', [
    [
        [
            {'name': 'Sol Ring', 'salt': 3.0},
            {'name': 'Mana Crypt', 'salt': 2.0},
        ],
        5.0,
    ]
])
def test_salt_step_call_no_cache(requests_mock, cards, salt_score):

    requests_mock.get(
        re.compile('https://json.edhrec.com/'),
        json={
            'container': {
                'json_dict': {
                    'cardlists': [{
                        'cardviews': cards
                    }]
                }
            }
        }
    )

    step = SaltStep()
    result = step({'cards': cards})

    assert round(result['salt_score'], 2) == round(salt_score, 2)


@pytest.mark.slow
def test_salt_step_load_data():
    salt_score = SaltStep.load_data()

    assert len(salt_score) > 0
