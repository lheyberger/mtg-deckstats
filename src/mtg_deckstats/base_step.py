#!/usr/bin/env python
# -*- coding: utf-8 -*-


__all__ = ['BaseStep']


class BaseStep():

    def __init__(self, *args, **kwargs):
        del args
        _name = self.__class__.__name__
        self.data = (kwargs.get('data') or {}).get(_name)

    @classmethod
    def load_data(cls):
        return None
