#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from mtg_deckstats.parse_deck_step import ParseDeckStep
from .utils import mock_response, mock_responses


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
def test_call_no_cache(requests_mock, deck):
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

    step = ParseDeckStep(deck['url'])

    result = step()

    expected_fields = set([
        'name',
        'type_line',
        'cmc',
        'color_identity',
        'rarity',
        'quantity',
        'tags',
    ])

    for card in result.get('cards', []):
        assert expected_fields <= set(card.keys())
