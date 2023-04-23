#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests import Session
from requests.adapters import HTTPAdapter, Retry


__all__ = []


def cleanup_name(name):
    name = name.split('//', maxsplit=1)
    name = name[0]
    name = name.strip()
    return name


def yield_cards(deck):
    for card in deck.get('cards', ()):
        for _ in range(card.get('quantity', 1)):
            yield card


def requests_get(url):
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session = Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session.get(url)
