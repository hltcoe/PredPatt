Related work
============

**OpenIE** Most OpenIE systems produce predicate-argument structures
that resemble PredPatt output at first glance.

> Researchers at the University of Washington, home of related
> systems such as TextRunner ([Yates et al., 2007](references.md)) write:<br/>
> "SRL [semantic role labeling] and Open IE are quite related [...]
> semantically labeled arguments correspond to the arguments in Open
> IE extractions, and verbs often match up with Open IE
> relations" ([Christensen et al., 2011](references.md)).

The most closely related are those relying on dependency trees, including
[ClausIE](https://www.mpi-inf.mpg.de/departments/databases-and-information-systems/software/clausie/)
([Del Corro et al., 2013](references.md)) and ArgOE ([Gamallo & Garcia, 2015](references.md)), which
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


[Angeli et al. (2015)](references.md) developed an OpenIE system atop the Stanford
Depedencies, using knowledge base completion as an end-task to derive distant
supervision for a machine learning approach. They map open-domain relations
extracted to closed-domain relations using association mining techniques to
improve the coverage of a knowledge base population system. The bias towards the
knowledge base completion end-task leads to spurious extractions and low recall,
and is not geared toward succinct, human interpretable, language-neutral rules.

**PropBank** PredPatt extractions are similar to those found in the
manually constructed PropBank ([Palmer et al., 2005](references.md)), without the
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
could be assigned in later phases, e.g., PropBank roles ([Palmer et al., 2005](references.md)),
or proto-roles ([Reisinger et al., 2015](references.md)).  Unlike the recently popular Abstract
Meaning Representation ([Banarescu et al., 2013](references.md)), PredPatt retains a strict
commitment to the syntax/semantics interface.  This is both to directly benefit
from ongoing improvements by the community in syntactic parsing, as well as to
enable linguistically well-motivated compositional analysis. These goals
likewise motivated the KNEXT effort ([Schubert, 2002](references.md); [Van Durme & Schubert, 2008](references.md)), a transformation
process that was English-specific, applied to constituency parses to derive
shallow logical forms. A similar approach was explored in [Rudinger & Van Durme, 2014](references.md) with the goal of understanding the extent to which the Stanford dependency *syntax* representation is a *semantic* representation.

