PredPatt's Rules
================

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
    part of the predicate it complements.[1] Then all argument root
    tokens of the open clausal complement are extracted as the argument
    root of the predicate it complements.

    [1]: [Open clausal complements](http://universaldependencies.org/u/dep/xcomp.html) (*xcomp*) is a predicative or clausal complement without its own subject, which means it can’t be an independent predicate.


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


<!--
## Rules Description

At a high level PredPatt operates in the following stages

1. Predicate root identification
2. Argument root identification
3. Post-processing (xcomp merge, relative clause resolution, conjunction argument resolution)
4. Predicate and argument phrase extraction (and optionally simplification)
5. Conjunction expansion

### Rules for extracting predicate root token

- **a1**: Extract a predicate token from the dependent of clausal complement ``ccomp``.

  > He says that you **like** to swim.

- **a2**: Extract a predicate token from the dependent of clausal complement ``xcomp``.

  > I started to **work** there yesterday.

- **b**: Extract a predicate token from the dependent of clausal modifier.

  -  acl:

     > the issues as he **sees** them. ``acl(sees, issues)``

  -  acl:relcl:

     > a form of asbestos once **used** to make Kent cigarette filters. ``acl:relcl(used, form)``

  -  advcl:

     > The asbestos fiber, crocidolite, is unusually resilient once it **enters** the lungs. ``advcl(enters, resilient)``

- **c**: Extract a predicate token from the governor of the following relations.

    - nsubj:

    > Clinton **defeated** Dole. ``nsubj(Clinton, defeated)``

    - nsubjpass:

    > Dole was **defeated** by Clinton. ``nsubjpass(Dole, defeated)``

    - dobj:

    > Clinton **defeated** Dole. ``dobj(Dole, defeated)``

  - iobj:

    > She **gave** me a raise. ``iobj(me, gave)``

  - ccomp:

    > He **says** that you like to swim. ``ccomp(like, says)``.

  - xcomp:

    > I **started** to work there yesterday. ``xcomp(work, started)``

  - advcl:

    > The asbestos fiber, crocidolite, is unusually **resilient** once it enters the lungs. ``advcl(enters, resilient)``

- **d**: Extract a predicate token from the dependent of apposition.

  > Sam, my **brother**, arrived. ``appos(brother, Sam)``

- **e**: Extract a predicate token from the dependent of an adjectival modifier.

  > Sam eats **red** meat. ``amod(red, meat)``

- **v**: Extract a predicate token from the dependent of possessive relation.

  > I like **his** toy. ``nmod:poss(toy, his)``

- **f**: Extract a conjunct token of other predicate token.

  > He came home and **took** a shower. ``conj(took, came)``

### Rules for extracting argument root token:
- **g1**: Extract an argument token from the dependent of the following relations.

  - nsubj:

    > **Clinton** defeated Dole. ``nsubj(Clinton, defeated)``

  - nsubjpass:

    > **Dole** was defeated by Clinton. ``nsubjpass(Dole, defeated)``

- **g2**: Extract an argument token from the dependent of the following relations.

  - dobj:

    > She gave me a **raise**. ``dobj(raise, gave)``

  - iobj:

    > She gave **me** a raise. ``iobj(me, gave)``

- **h1**: Extract an argument token from the dependent of the following
  relations which directly depends on the predicate token.

  - nmod:

    > Mr. Vinken is chairman of **Elsevier**. ``nmod(Elsevier, chairman)``

  - nmod:npmod:

    > The average seven-day compound **yield** eased a fraction of a percentage point. ``nmod:npmod(yield, eased)``

  - nmod:tmod:

    > He spends his **days** sketching passers-by. ``nmod:tmod(days, spends)``

- **h2**: Extract an argument token, which indirectly depends on the
  predicate token, from the adverbial phrase.

  - nmod:

    > Dreyfus World-Wide Dollar had a seven-day compound yield of 9.37 %, down from **9.45%** a week earlier.

- **i**: Extract an argument token from the governor of an adjectival modifier.
  > Sam eats red **meat**. ``amod(red, meat)``

- **j**: Extract an argument token from the governor of apposition.

  > **Sam**, my brother, arrived. ``appos(brother, Sam)``

- **w1**: Extract an argument token from the governor of possessive relation.

  > I like his **toy**. ``nmod:poss(toy, his)``

- **w2**: Extract an argument token from the dependent of possessive relation.

  > I like **his** toy. ``nmod:poss(toy, his)``

- **k**: Extract an argument token from the dependent of the dependent of clausal complement ``ccomp``.

  > He says that you **like** to swim.

  From the triple ``ccomp(like, says)``, we finally get predpatt like ``(He, says, **SOMETHING**)``.

### Rules for post added argument root token:
- **l**: Merge the argument token set of xcomp's dependent to the argument
  token set of the real predicate token.

  > Rudolph Agnew was named a non-executive director of this British industrial
  conglomerate. Here, for the triple ``xcomp(director, named)``,

  We merge the arguments of "director" -- "this British industrial conglomerate"
  -- to the arguments of "named". Finally, we get predpatt like (Rudolph Agnew,
  was named a non-executive director of, this British industrial conglomerate).

- **m**: Extract a conjunct token of other argument token.

  > We have apples, **pears**, **oranges**, and **bananas**.

### Rules for extracting predicate phrase:
- **n1**: Extract a token from the subtree of the predicate root token,
and add it to the predicate phrase.

    > Pierre Vinken **will** join the board as a director.

- **n2**: Drop a token, which is an argument root token, from the subtree
of the predicate root token.

    > Pierre **Vinken** will join the board as a director.
``nsubj(Vinken, join)``

- **n3**: Drop a token, which is another predicate root token, from the subtree
of the predicate root token.

    > Although preliminary findings were **reported** more than a year ago , the
    latest results appear in today 's New England Journal of Medicine , a forum
    likely to bring new attention to the problem .
    ``advcl(reported, appear)``

- **n4**: Drop a token, which is the dependent of the relations set ``{ccomp, csubj, advcl, acl, acl:relcl, nmod:tmod, parataxis, appos, dep}``, from the
subtree of the predicate root token.

- **n5**: Drop a token, which is a conjunct of the predicate root token or a
conjunct of a xcomp's dependent token, from the subtree of the predicate root
token.

    > He came home and **took** a shower. ``conj(took, came)``

- **n6**: Add a case phrase to the predicate phrase.

  > He should be punished **according to** the U.S. law.

### Rules for extracting argument phrase:
- **o1**: Extract a token from the subtree of the argument root token,
and add it to the argument phrase.

    > Pierre Vinken will join **the** board as a director.

- **o2**: Extract a case token from the subtree of the argument root token.

    > He should be punished **according** to the U.S. law. ``case(according, law)``

- **o3**: Drop a token, which is a predicate root token, from the subtree
of the argument root token.

    > Mr. Vinken is chairman of Elsevier N.V. , the Dutch publishing **group**.
``appos(group, N.V.)``

- **o4**: Drop a token, which is the dependent of the relations set ``{acl, acl:relcl, appos, ccomp, dep}``
, from the subtree of the argument root token.

- **o5**: Drop the argument's cc (coordinating conjunction) from the subtree of
the argument root token.

    > We have apples, pears, oranges, **and** bananas.

- **o6**: Drop the argument's conjuct from the subtree of the argument root
token.

    > We have apples, **pears**, **oranges**, and **bananas**.

- **o7**: Drop the argument's case phrase.

    > Mr. Vinken is chairman **of** Elsevier N.V. , the Dutch publishing group.
    In ``(Elsevier N.V., is/are, the Dutch publishing group)``, ``case(of, N.V.)``

### Rules for simple predicate:
- **p1**: Remove a non-core argument, a nominal modifier, from the predpatt.

  > the office **of the Chair**.

- **p2**: Remove an argument of other type from the predpatt.

- **q**: Remove an adverbial modifier in the predicate phrase.

  > John works **closely** with Mary.

- **r**: Remove auxiliary in the predicate phrase.

  > Bird **can** fly.

### Rules for manually added tokens (English specific)
- **s**: Manually add "be" in the predicate phrase extracted in apposition.

  > "Sam, my **brother**, arrived. ``(Sam, is/are my brother)``.

- **t**: Manually add "be" in the predicate phrase extracted in adjectival modifier.

  > Sam eats **red** meat. ``(meat, is/are red)``.

### Rules for removing redundancy.

- **u**: Strip the punct in the phrase.


## TODO: ``aux,neg`` distributing rules in conjunction.
-->
