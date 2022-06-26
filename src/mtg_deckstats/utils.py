#!/usr/bin/env python
# -*- coding: utf-8 -*-


__all__ = ['cleanup_name', 'yield_cards']


def cleanup_name(name):
    name = name.split('//', maxsplit=1)
    name = name[0]
    name = name.strip()
    return name


def yield_cards(deck):
    for card in deck.get('cards', ()):
        for _ in range(card.get('quantity', 1)):
            yield card
