"""PredPatt web demo

TODO:

 * Use quick lime's visualization for trees.

 * Other views of PredPatt output (e.g., inlined spans, treelets)

 * Support multiple sentences?

 * Add option to list rules which fired.

 * Show calibration score.
"""
import re
from bottle import route, run, template, request
from predpatt import Parser, PredPatt, PredPattOpts
from textwrap import dedent


# TODO eventually we'll want to accept paragraphs as input.
#import nltk
#sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')


parser = Parser.get_instance()

@route('/')
@route('/', method='GET')
def main():

    patterns = ''
    sentence = 'The quick brown fox jumped over the lazy dog .'
    tags = ''
    parse = ''
    if request.GET.get('sentence','').strip():
        sentence = request.GET.get('sentence', '').strip()

    pp_opts = PredPattOpts()
    for k, v in sorted(PredPattOpts().__dict__.iteritems()):
        v = int(float(request.GET.get(k, v)))   # all options are true/false for now.
        setattr(pp_opts, k, v)

    if sentence:

        #for sent in sent_detector.tokenize('"John saw Mary", said Jason. Larry met Sally for dinner.'):
        #    print tokenize(sent)

        original_sentence = sentence
        parse = parser(sentence, tokenized=False)

        P = PredPatt(parse, opts=pp_opts)
        patterns = P.pprint(track_rule=True)
        tags = ' '.join('%s/%s' % x for x in zip(parse.tokens, parse.tags))
        parse = parse.pprint(K=3)

        # remove predpatt's bracketed comments
        patterns = re.sub(r'\s*\[.*?\]', '', patterns)
        patterns = dedent(patterns)

    opts = []
    for k, v in sorted(pp_opts.__dict__.iteritems()):
        # Create a hidden textbox with the false value because the values of
        # "unchecked" boxes don't get posted with form.
        opts.append('<input type="hidden" value="0" name="%s">' % (k,))
        opts.append('<input type="checkbox" name="%s" value="1" %s> %s<br/>' % (k, 'checked' if v else '', k))

    options = '\n'.join(opts)

    return template("""
<html>
<head>


<!-- JQuery -->
<script src="//code.jquery.com/jquery-2.1.4.min.js"></script>
<!-- Bootstrap -->
<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css"/>
<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap-theme.min.css"/>
<script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js"></script>
<!-- Chosen Dropdown Library -->
<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/chosen/1.4.2/chosen.css"/>
<script src="//cdnjs.cloudflare.com/ajax/libs/chosen/1.4.2/chosen.jquery.min.js"></script>

<style>
html {
     overflow: -moz-scrollbars-vertical;
     overflow: scroll;
}
</style>
</head>
<body>
<div style="width: 800px; padding: 10px; margin-left: auto; margin-right: auto;">
<h1>PredPatt</h1>
<strong>Sentence</strong>
<pre>{{sentence}}</pre>

<strong>Propositions</strong>
<div id="propositions">
<pre>
{{patterns}}
</pre>

<div>
<button class="btn" data-toggle="collapse" data-target="#parse" style="margin-bottom: 10px;">Toggle Parse</button>
<div id="parse" class="collapse">
<strong>Tags</strong>
<pre>
{{tags}}
</pre>
<strong>Parse</strong>
<pre>
{{parse}}
</pre>
</div>
</div>
<strong>Input</strong>
<form action="/" method="GET">
<textarea type="text" name="sentence" style="height:50px; width: 100%;"
placeholder="e.g., The quick brown fox jumped over the lazy dog."
class="form-control"
autofocus>{{original_sentence}}</textarea>
<div style="padding: 10px;"><strong>Options</strong><br/>""" + options + """
</div>
<br/>
<input type="submit" name="save" value="submit">
</form>
</div>
</body>
</html>
    """,
                    sentence=sentence,
                    original_sentence=original_sentence,
                    patterns=patterns,
                    tags=tags,
                    parse=parse,
                    options=options)


run(host='localhost', port=8080, debug=True)
