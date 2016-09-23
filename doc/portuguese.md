# a_tree-pt-s58-root
> Arnold_Schwarzenegger deu entrevistas como ator principal , foi substituído por Bruce_Willis há dois anos , mas o projeto nunca saiu de o papel .
<!--tags=
Arnold_Schwarzenegger/PROPN deu/VERB entrevistas/NOUN como/ADV ator/NOUN principal/ADJ ,/PUNCT foi/VERB substituído/VERB por/ADP Bruce_Willis/PROPN há/ADP dois/NUM anos/NOUN ,/PUNCT mas/CONJ o/DET projeto/NOUN nunca/ADV saiu/VERB de/ADP o/DET papel/NOUN ./PUNCT
-->
<!--parse=
nsubj(Arnold_Schwarzenegger/0, deu/1)  root(deu/1, ROOT/-1)          dobj(entrevistas/2, deu/1)            cop(como/3, ator/4)
advmod(ator/4, deu/1)                  amod(principal/5, ator/4)     punct(,/6, deu/1)                     conj(foi/7, deu/1)
ccomp(substituído/8, foi/7)            case(por/9, Bruce_Willis/10)  dobj(Bruce_Willis/10, substituído/8)  case(há/11, anos/13)
nummod(dois/12, anos/13)               nmod(anos/13, substituído/8)  punct(,/14, deu/1)                    cc(mas/15, deu/1)
det(o/16, projeto/17)                  nsubj(projeto/17, saiu/19)    advmod(nunca/18, saiu/19)             conj(saiu/19, deu/1)
case(de/20, papel/22)                  det(o/21, papel/22)           dobj(papel/22, saiu/19)               punct(./23, deu/1)
-->

    ?a deu ?b como ator principal
        ?a: Arnold_Schwarzenegger
        ?b: entrevistas
    ?a is/are principal
        ?a: ator
    ?a foi ?b
        ?a: Arnold_Schwarzenegger
        ?b: SOMETHING := substituído por Bruce_Willis há dois anos
    ?a substituído por ?b há ?c
        ?a: Arnold_Schwarzenegger
        ?b: Bruce_Willis
        ?c: dois anos
    ?a nunca saiu de ?b
        ?a: o projeto
        ?b: o papel


# a_tree-pt-s83-root
> O bombeiro suspeita que o golfinho tenha morrido afogado .
<!--tags=
O/DET bombeiro/NOUN suspeita/VERB que/SCONJ o/DET golfinho/NOUN tenha/VERB morrido/VERB afogado/VERB ./PUNCT
-->
<!--parse=
det(O/0, bombeiro/1)         nsubj(bombeiro/1, suspeita/2)  root(suspeita/2, ROOT/-1)   mark(que/3, tenha/6)
det(o/4, golfinho/5)         nsubj(golfinho/5, tenha/6)     ccomp(tenha/6, suspeita/2)  ccomp(morrido/7, tenha/6)
advcl(afogado/8, morrido/7)  punct(./9, suspeita/2)
-->

    ?a suspeita ?b
        ?a: O bombeiro
        ?b: SOMETHING := o golfinho tenha morrido
    ?a tenha ?b
        ?a: o golfinho
        ?b: SOMETHING := morrido
    ?a morrido
        ?a: o golfinho
    ?a afogado
        ?a: o golfinho
