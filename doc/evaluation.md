Evaluation
==========

Gold treebank in multiple languages
-----------------------------------
We evaluated PredPatt manually on
several randomly sampled sentences taken from the UD banks of Chinese, English,
Hebrew, Hindi and Spanish. This evaluation runs PredPatt with the gold standard
UD parse. For each language, we report the number of sentences evaluated along
with the number of extractions from those sentences (a proxy for recall) and
precision (95% confidence interval).

<table>
<tr><th>Lang</th><th>#Sent</th><th>#Output</th><th>Precision</th><tr>
<tr><td>  Chinese </td><td>   98 </td>    <td> 375 </td><td> 69.1%  ±  4.7% </td></tr>
<tr><td>  English </td><td>   79 </td>    <td> 210 </td><td> 86.2%  ±  4.7% </td></tr>
<tr><td>   Hebrew </td><td>   12 </td>    <td>  30 </td><td> 66.7%  ± 17.9% </td></tr>
<tr><td>    Hindi </td><td>   22 </td>    <td>  50 </td><td> 52.0%  ± 14.3% </td></tr>
<tr><td>  Spanish </td><td>   27 </td>    <td>  55 </td><td> 70.9%  ± 12.4% </td></tr>
</table>

Large-scale English evaluation with noisy parses
------------------------------------------------

We sampled 1000 sentences uniformly at random from Concretely Annotated Gigaword
([Ferraro et al., 2014](references.md)), which provides constituency parses from Stanford
CoreNLP. We converted these parses to Universal Dependencies using the
PyStanfordDependencies tool. We focus on English because it is one of the only
UD languages that has highly accurate automatic parsers. Instances were judged
as binary "good" or "bad", three-way redundant, by workers on Mechanical Turk,
following a qualification test to verify annotator reliability.

Running PredPatt on these 1000 sentences gave rise to 2380
automatically identified predicate-argument instances.[*] Overall, the
proportion of instances labeled “good” (precision) is 80.3%
(±1.6%). This is quite good given how heavily PredPatt
relies on quality of the automatic parses.


[*]: We added one English-specific tweak to PredPatt output for the
     HIT, which filters dummy arguments from relative clauses (i.e.,
     "which", "who" or "that"). Unfortunately, there is no
     language-independent way to filter these dummy arguments under the
     UD specification.

We trained a confidence estimator based on this data, which allows us to
improve precision at the expense of recall by thresholding the
confidence score. We trained a simple logistic regression classifier on
the each worker’s judgements. We use the following features: the
identity of which rules that fire, the identity of the conjunction of
the governing relations of each argument in the UD parse (e.g.,
``nsubj+dobj+iobj``), the number of arguments, the predicate
name length, and the sentence length. Results are presented and
discussed in .

The figure below shows the calibration score alongside the precision
against the majority vote of the 3 workers. The plot is an average of
5-fold cross-validation. We see that thresholding by the confidence
increases precision without much loss in the number of extractions. For
example, thresholding at a confidence of 80%, we get 91% precision
with 30% of extractions; thresholding at 60% we get 84%
precision and keep 85% of
extractions.

<img width="500px" src="calibration.png"/>
