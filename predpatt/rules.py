class Rule(object):
    def __init__(self):
        pass
    def __repr__(self):
        return self.name()
    @classmethod
    def name(cls):
        return cls.__name__.split('.')[-1]
    @classmethod
    def explain(cls):
        return cls.__doc__
    def __cmp__(self, other):
        return cmp(unicode(self), unicode(other))

class PredicateRootRule(Rule):
    rule_type = 'predicate_root'

class ArgumentRootRule(Rule):
    rule_type = 'argument_root'

class PredConjRule(Rule):
    type = 'predicate_conj'

class ArgumentResolution(Rule):
    type = 'argument_resolution'

class ConjunctionResolution(Rule):
    type = 'conjunction_resolution'

class SimplifyRule(Rule):
    type = 'simple'

#______________________________________________
# Predicate root identification

class a1(PredicateRootRule):
    "Extract a predicate token from the dependent of clausal relation {ccomp, csub, csubjpass}."
    rule_type = 'predicate_root'

class a2(PredicateRootRule):
    "Extract a predicate token from the dependent of clausal complement 'xcomp'."
    rule_type = 'predicate_root'

class b(PredicateRootRule):
    "Extract a predicate token from the dependent of clausal modifier."
    rule_type = 'predicate_root'

class c(PredicateRootRule):
    "Extract a predicate token from the governor of the relations {nsubj, nsubjpass, dobj, iobj, ccomp, xcomp, advcl}."
    rule_type = 'predicate_root'

class d(PredicateRootRule):
    "Extract a predicate token from the dependent of apposition."
    rule_type = 'predicate_root'

class e(PredicateRootRule):
    "Extract a predicate token from the dependent of an adjectival modifier."
    rule_type = 'predicate_root'

class v(PredicateRootRule):
    "Extract a predicate token from the dependent of the possessive relation 'nmod:poss' (English specific)."
    rule_type = 'predicate_root'

class f(PredicateRootRule):
    "Extract a conjunct token of a predicate token."
    rule_type = 'predicate_root'

#_________________________________________
# Argument root identification

class g1(ArgumentRootRule):
    "Extract an argument token from the dependent of the following relations {nsubj, nsubjpass, dobj, iobj}."
    def __init__(self, edge):
        self.edge = edge
        super(g1, self).__init__()
    def __repr__(self):
        return 'g1(%s)' % (self.edge.rel)

class h1(ArgumentRootRule):
    "Extract an argument token, which directly depends on the predicate token, from the dependent of the relations {nmod, nmod:npmod, nmod:tmod}."

class h2(ArgumentRootRule):
    "Extract an argument token, which indirectly depends on the predicate token, from the dependent of the relations {nmod, nmod:npmod, nmod:tmod}."

class i(ArgumentRootRule):
    "Extract an argument token from the governor of an adjectival modifier."

class j(ArgumentRootRule):
    "Extract an argument token from the governor of apposition."

class w1(ArgumentRootRule):
    "Extract an argument token from the governor of 'nmod:poss' (English specific)."

class w2(ArgumentRootRule):
    "Extract an argument token from the dependent of 'nmod:poss' (English specific)."

class k(ArgumentRootRule):
    "Extract an argument token from the dependent of the dependent of clausal complement 'ccomp'."


#__________________________________
# Predicate conjunction resolution

class pred_conj_borrow_aux_neg(PredConjRule):
    "Borrow aux and neg tokens from conjoined predicate's name."
    def __init__(self, friend, borrowed_token):
        self.friend = friend
        self.borrowed_token = borrowed_token
        super(pred_conj_borrow_aux_neg, self).__init__()

class pred_conj_borrow_tokens_xcomp(PredConjRule):
    "Borrow tokens from xcomp in a conjunction or predicates."
    def __init__(self, friend, borrowed_token):
        self.friend = friend
        self.borrowed_token = borrowed_token
        super(pred_conj_borrow_tokens_xcomp, self).__init__()

class cut_borrow_other(ArgumentResolution):
    def __init__(self, friend, borrowed):
        self.friend = friend
        self.borrowed = borrowed
        super(cut_borrow_other, self).__init__()

class cut_borrow_subj(ArgumentResolution):
    def __init__(self, friend, borrowed):
        self.friend = friend
        self.borrowed = borrowed
        super(cut_borrow_subj, self).__init__()

class cut_borrow_obj(ArgumentResolution):
    def __init__(self, friend, borrowed):
        self.friend = friend
        self.borrowed = borrowed
        super(cut_borrow_obj, self).__init__()


class borrow_subj(ArgumentResolution):
    "Borrow subject from governor in (conj, xcomp of conj root, and advcl)."

    # if gov_rel=='conj' and missing a subject, try to borrow the subject from
    # the other event. Still no subject. Try looking at xcomp of conjunction
    # root.
    #
    # if gov_rel==advcl and not event.has_subj() then borrow from governor.

    def __init__(self, friend, event, i):
        super(borrow_subj, self).__init__()
        self.event = event
        self.friend = friend
        self.i = i
    def __repr__(self):
        return 'borrow-subj(%s,%s,%s)' % (self.event.root, self.friend.root, self.event.root.gov_rel)
#        return 'borrow_subj(%s,%s,%s,%s)' % (self.i, self.event.root, self.friend.root, self.event.root.gov_rel)
#        return 'borrow_subj(%s,%s)' % (self.friend, self.friend.subj())

#___________________________
# Relative clause

class arg_resolve_relcl(ArgumentResolution):
    """Resolve argument of a predicate inside a relative clause. The missing
    argument that we take is rooted at the governor of the `acl` dependency
    relation (type acl:*) pointing at the embedded predicate.

    """

class pred_resolve_relcl(ArgumentResolution):
    "Predicate has an argument from relcl resolution (`arg_resolve_relcl`)."


#__________________________________________
# Rules for post added argument root token.

class l(ArgumentResolution):
    "Merge the argument token set of xcomp's dependent to the argument token set of the real predicate token."

class m(ConjunctionResolution):
    "Extract a conjunct token of the argument root token."

#_________________________________________
# Predicate phrase

class PredPhraseRule(Rule):
    type = 'pred_phrase'
    def __init__(self, x):
        self.x = x
        super(PredPhraseRule, self).__init__()
#    def __repr__(self):
#        return '%s(%s)' % (super(PredPhraseRule, self).__repr__(), self.x)

class n1(PredPhraseRule):
    "Extract a token from the subtree of the predicate root token, and add it to the predicate phrase."
class n6(PredPhraseRule):
    "Add a case phrase to the predicate phrase."

class n2(PredPhraseRule):
    "Drop a token, which is an argument root token, from the subtree of the predicate root token."
class n3(PredPhraseRule):
    "Drop a token, which is another predicate root token, from the subtree of the predicate root token."
class n4(PredPhraseRule):
    "Drop a token, which is the dependent of the relations set {ccomp, csubj, advcl, acl, acl:relcl, nmod:tmod, parataxis, appos, dep}, from the subtree of the predicate root token."
class n5(PredPhraseRule):
    "Drop a token, which is a conjunct of the predicate root token or a conjunct of a xcomp's dependent token, from the subtree of the predicate root token."

#______________________________________
# Rules for extracting argument phrase.

class ArgPhraseRule(Rule):
    type = 'arg_phrase'

class o1(ArgPhraseRule):
    "Extract a token from the subtree of the argument root token, and add it to the argument phrase."
class o2(ArgPhraseRule):
    "Extract a case token from the subtree of the argument root token."
class o3(ArgPhraseRule):
    "Drop a token, which is a predicate root token, from the subtree of the argument root token."
class o4(ArgPhraseRule):
    "Drop a token, which is the dependent of the relations set {acl, acl:relcl, appos, ccomp, dep} , from the subtree of the argument root token."
class o5(ArgPhraseRule):
    "Drop the argument's cc (coordinating conjunction) from the subtree of the argument root token."
class o6(ArgPhraseRule):
    "Drop the argument's conjuct from the subtree of the argument root token."
class o7(ArgPhraseRule):
    "Drop the argument's case phrase."


#________________________________
# Rules for simple predicate.

class p1(SimplifyRule):
    "Remove a non-core argument, a nominal modifier, from the predpatt."
class p2(SimplifyRule):
    "Remove an argument of other type from the predpatt."
class q(SimplifyRule):
    "Remove an adverbial modifier in the predicate phrase."
class r(SimplifyRule):
    "Remove auxiliary in the predicate phrase."

#____________________________________________________
# Rules for manually added tokens (English specific)

class u(Rule):
    "Strip the punct in the phrase."

#____________________________________________________
# English-specific rules

class LanguageSpecific(Rule):
    lang = None

class EnglishSpecific(Rule):
    lang = 'English'

class en_relcl_dummy_arg_filter(EnglishSpecific):
    def __init__(self):
        super(en_relcl_dummy_arg_filter, self).__init__()


if __name__ == '__main__':
    print a1(), a1().explain()
