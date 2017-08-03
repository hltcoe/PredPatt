# Get Started

## Installation

The most straight forward way to install `PredPatt` is via `pip:

    $ pip install git+https://github.com/hltcoe/PredPatt.git

Alternatively, one can install from source:

    $ git clone https://github.com/hltcoe/PredPatt.git
    $ cd PredPatt
    $ python setup.py develop

## Usage

PredPatt supports many input formats: raw text (English only; via Berkeley parser), CoNLLu
data formats and [Concretely annotated corpora](https://github.com/hltcoe/concrete-docs/blob/master/GETTING_STARTED.md).

Fire up the interactive web demo locally.

    $ python bin/server.py

Command-line usage (see ``--help`` for other usage)

    $ python -m predpatt test/en-ud-dev.conllu

Example [programmatic usage](using_predpatt.py)

```python
>>> from predpatt import PredPatt
>>> pp = PredPatt.from_sentence('Chris loves silly dogs and clever cats .')
>>> print pp.pprint()
```
```
	?a loves ?b	[loves-root]
		?a: Chris	[Chris-nsubj]
		?b: silly dogs and clever cats	[dogs-dobj]
```

Notes:

 - The first time you call `PredPatt.from_sentence`, the Berkeley parser will be
   downloaded. So it might take a little while and you'll need an internet
   connection. It will store the parser and it's grammar in `~/.PredPatt`.

- The parser is generally slow to parse the first sentence and significantly
  faster on subsequent ones because it lazily loads the parsing model, etc.

- There is a caching layer on top of the parser, which caches sentences under
  `~/.PredPatt`. To bypass the caching layer, invoke `from_sentence` with the
  `cacheable=False` option.

- There are a substantial number of options for a variety of syntactic
  phenomena. For more information see the [tutorial](tutorial.ipynb). 
