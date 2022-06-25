# mtg-deckstats

![PyPI](https://img.shields.io/pypi/v/mtg-deckstats)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mtg-deckstats)
![GitHub](https://img.shields.io/github/license/lheyberger/mtg-deckstats)


## How to install

	pip install mtg-deckstats


## Quick Start

Generate a deckstats report using the following steps:

	import mtg_deckstats
	
	report = mtg_deckstats.report('<decklist url>')
	print(report)


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
