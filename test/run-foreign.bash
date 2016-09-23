#!/usr/bin/env bash

function runtest {
    prefix="$1"
    got="$prefix.got"
    expect="$prefix.expect"
    cmd="$2"
    ( $cmd ) > "$got"
    diff $expect $got >/dev/null
    if [ $? -eq 0 ]; then
        echo "[test] OK $prefix"
    else
        echo "[test] FAIL $prefix"
        meld $expect $got
        #diff $expect $got
    fi
}

RESOLVEALL="--resolve-poss --resolve-relcl --resolve-amod --resolve-conj --resolve-appos"

UDROOT=/home/timv/projects/blab/data/UniversalDependencies1.2/universal-dependencies-1.2

PYTHON='python'
runtest test/pt.dev.conllu \
    "$PYTHON -m predpatt $UDROOT/UD_Portuguese/pt-ud-dev.conllu $RESOLVEALL --format plain --show-deps"

runtest test/es.dev.conllu \
    "$PYTHON -m predpatt $UDROOT/UD_Spanish/es-ud-dev.conllu $RESOLVEALL --format plain --show-deps"
