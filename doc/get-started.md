# Get Started

## Installation

    $ git clone https://github.com/hltcoe/PredPatt.git
    $ cd PredPatt
    $ python setup.py develop

## Usage

PredPatt supports many input formats: raw text (English only; via Berekely parser), CoNLLu
data formats and Concretely annotated corpora.

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
?a loves ?b	[loves-root,c,c,n1,n2,n2,u]
        ?a: Chris	[Chris-nsubj,g1(nsubj)]
        ?b: silly dogs	[dogs-dobj,g1(dobj),o1,o5,o6]
    ?a loves ?b	[loves-root,c,c,n1,n2,n2,u]
        ?a: Chris	[Chris-nsubj,g1(nsubj)]
        ?b: clever cats	[cats-conj,m,o1]
    ?a is/are silly	[silly-amod,e]
        ?a: dogs	[dogs-dobj,i,o3,o5,o6]
    ?a is/are clever	[clever-amod,e]
        ?a: cats	[cats-conj,i,o3]
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
