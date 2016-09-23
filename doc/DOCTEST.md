# PredPatt
> PredPatt extracts knowledge from text .

    ?a extracts ?b from ?c
        ?a: PredPatt
        ?b: knowledge
        ?c: text

# Basics

## Transitive
> Chris loves Pat .

    ?a loves ?b
        ?a: Chris
        ?b: Pat

## Intransitive
> Chris slept .

    ?a slept
        ?a: Chris

## Ditransitive
> Chris gave Pat the book .

    ?a gave ?b ?c
        ?a: Chris
        ?b: Pat
        ?c: the book

> Chris gave the book to Pat .

    ?a gave ?b to ?c
        ?a: Chris
        ?b: the book
        ?c: Pat

## Negation

PredPatt handles negation by modifying the predicate's name.

> Chris does not love Pat .

    ?a does not love ?b
        ?a: Chris
        ?b: Pat

## Embedded sentences
> Chris failed to dance at the party .

    ?a failed to dance at ?b
        ?a: Chris
        ?b: the party

## Prepositions
> Sheng loves to work on PredPatt with Tim .

    ?a loves to work on ?b with ?c
        ?a: Sheng
        ?b: PredPatt
        ?c: Tim

## Passive
> A boat was built by a boy .

    ?a was built by ?b
        ?a: A boat
        ?b: a boy


## Adverbs
> Chris built a boat quickly .

    ?a built ?b quickly
        ?a: Chris
        ?b: a boat

> Chris quickly built a boat .

    ?a quickly built ?b
        ?a: Chris
        ?b: a boat


## Conjunctions

### Lists of stuff
> Chris bought an apple , three bananas , a grapefruit , and two onions .

    ?a bought ?b
        ?a: Chris
        ?b: an apple
    ?a bought ?b
        ?a: Chris
        ?b: three bananas
    ?a bought ?b
        ?a: Chris
        ?b: a grapefruit
    ?a bought ?b
        ?a: Chris
        ?b: two onions

Distribution over tree place predicate ``?a bought ?b on ?c``

> Chris and Pat bought apples , bananas , and onions on Monday and Tuesday .

    ?a bought ?b on ?c
        ?a: Chris
        ?b: apples
        ?c: Monday
    ?a bought ?b on ?c
        ?a: Pat
        ?b: apples
        ?c: Monday
    ?a bought ?b on ?c
        ?a: Chris
        ?b: bananas
        ?c: Monday
    ?a bought ?b on ?c
        ?a: Pat
        ?b: bananas
        ?c: Monday
    ?a bought ?b on ?c
        ?a: Chris
        ?b: onions
        ?c: Monday
    ?a bought ?b on ?c
        ?a: Pat
        ?b: onions
        ?c: Monday
    ?a bought ?b on ?c
        ?a: Chris
        ?b: apples
        ?c: Tuesday
    ?a bought ?b on ?c
        ?a: Pat
        ?b: apples
        ?c: Tuesday
    ?a bought ?b on ?c
        ?a: Chris
        ?b: bananas
        ?c: Tuesday
    ?a bought ?b on ?c
        ?a: Pat
        ?b: bananas
        ?c: Tuesday
    ?a bought ?b on ?c
        ?a: Chris
        ?b: onions
        ?c: Tuesday
    ?a bought ?b on ?c
        ?a: Pat
        ?b: onions
        ?c: Tuesday

### Non-distributive

Not all predicates distribute over their arguments. With the ``--resolve-conj``
option enabled PredPatt will naively expand all predicates over arguments
containing a conjunction.

> Chris and Pat are a team .

    ?a are a team
        ?a: Chris
    ?a are a team
        ?a: Pat

> The average American has 2.5 children .

    ?a is/are average
        ?a: The American
    ?a has ?b
        ?a: The average American
        ?b: 2.5 children

<!--
TODO: maybe plural VBZ/VBG is a good clue for when we can/can't distribute. This
is not available in universal tags.
-->

## Clausal subjects
> Texting while driving is illegal .

    ?a is illegal
        ?a: SOMETHING := Texting while driving

## Appositives and possessives

> Chris , Pat 's sibling , loves pineapple .

sibling is a predicate

    ?a poss ?b
        ?a: Pat
        ?b: sibling
    ?a is/are ?b 's sibling
        ?a: Chris
        ?b: Pat
    ?a loves ?b
        ?a: Chris
        ?b: pineapple

<!--
TODO: Should this extract more similarly to copula ``Chris is Pat 's sibling ->
be(Chris, Pat's sibling)``?
-->

> Chris , the sibling of Pat , loves pineapple .

    ?a is/are the sibling of ?b
        ?a: Chris
        ?b: Pat
    ?a loves ?b
        ?a: Chris
        ?b: pineapple

> Pat 's sibling , Chris , loves pineapple .

    ?a poss ?b
        ?a: Pat
        ?b: sibling
    ?a is/are Chris
        ?a: Pat 's sibling
    ?a loves ?b
        ?a: Pat 's sibling
        ?b: pineapple

# Predicate coordination

## intransive + transitive predicates
> Chris stood up and sang the National Anthem .

    ?a stood up
        ?a: Chris
    ?a sang ?b
        ?a: Chris
        ?b: the National Anthem

> Chris stood up and jumped up and sang the National Anthem .

    ?a stood up
        ?a: Chris
    ?a jumped up
        ?a: Chris
    ?a sang ?b
        ?a: Chris
        ?b: the National Anthem

> Chris may stand up , jump up , or sing the National Anthem .

    ?a may stand up
        ?a: Chris
    ?a may jump up
        ?a: Chris
    ?a may sing ?b
        ?a: Chris
        ?b: the National Anthem

> Chris did not stand up or jump up .

    ?a did not stand up
        ?a: Chris
    ?a did not jump up
        ?a: Chris

> Chris bought and sold stocks .

    ?a bought
        ?a: Chris
    ?a sold ?b
        ?a: Chris
        ?b: stocks

Ideally, we'd extract ``bought(Chris stocks)``. At this time, PredPatt only
associates subjects with coordinated predicates.

# Relative clauses

The examples pair below has the referent in different syntactic positions (subj
and obj, respectively).

PredPatt over-generates the set of arguments to predicates in embedded clauses
because it can't figure out how to resolve the arguments. In many cases,
language-specific rules can tweak the output, e.g., dropping arguments that are
only function words (that, which).

> The plant , that Chris owns , is on fire .

    ?a ?b owns
        ?a: The plant
        ?b: Chris
    ?a is on fire
        ?a: The plant

> The plant , which is owned by Chris , is on fire .

    ?a is owned by ?b
        ?a: The plant
        ?b: Chris
    ?a is on fire
        ?a: The plant

> A form of asbestos used to make Kent cigarette filters causes cancer .

    ?a used to make ?b
        ?a: A form of asbestos
        ?b: Kent cigarette filters
    ?a causes ?b
        ?a: A form of asbestos
        ?b: cancer

### relative clause with an embedded ditransitive
> The book , which Chris gave to Pat , is on fire .

    ?a ?b gave to ?c
        ?a: The book
        ?b: Chris
        ?c: Pat
    ?a is on fire
        ?a: The book

> Pat , who Chris gave the book to , is on fire .

    ?a ?b gave ?c to
        ?a: Pat
        ?b: Chris
        ?c: the book
    ?a is on fire
        ?a: Pat

## acl and advcl

> Chris thanked Pat for donating money .
<!--tags=
Chris/NOUN thanked/VERB Pat/NOUN for/ADP donating/VERB money/NOUN ./.
-->
<!--parse=
nsubj(Chris/0, thanked/1)
root(thanked/1, ROOT/-1)
dobj(Pat/2, thanked/1)
mark(for/3, donating/4)
advcl(donating/4, thanked/1)
dobj(money/5, donating/4)
acl(donating/4, Pat/2)
punct(./6, thanked/1)
-->

    ?a thanked ?b
        ?a: Chris
        ?b: Pat
    ?a donating ?b
        ?a: Pat
        ?b: money


## Pied-piping
> The house , in which Chris grew up , is on fire .

    ?a in ?b grew up
        ?a: The house
        ?b: Chris
    ?a is on fire
        ?a: The house

# Drew's examples
### Dependents of ccomp are predicates

> I know that you hate hamsters

hate is a predicate

    ?a know ?b
        ?a: I
        ?b: SOMETHING := you hate hamsters
    ?a hate ?b
        ?a: you
        ?b: hamsters

Treatment of ccomp and xcomp is consistent with some of the literature according
to Aaron.

### Dependents of xcomp are predicates.

> I want to eat a banana

eat is a predicate

    ?a want to eat ?b
        ?a: I
        ?b: a banana

> I want you to eat a banana .

    ?a want ?b to eat ?c
        ?a: I
        ?b: you
        ?c: a banana

... unless the governor of xcomp is itself the root of an adjunct clause dep or second conjunct (w/ the right flag)
> The man who wants to go to the mall ate a banana .

    ?a wants to go to ?b
        ?a: The man
        ?b: the mall
    ?a ate ?b
        ?a: The man
        ?b: a banana

> The man has his own car and wants to go to the mall .

    ?a has ?b
        ?a: The man
        ?b: his own car
    ?a poss ?b
        ?a: his
        ?b: own car
    ?a is/are own
        ?a: his car
    ?a wants to go to ?b
        ?a: The man
        ?b: the mall


### Roots of adjunct clauses are predicates
> The man who wants to go to the mall ate a banana .

    ?a wants to go to ?b
        ?a: The man
        ?b: the mall
    ?a ate ?b
        ?a: The man
        ?b: a banana

> The man who wants to eat a banana went to the mall  .

    ?a wants to eat ?b
        ?a: The man
        ?b: a banana
    ?a went to ?b
        ?a: The man
        ?b: the mall

> The man wants to go to the mall and has his own car .

    ?a wants to go to ?b
        ?a: The man
        ?b: the mall
    ?a has ?b
        ?a: The man
        ?b: his own car
    ?a poss ?b
        ?a: his
        ?b: own car
    ?a is/are own
        ?a: his car

<!--
TODO: confusing ``[his car] is/are own``
TODO: look into "own" in udbank to see if we have the right parse.
TODO: filter out amod cases like the one above (look for things like nmod)
-->

... or it violates the adv clause/conj constraints directly (w/ the right flag)
> The apple that the man ate was rotten

    ?a ?b ate
        ?a: The apple
        ?b: the man
    ?a was rotten
        ?a: The apple

> The apple is red .

    ?a is red
        ?a: The apple

> Chris ate the red apple .

    ?a ate ?b
        ?a: Chris
        ?b: the red apple
    ?a is/are red
        ?a: the apple

<!--
 #> An apple , a red one , fell from the tree .
 #
 #    ?a is/are red
 #        ?a: a one            <<< weird
 #    ?a is/are a red one
 #        ?a: An apple
 #    ?a fell from ?b
 #        ?a: An apple
 #        ?b: the tree
-->

> Chris , a tall man , easily grabbed the book .

    ?a is/are tall
        ?a: a man
    ?a is/are a tall man
        ?a: Chris
    ?a easily grabbed ?b
        ?a: Chris
        ?b: the book

Attributive adjectives are predicates...

> The green apple is rotten .

green is a predicate

    ?a is/are green
        ?a: The apple
    ?a is rotten
        ?a: The green apple

... unless they modify another adjective (regardless of flag)
e.g. (from English UD bank)


northeastern is not a predicate (for now)

> Under the accord, a new northeastern provinical council was formed .

    ?a is/are new
        ?a: a northeastern provinical council
    ?a is/are northeastern
        ?a: a new provinical council
    ?a is/are provinical
        ?a: a new northeastern council
    Under ?a , ?b was formed
        ?a: the accord
        ?b: a new northeastern provinical council

Optionally, conjuncts with other predicates are predicates

> Chris bought and sold .

    ?a bought
        ?a: Chris
    ?a sold
        ?a: Chris

# Conjunction in xcomp
> The company said it expects to obtain regulatory approval and complete the transaction by year-end .

    ?a said ?b
        ?a: The company
        ?b: SOMETHING := it expects to obtain regulatory approval and complete the transaction by year-end
    ?a expects to obtain ?b
        ?a: it
        ?b: regulatory approval
    ?a is/are regulatory
        ?a: approval
    ?a expects to complete ?b by ?c
        ?a: it
        ?b: the transaction
        ?c: year-end

> The company sincerely expects to lie quickly , steal quietly and cheat magically .

    ?a sincerely expects to lie quickly
        ?a: The company
    ?a sincerely expects to steal quietly
        ?a: The company
    ?a sincerely expects to cheat magically
        ?a: The company

> I like his toy .

    ?a like ?b
        ?a: I
        ?b: his toy
    ?a poss ?b
        ?a: his
        ?b: toy

> I like Quinn's toy.

    ?a like ?b
        ?a: I
        ?b: Quinn 's toy
    ?a poss ?b
        ?a: Quinn
        ?b: toy

> It is a toy of Quinn's.

    ?a is a toy of ?b 's
        ?a: It
        ?b: Quinn

> It is one of Quinn's favorite toys.

    ?a is one of ?b
        ?a: It
        ?b: Quinn 's favorite toys
    ?a poss ?b
        ?a: Quinn
        ?b: favorite toys
    ?a is/are favorite
        ?a: Quinn 's toys

> Ten students passed the exam and six failed.

    ?a passed ?b
        ?a: Ten students
        ?b: the exam
    ?a failed
        ?a: six

Failed predicate conjunction. The dobj of failed is a trace back to the
exam. Ideally, we'd extract ``[six students] failed [the exam]``, but we don't
know that failed is transitive without language specific rules.

<!--
# Center embedding

Unfortunately, the parses for the following center embedding examples are
unusable.

 #> A man that a woman loves .
 #> A man that a woman that a child knows loves .
 #> A man that a woman that a child that a bird saw knows loves .
 #> A man that a woman that a child that a bird that I heard saw knows loves .
-->

# Rachel's examples

> Chris told Pat that a boy built a boat .

    ?a told ?b ?c
        ?a: Chris
        ?b: Pat
        ?c: SOMETHING := a boy built a boat
    ?a built ?b
        ?a: a boy
        ?b: a boat

> Chris told Pat that Quinn told Logan that Francis loves Jordan .

    ?a told ?b ?c
        ?a: Chris
        ?b: Pat
        ?c: SOMETHING := Quinn told Logan that Francis loves Jordan
    ?a told ?b ?c
        ?a: Quinn
        ?b: Logan
        ?c: SOMETHING := Francis loves Jordan
    ?a loves ?b
        ?a: Francis
        ?b: Jordan

> Chris was told by Pat that Quinn wants Logan to build a boat quickly .

    ?a was told by ?b ?c
        ?a: Chris
        ?b: Pat
        ?c: SOMETHING := Quinn wants Logan to build a boat quickly
    ?a wants ?b to build ?c quickly
        ?a: Quinn
        ?b: Logan
        ?c: a boat

<!--
 # mirror has the same role, but different syntax
 #> Chris broke the mirror .
 #> The mirror broke .
-->

## Ethical questions

### Will Pat eat their friend?
> Chris ate pasta with olives .

    ?a ate ?b
        ?a: Chris
        ?b: pasta with olives

> Chris ate pasta with a friend .

    ?a ate ?b with ?c
        ?a: Chris
        ?b: pasta
        ?c: a friend

### Does PredPatt eat grandma?
> Let 's eat grandma !

    ?a eat ?b
        ?a: 's
        ?b: grandma

> Let 's eat , grandma !

    ?a eat
        ?a: 's

## Predicate names can get big
> John would have been unable to come up for air .

    ?a would have been unable to come up for ?b
        ?a: John
        ?b: air

## Adverbial clause

We drop adveribal clauses (``advcl``) in predicate names.

> Chris would love Pat if she loved dogs .

    ?a would love ?b
        ?a: Chris
        ?b: Pat
    ?a loved ?b
        ?a: she
        ?b: dogs

It would be nice to extract a pattern ``?a would love ?b if ?c`` where ``?c:
SOMETHING := she loved dogs``


# Borrow subject for adverbial clauses
> Born in a small town , she took the midnight train going anywhere .

    Born in ?a ?b
        ?a: a small town
        ?b: she
    ?a is/are small
        ?a: a town
    ?a took ?b
        ?a: she
        ?b: the midnight train
    ?a going anywhere
        ?a: the midnight train

<!--
TODO: should probably be ``Born in ?a , ?b``
-->

# Ellipsis and the remnant tag

It's probably not worth the effort to handle the remnant tag because UD parsers
don't seem to handle them yet.

> Marie went to Paris and Miriam went to Prague .

    ?a went to ?b
        ?a: Marie
        ?b: Paris
    ?a went to ?b
        ?a: Miriam
        ?b: Prague

# Misc

> The company , which is owned by Chris , was under contract with Pat to make toys .

    ?a is owned by ?b
        ?a: The company
        ?b: Chris
    ?a was under contract with ?b to make ?c
        ?a: The company
        ?b: Pat
        ?c: toys


Declarative context sentences

> We expressed our hope that someday the world will know peace .

    ?a expressed ?b
        ?a: We
        ?b: our hope
    ?a poss ?b
        ?a: our
        ?b: hope
    someday ?a will know ?b
        ?a: the world
        ?b: peace

PredPatt doesn't handle language-specific rules such as the infamous ``W, such
as, X, Y & Z``.

> PredPatt extracts patterns , such as , relatives , appositives , and ditransitives .

    ?a extracts ?b , such as ?c
        ?a: PredPatt
        ?b: patterns
        ?c: relatives
    ?a extracts ?b , such as ?c
        ?a: PredPatt
        ?b: patterns
        ?c: appositives
    ?a extracts ?b , such as ?c
        ?a: PredPatt
        ?b: patterns
        ?c: ditransitives

<!--
%The following examples don't work yet.
%
%  The question is then how to treat the following example which is "missing" the
%  coordinated predicate.
%
%  > Marie went to Paris and Miriam to Prague .
%
%      ?a went to ?b
%          ?a: Marie
%          ?b: Paris
%      ?a went to ?b
%          ?a: Miriam
%          ?b: Prague
%
%  Check on conjunction expansion with special predicate types, e.g., appos.
%
%  > He fathered two children , John and Mary , and lived in Aberdeen until his death from tuberculosis in 1942 .
%
%      ?a fathered ?b
%          ?a: He
%          ?b: two children
%      ?a is/are John and Mary
%          ?a: two children
%      ?a lived in ?b until ?c from ?d in ?e
%          ?a: He
%          ?b: Aberdeen
%          ?c: his death
%          ?d: tuberculosis
%          ?e: 1942
%      ?a poss ?b
%          ?a: his
%          ?b: death
%
%
%  TODO: should we expand the modifiers of products?
%  TODO: How should we deal with dobj and iobj of conj predicates?
%
%  > Bell makes and distributes electronic , computer , and building products .
%
%      ?a makes ?b
%          ?a: Bell
%          ?b: electronic , computer , and building products
%      ?a distributes
%          ?a: Bell
%          ?b: electronic , computer , and building products
%      ?a is/are electronic
%          ?a: products
%      ?a is/are computer
%          ?a: products
%      ?a is/are building
%          ?a: products
-->


<!--
TODO: Could explode predicates by swapping ``appos``. Since "Chris" and "Pat 's
sibling" are likely coreferent, we can conclude ``loves(Chris,
pineapple)``. This reasoning should probably be done with a coref module
(explicitly blowing it up may be unnecessary).
-->
