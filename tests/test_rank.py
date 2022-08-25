#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mtg_deckstats


@pytest.mark.parametrize('src, report, rank', [
    [
        'https://www.moxfield.com/decks/Agzx8zsi5UezWBUX5hMJPQ',
        {
            'board_wipes': 0,
            'burst_draw': 0,
            'canadian_highlander_score': 0,
            'cmc_avg': 4.0,
            'cmc_avg_no_lands': 4.5,
            'combos_density': 0,
            'combos_level': 0,
            'commander_power_tier': 0,
            'mana_producers': 0,
            'steady_draw': 0,
            'target_answers': 0,
            'tutors': 0,
        },
        {
            'power': 0.0,
            'speed': 0.0,
            'control': 0.0,
            'consistency': 0.0,
        },
    ],
    [
        'https://www.moxfield.com/decks/Agzx8zsi5UezWBUX5hMJPQ',
        {
            'board_wipes': 3,
            'burst_draw': 5,
            'canadian_highlander_score': 20,
            'cmc_avg': 1.0,
            'cmc_avg_no_lands': 1.2,
            'combos_density': 3,
            'combos_level': 9,
            'commander_power_tier': 9,
            'mana_producers': 10.0,
            'steady_draw': 5,
            'target_answers': 10,
            'tutors': 5,
        },
        {
            'power': 1.0,
            'speed': 1.0,
            'control': 1.0,
            'consistency': 1.0,
        },
    ],
])
def test_rank(monkeypatch, src, report, rank):

    def mock_compute(*args, **kwargs):
        del args
        del kwargs
        return report

    monkeypatch.setattr(
        mtg_deckstats.rank, 'compute',
        mock_compute,
    )

    result = mtg_deckstats.rank_source(src)

    assert rank.items() <= result.items()


@pytest.mark.parametrize('report, rank', [
    [
        {
            'commander_power_tier': 0,
            'canadian_highlander_score': 0,
        },
        {
            'power': 0.0,
        },
    ],
    [
        {
            'commander_power_tier': 9,
            'canadian_highlander_score': 20,
        },
        {
            'power': 1.0,
        },
    ],
])
def test_rank_report_power(report, rank):
    result = mtg_deckstats.rank_report(report)
    assert rank.items() <= result.items()


@pytest.mark.parametrize('report, rank', [
    [
        {
            'cmc_avg': 4.0,
            'cmc_avg_no_lands': 4.5,
            'mana_producers': 0,
            'steady_draw': 0,
            'burst_draw': 0,
        },
        {
            'speed': 0.0,
        },
    ],
    [
        {
            'cmc_avg': 1.0,
            'cmc_avg_no_lands': 1.2,
            'mana_producers': 10,
            'steady_draw': 5,
            'burst_draw': 5,
        },
        {
            'speed': 1.0,
        },
    ],
])
def test_rank_report_speed(report, rank):
    result = mtg_deckstats.rank_report(report)
    assert rank.items() <= result.items()


@pytest.mark.parametrize('report, rank', [
    [
        {
            'board_wipes': 0,
            'target_answers': 0,
        },
        {
            'control': 0.0,
        },
    ],
    [
        {
            'board_wipes': 3,
            'target_answers': 10,
        },
        {
            'control': 1.0,
        },
    ],
])
def test_rank_report_control(report, rank):
    result = mtg_deckstats.rank_report(report)
    assert rank.items() <= result.items()


@pytest.mark.parametrize('report, rank', [
    [
        {
            'combos_level': 0,
            'combos_density': 0,
            'tutors': 0,
            'steady_draw': 0,
            'burst_draw': 0,
        },
        {
            'consistency': 0.0,
        },
    ],
    [
        {
            'combos_level': 9,
            'combos_density': 3,
            'tutors': 5,
            'steady_draw': 5,
            'burst_draw': 5,
        },
        {
            'consistency': 1.0,
        },
    ],
])
def test_rank_report_consistency(report, rank):
    result = mtg_deckstats.rank_report(report)
    assert rank.items() <= result.items()
