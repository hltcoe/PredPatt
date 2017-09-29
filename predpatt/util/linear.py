#!/usr/bin/env python
# encoding: utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import re


from predpatt.patt import Predicate, Argument, Token

# Regrex
RE_ARG_ENC = re.compile("\^\(\( | \)\)\$")
RE_ARG_LEFT_ENC = re.compile("\^\(\(")
RE_ARG_RIGHT_ENC = re.compile("\)\)\$")
RE_PRED_LEFT_ENC = re.compile("\^\(\(\(|\^\(\(\(:a")
RE_PRED_RIGHT_ENC = re.compile("\)\)\)\$|\)\)\)\$:a")
# ENCLOSER
ARG_ENC = ("^((", "))$")
PRED_ENC = ("^(((", ")))$")
ARGPRED_ENC = ("^(((:a", ")))$:a")
# SUFFIX
ARG_SUF = ":a"
PRED_SUF = ":p"
HEADER_SUF = "_h"
ARG_HEADER = ARG_SUF + HEADER_SUF
PRED_HEADER = PRED_SUF + HEADER_SUF
# SOMETHING
SOMETHING = "SOMETHING:a="


class LinearizedPPOpts:

    def __init__(self, recursive=True,
                 distinguish_header=True,
                 only_head=False,
                 ignore_content=False):
        self.recursive = recursive
        self.distinguish_header = distinguish_header
        self.only_head = only_head
        self.ignore_content = ignore_content


def sort_by_position(x):
    return list(sorted(x, key=lambda y: y.position))

def is_dep_of_pred(t):
    if t.gov_rel in {"nsubj", "nsubjpass", "dobj", "iobj",
                     "csubj", "csubjpass", "ccomp", "xcomp",
                     "nmod", "advcl", "advmod", "neg"}:
        return True

def important_pred_tokens(p):
    ret = [p.root]
    for x in p.tokens:
        # direct denpendents of the predicate
        if x.gov and x.gov.position == p.root.position:
            if x.gov_rel in {'neg'}:
                ret.append(x)
    return sort_by_position(ret)

def likely_to_be_pred(pred):
    if len(pred.arguments) == 0:
        return False
    if pred.root.tag in ('VERB', 'ADJ'):
        return True
    if pred.root.gov_rel in ('appos',):
        return True
    for t in pred.tokens:
        if t.gov_rel == 'cop':
            return True


def build_pred_dep(pp):
    """ Build dependencies between predicates. """
    root_to_preds = {p.root.position:p for p in pp.instances}
    id_to_root_preds = {}
    for p in pp.instances:
        # only keep predicates with high confidence
        if not likely_to_be_pred(p):
            continue
        gov = p.root.gov
        # record the current predicate as a root predicate
        if gov is None:
            id_to_root_preds[p.identifier()] = p
        # climb up until finding a gov predicate
        while gov is not None and gov.position not in root_to_preds:
            gov = gov.gov
        gov_p = root_to_preds[gov.position] if gov else None
        # Add the current predicate as a root predicate
        # if not find any gov predicate or
        # the gov predicate is not likely_to_be_pred.
        if gov is None or not likely_to_be_pred(gov_p):
            id_to_root_preds[p.identifier()] = p
            continue
        # build a dependency between the current pred and the gov pred.
        gov_p.children.append(p)
    return sort_by_position(id_to_root_preds.values())


def get_prediates(pp, only_head=False):
    idx_list = []
    preds = []
    for pred in pp.instances:
        if pred.root.position not in idx_list:
            idx_list.append(pred.root.position)
            preds.append(pred)
    if only_head:
        return [pred.root.text for pred in sort_by_position(preds)]
    else:
        enc = PRED_ENC
        ret = []
        for pred in preds:
            pred_str = pred.phrase()    # " ".join(token.text for token in pred.tokens)
            ret.append("%s %s %s" % (enc[0], pred_str, enc[1]))
        return ret


def linearize(pp, opt=LinearizedPPOpts()):
    """
    Here we define the way to represent the predpatt ouptut in a linearized
    form:
        1. Add a label to each token to indicate that it is a predicate
           or argument token:
                (1) argument_token:a
                (2) predicate_token:p
        2. Build the dependency tree among the heads of predicates.
        3. Print the predpatt output in a depth-first manner. At each layer,
           items are sorted by position. There are following items:
                (1) argument_token
                (2) predicate_token
                (3) predicate that depends on token in this layer.
        4. The output of each layer is enclosed by a pair of parentheses:
                (1) Special parentheses "(:a predpatt_output ):a" are used
                    for predicates that are dependents of clausal predicate.
                (2) Normal parentheses "( predpatt_output )" are used for
                    for predicates that are noun dependents.

    """

    ret = []
    roots = build_pred_dep(pp)
    for root in roots:
        repr_root = flatten_and_enclose_pred(root, opt)
        ret.append(repr_root)
    return " ".join(ret)


def flatten_and_enclose_pred(pred, opt):
    repr_y, is_argument = flatten_pred(pred, opt)
    enc = PRED_ENC
    if is_argument:
        enc = ARGPRED_ENC
    return '%s %s %s' % (enc[0], repr_y, enc[1])


def flatten_pred(pred, opt):
    ret = []
    args = pred.arguments
    child_preds = pred.children

    if pred.type == 'poss':
        arg_i = 0
        # Only take the first two arguments into account.
        for y in sort_by_position(args[:2] + child_preds):
            if isinstance(y, Argument):
                arg_i += 1
                if arg_i == 1:
                    # Generate the special ``poss'' predicate with label.
                    poss = 'poss' + (PRED_HEADER if opt.distinguish_header
                                     else PRED_SUF)
                    if opt.ignore_content:
                        poss = "PRED"
                    ret += [phrase_and_enclose_arg(y, opt), poss]
                else:
                    ret += [phrase_and_enclose_arg(y, opt)]
            else:
                if opt.recursive:
                    repr_y = flatten_and_enclose_pred(y, opt)
                    ret.append(repr_y)
        return ' '.join(ret), False

    if pred.type in {'amod', 'appos'}:
        # Special handling for `amod` and `appos` because the target
        # relation `is/are` deviates from the original word order.
        arg0 = None
        other_args = []
        for arg in args:
            if arg.root == pred.root.gov:
                arg0 = arg
            else:
                other_args.append(arg)
        relation = 'is/are' + (PRED_HEADER if opt.distinguish_header
                               else PRED_SUF)
        if opt.ignore_content:
            relation = "PRED"
        if arg0 is not None:
            ret = [phrase_and_enclose_arg(arg0, opt), relation]
            args = other_args
        else:
            ret = [phrase_and_enclose_arg(args[0], opt), relation]
            args = args[1:]

    # Mix arguments with predicate tokens. Use word order to derive a
    # nice-looking name.
    items = pred.tokens + args + child_preds
    if opt.only_head:
        items = important_pred_tokens(pred) + args + child_preds
    if opt.ignore_content:
        items = [pred.root] + args + child_preds

    for i, y in enumerate(sort_by_position(items)):
        if isinstance(y, Argument):
            if (y.isclausal() and y.root.gov in pred.tokens):
                # In theory, "SOMETHING:a=" should be followed by a embedded
                # predicate. But in the real world, the embedded predicate
                # could be broken, which means such predicate could be empty
                # or missing. Therefore, it is necessary to add this special
                # symbol "SOMETHING:a=" to indicate that there is a embedded
                # predicate viewed as an argument of the predicate under
                # processing.
                ret.append(SOMETHING)
            else:
                ret.append(phrase_and_enclose_arg(y, opt))
            # if (pred.root.gov_rel == 'xcomp' and
            #     pred.root.tag not in {'VERB', 'ADJ', 'JJ'} and
            #     i == 0):
            #     ret.append('is/are:p_h' if distinguish_header else 'is/are:p')
        elif isinstance(y, Predicate):
            if opt.recursive:
                repr_y = flatten_and_enclose_pred(y, opt)
                ret.append(repr_y)
        else:
            if opt.ignore_content:
                ret.append("PRED")
            elif opt.distinguish_header and y.position == pred.root.position:
                ret.append(y.text.decode('utf8') + PRED_HEADER)
            else:
                ret.append(y.text.decode('utf8') + PRED_SUF)
    return ' '.join(ret), is_dep_of_pred(pred.root)


def phrase_and_enclose_arg(arg, opt):
    if opt.ignore_content:
        return "ARG"
    repr_arg = ''
    if opt.only_head:
        root_text = arg.root.text.decode('utf8')
        if opt.distinguish_header:
            repr_arg = root_text + ARG_HEADER
        else:
            repr_arg = root_text + ARG_SUF
    else:
        ret = []
        for x in arg.tokens:
            if opt.distinguish_header and x.position == arg.root.position:
                ret.append(x.text.decode('utf8') + ARG_HEADER)
            else:
                ret.append(x.text.decode('utf8') + ARG_SUF)
        repr_arg = ' '.join(ret)
    return "%s %s %s" % (ARG_ENC[0], repr_arg, ARG_ENC[1])


def collect_embebdded_tokens(tokens_iter, start_token):
    if start_token == PRED_ENC[0]:
        end_token = PRED_ENC[1]
    else:
        end_token = ARGPRED_ENC[1]

    missing_end_token = 1
    embedded_tokens = []
    for _, t in tokens_iter:
        if t == start_token:
            missing_end_token += 1
        if t == end_token:
            missing_end_token -= 1
        if missing_end_token == 0:
            return embedded_tokens
        embedded_tokens.append(t)
    # No ending bracket for the predicate.
    return embedded_tokens


def linear_to_string(tokens):
    ret = []
    for t in tokens:
        if t in PRED_ENC or t in ARG_ENC or t in ARGPRED_ENC:
            continue
        elif t == SOMETHING:
            continue
        elif ":" not in t:
            continue
        else:
            ret.append(t.rsplit(":", 1)[0])
    return ret


def get_something(idx, tokens):
    root = Token(idx, "SOMETHING", None)
    arg = Argument(root, [])
    arg.tokens = [root]
    # Get details for SOMETHING.
    if idx + 2 < len(tokens) and tokens[idx + 1] in {PRED_ENC[0], ARGPRED_ENC[0]}:
        tokens_iter = enumerate(tokens[idx + 2:])
        start_token = tokens[idx + 1]
        embedded_tokens = collect_embebdded_tokens(tokens_iter, start_token)
        # embedded_tokens = pprint(" ".join(embedded_tokens)).split()
        embedded_tokens = linear_to_string(embedded_tokens)
        if len(embedded_tokens):
            arg.tokens.append(Token(idx + 1, ":=", None))
            for i, t in enumerate(embedded_tokens, 2):
                arg_t = Token(idx + i, t, None)
                arg.tokens.append(arg_t)
    return arg

def is_argument_finished(t, current_argument):
    if current_argument.position != -1:
        # only one head is allowed.
        if t.endswith(ARG_SUF):
            return False
    else:
        if t.endswith(ARG_SUF) or t.endswith(ARG_HEADER):
            return False
    return True

def construct_arg_from_flat(tokens_iter):
    empty_token = Token(-1, None, None)
    argument = Argument(empty_token, [])
    idx = -1
    for idx, t in tokens_iter:
        if t == ARG_ENC[1]:
            if argument.root.position == -1:
                # Special case: No head is found.
                argument.position = idx
            return argument
        # add argument token
        if ARG_SUF in t:
            text, _ = t.rsplit(ARG_SUF, 1)
        else:
            # Special case: a predicate tag is given.
            text, _ = t.rsplit(":", 1)
        token = Token(idx, text, None)
        argument.tokens.append(token)
        # update argument root
        if t.endswith(ARG_HEADER):
            argument.root = token
            argument.position = token.position
    # No ending bracket for the argument.
    if argument.root.position == -1:
        # Special case: No head is found.
        argument.position = idx
    return argument

def construct_pred_from_flat(tokens):
    if tokens is None or len(tokens) == 0:
        return []
    # Construct one-layer predicates
    ret = []
    # Use this empty_token to initialize a predicate or argument.
    empty_token = Token(-1, None, None)
    # Initialize a predicate in advance, because argument or sub-level
    # predicates may come before we meet the first predicate token, and
    # they need to build connection with the predicate.
    current_predicate = Predicate(empty_token, [])
    tokens_iter = enumerate(iter(tokens))
    for idx, t in tokens_iter:
        if t  == ARG_ENC[0]:
            argument = construct_arg_from_flat(tokens_iter)
            current_predicate.arguments.append(argument)
        elif t in {PRED_ENC[0], ARGPRED_ENC[0]}:
            # Get the embedded tokens, including special tokens.
            embedded = collect_embebdded_tokens(tokens_iter, t)
            # Recursively construct sub-level predicates.
            preds = construct_pred_from_flat(embedded)
            ret += preds
            # if t == "(:a":
            #     # Add a special argument.
            #     current_predicate.arguments.append(something(idx))
        elif t == SOMETHING:
            current_predicate.arguments.append(get_something(idx, tokens))
        elif t.endswith(PRED_SUF) or t.endswith(PRED_HEADER):
            # add predicate token
            text, _ = t.rsplit(PRED_SUF, 1)
            token = Token(idx, text, None)
            current_predicate.tokens.append(token)
            # update predicate root
            if t.endswith(PRED_HEADER):
                current_predicate.root = token
                ret += [current_predicate]
        else:
            continue
    return ret

def check_recoverability(tokens):
    def encloses_allowed():
        return (counter["arg_left"] >= counter["arg_right"] and
                counter["pred_left"] >= counter["pred_right"] and
                counter["argpred_left"] >= counter["argpred_right"])

    def encloses_matched():
        return (counter["arg_left"] == counter["arg_right"] and
                counter["pred_left"] == counter["pred_right"] and
                counter["argpred_left"] == counter["argpred_right"])


    encloses = {"arg_left": ARG_ENC[0], "arg_right": ARG_ENC[1],
                "pred_left": PRED_ENC[0], "pred_right": PRED_ENC[1],
                "argpred_left": ARGPRED_ENC[0], "argpred_right": ARGPRED_ENC[1]}
    sym2name = {y:x for x, y in encloses.iteritems()}
    counter = {x: 0 for x in encloses}
    # check the first enclose
    if tokens[0] not in {encloses["pred_left"], encloses["argpred_left"]}:
        return False, tokens
    # check the last enclose
    if tokens[-1] not in {encloses["pred_right"], encloses["argpred_right"]}:
        return False, tokens
    for t in tokens:
        if t in sym2name:
            counter[sym2name[t]] += 1
            if not encloses_allowed():
                return False, tokens
    return encloses_matched(), tokens

def pprint_preds(preds):
    return [format_pred(p) for p in preds]

def argument_names(args):
    """Give arguments alpha-numeric names.

    >>> names = argument_names(range(100))

    >>> [names[i] for i in range(0,100,26)]
    [u'?a', u'?a1', u'?a2', u'?a3']

    >>> [names[i] for i in range(1,100,26)]
    [u'?b', u'?b1', u'?b2', u'?b3']

    """
    # Argument naming scheme: integer -> `?[a-z]` with potentially a number if
    # there more than 26 arguments.
    name = {}
    for i, arg in enumerate(args):
        c = i // 26 if i >= 26 else ''
        name[arg] = '?%s%s' % (unichr(97+(i % 26)), c)
    return name

def format_pred(pred, indent="\t"):
    lines = []
    name = argument_names(pred.arguments)
    # Format predicate
    lines.append('%s%s%s'
                 % (indent, _format_predicate(pred, name),
                    ('%s[%s]' % (indent, pred.root.text))))
    # Format arguments
    for arg in pred.arguments:
        s = arg.phrase()
        lines.append('%s%s: %s%s'
                     % (indent*2, name[arg], s,
                        ('%s[%s]' % (indent, arg.root.text))))
    return '\n'.join(lines)

def _format_predicate(pred, name):
    ret = []
    args = pred.arguments
    # Mix arguments with predicate tokens. Use word order to derive a
    # nice-looking name.
    for i, y in enumerate(sort_by_position(pred.tokens + args)):
        if isinstance(y, Argument):
            ret.append(name[y])
        else:
            ret.append(y.text)
    return ' '.join(ret)

def pprint(s):
    return re.sub(RE_ARG_RIGHT_ENC, ")",
                  re.sub(RE_ARG_LEFT_ENC, "(",
                         re.sub(RE_PRED_LEFT_ENC, "[",
                                re.sub(RE_PRED_RIGHT_ENC, "]", s))))

def test(pp, flat_s):
    def fail(g, t):
        if len(g) != len(t):
            return True
        else:
            for i in g:
                if i not in t:
                    return True
    no_color = lambda x,_: x
    gold_preds = [p.format(C=no_color, track_rule=False)
             for p in pp.instances if likely_to_be_pred(p)]
    test_preds = pprint_preds(construct_pred_from_flat(flat_s.split()))
    return not fail(gold_preds, test_preds), gold_preds, test_preds


if __name__ == "__main__":
    # Test the recovering function.
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    line = open(sys.argv[1]).read()
    print line
    print "\n".join(pprint_preds(construct_pred_from_flat(line.split())))
