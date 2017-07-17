#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from collections import namedtuple, defaultdict
from tabulate import tabulate
from termcolor import colored
from predpatt.util.ud import dep_v1


class DepTriple(namedtuple('DepTriple', 'rel gov dep')):
    def __repr__(self):
        return '%s(%s,%s)' % (self.rel, self.dep, self.gov)


class UDParse:

    def __init__(self, tokens, tags, triples, ud=dep_v1):
        self.ud = dep_v1
        self.tokens = tokens
        self.tags = tags
        self.triples = triples
        self.governor = {e.dep: e for e in triples}
        self.dependents = defaultdict(list)
        for e in self.triples:
            self.dependents[e.gov].append(e)

    def pprint(self, color=False, K=1):
        """Pretty-print list of dependencies.

        K: number of columns.

        """
        tokens1 = self.tokens + ['ROOT']
        C = colored('/%s', 'magenta') if color else '/%s'
        E = ['%s(%s%s, %s%s)' % (e.rel, tokens1[e.dep],
                                 C % e.dep,
                                 tokens1[e.gov],
                                 C % e.gov)
             for e in sorted(self.triples, key=lambda x: x.dep)]
        cols = [[] for _ in range(K)]
        for i, x in enumerate(E):
            cols[i % K].append(x)
        # add padding to columns because zip stops at shortest iterator.
        for c in cols:
            c.extend('' for _ in xrange(len(cols[0]) - len(c)))
        return tabulate(zip(*cols), tablefmt='plain')

    def latex(self):
        "LaTeX dependency diagrams."
        # http://ctan.mirrors.hoobly.com/graphics/pgf/contrib/tikz-dependency/tikz-dependency-doc.pdf
        boilerplate = r"""\documentclass{standalone}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{tikz}
\usepackage{tikz-dependency}
\begin{document}
\begin{dependency}[theme = brazil]
\begin{deptext}
%s \\
%s \\
\end{deptext}
%s
\end{dependency}
\end{document}"""
        tok = ' \\& '.join(x.replace('&', r'and').replace('_', ' ') for x in self.tokens)
        tag = ' \\& '.join(self.tags).lower()
        dep = '\n'.join(r'\depedge{%d}{%d}{%s}' % (e.gov+1, e.dep+1, e.rel)
                        for e in self.triples if e.gov >= 0)
        return (boilerplate % (tok, tag, dep)).replace('$','\\$').encode('utf-8')

    def view(self, do_open=True):
        """
        Open a dependency parse diagram of the sentence. Requires
        that pdflatex be in PATH and that Daniele Pighin's
        tikz-dependency.sty be in the current directory
        """
        from hashlib import md5
        latex = self.latex()
        was = os.getcwd()
        try:
            os.chdir('/tmp')
            base = 'parse_%s' % md5(' '.join(self.tokens).encode('ascii', errors='ignore')).hexdigest()
            pdf = '%s.pdf' % base
            if not os.path.exists(pdf):
                with file('%s.tex' % base, 'w') as f:
                    f.write(latex)
                os.system('pdflatex -halt-on-error %s.tex >/dev/null' % base)
            if do_open:
                os.system('xdg-open %s' % pdf)
            return os.path.abspath(pdf)
        finally:
            os.chdir(was)

    def toimage(self):
        img = self.view(do_open=0)
        if img is not None:
            out = img[:-4] + '.png'
            if not os.path.exists(out):
                cmd = 'gs -dBATCH -dNOPAUSE -sDEVICE=pngalpha -o %s %s' % (out, img)
                os.system(cmd)
            return out
