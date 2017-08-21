import os
import tensorflow as tf
from dragnn.protos import spec_pb2
from dragnn.python import graph_builder
from dragnn.python import spec_builder
from dragnn.python import load_dragnn_cc_impl  # This loads the actual op definitions
from dragnn.python import render_parse_tree_graphviz
from dragnn.python import visualization
from google.protobuf import text_format
from syntaxnet import load_parser_ops  # This loads the actual op definitions
from syntaxnet import sentence_pb2
from syntaxnet.ops import gen_parser_ops
from tensorflow.python.platform import tf_logging as logging

from predpatt import PredPatt
from predpatt import load_conllu
from predpatt import PredPattOpts
from predpatt.util.ud import dep_v2


def load_model(base_dir, master_spec_name, checkpoint_name):
    """
    Function to load the syntaxnet models. Highly specific to the tutorial
    format right now.
    """
    # Read the master spec
    master_spec = spec_pb2.MasterSpec()
    with open(os.path.join(base_dir, master_spec_name), "r") as f:
        text_format.Merge(f.read(), master_spec)
    spec_builder.complete_master_spec(master_spec, None, base_dir)
    logging.set_verbosity(logging.WARN)  # Turn off TensorFlow spam.

    # Initialize a graph
    graph = tf.Graph()
    with graph.as_default():
        hyperparam_config = spec_pb2.GridPoint()
        builder = graph_builder.MasterBuilder(master_spec, hyperparam_config)
        # This is the component that will annotate test sentences.
        annotator = builder.add_annotation(enable_tracing=True)
        builder.add_saver()  # "Savers" can save and load models; here, we're only going to load.

    sess = tf.Session(graph=graph)
    with graph.as_default():
        #sess.run(tf.global_variables_initializer())
        #sess.run('save/restore_all', {'save/Const:0': os.path.join(base_dir, checkpoint_name)})
        builder.saver.restore(sess, os.path.join(base_dir, checkpoint_name))
        
    def annotate_sentence(sentence):
        with graph.as_default():
            return sess.run([annotator['annotations'], annotator['traces']],
                            feed_dict={annotator['input_batch']: [sentence]})
    return annotate_sentence


def annotate_text(text):
    """
    Segment and parse input text using syntaxnet models.
    """
    sentence = sentence_pb2.Sentence(
        text=text,
        token=[sentence_pb2.Token(word=text, start=-1, end=-1)]
    )

    # preprocess
    with tf.Session(graph=tf.Graph()) as tmp_session:
        char_input = gen_parser_ops.char_token_generator([sentence.SerializeToString()])
        preprocessed = tmp_session.run(char_input)[0]
    segmented, _ = SEGMENTER_MODEL(preprocessed)

    annotations, traces = PARSER_MODEL(segmented[0])
    assert len(annotations) == 1
    assert len(traces) == 1
    return sentence_pb2.Sentence.FromString(annotations[0]), traces[0]


def parse_to_conll(parse_tree):
    """
    Convert from the syntaxnet output format to a CoNLL-U format.
    """
    out_str = ''
    for i, token in enumerate(parse_tree.token, 1):
        if token.head == -1:
            head = 0
        else:
            head = token.head + 1
        pos1, pos2 = token.tag.split('attribute')[-1].split('value')[-1].replace(': "', '').replace('" } ', '').split('++')
        out_str += '{}\t{}\t-\t{}\t{}\t-\t{}\t{}\t-\t-\n'.format(i, token.word, pos1, pos2, head, token.label)

    return out_str

path = '/opt/tensorflow/syntaxnet/examples/dragnn/data'
SEGMENTER_MODEL = load_model(os.path.join(path, "en/segmenter"),
                             "spec.textproto", "checkpoint")
PARSER_MODEL = load_model(os.path.join(path, 'en'),
                          "parser_spec.textproto", "checkpoint")
def parse(text):
    """
    Primary function to run syntaxnet and PredPatt over input sentences.
    """
    parse_tree, trace = annotate_text(text)
    conll_parsed = parse_to_conll(parse_tree)

    conll_pp = [ud_parse for sent_id, ud_parse in load_conllu(conll_parsed)][0]

    #PredPatt options. Modify as needed.
    resolve_relcl = True  # relative clauses
    resolve_appos = True  # appositional modifiers
    resolve_amod = True   # adjectival modifiers
    resolve_conj = True   # conjuction
    resolve_poss = True   # possessives
    ud = dep_v2.VERSION   # the version of UD
    opts = PredPattOpts(resolve_relcl=resolve_relcl,
                        resolve_appos=resolve_appos,
                        resolve_amod=resolve_amod,
                        resolve_conj=resolve_conj,
                        resolve_poss=resolve_poss,
                        ud=ud)
    ppatt = PredPatt(conll_pp, opts=opts)

    #NOTE:
    #This returns the pretty print formatted string from PredPatt. This is done
    #largely as a place holder for JSON compatability within the REST API. 
    return {'predpatt': ppatt.pprint(), 'conll': conll_parsed, 'original': text}
