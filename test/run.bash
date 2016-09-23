#!/usr/bin/env bash

#set -e

PYTHON="python"

RUNCOVERAGE=

if [[ $RUNCOVERAGE ]]; then
    echo "[test] Running test coverage."
    coverage erase
    PYTHON="coverage run -a --rcfile test/coveragerc"
fi

function runtest {
    prefix="$1"
    got=$prefix.got
    expect=$prefix.expect
    cmd="$2"
    $cmd > $got
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

comm="test/data.100.fine.all.ud.comm"

runtest test/data.100.fine.all.ud-cut \
    "$PYTHON -m predpatt $comm $RESOLVEALL --format plain --cut --track-rule"

runtest test/data.100.fine.all.ud-norelcl \
    "$PYTHON -m predpatt $comm --resolve-conj --format plain --show-deps --track-rule"

runtest test/data.100.fine.all.ud \
    "$PYTHON -m predpatt $comm $RESOLVEALL --format plain --show-deps --track-rule"

runtest test/data.100.fine.all.ud-simple \
    "$PYTHON -m predpatt $comm $RESOLVEALL --format plain --show-deps --track-rule --simple"

$PYTHON test/doctest.py

if [[ $RUNCOVERAGE ]]; then
    coverage html \
        --rcfile test/coveragerc \
        --include 'predpatt/*' \
        -d coverage-report

    xdg-open coverage-report/index.html
fi
