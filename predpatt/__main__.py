"""
PredPatt command-line program.
"""
import sys, codecs
from argparse import ArgumentParser
from predpatt import PredPatt, PredPattOpts, load_conllu, load_comm


def main():
    # Make stdout utf-8 friendly. This is only really needed when redirecting stdout
    # to a file or less.
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

    parser = ArgumentParser()
    parser.add_argument('filename',
                        help='Path to the input file. Accepts Concrete communications and CoNLLU format.')
    parser.add_argument('-n', '--num', type=int, default=None,
                        help='The number of sents.')
    parser.add_argument('-f', '--format',
                        choices=('color', 'plain'), default='plain')
    parser.add_argument('-d', '--debug', default='')
    parser.add_argument('--simple', action='store_true')
    parser.add_argument('--cut', action='store_true')
    parser.add_argument('--track-rule', action='store_true')
    parser.add_argument('--show-deps', action='store_true')
    parser.add_argument('--show-deps-cols', type=int, default=4)
    parser.add_argument('--resolve-relcl', action='store_true',
                        help='Enable relative clause resolution rule.')
    parser.add_argument('--resolve-appos', action='store_true',
                        help='Enable apposition resolution rule.')
    parser.add_argument('--resolve-poss', action='store_true',
                        help='Enable possessive resolution rule.')
    parser.add_argument('--resolve-conj', action='store_true',
                        help='Enable conjuction resolution rule.')
    parser.add_argument('--resolve-amod', action='store_true',
                        help='Enable adjectival modifier resolution rule.')
    args = parser.parse_args()

    if args.filename.endswith('.conllu'):
        sentences = load_conllu(args.filename)
    else:
        sentences = load_comm(args.filename)

    for sent_i, (slabel, parse) in enumerate(sentences, 1):
        if args.debug and slabel != args.debug:  # supports substring match
            continue

        print 'label:   ', slabel
        print 'sentence:', ' '.join(parse.tokens)

        if args.debug:
            args.show_deps = True

        if args.show_deps:
            print
            print 'tags:', ' '.join('%s/%s' % (x, tag) for tag, x in zip(parse.tags, parse.tokens))
            print
            print parse.pprint(args.format=='color', K=args.show_deps_cols)

        opts = PredPattOpts(simple = args.simple,
                            cut = args.cut,
                            resolve_relcl = args.resolve_relcl,
                            resolve_amod = args.resolve_amod,
                            resolve_appos = args.resolve_appos,
                            resolve_poss = args.resolve_poss,
                            resolve_conj = args.resolve_conj)

        ppatt = PredPatt(parse, opts=opts)

        #ppatt.instances = [e for e in ppatt.instances if filter_events_ksk(e, parse)]

        print
        print 'ppatt:'
        print ppatt.pprint(color=args.format == 'color',
                           track_rule=args.track_rule)
        print
        print

        if args.debug or sent_i == args.num:
            return


if __name__ == '__main__':
    main()
