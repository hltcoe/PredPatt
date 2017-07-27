"""
Wrapper around the Berkeley parser and the pyStanfordDependency converter.
"""

from __future__ import print_function, unicode_literals
from past.builtins import basestring

import os
import shelve
try:
    import cPickle as pickle
except:
    import pickle
import StanfordDependencies
from subprocess import Popen, PIPE
from predpatt.UDParse import UDParse, DepTriple
from predpatt.util.universal_tags import ptb2universal
from nltk.tokenize import TreebankWordTokenizer
from contextlib import contextmanager


@contextmanager
def cd(d):
    "Change directory, but pop back when you exit the context."
    cwd = os.path.abspath(os.path.curdir)   # record cwd, so we can go back to it.
    try:
        os.chdir(d)
        yield
    finally:
        os.chdir(cwd)


def ensure_dir(d):
    "Create directory if it doesn't exist."
    if not os.path.exists(d):
        os.makedirs(d)
    return d

def download(src, dst):
    "Download resource."
    return os.system("curl -L '%s' -o %s" % (src, dst))


# URL for Stanford Parser JAR
DEFAULT_VERSION = '3.5.2'
STANFORD_JAR_NAME = 'stanford-corenlp-%s.jar' % DEFAULT_VERSION
STANFORD_PARSER_URL = ('http://search.maven.org/remotecontent?filepath='
                       'edu/stanford/nlp/stanford-corenlp/'
                       '%s/%s' % (
                           DEFAULT_VERSION, STANFORD_JAR_NAME))
# URL for Berkeley Parser and Grammar
BERKELEY_PARSER_URL = ('https://github.com/slavpetrov/berkeleyparser'
                       '/blob/master/BerkeleyParser-1.7.jar?raw=true')
GRAMMAR_URL = 'https://github.com/slavpetrov/berkeleyparser/blob/master/eng_sm6.gr?raw=true'

# Local storage dir
DEFAULT_DIR = ensure_dir(os.path.expanduser('~/.PredPatt/'))
STANFORD_JAR = os.path.abspath(os.path.join(DEFAULT_DIR, STANFORD_JAR_NAME))
BERKELEY_JAR = os.path.abspath(os.path.join(DEFAULT_DIR, 'BerkeleyParser-1.7.jar'))
GR = os.path.abspath(os.path.join(DEFAULT_DIR, 'eng_sm6.gr'))

REPLACEMENTS = {'-LRB-': '(',
                '-RRB-': ')',
                '-LSB-': '[',
                '-RSB-': ']',
                '-LCB-': '{',
                '-RCB-': '}'}

# reverse mapping
REPLACEMENTS_R = dict(zip(REPLACEMENTS.values(), REPLACEMENTS.keys()))



def tokenize(sentence):
    "Tokenize sentence the way parser expects."
    tokenizer = TreebankWordTokenizer()
    s = tokenizer.tokenize(sentence)
    s = ' '.join(s)
    # character replacements
    s = ''.join(REPLACEMENTS_R.get(x,x) for x in s)
    return s


class Cached(object):
    """
    Caching mix-in for classes implementing a ``fresh(...)`` method.
    """

    def __init__(self, CACHE):
        self.cache = None
        if CACHE is not None:
            self.cache = shelve.open(CACHE, 'c')

    def __call__(self, *args, **kwargs):
        "Cached function call see documentation for ``fresh`` method."
        if self.cache is not None:
            # Serialize arguments using pickle to get a string-valued key
            # (shelve requires string-valued keys).
            s = pickle.dumps((args, tuple(sorted(kwargs.items()))), protocol=0)
            s = s.decode()
            if s in self.cache:
                try:
                    return self.cache[s]
                except Exception:
                    pass       # passing here means that we'll run fresh.
        x = self.fresh(*args, **kwargs)
        if self.cache is not None:
            self.cache[s] = x
        return x

    def fresh(self, *args, **kwargs):
        raise NotImplementedError()

    def __del__(self):
        if self.cache is not None:
            self.cache.close()


class UDConverter(Cached):

    def __init__(self, CACHE):
        Cached.__init__(self, CACHE)
        self.sd = StanfordDependencies.get_instance(jar_filename=STANFORD_JAR, backend='jpype')

    def fresh(self, parse):
        "Convert constituency parse to UD. Expects string, returns `UDParse` instance."
        assert isinstance(parse, basestring)
        deps = self.sd.convert_tree(parse)
        tokens = [e.form for e in deps]
        # convert tags
        tags = [ptb2universal[e.cpos] for e in deps]
        triples = []
        for e in deps:
            # PyStanfordDependencies indexing starts at one, but we want
            # indexing to start at zero. Hence the -1 below.
            triples.append(DepTriple(rel=e.deprel, gov=e.head-1, dep=e.index-1))
        return UDParse(tokens=tokens, tags=tags, triples=triples)

    @classmethod
    def get_instance(cls, CACHE=True):
        """Do whatever it takes to get parser instance, including downloading the
        external dependencies.
        """
        CACHE = (os.path.abspath(os.path.join(DEFAULT_DIR, 'udcoverter.shelve'))
                 if CACHE else None)

        if not os.path.exists(STANFORD_JAR):
            assert 0 == download(STANFORD_PARSER_URL, STANFORD_JAR)
        return cls(CACHE)


class Parser(Cached):
    """Interface for parsing to universal dependency syntax (UD). Uses the Berkeley
    parser for constituency parsing and Stanford's converter to UD.

    """

    def __init__(self, PARSER_JAR, GRAMMAR, CACHE):
        Cached.__init__(self, CACHE)
        self.PARSER_JAR = PARSER_JAR
        self.GRAMMAR = GRAMMAR
        self.process = None
        self._start_subprocess()
        self.to_ud = UDConverter.get_instance(CACHE)

    def _start_subprocess(self):
        self.process = Popen(['java', '-jar', self.PARSER_JAR, '-gr', self.GRAMMAR],
                             stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding='utf-8')

    def fresh(self, s, tokenized=False):
        """UD-parse and POS-tag sentence `s`. Returns (UDParse, PTB-parse-string).

        Pass in `tokenized=True` if `s` has already been tokenized, otherwise we
        apply `nltk.tokenize.TreebankWordTokenizer`.

        """
        if self.process is None:
            self._start_subprocess()
        s = str(s.strip())
        if not tokenized:
            s = tokenize(s)
        s = s.strip()
        assert '\n' not in s, "No newline characters allowed %r" % s
        try:
            self.process.stdin.write(s)
        except IOError as e:
            #if e.errno == 32:          # broken pipe
            #    self.process = None
            #    return self(s)  # retry will restart process
            raise e
        self.process.stdin.write('\n')
        self.process.stdin.flush()
        out = self.process.stdout.readline()
        return self.to_ud(out)

    def __del__(self):
        if self.process is not None:
            self.process.terminate()

    @staticmethod
    def get_instance(CACHE=True):
        """Do whatever it takes to get parser instance, including downloading the
        external dependencies.
        """
        CACHE = (os.path.abspath(os.path.join(DEFAULT_DIR, 'parser-cache.shelve'))
                 if CACHE else None)

        with cd(DEFAULT_DIR):
            if not os.path.exists(BERKELEY_JAR):
                assert 0 == download(BERKELEY_PARSER_URL, BERKELEY_JAR)
            if not os.path.exists(GR):
                assert 0 == download(GRAMMAR_URL, GR)

        return Parser(BERKELEY_JAR, GR, CACHE)


def main():
    from argparse import ArgumentParser
    q = ArgumentParser()
    q.add_argument('sentence')
    q.add_argument('--view', action='store_true')
    args = q.parse_args()
    p = Parser.get_instance()
    t = p(args.sentence)
    print(t.pprint())
    if args.view:
        t.view()


if __name__ == '__main__':
    main()
