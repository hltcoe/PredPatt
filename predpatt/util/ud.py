#!/usr/bin/env python
# encoding: utf-8


class postag(object):
    # ref: http://universaldependencies.org/u/pos/index.html

    # Open class words
    ADJ = "ADJ"
    ADV = "ADV"
    INTJ = "INTJ"
    NOUN = "NOUN"
    PROPN = "PROPN"
    VERB = "VERB"

    # Closed class words
    ADP = "ADP"
    AUX ="AUX"
    CCONJ = "CCONJ"
    DET = "DET"
    NUM = "NUM"
    PART = "PART"
    PRON = "PRON"
    SCONJ = "SCONJ"

    # Other
    PUNCT = "PUNCT"
    SYM = "SYM"
    X = "X"


class dep_v1(object):
    # VERSION
    VERSION = "1.0"

    # subj relations
    nsubj = "nsubj"
    nsubjpass = "nsubjpass"
    csubj = "csubj"
    csubjpass = "csubjpass"

    # obj relations
    dobj = "dobj"
    iobj = "iobj"

    # copular
    cop = "cop"

    # auxiliary
    aux = "aux"
    auxpass = "auxpass"

    # negation
    neg = "neg"

    # non-nominal modifier
    amod = "amod"
    advmod = "advmod"

    # nominal modifers
    nmod = "nmod"
    nmod_poss = "nmod:poss"
    nmod_tmod = "nmod:tmod"
    nmod_npmod = "nmod:npmod"
    obl = "nmod"
    obl_npmod = "nmod:npmod"

    # appositional modifier
    appos = "appos"

    # cooordination
    cc = "cc"
    conj = "conj"
    cc_preconj = "cc:preconj"

    # marker
    mark = "mark"
    case = "case"

    # fixed multiword expression
    mwe = "fixed"

    # parataxis
    parataxis = "parataxis"

    # punctuation
    punct = "punct"

    # clausal complement
    ccomp = "ccomp"
    xcomp = "xcomp"

    # relative clause
    advcl = "advcl"
    acl = "acl"
    aclrelcl = "acl:relcl"

    # unknown dep
    dep = "dep"

    SUBJ = {nsubj, csubj, nsubjpass, csubjpass}

    OBJ = {dobj, iobj}

    NMODS = {nmod, obl, nmod_npmod, nmod_tmod}

    ADJ_LIKE_MODS = {amod, appos, acl, aclrelcl}

    ARG_LIKE = {nmod, obl, nmod_npmod, nmod_tmod, nsubj, csubj, csubjpass,
                dobj, iobj}

    # trivial symbols to be stripped out
    TRIVIALS = {mark, cc, punct}

    # These dependents of a predicate root shouldn't be included in the
    # predicate phrase.
    PRED_DEPS_TO_DROP = {ccomp, csubj, advcl, acl, aclrelcl, nmod_tmod,
                         parataxis, appos, dep}

    # These dependents of an argument root shouldn't be included in the
    # argument pharse if the argument root is the gov of the predicate root.
    SPECIAL_ARG_DEPS_TO_DROP = {nsubj, dobj, iobj, csubj, csubjpass, neg,
                                aux, advcl, auxpass, ccomp, cop, mark, mwe,
                                parataxis}

    # Predicates of these rels are hard to find arguments.
    HARD_TO_FIND_ARGS = {amod, dep, conj, acl, aclrelcl, advcl}


class dep_v2(object):
    # VERSION
    VERSION = "2.0"

    # subj relations
    nsubj = "nsubj"
    nsubjpass = "nsubj:pass"
    csubj = "csubj"
    csubjpass = "csubj:pass"

    # obj relations
    dobj = "obj"
    iobj = "iobj"

    # auxiliary
    aux = "aux"
    auxpass = "aux:pass"

    # negation
    neg = "neg"

    # copular
    cop = "cop"

    # non-nominal modifier
    amod = "amod"
    advmod = "advmod"

    # nominal modifers
    nmod = "nmod"
    nmod_poss = "nmod:poss"
    nmod_tmod = "nmod:tmod"
    nmod_npmod = "nmod:npmod"
    obl = "obl"
    obl_npmod = "obl:npmod"

    # appositional modifier
    appos = "appos"

    # cooordination
    cc = "cc"
    conj = "conj"
    cc_preconj = "cc:preconj"

    # marker
    mark = "mark"
    case = "case"

    # fixed multiword expression
    mwe = "fixed"

    # parataxis
    parataxis = "parataxis"

    # punctuation
    punct = "punct"

    # clausal complement
    ccomp = "ccomp"
    xcomp = "xcomp"

    # relative clause
    advcl = "advcl"
    acl = "acl"
    aclrelcl = "acl:relcl"

    # unknown dep
    dep = "dep"

    SUBJ = {nsubj, csubj, nsubjpass, csubjpass}

    OBJ = {dobj, iobj}

    NMODS = {nmod, obl, nmod_npmod, nmod_tmod}

    ADJ_LIKE_MODS = {amod, appos, acl, aclrelcl}

    ARG_LIKE = {nmod, obl, nmod_npmod, nmod_tmod, nsubj, csubj, csubjpass,
                dobj, iobj}

    # trivial symbols to be stripped out
    TRIVIALS = {mark, cc, punct}

    # These dependents of a predicate root shouldn't be included in the
    # predicate phrase.
    PRED_DEPS_TO_DROP = {ccomp, csubj, advcl, acl, aclrelcl, nmod_tmod,
                         parataxis, appos, dep}

    # These dependents of an argument root shouldn't be included in the
    # argument pharse if the argument root is the gov of the predicate root.
    SPECIAL_ARG_DEPS_TO_DROP = {nsubj, dobj, iobj, csubj, csubjpass, neg,
                                aux, advcl, auxpass, ccomp, cop, mark, mwe,
                                parataxis}

    # Predicates of these deps are hard to find arguments.
    HARD_TO_FIND_ARGS = {amod, dep, conj, acl, aclrelcl, advcl}
