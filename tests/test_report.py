#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint
import pytest
import mtg_deckstats


@pytest.mark.slow
@pytest.mark.parametrize('src', [
    (
        'https://aetherhub.com'
        '/Deck/mtg-parser-3-amigos'
    ),
    (
        'https://www.archidekt.com'
        '/decks/1365846/'
    ),
    (
        'https://deckstats.net'
        '/decks/30198/2034245--mtg-parser-3-amigos'
    ),
    (
        'https://www.moxfield.com'
        '/decks/Agzx8zsi5UezWBUX5hMJPQ'
    ),
    (
        'https://www.mtggoldfish.com'
        '/deck/3935836'
    ),
    (
        'https://scryfall.com'
        '/@gorila/decks/e7aceb4c-29d5-49f5-9a49-c24f64da264b'
    ),
    (
        'https://tappedout.net'
        '/mtg-decks/mtg-parser-3-amigos/'
    ),
    (
        'https://decks.tcgplayer.com'
        '/magic/commander/gorila/mtg-parser--3-amigos/1384198'
    ),
])
def test_report(src):
    result = mtg_deckstats.report(src)

    assert result
    pprint(result)
