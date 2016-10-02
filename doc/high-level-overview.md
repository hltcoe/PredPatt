How PredPatt works
==================

PredPatt employs deterministic, unlexicalized rules over UD parses: a detailed
description of PredPatt’s rules is available [here](RULES.md). For a collection
of linguistically-motivated examples see our [documentation tests](DOCTEST.md).

Here we provide a high-level overview of the process and examples.

1. Predicate and argument root identification
2. Argument resolution
3. Predicate and argument phrase extraction
4. Optional Post-processing

<img width="500px" src="figure1.png"/>

**UD Parse** A universal dependency (UD) parse, is a set of labeled pairs of the
form `relation(dependent,governor)`. The UD parse also includes a sequence of
Universal POS tags. An example of a UD parse is given in Figure 1.

**Predicate and argument root identification** Predicate and argument
roots (i.e., dependency tree nodes) are identified by local
configurations—specifically edges in the UD parse. The simplest example
is `nsubj(s, v)` and `dobj(o, v)`, which indicate that `v` is a
predicate root, and that `s` and `o` are argument roots. Similarly,
roots of clausal subjects and clausal complements are also predicate
roots. Nominal modifiers inside adverbial modifiers are arguments to the
verb being modified, e.g., *Investors turned away from [the stock
market]*. PredPatt also extracts relations from appositives,
possessives, copula, and adverbial modifiers.

**Argument resolution** For example, the sentence *Chris expects to visit Pat*
is missing the explicit arc `nsubj(Chris, visit)` because UD analysis does not
include traces nodes.  PredPatt includes argument resolution rules to handle
missing arguments of many syntactic constructions, including predicate
coordination, relative clauses, and embedded clauses. Argument resolution is
crucial in languages that mark arguments using morphology, such as Spanish and
Portuguese, because there are more cases of covert subjects. Other common cases
for argument resolution are when predicates appear in a conjunction, e.g.,
*Chris likes to sing and dance*, has no arc from *dance* to its subject
*Chris*. In relative clauses, the arguments of an embedded clause appear outside
the subtree, e.g., *borrowed* in *The books John borrowed from the library are
overdue.* has *books* as an argument and so does *are-overdue*.

**Predicate phrase extraction** PredPatt extract a descriptive name for complex
predicate. For example, "*[PredPatt]* **finds** *[structure]* **in** *[text]*".
has a 3-place predicate named (`?a` **finds** `?b` **in** `?c`). The primary
logic here is (a) to lift mark and case tokens (e.g., *in*) out of the argument
subtree, (b) to add adverbial modifiers, auxiliaries, and negation (e.g.,
"*[Chris]* **did not sleep quietly**"). PredPatt uses the text order of tokens
and arguments to derive a name for the predicate; no effort is made to further
canonicalize this name, nor align it to a verb ontology.


**Argument phrase extraction** Argument extraction filters tokens from
the dependency subtree below the argument root. These filters primarily
simplify the subtree, e.g., removing relative clauses and appositives
inside an argument. The default set of filters were chosen to preserve
meaning, since it is not generally the case that all modifiers can
safely be dropped (more aggressive argument simplification settings are
available as options).

**Post-processing** PredPatt implements a number
of optional post-processing routines, such as conjunction expansion,
argument simplification (which filters out non-core arguments, leaving
only subjects and objects), and language-specific hooks.[6] For
example, conjunctions appearing inside arguments may be optionally
expanded, e.g.:

> *Chris loves cake and ice cream.* <br/>
> ⇒ *[Chris]* **loves** *[cake]* <br/>
> ⇒ *[Chris]* **loves** *[ice cream]* <br/>

where these optional steps may lead to errors, such as here with respect to
distributivity:

> *Chris and Pat are a team* <br/>
> ⇒ * *[Chris]* **are a team** <br/>
> ⇒ * *[Pat]* **are a team** <br/>

[6]: UD itself allows for language-specific exceptions to the ``universal'' standard, and we therefore allow that practice here.}


<!--
Example output
--------------

Below we show some "good" and "bad" outputs from our evaluation in multiple
languages.

**Good examples**

1.
> Yuvraj made 68 before he top-edged a ball from Muttiah Muralitharan to the
> cover region, but Indian captain Mahendra Singh Dhoni kept Dravid company at
> the break on 29.<br/>
> ⇒ *[Indian captain Mahendra Singh Dhoni]* **kept** *[Dravid company]* **at** *[the break]* **on** *[29]*

2.
> Conklin said he watched the vehicle sail through the air and had turned to
> wait for the next one when he heard a commotion.<br/>
> ⇒  *[he]* **hand turned to wait for** *[the next one]*

3.

> Ambos habían insonorizadas este espacio subterráneo pequeño, que se encontraba
> en el jardín delantero de la casa.<br/>
> ⇒ *[este espacio subterráneo pequeño]* *[se]* **encontrabaen** *[el jardín delantero de la casa]*

**Bad examples**

4.
> Minutes earlier, three other attackers fired two missiles at an Israeli
> passenger plane with 261 Israeli tourists on board, as it took off from
> Mombasa airport, and narrowly missed the aircraft.<br/>

> ⇒ **Minute earlier** *[three other attackers]*

> Reason: Parse error: *[Minute earlier]* is not `ccomp`.

5.
> Este enfoque destacó los diseños de aviones que fueran capaces de realizar
> "rápidas transiciones" – cambios rápidos en velocidad, altitud, y dirección –
> en lugar de basar se solamente en la alta velocidad como virtud principal .<br/>

> ⇒ *[los diseños de aviones]* **fueran capaces**

> Reason: PredPatt error: Missing arguments.

6.
> 中国大学南方学院积极开展国际交流与合作，与国外十 余所高等院校保持紧密联系，开展形式多样的合作交流。<br/>
> ⇒ **与** *[国外十余所高等院校]* **保持** *[紧密联系]* *[开展]*

> Reason: Treebank error: 开展 is not the governor of 保持.
-->


<!--
Conclusion
==========

PredPatt is a predicate-argument framework built atop Universal
Dependencies, illustrated with an evaluation on 5 distinct treebanks.
We performed a large crowd-sourced evaluation on English data, which
enabled us to develop a calibration system for controlling precision.
PredPatt forms an initial shallow semantic layer that is a basis for
future layering of semantic annotations, and can also be considered a
linguistically well-founded component of a “Universal” information
extraction mechanism which will improve automatically in its quality and
multi-lingual support as UD treebanks continue to be created and
enriched.
-->
