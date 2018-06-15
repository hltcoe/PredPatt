#!/usr/bin/env python
"""
Predicate and argument filter functions.
"""

# good_morphology
#
# - returns True iff the predicate does not have the Mood=Imp feature in its
#   feats field. Intuitively, this is a better filter for imperatives than
#   hasSubj, since some imperatives + vocatives are annotated as having subjects
#   (incorrectly, in my opinion) e.g. Dan, please *open* the door. (Dan is
#   annotated as nsubj of open)

# Which filters can we omit from PredPatt (making the end-user
# responsible for them)?
#
# - definitely good_morphology, since PredPatt only looks at the dependency
#   parse and not any morphological features :(
#
# - definitely isNotInterrogative; this filter is gross and hacky, and also easy
#   to apply post-hoc
#
# - maybe isNotCopula/isNotHave/is_expletive/isNotPronoun (i.e. the lexicalized
#   filters)? I'm not sure about this, but they're relatively easy to apply
#   post-hoc, and they're the least universal. These could live in a flag,
#   though.

def isNotInterrogative(pred):
    # tokens = [tk.text for tk in pred.tokens]
    tokens = pred.tokens
    if '?' not in tokens:
        filter_rules = getattr(pred, 'rules', [])
        filter_rules.append(isNotInterrogative.__name__)
        return True
    return False


def isPredVerb(pred):
    if not pred.root.tag.startswith('V'):
        return False
    filter_rules = getattr(pred, 'rules', [])
    filter_rules.append(isPredVerb.__name__)
    return True


def isNotCopula(pred):
    """
        Checks if any of the dependents of pred are copula verbs.
        UD annotates copula verbs only when the nonverbal predicate
        is the head of the clause.

        Input: Predicate object
        Output: bool
    """
    copula_verbs = ['be', 'am', 'is', 'are', 'was', 'were', 'being', 'been']

    pred_deps_rel = [p.rel for p in pred.root.dependents]
    pred_deps_txt = [p.dep.text for p in pred.root.dependents]
    if u'cop' in pred_deps_rel:
        return False
    # just in case for parsing error (from Stanford Parser)
    if set(pred_deps_txt).intersection(set(copula_verbs)):
        return False
    else:
        filter_rules = getattr(pred, 'rules', [])
        filter_rules.append(isNotCopula.__name__)
        return True


def isGoodAncestor(pred):
    """
    Returns true if verb is not dominated by a relation
    that might alter its veridicality. This filter is very
    conservative; many veridical verbs will be excluded.
    """
    # Move to ud_filters
    # Technically, conj shouldn't be a problem, but
    # some bad annotations mean we need to exclude it.
    #   ex. "It is a small one and easily missed" ("missed" has
    #   "one" as a head with relation "conj")
    embedding_deps = {"acl", "mwe", "ccomp", "xcomp", "advcl",
                      "acl:relcl", "case", "conj", "parataxis", "csubj",
                      "compound", "nmod"}
    pointer = pred.root # index of predicate
    while pointer.gov_rel != u'root':
        if pointer.gov_rel in embedding_deps:
            return False
        # Replace pointer with its head
        pointer = pointer.gov
    filter_rules = getattr(pred, 'rules', [])
    filter_rules.append(isGoodAncestor.__name__)
    return True


def isGoodDescendants(pred):
    """
    Returns true if verb immediately dominates a relation that might alter
    its veridicality. This filter is very
    conservative; many veridical verbs will be excluded.
    """
    embedding_deps = {"neg", "advmod", "aux", "mark", "advcl", "appos"}
    for desc in pred.root.dependents:
        # The following is true if child is in fact a child
        # of verb
        if desc.rel in embedding_deps:
            return False
    filter_rules = getattr(pred, 'rules', [])
    filter_rules.append(isGoodDescendants.__name__)
    return True


def hasSubj(pred, passive = False):
    subj_rels = ('nsubj','nsubjpass') if passive else ('nsubj',)
    # the original filter function considers nsubjpass
    #if (('nsubj' in [x.rel for x in parse.dependents[event.root]])
    #    or ('nsubjpass' in [x.rel for x in parse.dependents[event.root]])):
    for x in pred.root.dependents:
        if x.rel in subj_rels:
            filter_rules = getattr(pred, 'rules', [])
            filter_rules.append(hasSubj.__name__)
            return True
    return False


def isNotHave(pred):
    have_verbs = {'have', 'had', 'has'}
    if pred.root.text in have_verbs:
        return False
    else:
        filter_rules = getattr(pred, 'rules', [])
        filter_rules.append(isNotHave.__name__)
        return True


def isSbjOrObj(arg):
    if arg.root.gov_rel in ('nsubj', 'dobj', 'iobj'):
        filter_rules = getattr(arg, 'rules', [])
        filter_rules.append(isSbjOrObj.__name__)
        return True
    return False


def isNotPronoun(arg):
    if arg.root.tag == 'PRP':
        return False
    if arg.root.text.lower() in ['that', 'this', 'which', 'what']:
        return False
    else:
        filter_rules = getattr(arg, 'rules', [])
        filter_rules.append(isNotPronoun.__name__)
        return True


def has_direct_arc(pred, arg):
    "Check if the argument and predicate has a direct arc."
    if arg.root.gov == pred.root:
        filter_rules = getattr(arg, 'rules', [])
        filter_rules.append(has_direct_arc.__name__)
        return True
    return False


def filter_events_NUCL(event, parse):
    "Filters for running Keisuke's NUCLE HIT."
    if isNotInterrogative(parse):
        return all(f(event) for f in (isPredVerb,
                                      isNotCopula,
                                      isNotHave,
                                      hasSubj,
                                      isGoodAncestor,
                                      isGoodDescendants))
    #isSbjOrObj (without nsubjpass)
    #isNotPronoun
    #has_direct_arc


def filter_events_SPRL(event, parse):
    "Filters for running UD SPRL HIT"
    if isNotInterrogative(parse):
        return all(f(event) for f in (isPredVerb,
                                      isGoodAncestor,
                                      isGoodDescendants,
                                      lambda p: hasSubj(p, passive=True), #(including nsubjpass)
                                      #good_morphology, (documented below; depends on full UD/CoNLLU schema)
                                      # isSbjOrObj, #(including nsubjpass)
                                      #is_expletive,
                                  ))


def activate(pred):
    pred.rules = []
    isNotInterrogative(pred)
    isPredVerb(pred)
    isNotCopula(pred)
    isGoodAncestor(pred)
    isGoodDescendants(pred)
    hasSubj(pred, passive = True)
    isNotHave(pred)
    for arg in pred.arguments:
        arg.rules = []
        isSbjOrObj(arg)
        isNotPronoun(arg)
        has_direct_arc(pred, arg)


def apply_filters(_filter, pred, **options):
    if _filter in {isSbjOrObj, isNotPronoun}:
        for arg in pred.arguments:
            if _filter(arg):
                return True
        return False
    elif _filter ==  has_direct_arc:
        for arg in pred.arguments:
            if _filter(pred, arg):
                return True
        return False
    elif _filter == hasSubj:
        passive = options.get('passive', None)
        if passive:
            return _filter(pred, passive)
        else:
            return _filter(pred)
    else:
        return _filter(pred)
