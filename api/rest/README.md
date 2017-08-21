ParseyPredFace
==============

This repo contains the resources required to build a REST API around
PredPatt and Google's SyntaxNet/DRAGNN/ParseyMcParseface. The build
instructions for the SyntaxNet Docker image are currently (7.21.17) broken,
so this repo makes use of the pre-built image.

Building and Running
--------

To build the image:

```
docker build -t ppf .
```

Note that the above requires pulling the rather large `tensorflow/syntaxnet`
image, so will take a bit of time.

To run:

```
docker run -p 5000:5000 ppf
```

This will run a REST API listening on port `5000` on `localhost`.

Usage
-----

```
headers = {'Content-Type': 'application/json'}
data = {'text': "John brought the pizza to Loren."
}
data = json.dumps(data)
r = requests.get('http://localhost:5000/ppf/extract', data=data, headers=headers)

#This has the output dictionary
r.json()
```

The final output will look something like:

```
{u'conll': u'1\tJohn\t-\tPROPN\tNNP\t-\t2\tnsubj\t-\t-\n2\tbrought\t-\tVERB\tVBD\t-\t0\troot\t-\t-\n3\tthe\t-\tDET\tDT\t-\t4\tdet\t-\t-\n4\tpizza\t-\tNOUN\tNN\t-\t2\tobj\t-\t-\n5\tto\t-\tADP\tIN\t-\t6\tcase\t-\t-\n6\tLoren\t-\tPROPN\tNNP\t-\t4\tnmod\t-\t-\n7\t.\t-\tPUNCT\t.\t-\t2\tpunct\t-\t-\n',
 u'original': u'John brought the pizza to Loren.',
 u'predpatt': u'\t?a brought ?b\t[brought-root]\n\t\t?a: John\t[John-nsubj]\n\t\t?b: the pizza to Loren\t[pizza-obj]'}
```

As shown above, the keys in the output dictionary are:

* `conll`: The CoNLL-U formatted parse returned by SyntaxNet
* `original`: The original text sent to the API
* `predpatt`: A nested JSON object containing `predicate_deps` and `arg_deps`.
 The `predicate_deps` field contains the dependency fragments for the exracted
 predicates. The fragments are of the form `(governor_text, governor_position,
 relation, token_text, token_position)`. The `arg_deps` field is formatted as
 a dictionary with keys of integers representing the argument location, and
 values as the extracted argument fragments. The format is the same as with the
 `predicate_deps` field.
