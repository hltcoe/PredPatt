ParseyPredFace
==============

This repo contains the resources required to build an API around
PredPatt and Google's SyntaxNet/DRAGNN/ParseyMcParseface. The build
instructions for the SyntaxNet Docker image are currently (7.21.17) broken,
so this repo makes use of the pre-built image.

There are two subdirectories: `rest` and `concrete`. The `rest` directory 
contains code to build a RESTful API around PredPatt and SyntaxNet. This will
allow users to make a `GET` call to a local port and receive parsed
information. The `concrete` directory builds a
[`concrete`](https://github.com/hltcoe/concrete) annotation service around
PredPatt and SyntaxNet. The `concrete` approach allows for more nuance in the
returned data structures, so it is suggested for uses beyond a shallow
exploration of PredPatt and SyntaxNet.
