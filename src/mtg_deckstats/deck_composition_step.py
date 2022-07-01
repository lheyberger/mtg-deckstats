#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mtg_parser
from mtg_deckstats.base_step import BaseStep


__all__ = ['DeckCompositionStep']


class DeckCompositionStep(BaseStep):

    def __call__(self, deck):
        categories = self.data or self.load_data()
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
    def load_data(cls):
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
            cat: set(card.name for card in mtg_parser.parse_deck(src))
            for cat, src in sources.items()
        }
