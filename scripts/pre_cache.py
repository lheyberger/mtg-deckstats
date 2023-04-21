#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import pickle
import mtg_deckstats


DEFAULT_CACHE_NAME='cache.pkl'


@click.command()
@click.argument('output', type=click.File('wb'), default=DEFAULT_CACHE_NAME)
def main(output):
    """Generates a cache file."""
    data = mtg_deckstats.pre_cache()
    pickle.dump(
        data,
        output,
        pickle.HIGHEST_PROTOCOL,
    )


if __name__ == '__main__':
    main(DEFAULT_CACHE_NAME)
