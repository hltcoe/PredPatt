## PredPatt: Predicate-Argument Extraction from Universal Dependencies

PredPatt is a framework of extensible, interpretable, language-neutral
predicate-argument extraction patterns. PredPatt bridges the deep syntax of the
[Universal Dependency](http://universaldependencies.org/) project to an initial
shallow semantic layer: this can form the basis for future layering of semantic
annotations atop Universal Dependency treebanks, and separately can be
considered a linguistically well-founded component of a "Universal IE"
mechanism.

> PredPatt extracts predicates and arguments from text .

    ?a extracts ?b from ?c
        ?a: PredPatt
        ?b: predicates
        ?c: text
    ?a extracts ?b from ?c
        ?a: PredPatt
        ?b: arguments
        ?c: text

See [doctests](doc/DOCTEST.md) for sample output (as well as,
[Portuguese](doc/portuguese.md), [Spanish](doc/spanish.md),
[Chinese](doc/chinese.md)). Additionally, we have example output from the
UDBank in [English](test/data.100.fine.all.ud.expect),
[Spanish](test/es.dev.conllu.expect), and
[Portuguese](test/pt.dev.conllu.expect).


### Installation

    $ git clone https://github.com/hltcoe/PredPatt.git
    $ cd PredPatt
    $ python setup.py develop

### Usage

PredPatt supports many input formats: raw text (English only; via Berekely parser), CoNLLu
data formats and Concretely annotated corpora.

Fire up the interactive web demo locally.

    $ python bin/server.py

Command-line usage (see ``--help`` for other usage)

    $ python -m predpatt test/en-ud-dev.conllu

Example [programmatic usage](doc/using_predpatt.py)

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

### Citation

If you use PredPatt please cite it as follows.

    @inproceedings{white2016universal,
       title  = {Universal Decompositional Semantics on Universal Dependencies},
       author = {Aaron Steven White and Drew Reisinger and Keisuke Sakaguchi and Tim Vieira
                 and Sheng Zhang and Kyle Rawlins and Benjamin {Van Durme}}
       booktitle = {{EMNLP}},
       year   = {2016}
    }
