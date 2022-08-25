#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mtg_deckstats.report import compute


__all__ = ['rank_source', 'rank_report']
__version__ = '0.0.1-alpha.5'


def rank_source(src: str, data: dict = None) -> dict:

    report = compute(src, data=data)

    return rank_report(report)


def rank_report(report: dict = None) -> dict:
    return {
        'report': report,
        'version': __version__,
        'power': _compute_power(report),
        'speed': _compute_speed(report),
        'control': _compute_control(report),
        'consistency': _compute_consistency(report),
    }


def _compute_power(report):
    """
    USED:
        'commander_power_tier': 4,
        'canadian_highlander_score': 4,

    UNUSED:
        'rarity_common': 40,
        'rarity_rare': 37,
        'rarity_uncommon': 19,
        'rarity_mythic': 4,
        'salt_score': 1.98,
    """
    commander_power_tier = report.get('commander_power_tier', 0)
    commander_power_tier = min(commander_power_tier / 9.0, 1.0)

    canadian_highlander_score = report.get('canadian_highlander_score', 0)
    canadian_highlander_score = min(canadian_highlander_score / 20.0, 1.0)

    power = (
        commander_power_tier * 0.8
        +
        canadian_highlander_score * 0.2
    )

    return round(power, 3)


def _compute_speed(report):
    """
    USED:
        'cmc_avg': 1.26,
        'cmc_avg_no_lands': 1.97,
        'steady_draw': 0,
        'burst_draw': 1,
        'mana_producers': 12

    UNUSED:
        'cmc_sum': 126.0,
        'tutors': 0,
    """

    # cmc_avg >= 4.0 --> rank = 0.0
    # cmc_avg <= 1.0 --> rank = 1.0
    cmc_avg = report.get('cmc_avg', 4.0)
    cmc_avg = min((3.0 - (cmc_avg - 1.0)) / 3.0, 1.0)

    # cmc_avg >= 4.5 --> rank = 0.0
    # cmc_avg <= 1.2 --> rank = 1.0
    cmc_avg_no_lands = report.get('cmc_avg_no_lands', 4.5)
    cmc_avg_no_lands = min((3.3 - (cmc_avg_no_lands - 1.2)) / 3.3, 1.0)

    mana_producers = report.get('mana_producers', 0)
    mana_producers = min(mana_producers / 10.0, 1.0)

    steady_draw = report.get('steady_draw', 0)
    steady_draw = min(steady_draw / 5.0, 1.0)

    burst_draw = report.get('burst_draw', 0)
    burst_draw = min(burst_draw / 5.0, 1.0)

    speed = (
        cmc_avg * 0.2
        +
        cmc_avg_no_lands * 0.2
        +
        mana_producers * 0.2
        +
        steady_draw * 0.2
        +
        burst_draw * 0.2
    )

    return round(speed, 3)


def _compute_control(report):
    """
    USED:
        'board_wipes': 0,
        'target_answers': 7,
    """
    board_wipes = report.get('board_wipes', 0)
    board_wipes = min(board_wipes / 3.0, 1.0)

    target_answers = report.get('target_answers', 0)
    target_answers = min(target_answers / 10.0, 1.0)

    control = (
        board_wipes * 0.4
        +
        target_answers * 0.6
    )

    return round(control, 3)


def _compute_consistency(report):
    """
    USED:
        'combos_level': 0,
        'combos_density': 0,
        'tutors': 0,
        'steady_draw': 0,
        'burst_draw': 1,
    """
    combos_level = report.get('combos_level', 0)
    combos_level = min(combos_level / 9.0, 1.0)

    combos_density = report.get('combos_density', 0)
    combos_density = min(combos_density / 3.0, 1.0)

    tutors = report.get('tutors', 0)
    tutors = min(tutors / 5.0, 1.0)

    steady_draw = report.get('steady_draw', 0)
    steady_draw = min(steady_draw / 5.0, 1.0)

    burst_draw = report.get('burst_draw', 0)
    burst_draw = min(burst_draw / 5.0, 1.0)

    consistency = (
        combos_level * 0.4
        +
        combos_density * 0.2
        +
        tutors * 0.2
        +
        steady_draw * 0.15
        +
        burst_draw * 0.05
    )

    return round(consistency, 3)
