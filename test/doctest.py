"""
Documentation test runner.
"""
import re, codecs
from predpatt import PredPatt, PredPattOpts, Parser
from termcolor import colored

ppattopts = PredPattOpts(simple=False,
                         cut=False,
                         resolve_relcl=True,
                         resolve_appos=True,
                         resolve_amod=True,
                         resolve_conj=True,
                         resolve_poss=True,
                         borrow_arg_for_relcl=True,
                         big_args=False,
                         ud="1.0")


def test():
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('--filename', default='doc/DOCTEST.md')
    args = p.parse_args()

    sentences = re.findall('^> (.*)\n([\w\W]*?)(?=^>|<END>)', codecs.open(args.filename, encoding='utf-8').read() + '\n<END>', re.MULTILINE)

    # TODO: Use PredPatt.from_string instead of duplicating code here.
    parser = Parser.get_instance()

    passed = 0
    failed = 0
    blank = 0
    for s, chunk in sentences:
        s = s.strip()
        if not s:
            continue

        # use cached parse listed in doctest chunk.
        parse_chunk = re.findall('<\!--parse=([\w\W]+?)-->', chunk)
        if parse_chunk:
            from predpatt.UDParse import DepTriple, UDParse
            [parse_chunk] = parse_chunk
            triples = [DepTriple(r,int(b),int(a)) for r,a,b in re.findall('(\S+)\(\S+?/(\d+), \S+?/(\d+)\)', parse_chunk)]
            tokens = s.split()
            [tags_chunk] = re.findall('<\!--tags=([\w\W]+?)-->', chunk)
            tags = re.findall('\S+/(\S+)', tags_chunk)
            parse = UDParse(tokens, tags, triples)

        else:
            parse = parser(s)

        P = PredPatt(parse, ppattopts)
        relations = P.pprint(track_rule=True)
        tags = ' '.join('%s/%s' % x for x in zip(parse.tokens, parse.tags))
        parse = parse.pprint(K=4)

        relations = relations.replace('\t','    ')
        relations = '\n'.join(line[4:].rstrip() for line in relations.split('\n'))

        expected = []
        chunk = chunk.replace('\t','    ')
        for line in chunk.split('\n'):
            if line.startswith('    '):
                line = line[4:].rstrip()
                expected.append(line)

        expected = '\n'.join(expected)

        if not expected.strip():
            blank += 1

        #got = '%s\n%s\n%s' % (tags, parse, relations)
        got = relations.strip() or '<empty>'
        got = re.sub(r'\s*\[.*\]', '', got)

        if expected.strip() == got.strip():
            #print colored('pass', 'green')
            passed += 1
        else:
            print
            print colored('> ' + s, 'yellow')
            print colored('fail', 'red')
            print 'expected:'
            for line in expected.split('\n'):
                print '   ', colored(line, 'blue')
            print 'got:'
            for line in got.split('\n'):
                print '   ', line
            print
            print colored(tags, 'magenta')
            print
            print colored(parse, 'magenta')
            failed += 1

    msg = '[doctest] %.f%% (%s/%s) passed' % (passed * 100.0 / (passed+failed), passed, passed+failed)
    if failed == 0:
        print msg
    else:
        print
        print msg
        print
        if blank:
            print 'blank:', blank


if __name__ == '__main__':
    test()
