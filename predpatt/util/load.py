#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Load different sources of data.
"""

import os
import codecs
from collections import namedtuple
from predpatt.UDParse import UDParse


class DepTriple(namedtuple('DepTriple', 'rel gov dep')):
    def __repr__(self):
        return '%s(%s,%s)' % (self.rel, self.dep, self.gov)


def load_comm(filename, tool='ud converted ptb trees using pyStanfordDependencies'):
    "Load a concrete communication file with required pyStanfordDependencies output."
    # import here to avoid requiring concrete
    from concrete.util.file_io import read_communication_from_file
    comm = read_communication_from_file(filename)
    if comm.sectionList:
        for sec in comm.sectionList:
            if sec.sentenceList:
                for sent in sec.sentenceList:
                    yield sec.label, get_udparse(sent, tool)


def load_conllu(filename):
    "Load CoNLLu style files (e.g., the Universal Dependencies treebank)."
    sent_num = 1
    if os.path.isfile(filename):
        with codecs.open(filename, encoding='utf-8') as f:
            content = f.read().strip()
    else:
        content = filename.strip()

    for block in content.split('\n\n'):
        block = block.strip()
        if not block:
            continue
        lines = []
        sent_id = 'sent_%s' % sent_num
        has_sent_id = 0
        for line in block.split('\n'):
            if line.startswith('#'):
                if line.startswith('# sent_id'):
                    sent_id = line[10:].strip()
                    has_sent_id = 1
                else:
                    if not has_sent_id:   # don't take subsequent comments as sent_id
                        sent_id = line[1:].strip()
                continue
            line = line.split('\t') # data appears to use '\t'
            if '-' in line[0]:      # skip multi-tokens, e.g., on Spanish UD bank
                continue
            assert len(line) == 10, line
            lines.append(line)
        [_, tokens, _, tags, _, _, gov, gov_rel, _, _] = list(zip(*lines))
        triples = [DepTriple(rel, int(gov)-1, dep) for dep, (rel, gov) in enumerate(zip(gov_rel, gov))]
        parse = UDParse(list(tokens), tags, triples)
        yield sent_id, parse
        sent_num += 1


def get_tags(tokenization, tagging_type='POS'):
    for tokenTagging in tokenization.tokenTaggingList:
        if tokenTagging.taggingType == tagging_type:
            idx2pos = {taggedToken.tokenIndex: taggedToken.tag
                       for taggedToken in tokenTagging.taggedTokenList}
            return [idx2pos[idx] for idx in sorted(idx2pos.keys())]


def get_udparse(sent, tool):
    "Create a ``UDParse`` from a sentence extracted from a Communication."

    # extract dependency parse for Communication.
    triples = []
    for ud_parse in sent.tokenization.dependencyParseList:
        if ud_parse.metadata.tool == tool:
            for dependency in ud_parse.dependencyList:
                triples.append(DepTriple(dependency.edgeType,
                                         dependency.gov, dependency.dep))
            break

    # Extract token strings
    tokens = [x.text for x in sent.tokenization.tokenList.tokenList]

    # Extract POS tags
    tags = get_tags(sent.tokenization, 'POS')

    #triples.sort(key=lambda triple: triple.dep)
    parse = UDParse(tokens=tokens, tags=tags, triples=triples)

    # Extract lemmas
    #parse.lemmas = get_tags(sent.tokenization, 'LEMMA')

    return parse
