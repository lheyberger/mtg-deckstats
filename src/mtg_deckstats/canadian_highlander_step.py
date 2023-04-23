#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from mtg_deckstats.utils import yield_cards, requests_get
from mtg_deckstats.base_step import BaseStep


__all__ = []


class CanadianHighlanderStep(BaseStep):

    def __call__(self, deck):
        points = self.data or self.load_data()
        card_names = [card.get('name') for card in yield_cards(deck)]
        score = sum(v for k, v in points.items() if k in card_names)
        return {
            'canadian_highlander_score': score,
        }

    @classmethod
    def load_data(cls):
        result = (
            requests_get('https://www.canadianhighlander.ca/points-list/')
            .text
        )
        soup = BeautifulSoup(result, features='html.parser')

        points = {}
        for row in soup.find('table').tbody('tr'):
            children = list(row('td', limit=2))
            points[str(children[0].string)] = int(children[1].string)

        return points
