#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mtg_deckstats.run_graph import run_graph


def test_run_graph():

    functions = {
        'return_1': lambda: 1,
        'return_2': lambda: 2,
        'sum': lambda x,y: x+y,
    }
    dependencies = {
        'return_1': [],
        'return_2': [],
        'sum': [
            'return_1',
            'return_2'
        ],
    }

    results = run_graph(functions, dependencies)

    return results.get('sum') == 3
