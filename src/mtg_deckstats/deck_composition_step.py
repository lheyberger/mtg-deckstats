#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import mtg_parser


__all__ = []


class DeckCompositionStep():

    def __init__(self, data: dict = None, session=None):
        self._data = (data or {}).get(self.__class__.__name__)
        self._session = session

    def __call__(self, deck):
        categories = self._data or self.load_data(self._session)
        card_names = set(c.get('name') for c in deck.get('cards', []))

        def how_many(category):
            return len(card_names & categories.get(category, set()))

        return {
            'board_wipes': how_many('board_wipes'),
            'target_answers': how_many('target_answers'),
            'steady_draw': how_many('steady_draw'),
            'burst_draw': how_many('burst_draw'),
            'tutors': how_many('tutors'),
        }

    @classmethod
    def load_data(cls, session=None):
        session = session or requests
        sources = {
            'board_wipes':
                'https://tappedout.net/mtg-decks/mh-mass-answers/',
            'target_answers':
                'https://tappedout.net/mtg-decks/mh-targeted-answers/',
            'steady_draw':
                'https://tappedout.net/mtg-decks/mh-draw-s/',
            'burst_draw':
                'https://tappedout.net/mtg-decks/mh-draw-b/',
            'tutors':
                'https://tappedout.net/mtg-decks/mh-tutors/',
        }
        return {
            cat: set(card.name for card in mtg_parser.parse_deck(src, session))
            for cat, src in sources.items()
        }
