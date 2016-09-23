"""
Example of programmatic PredPatt usage.
"""

# Run PredPatt on sentence
from predpatt import PredPatt
sentence = 'Chris loves silly dogs and clever cats .'
P = PredPatt.from_sentence(sentence)

# Pretty-print output
print P.pprint(track_rule=True, color=True)

print '______________________________________________________________________________'

# A deeper look into PredPatt's internal representations.
#
# Each extraction is kept in a list called instances. Below we will loop through
# each instance and print it's arguments.
for x in P.instances:
    print
    print x, x.phrase()
    for a in x.arguments:
        print ' ', a, a.phrase()

        # Uncomment to list rules which fired on this proposition. Along with
        # an explanation.
        #for r in a.rules:
        #    print '    %s: %s' % (r, r.explain())


print '______________________________________________________________________________'
print

# To change certain behaviors, you can pass different options for the PredPatt
# instance. For example, to disable expansion of conjunctions and extraction of
# amods, use the following:
from predpatt import PredPattOpts
P = PredPatt.from_sentence(sentence, opts=PredPattOpts(resolve_amod=0, resolve_conj=0))

print P.pprint(color=1)

print '______________________________________________________________________________'
print

#______________________________________________________________________________
# Bonus material

# Already have a constituency parse? No problem!
P = PredPatt.from_constituency('( (S (NP (NNP Chris)) (VP (VBZ loves) (NP (NNP Pat))) (. .)) )')
print P.pprint(track_rule=True, color=True)

print '______________________________________________________________________________'
print

# Using PredPatt's Parser interface
from predpatt import Parser
parser = Parser.get_instance()   # Create UD parser instance
parse = parser(sentence)         # Parse sentence
print parse.pprint()
