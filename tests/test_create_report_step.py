#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from mtg_deckstats.create_report_step import CreateReportStep
from .utils import assert_objects_are_equal


@pytest.mark.parametrize('args, expected', [[
    [
        {'report_1': 1},
        {'report_2': 2},
    ],
    {
        'report_1': 1,
        'report_2': 2,
    }
]])
def test_step_call(args, expected):

    step = CreateReportStep()

    result = step(*args)

    assert_objects_are_equal(result, expected)
