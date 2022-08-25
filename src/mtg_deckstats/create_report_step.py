#!/usr/bin/env python
# -*- coding: utf-8 -*-


__all__ = []


class CreateReportStep():

    def __call__(self, *args):
        result = {}
        for arg in args:
            result.update(arg)
        return result
