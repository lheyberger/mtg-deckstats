#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mtg_deckstats.base_step import BaseStep


def test_init():

    class TestStep(BaseStep):
        pass

    step = TestStep(data={'TestStep': 42})

    assert step.data == 42


def test_load_data_default():

    step = BaseStep()

    assert step.load_data() is None


def test_load_data_overload():

    class TestStep(BaseStep):

        @classmethod
        def load_data(cls):
            return 42

    step = TestStep()

    assert step.load_data() == 42
