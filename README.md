# mtg-deckstats

![PyPI](https://img.shields.io/pypi/v/mtg-deckstats)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mtg-deckstats)
![GitHub](https://img.shields.io/github/license/lheyberger/mtg-deckstats)


## How to install

	pip install mtg-deckstats


## Quick Start

Generate a deckstats report using the following steps:

	import mtg_deckstats
	
	report = mtg_deckstats.compute('<decklist url>')
	print(report)


To speed things up, you can also compute reports with a pre-generated cache using the following steps:

	import mtg_deckstats

	cache = mtg_deckstats.pre_cache()

	report_1 = mtg_deckstats.compute('<decklist url 1>', data=cache)
	print(report_1)

	report_2 = mtg_deckstats.compute('<decklist url 2>', data=cache)
	print(report_2)


## Supported deckbuilding websites

Internally `mtg_deckstats` relies on `mtg_parser` and thus, supports the following deckbuilding websites:
* aetherhub.com
* archidekt.com
* deckstats.net
* moxfield.com
* mtggoldfish.com
* scryfall.com
* tappedout.net
* tcgplayer.com
