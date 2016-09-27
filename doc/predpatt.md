PredPatt: Predicate-Argument Extraction from Universal Dependencies
===================================================================

We present PredPatt, a framework of extensible, interpretable, language-neutral
predicate-argument extraction patterns. PredPatt bridges the deep syntax of the
Universal Dependency project to an initial shallow semantic layer: this can form
the basis for future layering of semantic annotations atop Universal Dependency
treebanks, and separately can be considered a linguistically well-founded
component of a "Universal IE" mechanism.

We consider these dual-uses through manual evaluation of output based on
automatically generated parses in English, and on gold treebanks in Chinese,
English, Hebrew, Hindi, and Spanish.

Introduction and Motivation
===========================

The Stanford Dependencies have become a widely adopted syntactic representation,
lately forming the basis of the
[Universal Dependencies (UD) project](http://universaldependencies.org), an
international effort to convert and create syntactic treebanks into a single
standard form ([de Marneffe et al., 2014](); [Nivre et al., 2016]()). This deep
syntactic representation has become the backbone of a variety of downstream
efforts in information extraction and computational semantics.

The initial Stanford effort ([de Marneffe et al., 2006]()) consisted of a
clearly stated target representation, along with a transformation process over
Penn Treebank style constituency trees: this process was language specific and
not implemented in a way that lent to easy modification by others.

> "The method is general, but requires appropriate rules for each language and
> treebank representation." ([de Marneffe et al., 2006]())

We embrace and extend this highly successful approach, as an effort to enhance
the UD effort with semantic annotations, and to have a cross-lingual information
extraction framework that transparently improves in quality as a result of the
community’s continued progress in UD parsing. Our predicate-argument extraction
framework, PredPatt, is based on extensible, interpretable, language-neutral
extraction patterns. Improving on the strategy of the Stanford conversion
process, we pay special care that our framework can be easily understood and
modified by others: this is meant to improve scientific replicability and to
enable the framework to evolve in sync with future developments in UD.

<img width="50%" align="center" src="figure1.png"/>

PredPatt’s goal is to identify the structure of predicates and
arguments—leaving further analysis to systems pursuing competing
theories.[3] The rules are non-lexicalized, relying on the
“universality” of the UD syntax, which means the framework applies
directly to all UD-supported languages, and to syntactic parses either
manually constructed (as part of enhancing treebanks) or automatically
derived (as part of semantic parsing or information extraction). We
consider these cases through evaluation of output based on automatically
generated parses in English, and on gold treebanks in Chinese, English,
Hebrew, Hindi, and Spanish.

[3]: E.g., PropBank ([Palmer et al., 2005]()), semantic proto-roles ([Reisinger et al., 2015]()), unsupervised approaches ([Poon & Domingoes, 2009]()), interpretation as "OpenIE" tuples

How PredPatt works
==================

PredPatt employs deterministic, unlexicalized rules over UD parses: a
detailed description of PredPatt’s rules is available in the appendix.
Here we provide a high-level overview of the process and examples.

1. Predicate and argument root identification
2. Argument resolution
3. Predicate and argument phrase extraction
4. Optional Post-processing

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


Evaluation
==========

**Gold treebank in multiple languages** We evaluated PredPatt manually on
several randomly sampled sentences taken from the UD banks of Chinese, English,
Hebrew, Hindi and Spanish. This evaluation runs PredPatt with the gold standard
UD parse. For each language, we report the number of sentences evaluated along
with the number of extractions from those sentences (a proxy for recall) and
precision (95% confidence interval).

<table>
<tr><th>Lang</th><th>#Sent</th><th>#Output</th><th>Precision</th><tr>
<tr><td>  Chinese </td><td>   98 </td>    <td> 375 </td><td> 69.1%  ±  4.7% </td></tr>
<tr><td>  English </td><td>   79 </td>    <td> 210 </td><td> 86.2%  ±  4.7% </td></tr>
<tr><td>   Hebrew </td><td>   12 </td>    <td>  30 </td><td> 66.7%  ± 17.9% </td></tr>
<tr><td>    Hindi </td><td>   22 </td>    <td>  50 </td><td> 52.0%  ± 14.3% </td></tr>
<tr><td>  Spanish </td><td>   27 </td>    <td>  55 </td><td> 70.9%  ± 12.4% </td></tr>
</table>

**Large-scale evaluation** We sampled 1000 sentences uniformly at
random from Concretely Annotated Gigaword ([Ferraro et al., 2014]()), which provides
constituency parses from Stanford CoreNLP. We converted these parses to
Universal Dependencies using the PyStanfordDependencies tool. We focus
on English because it is one of the only UD languages that has highly
accurate automatic parsers. Instances were judged as binary "good" or
"bad", three-way redundant, by workers on Mechanical Turk, following a
qualification test to verify annotator reliability.

Running PredPatt on these 1000 sentences gave rise to 2380
automatically identified predicate-argument instances.[^7] Overall, the
proportion of instances labeled “good” (precision) is 80.3%
(±1.6%). This is quite good given how heavily PredPatt
relies on quality of the automatic parses.


[^7]: We added one English-specific tweak to PredPatt output for the
    HIT, which filters dummy arguments from relative clauses (i.e.,
    “which”, “who” or “that”). Unfortunately, there is no
    language-independent way to filter these dummy arguments under the
    UD specification.

We trained a confidence estimator based on this data, which allows us to
improve precision at the expense of recall by thresholding the
confidence score. We trained a simple logistic regression classifier on
the each worker’s judgements. We use the following features: the
identity of which rules that fire, the identity of the conjunction of
the governing relations of each argument in the UD parse (e.g.,
``nsubj+dobj+iobj``), the number of arguments, the predicate
name length, and the sentence length. Results are presented and
discussed in .

The figure below shows the calibration score alongside the precision
against the majority vote of the 3 workers. The plot is an average of
5-fold cross-validation. We see that thresholding by the confidence
increases precision without much loss in the number of extractions. For
example, thresholding at a confidence of 80%, we get 91% precision
with 30% of extractions; thresholding at 60% we get 84%
precision and keep 85% of
extractions.

<img align="center" width="50%" src="calibration.png"/>

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


Related work
============

**OpenIE** Most OpenIE systems produce predicate-argument structures
that resemble PredPatt output at first glance.

> Researchers at the University of Washington, home of related
> systems such as TextRunner ([Yates et al., 2007]()) write:<br/>
> "SRL [semantic role labeling] and Open IE are quite related [...]
> semantically labeled arguments correspond to the arguments in Open
> IE extractions, and verbs often match up with Open IE
> relations" ([Christensen et al., 2011]()).

The most closely related are those relying on dependency trees, including
[ClausIE](https://www.mpi-inf.mpg.de/departments/databases-and-information-systems/software/clausie/)
([Del Corro et al., 2013]()) and ArgOE ([Gamallo & Garcia, 2015]()), which
support multiple languages (Spanish, Portuguese, Galician and English), but are
not based on UD. A key distinction is the flat representation of such OpenIE
statements: relational triples, with predicates and arguments all considered
strings with no internal (compositional) structure. Further, the sets of rules
employed by those systems are less complex, can be dependent on word order, and
rely on lexicalization (language-specific).  For example, consider the forced
binary outputs:


> *John gave the book to Mary yesterday.* <br/>
> **ClausIE**:<br/>
⇒ *[John]* **gave** *[the book to Mary]*<br/>
⇒ *[John]* **gave** *[the book yesterday]*<br/>
⇒ *[John]* **gave** *[the book]*<br/>

> **PredPatt**:<br/>
> ⇒ *[John]* **gave** *[the book]* **to** *[Mary]* *[yesterday]*


[Angeli et al. (2015)]() developed an OpenIE system atop the Stanford
Depedencies, using knowledge base completion as an end-task to derive distant
supervision for a machine learning approach. They map open-domain relations
extracted to closed-domain relations using association mining techniques to
improve the coverage of a knowledge base population system. The bias towards the
knowledge base completion end-task leads to spurious extractions and low recall,
and is not geared toward succinct, human interpretable, language-neutral rules.

**PropBank** PredPatt extractions are similar to those found in the
manually constructed PropBank ([Palmer et al., 2005]()), without the
attendant semantic roles. PredPatt extracts more types of structures,
e.g., copula, appositives, possessives. There are also a number of
differences in argument boundaries.

**Textual Inference** observe that many shallow approaches to
recognizing textual inference break down as the text and hypothesis
become lengthier and more complex. Their solution is to extract a set of
discourse commitments from the text and hypothesis, and determine
entailment by searching for matches over these resulting sets of simpler
propositions. In this case, the process of extracting discourse
commitments from text could be aided by a tool like PredPatt.

**Meaning representations** PredPatt is not a semantic representation, but might
be a useful preprocessing step towards building one. Richer semantic labels
could be assigned in later phases, e.g., PropBank roles ([Palmer et al., 2005]()),
or proto-roles ([Reisinger et al., 2015]()).  Unlike the recently popular Abstract
Meaning Representation ([Banarescu et al., 2013]()), PredPatt retains a strict
commitment to the syntax/semantics interface.  This is both to directly benefit
from ongoing improvements by the community in syntactic parsing, as well as to
enable linguistically well-motivated compositional analysis. These goals
likewise motivated the KNEXT effort ([Schubert, 2002](); [Van Durme & Schubert, 2008]()), a transformation
process that was English-specific, applied to constituency parses to derive
shallow logical forms.

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


References
==========

* Gabor Angeli, Melvin Johnson Premkumar, and Christopher D
  Manning. 2015. Leveraging linguistic structure for open domain information
  extraction. In ACL.

* Laura Banarescu, Claire Bonial, Shu Cai, Madalina Georgescu, Kira Griffitt, Ulf Hermjakob, Kevin Knight,
  Philipp Koehn, Martha Palmer, and Nathan Schneider. 2013. Abstract meaning representation for sembanking.
  In Proceedings of the 7th Linguistic Annotation Workshop and Interoperability with Discourse.

* Janara Christensen, Mausam, Stephen Soderland, and Oren Etzioni. 2011. An analysis of open information extraction based on semantic role labeling.
  In Proceedings of KCAP.

* Marie-Catherine de Marneffe, Bill MacCartney, and Christopher D. Manning. 2006.
  Generating typed dependency parses from phrase structure parses. In LREC.

* Marie-Catherine de Marneffe, Timothy Dozat, Natalia Silveira, Katri Haverinen, Filip Ginter, Joakim Nivre,
  and Christopher D Manning. 2014. Universal stanford dependencies: A cross-linguistic typology. In LREC,
  Volume 14.

* Luciano Del Corro and Rainer Gemulla. 2013.
  Clausie: clause-based open information extraction. In WWW.

* Francis Ferraro, Max Thomas, Matthew R. Gormley, Travis Wolfe, Craig Harman, and Benjamin Van Durme. 2014.
  Concretely annotated corpora. In NIPS Workshop on Automated Knowledge Base Construction (AKBC).

* Pablo Gamallo and Marcos Garcia. 2015. Multilingual open information extraction.
  In Lecture Notes in Computer Science. Springer-Verlag, Berlin.

* Andrew Hickl and Jeremy Bensley. 2007.
  A discourse commitment-based framework for recognizing textual entailment.
  In Proceedings of the ACL-PASCAL Workshop on Textual Entailment and Paraphrasing.

* Joakim Nivre, Marie-Catherine de Marneffe, Filip Ginter, Yoav Goldberg, Jan Hajiˇc, Christopher D. Manning,
  Ryan McDonald, Slav Petrov, Sampo Pyysalo, Natalia Silveira, Reut Tsarfaty, and Daniel Zeman. 2016.
  Universal dependencies v1: A multilingual treebank collection. In LREC.

* Martha Palmer, Daniel Gildea, and Paul Kingsbury. 2005.
  The proposition bank: An annotated corpus of semantic roles.
  Computational linguistics, 31(1):71–106.

* Hoifung Poon and Pedro Domingos. 2009.
  Unsupervised semantic parsing.
  In EMNLP

* Drew Reisinger, Rachel Rudinger, Francis Ferraro, Craig Harman, Kyle Rawlins, and Benjamin Van Durme. 2015.
  Semantic proto-roles. In TACL, volume 3.

* Lenhart K. Schubert. 2002.
  Can we derive general world knowledge from texts?
  In International Conference on Human Language Technology Research.

* Benjamin Van Durme and Lenhart K. Schubert. 2008.
  Open knowledge extraction through compositional language processing.
  In Symposium on Semantics in Systems for Text Processing (STEP).

* Alexander Yates, Michael Cafarella, Michele Banko, Oren Etzioni, Matthew Broadhead, and Stephen Soderland. 2007.
  Textrunner: Open information extraction on the web.
  In Proceedings of HLT-NAACL: Demonstrations.

Appendix: Rules
===============

Predicate root identification
-----------------------------

At this stage, PredPatt identifies predicate root tokens in the input
sentence. The following kinds of tokens are identified as predicate
roots:

-   Governor of subjects (*nsubj, csubj, nsubjpass, csubjpass*), objects
    (*dobj, iobj*), or adverbial clausal modifiers (*advcl*).

-   Clausal modifiers: dependents of *acl*, or *advcl*.

-   (Open) clausal complements: dependents of *ccomp*, or *xcomp*.

-   Conjuncts of other predicate root token (*conj*).

Argument root identification
----------------------------

Given a predicate root token, PredPatt identifies the following tokens
as its argument root tokens.

-   Nominal subjects (*nsubj, nsubjpass*), or objects (*dobj, iobj*) of
    the predpatt root token.

-   Nominal modifier (*nmod*) of the predicate root token.

-   Nominal modifier (*nmod*) of an adverb (*advmod*) which modifies the
    predicate root token.

Argument resolution
-------------------

At this stage, PredPatt extracts additional argument root tokens for the
predicate in special cases:

-   An open clausal complement (the dependent of *xcomp*) is viewed as
    part of the predicate it complements[^xcomp]. Then all argument root
    tokens of the open clausal complement are extracted as the argument
    root of the predicate it complements.

[^xcomp]: [Open clausal complements](http://universaldependencies.org/u/dep/xcomp.html) (*xcomp*) is a predicative or clausal
    complement without its own subject, which means it can’t be an independent predicate.


-   In relative clauses, PredPatt borrows an argument for adjectival
    clausal modifiers (the dependent of *acl*) from the token they
    modify (the governor of *acl*).

-   PredPatt extracts a conjunct token of other argument root token as
    an argument root.

Predicate phrase extraction
---------------------------

At this stage, PredPatt recursively extracts tokens from the subtree of
the predicate root token, then adds them to the predicate phrase, or
stops extraction if one of the following situations is satisfied:

-   The current token is an argument root token of the predicate.

-   The current token is another predicate root token.

-   The current token is a dependent of an *dep* relation.

Argument phrases extraction
---------------------------

At this stage, PredPatt recursively extracts tokens from the subtree of
the argument root token, then adds them to the argument phrase, or stops
extraction if one of the following situations is satisfied:

-   The current token is an argument root token of the predicate.

-   The current token is another predicate root token.

-   The current token is a dependent of the *dep* relation.

-   The current token is a dependent of coordinating conjunction (*cc*).

-   The current token is a dependent of the *case* relation (this token
    will be added to the predicate phrase).

Option: simplification
----------------------

-   Remove a non-core argument, e.g., a nominal modifiers

-   Remove an argument of other type from the predpatt.

-   Remove an adverbial modifiers

-   Remove auxiliary in the predicate phrase.

Special predicate extraction
----------------------------

Besides normal predicate extraction, PredPatt extracts modifiers, such as
the dependent of *amod*, *appos*, or *nmod:poss*, as a predicate and
treats the noun it modifies as an argument of the predicate.
